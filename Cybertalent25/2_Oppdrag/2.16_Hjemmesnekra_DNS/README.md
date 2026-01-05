# Hjemmesnekra DNS

Vi har klart å få tak i en kopi av DNS-videresenderen som kjører på ruteren til GooodGames. Ved første øyekast ser det ut til at DNS-videresenderen er proprietær og kan være sårbar. Se om du kan få tilgang til ruteren, og undersøk om du finner noe mistenkelig på den.

## Testmiljø
Serveren er kompilert for MIPSEL-arkitekturen. Vi antar at du vanligvis ikke kjører MIPSEL, så for å kjøre den lokalt kan du bruke _qemu-user-static_. Serveren trenger også sudo for å binde seg til port 53.

```sh
mkdir -p /<path>/mips-root
cp -a /usr/mipsel-linux-gnu/lib /<path>/mips-root/lib
sudo qemu-mipsel-static -L /<path>/mips-root ./dnsserver
```

En debugger-server kan startes med:

```sh
sudo qemu-mipsel-static -L /<path>/mips-root -g <port> ./dnsserver
```

## Annet
På grunn av begrensninger i brannmuren må du bruke port **4444/tcp** for omvendte skall, men bare i tilfelle du trenger det.

---

Ga opp

Fant ingen måte å bruteforce eller lekke canaryen på, da den endres hver gang serveren kræsjer (tror jeg? ihvertfall lokalt, men kanskje jeg gjorde noe feil i setup).\
Jeg kunne kræsje med segfault uten `stack smashing detected` ved noen lengde-mismatch, men jeg fant ikke ut mer eller hvordan jeg kunne exploite dette.
