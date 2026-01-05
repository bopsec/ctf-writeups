# C+-

Vi fant dette programmet kjørende på infrastrukturen deres, men det virker som om Joe Logan ikke klarte å finne en C++-kompilator i tide, så han bestemte seg for å implementere OOP og virtuelle funksjoner i C?

Hjelp oss med å finne ut hva de skjuler!

```sh
nc cplusminus 1337
```

--------------------------------------------------------------------------


Segfault på create mouse device med DPI -1 for så å deretter sjekke mouse object på denne indexen


USB først - så den tar sin egen vtable-chunk\
Mouse med negativ DPI - frigjør mouse vtable (16 bytes) til tcache\
Configure USB (size=16) - malloc(16) gjenbruker freed mouse vtable\
Trigger på mouse - kaller vår fake vtable → admin-funksjonen\
Typisk use after free


```sh
Received 0x85 bytes:
    b'Admin detected, showing hidden admin-flags:\n'
    b'e7fd6650ef9ab4806b711188539a4fb8\n'
    b'-----------------\n'
    b'1. Add USB Device\n'
    b'2. Add Mouse Device\n'
Admin detected, showing hidden admin-flags:
e7fd6650ef9ab4806b711188539a4fb8
-----------------
1. Add USB Device
2. Add Mouse Device
[...]
```
Koden ligger i [exploit.py](exploit.py)

login@corax ~/storage $ scoreboard e7fd6650ef9ab4806b711188539a4fb8

2.6.1 Cplusminus\
Objektorientert C var kanskje ikke så lurt?

