## 2. Oppdrag

# 2.0.1_manipulaite_1
Denne virket det som at man fikk gratis, skulle bare prøve å Social Engineere forskjellige "liksom"-employees. Inneholdt noen småhint til oppgavene i anvilticket.

# 2.0.2_anvilticket_1
Testet litt av hvert fra cookie manipulation til SQLi etc. Fant ut at jeg kunne se hvilke tickets som fantes ved å åpne https://anvilticket.cybertalent.no/ticket/{x}. \
Fant etter ut at comment hadde samme funksjonalitet, men at denne ikke hadde noen credentials sjekk.

> https://anvilticket.cybertalent.no/comment/4
```
{"count": 1, "comments": [["admin", "Hey Tova,\n\nAs per your request, your password has been reset. Your new login credentials are as follows:\n\nNew Password: SamplePasswordForChange!\n\nPlease ensure to update this password upon your next login for security purposes. If you require any further assistance or have additional concerns, feel free to reach out.\n\nThank you for your patience and understanding.\n\nBest regards,\nMelow\nIT support"]]}
```

> https://anvilticket.cybertalent.no/comment/7
```
{"count": 1, "comments": [["admin", "Hi Carla,\n\nNew user account created:\nthenewguy:FLAG{c4dcdfbbbb81e532889cb676b8b2bc72}\n\nPlease share these credentials securely with our Eva. Let us know if further assistance is needed.\n\nThanks,\nAdmin"]]}
```

Der lå flagget, og en bruker som jeg kan logge inn på for å finne flere flagg.
```
login@corax:~$ scoreboard FLAG{c4dcdfbbbb81e532889cb676b8b2bc72}
Kategori: 2. Initiell aksess
Oppgave:  2.0.2_anvilticket_1
Svar:     c4dcdfbbbb81e532889cb676b8b2bc72
Poeng:    10

Godt jobbet!
```

# 2.0.3_anvilticket_2
Fant noen nye tickets, men ingenting som så ut til å inneholde noe spesielt. \
Testet igjen litt rundt med cookie manipulations før jeg sjekket Update-funksjonen.\
Fanget en Update-request, så at ting ble sendt i klartekst, visste at det fantes group=x og admin=bool, tok det beste og prøvde å legge til &admin=true\
Fikk tilbake en ?update_ok.\

Flagget havnet øverst sammen med den nye groupen.\
Welcome thenewguy!\

Group: IT/admin FLAG: c40d1fa3cca67f7fd75047858194a076

```
login@corax:~$ scoreboard FLAG{c40d1fa3cca67f7fd75047858194a076}
Kategori: 2. Initiell aksess
Oppgave:  2.0.3_anvilticket_2
Svar:     c40d1fa3cca67f7fd75047858194a076
Poeng:    10

Veldig bra! Kan du bruke dette til noe mer?
```
# 2.0.4_manipulaite_2
Tok noen minutter før jeg skjønte at manipulaite 2 var gjennom kommentarfeltet til en av requestene i anvilticket gjennom en AI som het Eva.
Testet litt og innså at Eva kunne gjøre det meste ganske lett, men pga 
```Hey,

Sorry for the late ticket. A couple of days ago the IT development team implemented a system to censor all sensitive information in tickets.
It seems like the developers completely forgot to relay this information during last minute integration.

As you can see, if I copy-paste my ssh key it will show as CLASSIFIED.

[CLASSIFIED], see!

- IT Admin
```
Så var det ikke mulig for Eva å gi meg flagget uten at det ble FLAG{[Classified]}.\
Ba Eva om å sende det til meg i binary. Tok litt frem og tilbake før hun til slutt [ga meg flagget](eva.png).

# 2.0.5_pcap
Denne lå i en av ticketene i anvilticket, en drop.pcap som hadde noe trafikk til bl.a reddit, CNN, tiktok og github.\
Lette litt gjennom og fant ut at den hentet to filer\

```
GET /package.txt HTTP/1.1
Host: 172.18.0.5:8000
Connection: close
Via: 1.1 tinyproxy (tinyproxy/1.11.1)
User-Agent: Mozilla/4.0 (compatible; MSIE 5.00; Windows 98)
Accept: */*

HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.11.2
Date: Thu, 14 Dec 2023 18:15:39 GMT
Content-type: text/plain
Content-Length: 19
Last-Modified: Thu, 07 Dec 2023 16:35:16 GMT

pbq5cdr1ymk6mrh_GKT
```

