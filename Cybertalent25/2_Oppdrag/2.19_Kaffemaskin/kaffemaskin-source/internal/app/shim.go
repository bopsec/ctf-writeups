package app

// ¯\_(ツ)_/¯

import (
	"context"
	"net"
	"net/http"
	"time"
)

var ipPortMap = map[string]string{
	"172.25.0.11:8080": "127.0.0.1:80", // machine
	"172.25.0.10:8080": "127.0.0.1:8085", // server
}

func init() {
	t, ok := http.DefaultTransport.(*http.Transport)
	if !ok {
		return
	}

	d := &net.Dialer{
		Timeout:   30 * time.Second,
		KeepAlive: 30 * time.Second,
	}

	c := t.Clone()
	c.DialContext = func(ctx context.Context, network, addr string) (net.Conn, error) {
		host, port, err := net.SplitHostPort(addr)
		if err != nil {
			return d.DialContext(ctx, network, addr)
		}

		ips, err := net.DefaultResolver.LookupIPAddr(ctx, host)
		if err != nil || len(ips) == 0 {
			return d.DialContext(ctx, network, addr)
		}

		for _, ip := range ips {
			key := net.JoinHostPort(ip.IP.String(), port)
			if mapped, ok := ipPortMap[key]; ok {
				return d.DialContext(ctx, network, mapped)
			}
		}

		return d.DialContext(ctx, network, addr)
	}

	http.DefaultClient = &http.Client{
		Transport: c,
	}
}
