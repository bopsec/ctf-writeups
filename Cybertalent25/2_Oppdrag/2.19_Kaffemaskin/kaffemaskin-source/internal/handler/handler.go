// Package handler contains HTTP handlers.
package handler

import (
	"net/http"
	"strings"
)

const (
	flashCookieName  = "GoodGamesFlashFeedback"
	flashCookiePath  = "/"
	flashKindSuccess = "success"
	flashKindWarning = "warning"
	flashKindError   = "error"
)

// setFlash sets a one-time flash cookie.
func setFlash(w http.ResponseWriter, kind, message string) {
	value := kind + ":" + message

	http.SetCookie(w, &http.Cookie{
		Name:     flashCookieName,
		Value:    value,
		Path:     flashCookiePath,
		HttpOnly: true,
		Secure:   false,
		SameSite: http.SameSiteLaxMode,
	})
}

// consumeFlash reads and clears the flash cookie.
func consumeFlash(w http.ResponseWriter, r *http.Request) (string, string) {
	c, err := r.Cookie(flashCookieName)
	if err != nil {
		return "", ""
	}

	http.SetCookie(w, &http.Cookie{
		Name:     flashCookieName,
		Value:    "",
		Path:     flashCookiePath,
		MaxAge:   -1,
		HttpOnly: true,
		Secure:   false,
		SameSite: http.SameSiteLaxMode,
	})

	kind, message, ok := strings.Cut(c.Value, ":")
	if !ok {
		return "", ""
	}

	return kind, message
}

// flashRedirect sets a flash and redirects with see other.
func flashRedirect(w http.ResponseWriter, r *http.Request, kind, message, location string) {
	setFlash(w, kind, message)
	http.Redirect(w, r, location, http.StatusSeeOther)
}
