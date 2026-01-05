package main

import (
	"machine/internal/web"
)

func main() {
	// start web server
	web.Start(":80")
}
