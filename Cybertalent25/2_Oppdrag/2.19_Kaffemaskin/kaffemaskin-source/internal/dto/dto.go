// Package dto contains objects going out.
package dto

import "machine/internal/domain"

// HomePageDto holds data for the home page.
type HomePageDto struct {
	Title             string
	FlashKind         string
	FlashMessage      string
	IsAdmin           bool
	State             *domain.BrewerStateFile
	SelectedDrinkName string
	IsBrewing         bool
	Drinks            []*domain.DrinkRecord
}

// ConfigPageDto holds data for the config page.
type ConfigPageDto struct {
	Title        string
	FlashKind    string
	FlashMessage string
	IsAdmin      bool
}

// FilePageDto holds data for the file page with menu and optional active file.
type FilePageDto struct {
	Title        string
	FlashKind    string
	FlashMessage string
	IsAdmin      bool

	UserFiles  []string
	AdminFiles []string

	Path    string
	Content string
}

// ServicePageDto holds data for the service page.
type ServicePageDto struct {
	Title        string
	FlashKind    string
	FlashMessage string
	IsAdmin      bool

	ServiceTimeOfDay string

	HasDaily               bool
	DailyLastRan           string
	DailyIntervalMinutes   int
	HasWeekly              bool
	WeeklyLastRan          string
	WeeklyIntervalMinutes  int
	HasMonthly             bool
	MonthlyLastRan         string
	MonthlyIntervalMinutes int
}

// PinPageDto holds data for the pin page.
type PinPageDto struct {
	Title        string
	FlashKind    string
	FlashMessage string
	IsAdmin      bool
}

// LoginPageDto holds data for the login page.
type LoginPageDto struct {
	Title        string
	FlashKind    string
	FlashMessage string
}
