package service

import (
	"crypto"
	"crypto/rand"
	"crypto/rsa"
	"crypto/sha256"
	"encoding/base64"
	"fmt"
	"io"

	"machine/internal/domain"
	"machine/internal/repository"
)

// AssetService provides signed assets and asset-related operations.
type AssetService struct {
	assetsRepo   *repository.AssetRepository
	securityRepo *repository.SecurityRepository
}

// NewAssetService creates a new AssetService.
func NewAssetService(assetsRepo *repository.AssetRepository, securityRepo *repository.SecurityRepository) *AssetService {
	return &AssetService{
		assetsRepo:   assetsRepo,
		securityRepo: securityRepo,
	}
}

// GetSignedAsset loads an asset and returns it with a base64-encoded signature.
func (s *AssetService) GetSignedAsset(path string) (*domain.SignedAsset, error) {
	data, name, modTime, err := s.assetsRepo.LoadAsset(path)
	if err != nil {
		return nil, fmt.Errorf("get signed asset: %w", err)
	}

	privateKey, err := s.securityRepo.LoadPrivateKey()
	if err != nil {
		return nil, fmt.Errorf("get signed asset: %w", err)
	}

	hash := sha256.Sum256(data)

	sig, err := rsa.SignPKCS1v15(rand.Reader, privateKey, crypto.SHA256, hash[:])
	if err != nil {
		return nil, fmt.Errorf("get signed asset: %w", err)
	}

	sigB64 := base64.StdEncoding.EncodeToString(sig)

	return &domain.SignedAsset{
		Data:      data,
		Name:      name,
		ModTime:   modTime,
		Signature: sigB64,
	}, nil
}

// UpdateBackgroundImage stores a background image, validates it and replaces the current background.
func (s *AssetService) UpdateBackgroundImage(src io.Reader, maxSize int) error {
	return s.assetsRepo.SaveBackground(src, maxSize)
}

// GetSourceCode returns the path to the source.zip file or an error.
func (s *AssetService) GetSourceCode() (string, error) {
	return s.assetsRepo.LoadSourceCode()
}
