// Package view contains template renderer.
package view

import (
	"html/template"
	"net/http"
)

// TemplateRenderer renders html templates.
type TemplateRenderer struct {
	templates *template.Template
}

// NewTemplateRenderer creates a TemplateRenderer from template files.
func NewTemplateRenderer(pattern string) (*TemplateRenderer, error) {
	funcMap := template.FuncMap{
		"raw": func(s string) template.HTML { return template.HTML(s) },
	}

	tmpl, err := template.New("").Funcs(funcMap).ParseGlob(pattern)
	if err != nil {
		return nil, err
	}

	return &TemplateRenderer{
		templates: tmpl,
	}, nil
}

// Render renders a named template with data to the writer.
func (r *TemplateRenderer) Render(w http.ResponseWriter, name string, data any) error {
	w.Header().Set("Content-Type", "text/html; charset=utf-8")
	return r.templates.ExecuteTemplate(w, name, data)
}
