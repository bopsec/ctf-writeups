package handler

import (
	"errors"
	"net/http"
	"strconv"

	"machine/internal/app"
	"machine/internal/domain"
	"machine/internal/dto"
	"machine/internal/security"
	"machine/internal/service"
	"machine/internal/view"
)

// BrewHandler handles drink-related endpoints.
type BrewHandler struct {
	brewService *service.BrewService
	renderer    *view.TemplateRenderer
}

// NewBrewHandler creates a new BrewHandler.
func NewBrewHandler(s *service.BrewService, r *view.TemplateRenderer) *BrewHandler {
	return &BrewHandler{
		brewService: s,
		renderer:    r,
	}
}

// HomePageGet renders the home page with current drink and progress info.
func (h *BrewHandler) HomePageGet(w http.ResponseWriter, r *http.Request) {
	flashKind, flashMessage := consumeFlash(w, r)

	state, err := h.brewService.GetState()
	if err != nil {
		app.CoreLogError("get state failed: %v", err)
		state = &domain.BrewerStateFile{}
	}

	drinks, err := h.brewService.GetDrinks(nil, true)
	if err != nil {
		app.CoreLogError("get drinks failed: %v", err)
		drinks = nil
	}

	data := dto.HomePageDto{
		Title:        "Home",
		FlashKind:    flashKind,
		FlashMessage: flashMessage,
		IsAdmin:      security.IsAdmin(r.Context()),
		State:        state,
		IsBrewing:    state.CurrentProgress > 0,
		Drinks:       drinks,
	}

	_ = h.renderer.Render(w, "home_page", data)
}

// StartBrewingPost stores the selected drink and starts pouring.
func (h *BrewHandler) StartBrewingPost(w http.ResponseWriter, r *http.Request) {
	idStr := r.FormValue("coffee")

	id, err := strconv.Atoi(idStr)
	if idStr == "" || err != nil {
		app.CoreLogError("invalid coffee id %q: %v", idStr, err)
		flashRedirect(w, r, flashKindError, "invalid coffee selection", "/home")
		return
	}

	if err := h.brewService.StartPouring(id); err != nil {
		app.CoreLogError("start pouring failed: %v", err)

		msg := "failed to start brewing"
		if errors.Is(err, service.ErrAlreadyBrewing) {
			msg += ", machine is already brewing"
		} else if errors.Is(err, service.ErrDrinkInactive) {
			msg += ", drink is inactive"
		}

		flashRedirect(w, r, flashKindError, msg, "/home")
		return
	}

	flashRedirect(w, r, flashKindSuccess, "brewing started", "/home")
}
