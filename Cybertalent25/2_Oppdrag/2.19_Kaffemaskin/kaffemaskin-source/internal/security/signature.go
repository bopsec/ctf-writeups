package security

import (
	"crypto"
	"crypto/rsa"
	"crypto/sha256"
	"encoding/base64"
	"errors"
	"fmt"
)

var ErrInvalidSignature = errors.New("invalid signature")

// VerifySignature verifies an rsa-sha256 signature of the script bytes using an rsa public key.
func VerifySignature(script []byte, sigB64 string, pub *rsa.PublicKey) error {
	sig, err := base64.StdEncoding.DecodeString(sigB64)
	if err != nil {
		return fmt.Errorf("decode signature: %w", err)
	}

	hash := sha256.Sum256(script)

	if err := rsa.VerifyPKCS1v15(pub, crypto.SHA256, hash[:], sig); err != nil {
		return ErrInvalidSignature
	}

	return nil
}
