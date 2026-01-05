// Package repository handles persistence
package repository

import (
	"encoding/json"
	"os"
	"path/filepath"
	"sync"

	"machine/internal/domain"
)

// BrewerRepository provides access to drinks, state, sessions, users and keys.
type BrewerRepository struct {
	baseDir      string
	backgroundMu sync.Mutex
}

// NewBrewerRepository creates a new BrewRepository.
func NewBrewerRepository(baseDir string) *BrewerRepository {
	return &BrewerRepository{
		baseDir: baseDir,
	}
}

// LoadBrewerSettings loads user/brewer_settings.json.
func (r *BrewerRepository) LoadBrewerSettings() (*domain.BrewerSettingsFile, error) {
	path := filepath.Join(r.baseDir, "user", "brewer_settings.json")

	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}

	var f domain.BrewerSettingsFile
	if err := json.Unmarshal(data, &f); err != nil {
		return nil, err
	}

	return &f, nil
}

// LoadBrewerState loads hidden/brewer_state.json.
func (r *BrewerRepository) LoadBrewerState() (*domain.BrewerStateFile, error) {
	path := filepath.Join(r.baseDir, "hidden", "brewer_state.json")

	data, err := os.ReadFile(path)
	if err != nil {
		if os.IsNotExist(err) {
			return &domain.BrewerStateFile{}, nil
		}
		return nil, err
	}

	var state domain.BrewerStateFile
	if err := json.Unmarshal(data, &state); err != nil {
		return nil, err
	}

	return &state, nil
}

// SaveBrewerState writes hidden/brewer_state.json.
func (r *BrewerRepository) SaveBrewerState(state *domain.BrewerStateFile) error {
	r.backgroundMu.Lock()
	defer r.backgroundMu.Unlock()

	path := filepath.Join(r.baseDir, "hidden", "brewer_state.json")

	data, err := json.MarshalIndent(state, "", "  ")
	if err != nil {
		return err
	}

	return os.WriteFile(path, data, 0o644)
}

// LoadMaintenance loads admin/maintenance.json.
func (r *BrewerRepository) LoadMaintenance() (*domain.MaintenanceFile, error) {
	path := filepath.Join(r.baseDir, "admin", "maintenance.json")

	data, err := os.ReadFile(path)
	if err != nil {
		return nil, err
	}

	var f domain.MaintenanceFile
	if err := json.Unmarshal(data, &f); err != nil {
		return nil, err
	}

	return &f, nil
}
