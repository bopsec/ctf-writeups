## Dag 23 - KVU-dokumenter

```
Emne: KVU-dokumenter

Hei {{brukernavn}},

Taskforce ALV utvides stadig og trenger derfor nye lokaler, og dermed er det satt i gang en Konseptvalgsutredning.

Vi har leid inn arkitektfirmaet Juxx og Fauxtneri for å bistå med forslag til nye bygg. Men i lys av aktuelle hendelser har vi innsett at vi må gå arbeidet deres litt mer i sømmene.

Vi må forsikre oss om at det ikke skjuler seg noe juks eller fanteri i arbeidet deres. Vi har fått tilgang til budsjettet deres, og et utkast til et nytt bygg. Problemet er at budsjettet er kryptert, så vi får ikke lest det. Har du noen alternative løsninger?

📎
```

Inneholdt en JuxxOgFauxtneri.Wim, konverterte bare til .zip\
Juxx-- inneholdt en mappe Nedbetalingsplan med en blueprint.png, samt en kryptert Cashflow.xlsx og et dekrypteringsskript i python.\
Åpnet bildet i [aperisolve](https://www.aperisolve.com), fant [image_b_4.png](image_b_4.png) med en tekststreng skjult. Brukte denne (e24f52497bcf4c332f1283ec925f77a1) som nøkkel i dekrypteringsskriptet.\
Cashflow ble dekryptert, og fikk en budsjettoversikt. I månedlige inntekter fant jeg PST{alternativ_pengestrøm} på 1000 kr.\
\
Flagg:\
`PST{alternativ_pengestrøm}`
