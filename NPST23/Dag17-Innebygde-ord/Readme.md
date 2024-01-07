## Dag 17 - Innebygde ord

```
Emne: Innebygde ord

Vi har snappet opp to meldinger som ble sendt til hovedobjektet i J-SAK EMBED. Vi mistenker at meldingene ikke er hva det ser ut til å være.

Den første meldingen som ble sendt var en merkelig tekst om å telle, mens melding nummer to bare ser ut til å være en rekke med tall. Vi tror det er en betydning i disse tallene, kan du se på det og gi oss tilbakemelding hvis du finner noe meningsfylt?

- Tastefinger

📎melding_1.txt
📎melding_2.txt
```
melding_1.txt:
```
{}

en rekkefølge man må se.
nummer en, nummer to, nummer tre,
tells det å telle, gjør det det?

oversikt og sekvens, en viktig oppgave i alle fall,
hva ellers er vel vitsen med tall?
```
melding_2.txt:
`26, 6, 3, 0, 16, 4, 8, 4, 7, 21, 19, 14, 7, 3, 4, 5, 5, 25, 16, 11, 1`


Innså tidlig at det måtte være indeks av tegnene i melding_1 på en eller annen måte, da det matchet med 0 som { og 1 som }, pluss 3 bokstaver før {, og } som siste tegn.\
Prøvde meg litt frem og tilbake, endte opp med å fjerne duplicates og bruke tallene som indeks i denne listen.\
Pythonscriptet mitt kan finnes [her](dag17.py).

Flagg:\
`pst{nede for telling}`
