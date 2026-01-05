package security

import (
	"context"

	"machine/internal/domain"
)

// sessionFromContext returns the session stored in context, or nil.
func sessionFromContext(ctx context.Context) *domain.SessionRecord {
	v := ctx.Value(domain.SessionContextKey{})
	s, _ := v.(*domain.SessionRecord)
	return s
}

// IsAdmin returns true if the context has a session marked as admin.
func IsAdmin(ctx context.Context) bool {
	s := sessionFromContext(ctx)
	return s != nil && s.IsAdmin
}

// IsAuthenticated returns true if the context has an active session.
func IsAuthenticated(ctx context.Context) bool {
	return sessionFromContext(ctx) != nil
}
