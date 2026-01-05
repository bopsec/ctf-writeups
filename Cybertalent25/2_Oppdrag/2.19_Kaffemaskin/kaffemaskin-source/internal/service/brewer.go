package service

import (
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"time"

	"machine/internal/app"
	"machine/internal/domain"
	"machine/internal/repository"
	"machine/internal/security"
)

var (
	ErrAlreadyBrewing         = errors.New("machine is already brewing")
	ErrDrinkNotFound          = errors.New("drink not found")
	ErrDrinkInactive          = errors.New("drink is inactive")
	ErrMissingSignatureHeader = errors.New("missing signature header")
	ErrUnexpectedSignatureAlg = errors.New("unexpected signature algorithm")
)

// BrewService handles drink retrieval and filtering.
type BrewService struct {
	brewer   *repository.BrewerRepository
	security *repository.SecurityRepository
}

// NewBrewService creates a new BrewService.
func NewBrewService(brewer *repository.BrewerRepository, security *repository.SecurityRepository) *BrewService {
	return &BrewService{
		brewer:   brewer,
		security: security,
	}
}

// GetDrinks returns drinks filtered by ids and active flag.
func (s *BrewService) GetDrinks(ids []int, activeOnly bool) ([]*domain.DrinkRecord, error) {
	settings, err := s.brewer.LoadBrewerSettings()
	if err != nil {
		return nil, fmt.Errorf("get drinks: %w", err)
	}

	idSet := make(map[int]struct{}, len(ids))
	for _, id := range ids {
		idSet[id] = struct{}{}
	}

	var result []*domain.DrinkRecord
	for _, rec := range settings.Drinks {
		if activeOnly && !rec.Active {
			continue
		}
		if len(idSet) > 0 {
			if _, ok := idSet[rec.ID]; !ok {
				continue
			}
		}
		result = append(result, &domain.DrinkRecord{
			ID:              rec.ID,
			Name:            rec.Name,
			Description:     rec.Description,
			BeansGram:       rec.BeansGram,
			CacaoPowderGram: rec.CacaoPowderGram,
			WaterTempC:      rec.WaterTempC,
			WaterMl:         rec.WaterMl,
			MilkTempC:       rec.MilkTempC,
			MilkMl:          rec.MilkMl,
			Active:          rec.Active,
		})
	}

	return result, nil
}

// StartPouring validates the drink and marks the machine as pouring.
func (s *BrewService) StartPouring(drinkID int) error {
	state, err := s.brewer.LoadBrewerState()
	if err != nil {
		return fmt.Errorf("failed to load brewer state: %w", err)
	}

	if isBrewing(state) {
		return ErrAlreadyBrewing
	}

	drink, err := s.GetDrinkByID(drinkID)
	if err != nil {
		return err
	}

	if !drink.Active {
		return ErrDrinkInactive
	}

	state.SelectedDrinkID = drinkID
	state.CurrentProgress = 1
	state.TimeToBrew = 25

	if err := s.brewer.SaveBrewerState(state); err != nil {
		return fmt.Errorf("failed to save brewer state: %w", err)
	}

	go s.runProgressLoop()

	return nil
}

// GetState returns the current brewing state.
func (s *BrewService) GetState() (*domain.BrewerStateFile, error) {
	return s.brewer.LoadBrewerState()
}

// GetDrinkByID returns a drink by id.
func (s *BrewService) GetDrinkByID(id int) (*domain.DrinkRecord, error) {
	drinks, err := s.GetDrinks(nil, false)
	if err != nil {
		return nil, err
	}

	for _, d := range drinks {
		if d.ID == id {
			return d, nil
		}
	}

	return nil, ErrDrinkNotFound
}

// SetSelectedDrinkID persists the selected drink id.
func (s *BrewService) SetSelectedDrinkID(id int) error {
	state, err := s.brewer.LoadBrewerState()
	if err != nil {
		return fmt.Errorf("failed to load brewer state: %w", err)
	}

	if isBrewing(state) {
		return ErrAlreadyBrewing
	}

	state.SelectedDrinkID = id

	if err := s.brewer.SaveBrewerState(state); err != nil {
		return fmt.Errorf("failed to save brewer state: %w", err)
	}

	return nil
}

// runProgressLoop increments current progress every 1 second until done, simulates the machine making a drink.
func (s *BrewService) runProgressLoop() {
	// Always reset progress on exit
	defer func() {
		state, err := s.brewer.LoadBrewerState()
		if err != nil {
			app.CoreLogError("load brewer state for reset failed: %v", err)
			return
		}

		state.CurrentProgress = 0

		if err := s.brewer.SaveBrewerState(state); err != nil {
			app.CoreLogError("save brewer state for reset failed: %v", err)
		}
	}()

	ticker := time.NewTicker(time.Second)
	defer ticker.Stop()

	for range ticker.C {
		state, err := s.brewer.LoadBrewerState()
		if err != nil {
			app.CoreLogError("load brewer state failed: %v", err)
			return
		}

		if !isBrewing(state) {
			return
		}

		state.CurrentProgress++

		if err := s.brewer.SaveBrewerState(state); err != nil {
			app.CoreLogError("save state failed: %v", err)
			return
		}
	}
}

