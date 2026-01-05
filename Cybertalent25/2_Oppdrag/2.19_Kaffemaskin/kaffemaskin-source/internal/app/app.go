// Package app contains application-level constants and settings.
package app

import (
	"log"
	"os"
)

// RootPath is the root to the persitence folder.
var RootPath = os.Getenv("PERSISTENCE_ROOT")

// CoreLoggingEnabled controls whether logging is active.
var CoreLoggingEnabled = true

// CoreLogInfo logs core informational messages.
func CoreLogInfo(format string, args ...any) {
	if !CoreLoggingEnabled {
		return
	}

	log.Printf("[INFO] "+format, args...)
}

// CoreLogError logs core error messages.
func CoreLogError(format string, args ...any) {
	if !CoreLoggingEnabled {
		return
	}

	log.Printf("[ERROR] "+format, args...)
}
