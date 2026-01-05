package service

import (
	"context"
	"fmt"
	"os"
	"os/exec"

	"machine/internal/app"
	"machine/internal/domain"
	"machine/internal/security"
)

// FileService handles file editing logic.
type FileService struct{}

// NewFileService creates a new FileService.
func NewFileService() *FileService {
	return &FileService{}
}

// GetFile returns a file for editing after resolving a safe path (only data/user and data/admin).
func (s *FileService) GetFile(ctx context.Context, relPath string) (*domain.File, error) {
	allowedBasePaths := []string{app.RootPath + "data/user/"}
	if security.IsAdmin(ctx) {
		allowedBasePaths = append(allowedBasePaths, app.RootPath+"data/admin/")
	}

	safePath, err := security.SafePath(allowedBasePaths, relPath)
	if err != nil {
		return nil, err
	}

	b, err := os.ReadFile(safePath)
	if err != nil {
		return nil, err
	}

	return &domain.File{
		Path:    safePath,
		Content: b,
	}, nil
}

// SaveFile persists edited file content after resolving a safe path (only data/user and data/admin).
func (s *FileService) SaveFile(ctx context.Context, relPath string, content string) error {
	allowedBasePaths := []string{app.RootPath + "data/user/"}
	if security.IsAdmin(ctx) {
		allowedBasePaths = append(allowedBasePaths, app.RootPath+"data/admin/")
	}

	safePath, err := security.SafePath(allowedBasePaths, relPath)
	if err != nil {
		return err
	}

	if err := os.WriteFile(safePath, []byte(content), 0o644); err != nil {
		return err
	}

	cmd := exec.Command("/usr/local/bin/sync-etc-wrapper")
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		return fmt.Errorf("failed to sync etc files: %w", err)
	}

	return nil
}

// ListDirectory returns user and admin file names from the data directories.
func (s *FileService) ListDirectory(ctx context.Context) ([]string, []string, error) {
	userDirContent, err := list(app.RootPath + "data/user")
	if err != nil {
		return nil, nil, err
	}
	userFiles := userDirContent.FileNames

	if !security.IsAdmin(ctx) {
		return userFiles, nil, nil
	}

	adminDirContent, err := list(app.RootPath + "data/admin")
	if err != nil {
		return userFiles, nil, nil
	}
	adminFiles := adminDirContent.FileNames

	return userFiles, adminFiles, nil
}

// list returns file and directory names for the given absolute directory path.
func list(absDir string) (*domain.FileListing, error) {
	entries, err := os.ReadDir(absDir)
	if err != nil {
		return nil, fmt.Errorf("read dir %q: %w", absDir, err)
	}

	files := make([]string, 0, len(entries))
	dirs := make([]string, 0, len(entries))

	for _, e := range entries {
		name := e.Name()
		if e.IsDir() {
			dirs = append(dirs, name)
		} else {
			files = append(files, name)
		}
	}

	return &domain.FileListing{
		FileNames:      files,
		DirectoryNames: dirs,
	}, nil
}
