## Dag 22 - Gaveliste-endring

```
Emne: Gaveliste-endring

Hei {{brukernavn}},

JULESOC har fått en alarm fra informasjonssystemet tilknyttet NISSENS gavelager på VALøya i Tromsø. Alarmen handlet om en uautorisert modifikasjon i databasen som styrer inventaret til lageret, og JULESOC har sendt oss databasefilene slik de forekom på tidspunktet alarmen gikk.

Har du mulighet til å sjekke ut filene og finne ut hvilken rad som er blitt modifisert?

📎 ALARM_JULESOC.zip

Returner UUID til den modifiserte raden, f.eks. PST{6eab374e-735f-416e-bcc6-81b4b8dfc7a9}
```

Prøvde bare SQLite for å se hva som ble endret, fant ut at det var en del, sjekket hva alle ble endret til, så at Nano Jade Mindflex var den eneste som ble endret til 0 quantity\
Hentet ut UUID fra denne med [dette pythonscriptet](categorize_modification.py).

\Skrivebord\dass\Dag22-Gaveliste-endring>py categorize_modification.py\
Changes identified in the database:\
                                       uuid            giftname  quantity\
42068  9da1b2a6-5a52-41ec-8bf0-32381e054db7  Nano Jade Mindflex     48564\
42068  9da1b2a6-5a52-41ec-8bf0-32381e054db7  Nano Jade Mindflex         0\
\
Entry with zero quantity in the merged database:\
                                       uuid            giftname  quantity\
42068  9da1b2a6-5a52-41ec-8bf0-32381e054db7  Nano Jade Mindflex         0\
\
Flagg:\
`PST{9da1b2a6-5a52-41ec-8bf0-32381e054db7}`
