// Package domain contains core domain entities and concepts.
package domain

import "time"

// File represents an editable file.
type File struct {
	Path    string
	Content []byte
}

// FileListing holds file and directory names for a single directory.
type FileListing struct {
	FileNames      []string
	DirectoryNames []string
}

// SessionContextKey is the context key for sessions.
type SessionContextKey struct{}

// SignedAsset represents an asset with signing metadata.
type SignedAsset struct {
	Data      []byte
	Name      string
	ModTime   time.Time
	Signature string
}