// GetServiceStatus returns the current service schedule configuration.
func (s *BrewService) GetServiceStatus() (*domain.MaintenanceFile, error) {
	return s.brewer.LoadMaintenance()
}

// RunMaintenanceScript fetches, verifies, stores, and runs the maintenance script for a mode.
func (s *BrewService) RunMaintenanceScript(mode string) error {
	scriptName, err := s.maintenanceScriptPath(mode)
	if err != nil {
		return err
	}

	body, headers, err := s.fetchMaintenanceScript(scriptName)
	if err != nil {
		return err
	}

	if err := s.verifyMaintenanceScript(body, headers); err != nil {
		return err
	}

	path, err := s.saveMaintenanceScript(body)
	if err != nil {
		return err
	}

	if err := s.runServiceScript(path); err != nil {
		return fmt.Errorf("failed running maintaince script: %w", err)
	}

	return nil
}

// maintenanceScriptPath resolves the script path for a maintenance mode.
func (s *BrewService) maintenanceScriptPath(mode string) (string, error) {
	cfg, err := s.brewer.LoadMaintenance()
	if err != nil {
		return "", fmt.Errorf("load config: %w", err)
	}

	for _, rec := range cfg.Entries {
		if rec.MaintenanceMode == mode && rec.ScriptPath != "" {
			return rec.ScriptPath, nil
		}
	}

	return "", fmt.Errorf("maintenance mode %q not found", mode)
}

// fetchMaintenanceScript downloads the script and returns its body and headers.
func (s *BrewService) fetchMaintenanceScript(scriptName string) ([]byte, http.Header, error) {
	resp, err := http.Get("http://maintenance-server.utlandia:8080/service/" + scriptName)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to fetch: %w", err)
	}
	defer resp.Body.Close()

	body, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, nil, fmt.Errorf("failed to read body: %w", err)
	}

	return body, resp.Header, nil
}

// verifyMaintenanceScript checks the script signature using headers and public key.
func (s *BrewService) verifyMaintenanceScript(body []byte, headers http.Header) error {
	sigB64 := headers.Get("X-Signature")
	if sigB64 == "" {
		return ErrMissingSignatureHeader
	}

	if headers.Get("X-Signature-Alg") != "rsa-sha256" {
		return ErrUnexpectedSignatureAlg
	}

	pubKey, err := s.security.LoadPublicKey()
	if err != nil {
		return fmt.Errorf("load public key: %w", err)
	}

	if err := security.VerifySignature(body, sigB64, pubKey); err != nil {
		return err
	}

	return nil
}

// saveMaintenanceScript writes the script to a temp file and makes it executable.
func (s *BrewService) saveMaintenanceScript(body []byte) (string, error) {
	tmpFile, err := os.CreateTemp("", "script-*")
	if err != nil {
		return "", fmt.Errorf("temp file: %w", err)
	}
	defer tmpFile.Close()

	if _, err := tmpFile.Write(body); err != nil {
		return "", fmt.Errorf("write file: %w", err)
	}

	if err := os.Chmod(tmpFile.Name(), 0o700); err != nil {
		return "", fmt.Errorf("chmod: %w", err)
	}

	return tmpFile.Name(), nil
}

// runServiceScript runs an executable script located at path.
func (s *BrewService) runServiceScript(fullPath string) error {
	if fullPath == "" {
		return fmt.Errorf("empty script path")
	}
	if err := s.validateShebang(fullPath); err != nil {
		return err
	}

	cmd := exec.Command("/bin/sh", fullPath)
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		return fmt.Errorf("run service script %q: %w", fullPath, err)
	}

	return nil
}

// validateShebang returns nil iff the file starts with "#!".
func (s *BrewService) validateShebang(path string) error {
	f, err := os.Open(path)
	if err != nil {
		return err
	}
	defer f.Close()

	hdr := make([]byte, 2)
	if _, err := io.ReadFull(f, hdr); err != nil {
		return err
	}
	if string(hdr) != "#!" {
		return fmt.Errorf("missing shebang")
	}
	return nil
}

// TODO: Create handler /config/source/server for this method and create UI for download button.

// FetchServerSource downloads the server source code.
func (s *BrewService) FetchServerSource() {
	_, _ = http.Get("http://maintenance-server.utlandia:8080/source")
}

// isBrewing reports whether a brew is currently in progress.
func isBrewing(state *domain.BrewerStateFile) bool {
	return state != nil &&
		state.TimeToBrew > 0 &&
		state.CurrentProgress > 0 &&
		state.CurrentProgress < state.TimeToBrew
}
