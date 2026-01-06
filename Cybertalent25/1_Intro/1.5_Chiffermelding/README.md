# Chiffermelding

Når man vil sende meldinger uten at andre lett kan lese dem, kan man bruke en form for chiffer for å gjøre teksten uforståelig.

Ser du imidlertid litt nærmere på bokstavene, er det lett å få rimelig mening ut av dem...

```sh
nc chiffermelding 1337
```
--------------------------------------------


```sh
login@corax ~/1_grunnleggende/1.5_Chiffermelding $ nc chiffermelding 1337
Her har du en hemmelig melding:
omtfidogiriganøagmremfneohrraeareaenrldrsjekedeg
- Signert av Roscher Lund

Finn ut hva den opprinnelige meldingen var, og fortell meg hvem som skrev den

>
```

Hvis man tar hver 3. bokstav får man
"Oforaarforaarredmigingenharelsketdigømmereendjeg"
Dette er åpningslinjen fra diktet "Til Foraaret" og forfatteren er Henrik Wergeland


```sh
> Henrik Wergeland
ca85d88caabfba083aac18db476e2fa2
```

Flagget er ca85d88caabfba083aac18db476e2fa2