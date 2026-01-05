package main

import (
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"crypto/x509"
	"encoding/base64"
	"encoding/pem"
	"fmt"
	"log"
	"net/http"
	"os"
	"strings"
)

var privateKey *rsa.PrivateKey

func loadPrivateKey() (*rsa.PrivateKey, error) {
	data, err := os.ReadFile("/app/private.pem")
	if err != nil {
		return nil, fmt.Errorf("read key: %w", err)
	}

	block, _ := pem.Decode(data)
	if block == nil {
		return nil, fmt.Errorf("failed to parse pem block")
	}

	if block.Type == "PRIVATE KEY" {
		parsed, err := x509.ParsePKCS8PrivateKey(block.Bytes)
		if err != nil {
			return nil, fmt.Errorf("parse pkcs8 key: %w", err)
		}
		rsaKey, ok := parsed.(*rsa.PrivateKey)
		if !ok {
			return nil, fmt.Errorf("not an rsa private key")
		}
		return rsaKey, nil
	}

	return nil, fmt.Errorf("unsupported key type %q", block.Type)
}

func serveScript(w http.ResponseWriter, fileName string) {
	data, err := os.ReadFile("scripts/" + fileName)
	if err != nil {
		http.Error(w, "internal server error", http.StatusInternalServerError)
		return
	}

	hash := sha256.Sum256(data)

	sig, err := rsa.SignPKCS1v15(rand.Reader, privateKey, crypto.SHA256, hash[:])
	if err != nil {
		http.Error(w, "internal server error", http.StatusInternalServerError)
		return
	}

	sigB64 := base64.StdEncoding.EncodeToString(sig)

	w.Header().Set("Content-Type", "application/octet-stream")
	w.Header().Set("X-Content-Type-Options", "nosniff")
	w.Header().Set("Content-Disposition", "attachment; filename="+fileName)
	w.Header().Set("X-Signature", sigB64)
	w.Header().Set("X-Signature-Alg", "rsa-sha256")
	w.WriteHeader(http.StatusOK)
	_, _ = w.Write(data)
}

func serviceHandler(w http.ResponseWriter, r *http.Request) {
	if strings.Contains(r.RequestURI, "%") {
		http.Error(w, "bad path", http.StatusBadRequest)
		return
	}

	path := r.PathValue("path")
	if path == "" {
		http.NotFound(w, r)
		return
	}

	serveScript(w, path)
}

func main() {
	privateKey, _ = loadPrivateKey()

	mux := http.NewServeMux()

	mux.HandleFunc("/service/{path...}", serviceHandler)
	mux.HandleFunc("/source", func(w http.ResponseWriter, r *http.Request) { http.ServeFile(w, r, "/app/source.zip") })

	if err := http.ListenAndServe(":8085", mux); err != nil {
		log.Fatal(err)
	}
}
