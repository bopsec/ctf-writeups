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

// SessionHandler handles login and session endpoints.
type SessionHandler struct {
	sessionService *service.SessionService
	renderer       *view.TemplateRenderer
}

// NewSessionHandler creates a new SessionHandler.
func NewSessionHandler(s *service.SessionService, r *view.TemplateRenderer) *SessionHandler {
	return &SessionHandler{
		sessionService: s,
		renderer:       r,
	}
}

// PinPageGet renders the pin page.
func (h *SessionHandler) PinPageGet(w http.ResponseWriter, r *http.Request) {
	flashKind, flashMessage := consumeFlash(w, r)

	data := dto.PinPageDto{
		Title:        "Pin",
		FlashKind:    flashKind,
		FlashMessage: flashMessage,
		IsAdmin:      security.IsAdmin(r.Context()),
	}

	_ = h.renderer.Render(w, "pin_page", data)
}

// LoginPageGet renders the login page.
func (h *SessionHandler) LoginPageGet(w http.ResponseWriter, r *http.Request) {
	if security.IsAuthenticated(r.Context()) {
		http.Redirect(w, r, "/", http.StatusSeeOther)
		return
	}

	flashKind, flashMessage := consumeFlash(w, r)

	data := dto.LoginPageDto{
		Title:        "Login",
		FlashKind:    flashKind,
		FlashMessage: flashMessage,
	}

	_ = h.renderer.Render(w, "login_page", data)
}

// SessionPost handles login form submissions.
func (h *SessionHandler) SessionPost(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		flashRedirect(w, r, flashKindError, "bad form", "/login")
		return
	}

	username := r.FormValue("username")
	password := r.FormValue("password")

	if username == "" || password == "" {
		flashRedirect(w, r, flashKindError, "missing credentials", "/login")
		return
	}

	session, err := h.sessionService.Login(username, password)
	if err != nil {
		app.CoreLogError("login failed: %v", err)

		msg := "login failed"
		if errors.Is(err, service.ErrInvalidCredentials) {
			msg = "invalid credentials"
		}

		flashRedirect(w, r, flashKindError, msg, "/login")
		return
	}

	http.SetCookie(w, &http.Cookie{
		Name:     "session",
		Value:    session.ID,
		Path:     "/",
		HttpOnly: true,
		Secure:   false,
		SameSite: http.SameSiteLaxMode,
	})

	http.Redirect(w, r, "/home", http.StatusSeeOther)
}

// PinPost handles pin form submissions.
func (h *SessionHandler) PinPost(w http.ResponseWriter, r *http.Request) {
	if err := r.ParseForm(); err != nil {
		flashRedirect(w, r, flashKindError, "bad form", "/pin")
		return
	}

	pin := r.FormValue("password")

	var sessionID string
	if c, err := r.Cookie("session"); err == nil {
		sessionID = c.Value
	}

	if err := h.sessionService.ElevateSessionToAdmin(sessionID, pin); err != nil {
		app.CoreLogError("elevate session failed: %v", err)
		flashRedirect(w, r, flashKindError, "pin invalid", "/pin")
		return
	}

	flashRedirect(w, r, flashKindSuccess, "code correct", "/pin")
}

// SessionDelete handles logout requests.
func (h *SessionHandler) SessionDelete(w http.ResponseWriter, r *http.Request) {
	var sessionID string
	if c, err := r.Cookie("session"); err == nil {
		sessionID = c.Value
	}

	if err := h.sessionService.Logout(sessionID); err != nil {
		app.CoreLogError("logout failed: %v", err)
		flashRedirect(w, r, flashKindError, "logout failed", "/config")
		return
	}

	http.SetCookie(w, &http.Cookie{
		Name:   "session",
		Value:  "",
		Path:   "/",
		MaxAge: -1,
	})

	flashRedirect(w, r, flashKindSuccess, "successfully logged out", "/login")
}
