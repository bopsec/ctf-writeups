package handler

import (
	"errors"
	"net/http"
	"time"

	"machine/internal/app"
	"machine/internal/dto"
	"machine/internal/security"
	"machine/internal/service"
	"machine/internal/view"
)

// ServiceHandler routes all
type ServiceHandler struct {
	brewService *service.BrewService
	renderer    *view.TemplateRenderer
}

func NewServiceHandler(s *service.BrewService, renderer *view.TemplateRenderer) *ServiceHandler {
	return &ServiceHandler{
		brewService: s,
		renderer:    renderer,
	}
}

// ServicePageGet renders the service page.
func (h *ServiceHandler) ServicePageGet(w http.ResponseWriter, r *http.Request) {
	flashKind, flashMessage := consumeFlash(w, r)

	status, err := h.brewService.GetServiceStatus()
	if err != nil {
		app.CoreLogError("load service status failed: %v", err)
	}

	data := dto.ServicePageDto{
		Title:        "Service",
		FlashKind:    flashKind,
		FlashMessage: flashMessage,
		IsAdmin:      security.IsAdmin(r.Context()),
	}

	if status != nil {
		data.ServiceTimeOfDay = status.ServiceTimeOfDay

		for _, e := range status.Entries {
			if e.IntervalMinutes <= 0 {
				continue
			}

			var lastRan string
			if e.LastRan != nil {
				lastRan = e.LastRan.UTC().Format(time.RFC3339)
			}

			switch e.MaintenanceMode {
			case "daily":
				data.HasDaily = true
				data.DailyLastRan = lastRan
				data.DailyIntervalMinutes = e.IntervalMinutes
			case "weekly":
				data.HasWeekly = true
				data.WeeklyLastRan = lastRan
				data.WeeklyIntervalMinutes = e.IntervalMinutes
			case "monthly":
				data.HasMonthly = true
				data.MonthlyLastRan = lastRan
				data.MonthlyIntervalMinutes = e.IntervalMinutes
			}
		}
	}

	_ = h.renderer.Render(w, "service_page", data)
}

// RunServiceScriptPost runs a maintenance script for the given mode.
func (h *ServiceHandler) RunServiceScriptPost(w http.ResponseWriter, r *http.Request) {
	mode := r.URL.Query().Get("mode")
	if mode == "" {
		app.CoreLogError("missing mode query parameter")
		flashRedirect(w, r, flashKindError, "missing mode query parameter", "/service")
		return
	}

	err := h.brewService.RunMaintenanceScript(mode)
	if err != nil {
		app.CoreLogError("run maintenance script failed: %v", err)

		msg := "failed to run service script"

		switch {
		case errors.Is(err, service.ErrMissingSignatureHeader):
			msg += ", missing signature header"
		case errors.Is(err, service.ErrUnexpectedSignatureAlg):
			msg += ", unexpected signature algorithm"
		case errors.Is(err, security.ErrInvalidSignature):
			msg += ", signature verification failed"
		}

		flashRedirect(w, r, flashKindError, msg, "/service")
		return
	}

	flashRedirect(w, r, flashKindSuccess, "service script executed", "/service")
}
