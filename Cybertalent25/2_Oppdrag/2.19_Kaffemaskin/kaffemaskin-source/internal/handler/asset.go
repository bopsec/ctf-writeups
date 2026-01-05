package handler

import (
	"bytes"
	"errors"
	"net/http"
	"os"
	"strings"

	"machine/internal/app"
	"machine/internal/service"
)

// AssetsHandler serves static assets and signs them.
type AssetsHandler struct {
	assetService *service.AssetService
}

// NewAssetsHandler creates a new AssetsHandler.
func NewAssetsHandler(assetService *service.AssetService) *AssetsHandler {
	return &AssetsHandler{
		assetService: assetService,
	}
}

// ServeHTTP serves assets and adds rsa-sha256 signature headers.
func (h *AssetsHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	path := strings.TrimPrefix(r.URL.Path, "/assets/")

	asset, err := h.assetService.GetSignedAsset(path)
	if err != nil {
		app.CoreLogError("asset error: %v", err)
		if errors.Is(err, os.ErrNotExist) {
			http.NotFound(w, r)
			return
		}

		http.Error(w, "internal server error", http.StatusInternalServerError)
		return
	}

	w.Header().Set("X-Signature", asset.Signature)
	w.Header().Set("X-Signature-Alg", "rsa-sha256")
	w.Header().Set("X-Content-Type-Options", "nosniff")
	w.Header().Set("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
	w.Header().Set("Pragma", "no-cache")
	w.Header().Set("Expires", "0")

	http.ServeContent(w, r, asset.Name, asset.ModTime, bytes.NewReader(asset.Data))
}
