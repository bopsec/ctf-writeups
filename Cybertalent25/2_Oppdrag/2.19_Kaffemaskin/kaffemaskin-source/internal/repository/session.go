package repository

import (
	"encoding/json"
	"os"
	"path/filepath"
	"sync"

	"machine/internal/app"
	"machine/internal/domain"
)

// SessionRepository provides access to admin pin, users and sessions.
type SessionRepository struct {
	baseDir      string
	backgroundMu sync.Mutex
}

// NewSessionRepository creates a new SessionRepository.
func NewSessionRepository(baseDir string) *SessionRepository {
	return &SessionRepository{
		baseDir: baseDir,
	}
}

// LoadAdminPin loads user/admin_pin.json.
func (r *SessionRepository) LoadAdminPin() (*domain.AdminConfigFile, error) {
	path := filepath.Join(r.baseDir, "user", "admin_pin.json")

	data, err := os.ReadFile(path)
	if err != nil {
		app.CoreLogError("Failed to read file: %w", err)
		return nil, err
	}

	var cfg domain.AdminConfigFile
	if err := json.Unmarshal(data, &cfg); err != nil {
		app.CoreLogError("Failed to unmarshal file: %w", err)
		return nil, err
	}

	return &cfg, nil
}

// LoadUsers loads user/users.json.
func (r *SessionRepository) LoadUsers() (*domain.UserFile, error) {
	path := filepath.Join(r.baseDir, "user", "users.json")

	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}

	var uf domain.UserFile
	if err := json.Unmarshal(data, &uf); err != nil {
		return nil, err
	}

	return &uf, nil
}

// LoadSessions loads hidden/sessions.json.
func (r *SessionRepository) LoadSessions() (*domain.SessionFile, error) {
	path := filepath.Join(r.baseDir, "hidden", "sessions.json")

	data, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return &domain.SessionFile{}, nil
		}
		return nil, err
	}

	var sf domain.SessionFile
	if err := json.Unmarshal(data, &sf); err != nil {
		return nil, err
	}

	return &sf, nil
}

// SaveSessions writes hidden/sessions.json.
func (r *SessionRepository) SaveSessions(sf *domain.SessionFile) error {
	r.backgroundMu.Lock()
	defer r.backgroundMu.Unlock()

	path := filepath.Join(r.baseDir, "hidden", "sessions.json")

	data, err := json.MarshalIndent(sf, "", "  ")
	if err != nil {
		return err
	}

	return os.WriteFile(path, data, 0o600)
}
