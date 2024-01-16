# 2.2

## 2.2.1
Denne løste jeg ikke helt selv, trengte et ganske stort push.\
Fikk et cipher med fire ruter, hver rute med 7x14 bokstaver, ingen annen kontekst.\
Etter litt analyse fant jeg ut at det manglet Q, noe som er vanlig i visse ciphers for at alfabetet skal passe som 25 forskjellige characters. Satt meg litt inn i Four Square ciphers da det passet godt, men ga meg før jeg fant noe interessant.\
Fikk et nytt hint om Four Square, og at det kunne løses med riktig crib. Jeg hadde naturligvis testet FLAG/FLAGG tidligere, men nå testet jeg "officeforclassicalciphers".\
Sendte det gjennom et verktøy som bruteforcet med criben, og fikk ut en plaintext:
```
all of us in the office for classical ciphers congratulate you with passing the first hurdle there are still a few more steps until you are finished the next one is probably a little bit easier you just have to climb over a small fence victor delta papa tango india november echo india india india foxtrot victor india romeo victor victor zulu juliett november victor victor charlie lima juliett victor juliett juliett whiskey kilo lima india india india kilo romeo yankee
```
De fonetiske bokstavene stavet VDPTINEIIIFVIRVVZJNVVCLJVJJWKLIIIKRY.\
Jeg så referansen til å hoppe over "a fence", så jeg gikk rett til rail-fence cipher, og brukte [dcode sin "autosolver"](https://www.dcode.fr/rail-fence-cipher) for å teste diverse.\
På *key=4* og *offset=0* fant jeg en plaintext som startet med VENIVIDIVICI. Hele plaintexten var VENIVIDIVICIPFLIJVTIVKJRIVJRWVNZKYLJ.\
Resterende (PFLIJVTIVKJRIVJRWVNZKYLJ) var fremdeles kryptert, så tenkte kjapt en rot-N-cipher for å holde oss til latin.\
På ROT17 fant jeg YOURSECRETSARESAFEWITHUS.
```
login@corax:~/2_oppdrag$ scoreboard FLAG{YOURSECRETSARESAFEWITHUS}
Kategori: 2.2. Department of Cryptography
Oppgave:  2.2.1_klassisk_krypto
Svar:     YOURSECRETSARESAFEWITHUS
Poeng:    10

Godt jobbet, du klarte å knekke koden!
```

## 2.2.2
Fikk bare MOV16-koden i [2.2.2.txt](2.2.2/2_2_2.txt) og fikk vite at den tar kun inn store bokstaver. Ref [LESMEG.md](2.2.2/Lesmeg.md).\
Prøvde å mappe litt input -> output, men det var ikke noe lett mønster å finne, så jeg gikk til det neste jeg kom på, som var å overføre hele koden til et annet språk så jeg mer effektivt kunne bruteforce alle forskjellige alternativer...\
Under oversettelsen innså jeg ut at pga LRO og XOR så gjør programmet egentlig det samme som å ta inn 8 store bokstaver, selv om det egentlig krever 16.\
2.2.2-koden i C++ kan finnes [her](2.2.2/2_2_2.cpp). Dette er det første programmet jeg har skrevet i C++ så det kan være jeg har gjort mye tull, bestemte C++ for at det skulle gå litt raskere, var vel snakk om 200 milliard forskjellige inputs..\
Lagde så [et python-program](2_2_2.py) for å kjøre forskjellige "starting letters" i 2_2_2.cpp og delte disse på 13 tråder.\
Fikk til slutt [denne](2.2.2/possibleFlagZ.txt) som output. Den er utf16-encodet så kan hende den ikke vises ordentlig.
```
Possible flag found: FLAG 2f114edd6a}
Possible flag found: AEYATABBAEcACgAyAGYAMQAxADQAZQBkAGQANgBhAH0=
Possible flag found: 00ZX00TR00QO00UF
```
Manglet visst en { etter jeg hadde kjørt scriptet mitt, men så at jeg var på 15 av forventet 16 tegn, så jeg bare la det til selv.\
Hvis man skal sende det direkte inn til det originale MOV16-skriptet må man bare endre min input litt for å få f.eks AZZXATTRAQQOAUUF, dette gir også hele flagget. Det er flere inputs som mapper til flagget.
```
login@corax:~$ scoreboard FLAG{2f114edd6a}
Kategori: 2.2. Department of Cryptography
Oppgave:  2.2.2_moderne_krypto
Svar:     2f114edd6a
Poeng:    10

Utmerket! Når du knakk koden fant vi en brukermanual knyttet til et MOV<-16-system. Vi har lagt den i oppdragsmappen din på corax. Kanskje du får bruk for den i Department of Nuclear Power?

Ny fil: /home/login/2_oppdrag/ACCESS16 User Manual.pdf
```
# 2.2.3
Uløst.
