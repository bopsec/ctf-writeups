package handler

import (
	"errors"
	"io/fs"
	"net/http"

	"machine/internal/app"
	"machine/internal/dto"
	"machine/internal/security"
	"machine/internal/service"
	"machine/internal/view"
)

// ConfigHandler handles http endpoints for configuration pages and actions.
type ConfigHandler struct {
	assetService *service.AssetService
	renderer     *view.TemplateRenderer
}

// NewConfigHandler creates a new ConfigHandler.
func NewConfigHandler(a *service.AssetService, r *view.TemplateRenderer) *ConfigHandler {
	return &ConfigHandler{
		assetService: a,
		renderer:     r,
	}
}

// ConfigPageGet renders the config page.
func (h *ConfigHandler) ConfigPageGet(w http.ResponseWriter, r *http.Request) {
	flashKind, flashMessage := consumeFlash(w, r)

	data := dto.ConfigPageDto{
		Title:        "Config",
		FlashKind:    flashKind,
		FlashMessage: flashMessage,
		IsAdmin:      security.IsAdmin(r.Context()),
	}

	_ = h.renderer.Render(w, "config_page", data)
}

// UploadBackgroundPost handles background image uploads.
func (h *ConfigHandler) UploadBackgroundPost(w http.ResponseWriter, r *http.Request) {
	const maxSize = 2 * 1024 * 1024

	if err := r.ParseMultipartForm(int64(maxSize * 2)); err != nil {
		app.CoreLogError("parse multipart form failed: %v", err)
		flashRedirect(w, r, flashKindError, "bad form", "/config")
		return
	}

	file, header, err := r.FormFile("background")
	if err != nil {
		app.CoreLogError("get form file failed: %v", err)
		flashRedirect(w, r, flashKindError, "file is required", "/config")
		return
	}
	defer file.Close()

	if header == nil || header.Size <= 0 {
		app.CoreLogError("missing or empty file")
		flashRedirect(w, r, flashKindError, "empty file", "/config")
		return
	}

	if header.Size > int64(maxSize) {
		app.CoreLogError("file too large: %d bytes", header.Size)
		flashRedirect(w, r, flashKindError, "file too large (max 2mb)", "/config")
		return
	}

	if err := h.assetService.UpdateBackgroundImage(file, maxSize); err != nil {
		app.CoreLogError("update background failed: %v", err)
		flashRedirect(w, r, flashKindError, "failed to update background", "/config")
		return
	}

	flashRedirect(w, r, flashKindSuccess, "background updated", "/config")
}

// DownloadSourceCodeGet serves the admin source zip.
func (h *ConfigHandler) DownloadSourceCodeGet(w http.ResponseWriter, r *http.Request) {
	sourcePath, err := h.assetService.GetSourceCode()
	if err != nil {
		app.CoreLogError("getting source code failed: %v", err)

		msg := "internal server error"
		if errors.Is(err, fs.ErrNotExist) {
			msg = "source code not found"
		}

		flashRedirect(w, r, flashKindError, msg, "/config")
		return
	}

	w.Header().Set("Content-Type", "application/zip")
	w.Header().Set("Content-Disposition", `attachment; filename="source.zip"`)

	http.ServeFile(w, r, sourcePath)
}
