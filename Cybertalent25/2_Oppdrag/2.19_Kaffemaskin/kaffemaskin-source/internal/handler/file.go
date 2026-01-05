package handler

import (
	"errors"
	"net/http"

	"machine/internal/app"
	"machine/internal/dto"
	"machine/internal/security"
	"machine/internal/service"
	"machine/internal/view"
)

// FileHandler handles http endpoints for files and file edits.
type FileHandler struct {
	fileService *service.FileService
	renderer    *view.TemplateRenderer
}

// NewFileHandler creates a new ConfigHandler.
func NewFileHandler(f *service.FileService, r *view.TemplateRenderer) *FileHandler {
	return &FileHandler{
		fileService: f,
		renderer:    r,
	}
}

// FileEditPageGet renders file menu and the selected file (if any) for editing.
func (h *FileHandler) FileEditPageGet(w http.ResponseWriter, r *http.Request) {
	flashKind, flashMessage := consumeFlash(w, r)

	userFiles, adminFiles, err := h.fileService.ListDirectory(r.Context())
	if err != nil {
		app.CoreLogError("list directory failed: %v", err)
		flashRedirect(w, r, flashKindError, "failed to list files", "/file")
		return
	}

	relPath := r.PathValue("path")

	var path string
	var content string

	if relPath != "" {
		f, err := h.fileService.GetFile(r.Context(), relPath)
		if err != nil {
			app.CoreLogError("get file %q failed: %v", relPath, err)
			flashRedirect(w, r, flashKindError, "failed to load file", "/file")
			return
		}

		path = relPath
		content = string(f.Content)
	}

	data := dto.FilePageDto{
		Title:        "Edit File",
		FlashKind:    flashKind,
		FlashMessage: flashMessage,
		IsAdmin:      security.IsAdmin(r.Context()),
		UserFiles:    userFiles,
		AdminFiles:   adminFiles,
		Path:         path,
		Content:      content,
	}

	_ = h.renderer.Render(w, "file_edit_page", data)
}

// FilePost saves edited file content.
func (h *FileHandler) FilePost(w http.ResponseWriter, r *http.Request) {
	path := r.PathValue("path")
	if path == "" {
		app.CoreLogError("missing path")
		flashRedirect(w, r, flashKindError, "missing path", "/file")
		return
	}

	content := r.FormValue("content")

	if err := h.fileService.SaveFile(r.Context(), path, content); err != nil {
		app.CoreLogError("save file %q failed: %v", path, err)

		msg := "failed to save file"
		if errors.Is(err, security.ErrPathOutsideAllowedDirs) {
			msg = "invalid file path"
		}

		flashRedirect(w, r, flashKindError, msg, "/file/"+path)
		return
	}

	flashRedirect(w, r, flashKindSuccess, "file saved", "/file/"+path)
}
