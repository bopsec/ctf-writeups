## Dag 3 - Redacted

```
Emne: Redacted

Det er krise! Filene på alvemaskinene har blitt kryptert, og vi har ingen backups tilgjengelig!

På nissens skrivebord fant vi det vedlagte brevet, sammen med en kryptert fil.

Det er ubeskrivelig viktig at vi får åpnet denne filen igjen umiddelbart, da Jule NISSEN ikke klarer å huske innholdet!

- Mellomleder

📎 Mitt utpressingsbrev.docx
📎 huskeliste.txt.enc
```

Flyttet vekk "REDACTED" i Word\
Fant nøkkelen: dda2846b010a6185b5e76aca4144069f88dc7a6ba49bf128\
Flyttet bildet som beskrev "krypteringsmåten" med "Cut"-funksjonen i Word.\
Fant [dette](skjult_info.png)\
IVen er UtgangsVektor123, funnet av Edit log i dokumentet.

Brukte informasjonen fra bildet og løste som AES-CTR med ROT-13 på IVen.\
Flagg:\
`KRIPOS{Husk å se etter spor i snøen!}`


Hele outputen er [her](huskeliste.txt).
