// Package web contains the HTTP server and routing setup.
package web

import (
	"net/http"

	"machine/internal/app"
	"machine/internal/handler"
	"machine/internal/middleware"
	"machine/internal/repository"
	"machine/internal/service"
	"machine/internal/view"
)

// Start creates the http server and registers routes.
func Start(bind string) {
	renderer, err := view.NewTemplateRenderer(app.RootPath + "view/*/*.html")
	if err != nil {
		panic(err)
	}

	// repositories
	brewerRepo := repository.NewBrewerRepository(app.RootPath + "data/")
	sessionRepo := repository.NewSessionRepository(app.RootPath + "data/")
	assetRepo := repository.NewAssetRepository(app.RootPath + "assets/public/")
	securityRepo := repository.NewSecurityRepository(app.RootPath + "data/")

	// services
	fileService := service.NewFileService()
	sessionService := service.NewSessionService(sessionRepo)
	brewerService := service.NewBrewService(brewerRepo, securityRepo)
	assetService := service.NewAssetService(assetRepo, securityRepo)

	// handlers
	assetsHandler := handler.NewAssetsHandler(assetService)
	configHandler := handler.NewConfigHandler(assetService, renderer)
	sessionHandler := handler.NewSessionHandler(sessionService, renderer)
	fileHandler := handler.NewFileHandler(fileService, renderer)
	brewerHandler := handler.NewBrewHandler(brewerService, renderer)
	serviceHandler := handler.NewServiceHandler(brewerService, renderer)

	// middleware
	sessionMiddleware := middleware.NewSessionMiddleware(sessionService)

	// router
	mux := http.NewServeMux()

	// static assets
	mux.Handle("/assets/", assetsHandler)

	// api endpoints
	mux.HandleFunc("POST /session/login", sessionHandler.SessionPost)
	mux.HandleFunc("POST /session/logout", sessionMiddleware.RequireUser(sessionHandler.SessionDelete))
	mux.HandleFunc("POST /session/admin/pin", sessionMiddleware.RequireUser(sessionHandler.PinPost))

	mux.HandleFunc("POST /file/{path...}", sessionMiddleware.RequireUser(fileHandler.FilePost))

	mux.HandleFunc("POST /brewer/run", sessionMiddleware.RequireUser(brewerHandler.StartBrewingPost))

	mux.HandleFunc("POST /config/background", sessionMiddleware.RequireUser(configHandler.UploadBackgroundPost))
	mux.HandleFunc("GET /config/source", sessionMiddleware.RequireAdmin(configHandler.DownloadSourceCodeGet))

	mux.HandleFunc("POST /service/run", sessionMiddleware.RequireAdmin(serviceHandler.RunServiceScriptPost))

	// pages
	mux.Handle("GET /home", http.RedirectHandler("/", http.StatusMovedPermanently))
	mux.HandleFunc("/", sessionMiddleware.RequireUser(brewerHandler.HomePageGet))
	mux.HandleFunc("GET /login", sessionMiddleware.CtxSession(sessionHandler.LoginPageGet))
	mux.HandleFunc("GET /pin", sessionMiddleware.RequireUser(sessionHandler.PinPageGet))
	mux.HandleFunc("GET /config", sessionMiddleware.RequireUser(configHandler.ConfigPageGet))
	mux.HandleFunc("GET /file/{path...}", sessionMiddleware.RequireUser(fileHandler.FileEditPageGet))
	mux.HandleFunc("GET /service", sessionMiddleware.RequireAdmin(serviceHandler.ServicePageGet))

	// and begin
	_ = http.ListenAndServe(bind, mux)
}
