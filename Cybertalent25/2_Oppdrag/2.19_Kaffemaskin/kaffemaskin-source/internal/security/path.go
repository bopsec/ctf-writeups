// Package security contains security-related helpers.
package security

import (
	"errors"
	"path/filepath"
	"strings"
)

var ErrPathOutsideAllowedDirs = errors.New("path outside allowed directories")

// SafePath mitigates path traversal by enforcing allowed base directories.
func SafePath(baseDirs []string, userPath string) (string, error) {
	userPath = filepath.Clean(userPath)

	for _, baseDir := range baseDirs {
		baseDir = filepath.Clean(baseDir)
		joined := filepath.Join(baseDir, userPath)
		real, err := filepath.EvalSymlinks(joined)
		if err != nil {
			continue
		}

		if real == baseDir || strings.HasPrefix(real, baseDir+string(filepath.Separator)) {
			return real, nil
		}
	}

	return "", ErrPathOutsideAllowedDirs
}
