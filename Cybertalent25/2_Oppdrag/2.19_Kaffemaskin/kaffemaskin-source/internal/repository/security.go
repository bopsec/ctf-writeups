package repository

import (
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"os"
	"path/filepath"
)

// SecurityRepository provides access to cryptographic keys.
type SecurityRepository struct {
	baseDir string
}

// NewSecurityRepository creates a new SecurityRepository.
func NewSecurityRepository(baseDir string) *SecurityRepository {
	return &SecurityRepository{
		baseDir: baseDir,
	}
}

// LoadPublicKey returns the rsa public key used to verify assets and scripts.
func (r *SecurityRepository) LoadPublicKey() (*rsa.PublicKey, error) {
	path := filepath.Join(r.baseDir, "hidden", "public.pem")

	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("load public key: %w", err)
	}

	block, _ := pem.Decode(data)
	if block == nil {
		return nil, fmt.Errorf("load public key: invalid pem")
	}

	parsed, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		return nil, fmt.Errorf("load public key: parse pkix: %w", err)
	}

	key, ok := parsed.(*rsa.PublicKey)
	if !ok {
		return nil, fmt.Errorf("load public key: not an rsa public key")
	}

	return key, nil
}

// LoadPrivateKey returns the rsa private key used to sign assets and scripts.
func (r *SecurityRepository) LoadPrivateKey() (*rsa.PrivateKey, error) {
	path := filepath.Join(r.baseDir, "hidden", "private.pem")

	data, err := os.ReadFile(path)
	if err != nil {
		return nil, fmt.Errorf("load private key: %w", err)
	}

	block, _ := pem.Decode(data)
	if block == nil {
		return nil, fmt.Errorf("load private key: invalid pem")
	}

	parsed, err := x509.ParsePKCS8PrivateKey(block.Bytes)
	if err != nil {
		return nil, fmt.Errorf("load private key: parse pkcs8: %w", err)
	}

	key, ok := parsed.(*rsa.PrivateKey)
	if !ok {
		return nil, fmt.Errorf("load private key: not an rsa private key")
	}

	return key, nil
}
