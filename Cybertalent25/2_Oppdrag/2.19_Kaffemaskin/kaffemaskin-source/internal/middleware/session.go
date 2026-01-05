// Package middleware provides shared http middleware helpers.
package middleware

import (
	"context"
	"errors"
	"net/http"

	"machine/internal/domain"
	"machine/internal/service"
)

// SessionMiddleware provides auth helpers for handlers.
type SessionMiddleware struct {
	sessionService *service.SessionService
}

// NewSessionMiddleware creates a new AuthMiddleware.
func NewSessionMiddleware(s *service.SessionService) *SessionMiddleware {
	return &SessionMiddleware{
		sessionService: s,
	}
}

// SessionFromRequest returns the session from the request cookie.
func (m *SessionMiddleware) SessionFromRequest(r *http.Request) (*domain.SessionRecord, error) {
	c, err := r.Cookie("session")
	if err != nil || c.Value == "" {
		return nil, errors.New("missing session")
	}

	return m.sessionService.GetSession(c.Value)
}

// WithSession returns a new context with the given session stored.
func WithSession(ctx context.Context, s *domain.SessionRecord) context.Context {
	return context.WithValue(ctx, domain.SessionContextKey{}, s)
}

// RequireUser ensures a valid user session is present.
func (m *SessionMiddleware) RequireUser(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		sess, err := m.SessionFromRequest(r)
		if err != nil {
			http.Redirect(w, r, "/login", http.StatusFound)
			return
		}

		ctx := WithSession(r.Context(), sess)
		next(w, r.WithContext(ctx))
	}
}

// RequireAdmin ensures a valid admin session is present.
func (m *SessionMiddleware) RequireAdmin(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		sess, err := m.SessionFromRequest(r)
		if err != nil || !sess.IsAdmin {
			http.Redirect(w, r, "/home", http.StatusFound)
			return
		}

		ctx := WithSession(r.Context(), sess)
		next(w, r.WithContext(ctx))
	}
}

// CtxSession adds session to ctx without requiring a session.
func (m *SessionMiddleware) CtxSession(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		sess, _ := m.SessionFromRequest(r)
		ctx := WithSession(r.Context(), sess)
		next(w, r.WithContext(ctx))
	}
}
