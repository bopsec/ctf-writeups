// Package service contains application-level business services.
package service

import (
	"crypto/rand"
	"encoding/hex"
	"errors"
	"fmt"

	"machine/internal/app"
	"machine/internal/domain"
	"machine/internal/repository"
)

// SessionService handles authentication and sessions.
type SessionService struct {
	repo *repository.SessionRepository
}

// NewSessionService creates a new SessionService.
func NewSessionService(repo *repository.SessionRepository) *SessionService {
	return &SessionService{
		repo: repo,
	}
}

var ErrInvalidCredentials = errors.New("invalid credentials")

// Login validates credentials and creates a new session.
func (s *SessionService) Login(username, password string) (*domain.SessionRecord, error) {
	usersFile, err := s.repo.LoadUsers()
	if err != nil {
		return nil, fmt.Errorf("login: %w", err)
	}

	var valid bool
	for _, u := range usersFile.Users {
		if u.Username == username && u.Password == password {
			valid = true
			break
		}
	}

	if !valid {
		return nil, ErrInvalidCredentials
	}

	sessionsFile, err := s.repo.LoadSessions()
	if err != nil {
		return nil, fmt.Errorf("login: %w", err)
	}

	idBytes := make([]byte, 16)
	if _, err := rand.Read(idBytes); err != nil {
		return nil, fmt.Errorf("login: %w", err)
	}

	id := hex.EncodeToString(idBytes)

	sessionsFile.Sessions = append(sessionsFile.Sessions, domain.SessionRecord{
		ID:       id,
		Username: username,
		IsAdmin:  false,
	})

	if err := s.repo.SaveSessions(sessionsFile); err != nil {
		return nil, fmt.Errorf("login: %w", err)
	}

	return &domain.SessionRecord{
		ID:       id,
		Username: username,
		IsAdmin:  false,
	}, nil
}

// GetSession returns the session for the given id.
func (s *SessionService) GetSession(id string) (*domain.SessionRecord, error) {
	sessionsFile, err := s.repo.LoadSessions()
	if err != nil {
		return nil, fmt.Errorf("get session: %w", err)
	}

	for _, rec := range sessionsFile.Sessions {
		if rec.ID == id {
			return &domain.SessionRecord{
				ID:       rec.ID,
				Username: rec.Username,
				IsAdmin:  rec.IsAdmin,
			}, nil
		}
	}

	return nil, fmt.Errorf("session not found")
}

// Logout removes a session from the session store.
func (s *SessionService) Logout(id string) error {
	if id == "" {
		app.CoreLogInfo("empty session id, nothing to do")
		return nil
	}

	sessionsFile, err := s.repo.LoadSessions()
	if err != nil {
		return fmt.Errorf("logout: %w", err)
	}

	if len(sessionsFile.Sessions) == 0 {
		return nil
	}

	filtered := sessionsFile.Sessions[:0]
	for _, sess := range sessionsFile.Sessions {
		if sess.ID == id {
			continue
		}
		filtered = append(filtered, sess)
	}
	sessionsFile.Sessions = filtered

	if err := s.repo.SaveSessions(sessionsFile); err != nil {
		return fmt.Errorf("logout: %w", err)
	}

	return nil
}

// ElevateSessionToAdmin validates the pin and marks the session as admin.
func (s *SessionService) ElevateSessionToAdmin(sessionID, pin string) error {
	if sessionID == "" {
		return fmt.Errorf("missing session id")
	}

	cfg, err := s.repo.LoadAdminPin()
	if err != nil {
		return fmt.Errorf("load admin config failed: %w", err)
	}

	if cfg.AdminPin == "" || cfg.AdminPin != pin {
		return fmt.Errorf("invalid pin")
	}

	sessionsFile, err := s.repo.LoadSessions()
	if err != nil {
		return fmt.Errorf("load sessions failed: %w", err)
	}

	for i := range sessionsFile.Sessions {
		if sessionsFile.Sessions[i].ID == sessionID {
			sessionsFile.Sessions[i].IsAdmin = true

			if err := s.repo.SaveSessions(sessionsFile); err != nil {
				return fmt.Errorf("save sessions failed: %w", err)
			}

			return nil
		}
	}

	return fmt.Errorf("session not found")
}
