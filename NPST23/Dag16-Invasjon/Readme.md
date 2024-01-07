## Dag 16 - Invasjon

```
Emne: Invasjon

Gjennom temmelig hemmelige innhentingsmetoder har vi fått tak i det vedlagte dokumentet som avslører den egentlige hensikten bak løsepengeangrepet: Sydpolare aktører planlegger å invadere Nordpolen for å stoppe julen én gang for alle!

I dokumentet nevnes det at aktørene har plantet deep-cover agenter i blant oss, og at de har hemmelige koder for å etablere kontakt med disse. Analyser materialet og se om du klarer å avsløre de hemmelige kodene slik at vi kan få disse agentene på kroken!

I mellomtiden iverksetter vi umiddelbare mottiltak for å stanse invasjonen.

- Tastefinger

📎aksjon_2023.zip
```

Sjekket litt gjennom git branches, fant "ikke commit før julaften" der det står
```
Author: Pen Gwyn <p1@spst.no>
Date:   Mon Sep 25 11:11:11 2023 +0200

    Placeholder for eksfil av feltagenter

    Prosedyre for kodegenerering vil bli implementert senere for å beskytte
    våre agenter
```
Samt en fil som het feltagenter_kontaktmanual.md med noen KODE_PLACEHOLDERs for 3 agenter.\
Kjørte `grep -R feltagenter_kontaktmanual.md .` for å se om det var noen flere referanser til dette. Fant [pre-merge-commit](aksjon2023/_.git/hooks/pre-merge-commit) som skulle gjøre noen endringer, oversatte base64 jeg fant inne i filen

> Unnskyld, vet du veien til biblioteket? <RESPONS>. Sa jeg biblioteket? Jeg mente fiskeforhandleren, kan du vagge bort med meg

> Ikke god jul.

> KRIPOS{Flagg i alle kriker og kroker}

Flagg:\
`KRIPOS{Flagg i alle kriker og kroker}`


# Egg
Det fantes referanser til at noen hadde mistet et egg, sjekket lost-found og fant en commit som inneholdt et stort egg. Egget fantes i midten av [dette store egget](aksjon_2023/_.git/lost-found/other/fdfbb6ab8dda68e83853bf372a100e8ff6e8830f).

EGG 4:\
`EGG{h3ng3r 0g d1ngl3r}`
