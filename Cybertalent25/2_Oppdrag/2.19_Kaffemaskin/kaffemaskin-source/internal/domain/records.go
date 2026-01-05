package domain

import "time"

// ================================================================================

// BrewerSettingsFile represent user/brewer_settings.json
type BrewerSettingsFile struct {
	Brewer BrewerRecord
	Drinks []DrinkRecord `json:"drinks"`
}

// BrewerRecord represent brewer configuration.
type BrewerRecord struct {
	WarmupTimeS         int             `json:"warmup_time_s"`
	MaxShotsBeforeFlush int             `json:"max_shots_before_flush"`
	Containers          ContainerRecord `json:"containers"`
}

// ServiceTimeRecord represent recurring service times.
type ServiceTimeRecord struct {
	Daily   int `json:"daily"`
	Weekly  int `json:"weekly"`
	Monthly int `json:"monthly"`
}

// ContainerRecord represent consumable container levels.
type ContainerRecord struct {
	CoffeeBeans int `json:"coffee_beans"`
	CacaoPowder int `json:"cacao_powder"`
	Milk        int `json:"milk"`
}

// DrinkRecord represent a drink the machine serves.
type DrinkRecord struct {
	ID              int    `json:"id"`
	Name            string `json:"name"`
	Description     string `json:"description"`
	ImagePath       string `json:"image_path"`
	BeansGram       int    `json:"beans_gram"`
	CacaoPowderGram int    `json:"cacao_powder_gram"`
	WaterTempC      int    `json:"water_temp_c"`
	WaterMl         int    `json:"water_ml"`
	MilkTempC       int    `json:"milk_temp_c"`
	MilkMl          int    `json:"milk_ml"`
	Active          bool   `json:"active"`
}

// ================================================================================

// MaintenanceFile represent admin/maintenance.json.
type MaintenanceFile struct {
	ServiceTimeOfDay string              `json:"service_time_of_day"`
	Entries          []MaintenanceRecord `json:"maintenance"`
}

// MaintenanceRecord represents a maintenance entry.
type MaintenanceRecord struct {
	MaintenanceMode string     `json:"maintenance_mode"`
	ScriptPath      string     `json:"maintenance_script_path"`
	LastRan         *time.Time `json:"last_ran"`
	IntervalMinutes int        `json:"maintenance_interval_minutes"`
}

// ================================================================================

// AdminConfigFile represent admin/admin.json.
type AdminConfigFile struct {
	AdminPin string `json:"admin_pin"`
}

// ================================================================================

// UserFile represent user/users.json.
type UserFile struct {
	Users []UserRecord `json:"users"`
}

// UserRecord represent a single user.
type UserRecord struct {
	Username string `json:"username"`
	Password string `json:"password"`
}

// ================================================================================

// BrewerStateFile represent hidden/brewer_state.json.
type BrewerStateFile struct {
	SelectedDrinkID int  `json:"selected_drink"`
	CurrentProgress int  `json:"current_progress"`
	TimeToBrew      int  `json:"time_to_brew"`
}

// ================================================================================

// SessionFile represent hidden/sessions.json.
type SessionFile struct {
	Sessions []SessionRecord `json:"sessions"`
}

// SessionRecord represent a single session.
type SessionRecord struct {
	ID       string `json:"id"`
	Username string `json:"username"`
	IsAdmin  bool   `json:"is_admin"`
}

// ================================================================================
