package repository

import (
	"fmt"
	"image/png"
	"io"
	"os"
	"path/filepath"
	"sync"
	"time"

	"machine/internal/app"
)

// AssetRepository provides access to static assets on disk.
type AssetRepository struct {
	baseDir      string
	backgroundMu sync.Mutex
}

// NewAssetRepository creates a new AssetRepository.
func NewAssetRepository(baseDir string) *AssetRepository {
	return &AssetRepository{
		baseDir: baseDir,
	}
}

// LoadAsset returns file data, name and mod time for a relative asset path.
func (r *AssetRepository) LoadAsset(relPath string) ([]byte, string, time.Time, error) {
	fullPath := filepath.Join(r.baseDir, relPath)

	f, err := os.Open(fullPath)
	if err != nil {
		return nil, "", time.Time{}, err
	}
	defer f.Close()

	info, err := f.Stat()
	if err != nil {
		return nil, "", time.Time{}, err
	}
	if info.IsDir() {
		return nil, "", time.Time{}, os.ErrNotExist
	}

	data, err := io.ReadAll(f)
	if err != nil {
		return nil, "", time.Time{}, err
	}

	return data, info.Name(), info.ModTime(), nil
}

// LoadSourceCode returns the path to the source.zip file or an error.
func (r *AssetRepository) LoadSourceCode() (string, error) {
	sourcePath := filepath.Join(app.RootPath, "data", "hidden", "source.zip")

	if _, err := os.Stat(sourcePath); err != nil {
		return "", err
	}

	return sourcePath, nil
}

// SaveBackground removes old background for a new background.
func (r *AssetRepository) SaveBackground(bg io.Reader, maxSize int) error {
	r.backgroundMu.Lock()
	defer r.backgroundMu.Unlock()

	dstDir := filepath.Join(app.RootPath, "assets", "public", "images", "backgrounds")
	tmpPath := filepath.Join(dstDir, "background_tmp.png")
	finalPath := filepath.Join(dstDir, "background.png")

	if err := writeFileWithMaxSize(tmpPath, bg, maxSize); err != nil {
		return fmt.Errorf("failed to write tmp background: %w", err)
	}

	f, err := os.Open(tmpPath)
	if err != nil {
		return fmt.Errorf("failed to open file: %w", err)
	}
	defer f.Close()

	if _, err := png.Decode(f); err != nil {
		_ = os.Remove(tmpPath)
		return fmt.Errorf("background is not a png %w", err)
	}

	if err := os.Rename(tmpPath, finalPath); err != nil {
		_ = os.Remove(tmpPath)
		return fmt.Errorf("failed to rename background %w", err)
	}

	return nil
}

// writeFileWithMaxSize, not safe to path trversal.
func writeFileWithMaxSize(absPath string, src io.Reader, maxSize int) error {
	if maxSize <= 0 {
		return fmt.Errorf("maxSize must be > 0")
	}

	dst, err := os.Create(absPath)
	if err != nil {
		return fmt.Errorf("create %q: %w", absPath, err)
	}

	limited := io.LimitReader(src, int64(maxSize)+1)

	n, err := io.Copy(dst, limited)
	if err != nil {
		_ = dst.Close()
		_ = os.Remove(absPath)
		return fmt.Errorf("copy to %q: %w", absPath, err)
	}

	if n > int64(maxSize) {
		_ = dst.Close()
		_ = os.Remove(absPath)
		return fmt.Errorf("size too big")
	}

	if err := dst.Close(); err != nil {
		_ = os.Remove(absPath)
		return fmt.Errorf("close %q: %w", absPath, err)
	}

	return nil
}
