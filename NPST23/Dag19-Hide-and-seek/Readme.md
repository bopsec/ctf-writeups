## Dag 19 - Hide and seek

```
Emne: Hide and Seek

Som følge av et stadig økende trusselbilde, spesielt ifra sydligere strøk, har Nordpolar sikkerhetstjeneste etablert en intern enhet som skal beskytte tjenestens egne digitale systemer mot angrep. Enheten består av nøye selekterte tidligere alveteknologer som har god erfaring med bekjempelse av sydpolare aktører.

Grunnet tidligere prestasjoner på Nordpolen har NISSEN selv navngitt enheten til Julens Utvalgte Lærde Elektronisk databehandlende Sikkerhets og Operative Center, forkortet JULESOC. JULESOCen kan blant annet bidra til å finne ondsinnede fugler i datasystemene til Julenissens verksted, grave i sildcoin transaksjoner og analyse av speilglatte kopier.

JULESOC har nylig mottatt en speilkopi av en arbeidsstasjon lokalisert på Julenissens verksted. Det er mistanke om at noen uautoriserte har vært inne på maskinen og tukla. Vi trenger at du graver frem noen spor.

- Mellomleder

📎image.raw.gz
```

Måtte først dele image.raw i tre partisjoner med kpartx.\
En av delene hadde en mappe /hemmelig/ med en "code"-fil, denne inneholdt bare masse tall i et array.\
Den andre delen inneholdt noen tomme mapper, en python-fil som så ut til å lage "code"-filen, og et stort tekstdokument\
Den tredje delen inneholdt kun et bilde av en [QR-kode](Partisjoner/qr-kode.png) som bare var "blindspor dessverre, let videre"\
Tenkte bare prøve å bruke tallene fra code-filen som indeks til tegnene i tekstdokumentet.

Flagg:\
`PST{TheGrinchWouldHateThis}`

[1817, 1004, 2238, 1709, 18, 714, 2499, 3069, 2148, 854, 1480, 831, 2441, 373, 276, 374, 844, 2725, 736, 2204, 1107, 1478]\
Fant en annen array med indekser pluss en annen [nissetekst-lignende fil](nissetekst_2), men fant ingenting fra disse to..\
Kan hende det finnes et egg? Enn så lenge fikk jeg "eaf t ndpnc hhneteti p"...
