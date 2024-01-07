## Dag 15 - Bit-råte

```
Emne: Bit.råte

Brukerveiledningen til en av de eldste maskinene på verkstedet har blitt borte. Heldigvis har Julenissens arkiv 1000 sikkerhetskopier av dokumentet på magnetbånd. Det viser seg at alle kopiene er kraftig angrepet av bit-råte så dokumentet må gjenoppbygges. Ifølge arkivalven så er brukerveiledningen skrevet på gammel-nordpolarsk som har samme alfabet som norsk, men inneholder ikke nye tegn som disse: {}#$[]§¤@

Når du finer ut av det så send meg MD5-sjekksummen til det gjenoppbyggede dokumentet på formen PST{checksum}. Svaret er ikke versalfølsomt.

- Mellomleder

📎backups.zip
```

Tenkte først at jeg skulle ta den biten som var mest common for hver bit-posisjon, prøvde dette men det funket ikke\
Gjorde dette istedet for hver byte, der den går til nest mest common dersom jeg treffer en "ulovlig" char.\
Scriptet ligger [her](document_reconstruction_script.py).

Flagg:\
`PST{e32ba07d1254bafd1683b109c0fd6d6c}`