```
GET /package.zip HTTP/1.1
Host: 172.18.0.5:8000
Connection: close
Via: 1.1 tinyproxy (tinyproxy/1.11.1)
User-Agent: Mozilla/4.0 (compatible; MSIE 5.00; Windows 98)
Accept: */*

HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.11.2
Date: Thu, 14 Dec 2023 18:14:47 GMT
Content-type: application/zip
Content-Length: 314
Last-Modified: Thu, 14 Dec 2023 17:48:58 GMT

PK....	......W2.-.............configUT	../={eL?{eux..............1.Qp......T..34.*].J.._.k-Z.
_	....Q#..,&..v5XI.B.........b......r.....w.R7......W\.$....>.......}..O.	.>..a...|".*.N...8.....A8i....y.PK..2.-.........PK......	......W2.-...........................configUT.../={eux.............PK..........L.........
```

Hentet ut zip-filen fra package.zip, var først corrupted så fikset gjennom WinRAR sin "Repair"-funksjon. Dette fikset .zip-mappen og fikk en fil config som var passordbeskyttet.\
pbq5cdr1ymk6mrh_GKT fra package.txt var passordet.

```
Host gw
    HostName dep-gw.utl
    User preyz
    IdentityFile ~/.ssh/id_ed25519.key

# FLAG{ffd232792c966fe54d841e7e42c64fea}
```

Og der lå flagget.
```
login@corax:~$ scoreboard FLAG{ffd232792c966fe54d841e7e42c64fea}
Kategori: 2. Initiell aksess
Oppgave:  2.0.5_pcap
Svar:     ffd232792c966fe54d841e7e42c64fea
Poeng:    10

Veldig bra!

Ny fil: /home/login/.ssh/config
```
# 2.0.6_dep-gw
Når jeg løste 2.0.5 og 2.0.4(tror jeg?) fikk jeg beskjed om at to nye filer ble lagt til i /.ssh.\
\
config som inneholdt dette

Host gw dep-gw.utl\
    HostName dep-gw.utl\
    User preyz\
    IdentityFile ~/.ssh/id_ed25519\
    \
og id_ed25519 som inneholdt en private ssh key.\
SSHet inn til preyz@dep-gw.utl.\
ls -la viste en FLAGG-fil\
cat FLAGG

```
login@corax:~/.ssh$ ssh preyz@dep-gw.utl
Linux dep-gw 6.1.0-16-cloud-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.67-1 (2023-12-12) x86_64

The programs included with the Debian GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Debian GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
Last login: Wed Dec 27 23:20:51 2023 from 10.5.84.80
Welcome to fish, the friendly interactive shell
Type help for instructions on how to use fish
preyz@dep-gw ~> ls -la
total 44
drwxr-xr-x 1 preyz preyz 4096 Dec 27 23:17 ./
drwxr-xr-x 1 root  root  4096 Dec 13 09:25 ../
-rw-r--r-- 1 preyz preyz  220 Apr 23  2023 .bash_logout
-rw-r--r-- 1 preyz preyz 3526 Apr 23  2023 .bashrc
drwx------ 3 preyz preyz 4096 Dec 27 23:17 .config/
drwx------ 3 preyz preyz 4096 Dec 27 23:17 .local/
-rw-r--r-- 1 preyz preyz  807 Apr 23  2023 .profile
drwx------ 1 preyz preyz 4096 Dec 13 09:25 .ssh/
-rw-r--r-- 1 preyz preyz   40 Dec 27 12:09 FLAGG
preyz@dep-gw ~> cat FLAGG
FLAGG: 59f4c17e6a148ad7bf4b781a7de9e84a
```

```
login@corax:~$ scoreboard FLAG{59f4c17e6a148ad7bf4b781a7de9e84a}
Kategori: 2. Initiell aksess
Oppgave:  2.0.6_dep-gw
Svar:     59f4c17e6a148ad7bf4b781a7de9e84a
Poeng:    10

Bra jobba, vi har nå kommet inn i infrastrukturen deres igjen! Vi begynte å få oversikt over infrastrukturen deres sist vi hadde tilgang, og har lagt det vi har av informasjon om de forskjellige departementene i oppdragsmappen din på corax.

Nye filer i /home/login/2_oppdrag/
```
Dette unlocket altså 2.1-2.7