## Dag 12 - Pakkestorm

```
Emne: Pakkestorm

Jeg har vært på et temmelig hemmelig oppdrag og fulgt med på en server som har hatt mistenkelig oppførsel tidligere. Nå tok vi den igjen når den begynte å sende masse pakker, men selv om jeg som alle andre alver liker pakker så ble det litt for mye av det gode. Kan du finne de onde for meg?

- Tastefinger

📎fangede_pakker.pcap
```

Startet med å se litt kjapt på det gjennom wireshark, så at hver pakke hadde 6-7 bits på slutten av pakken.\
Hentet disse og sorterte på tid og IP, fant noen tusen forskjellige meldinger på formen\
PST{I/They/She/Zhe/He/It_can_haz_something}\
Skjønte at jeg måtte finne en som skilte seg ut, sjekket igjen Wireshark for å se om det var noe som var likt i alle pakkene (som kunne være ulikt i denne ene meldingen)\
Så at Reserved Bit aldri var satt til 1. Skrev et kjapt python-program for å hente ut hver pakke og se hvor mange som hadde de forskjellige bitene satt.\
Fikk bare 34 pakker med Reserved Bit til true, hentet ut disse med [dette pythonscriptet](extract_data.py).

Flagg:\
`PST{I_cAn_HaZ_rEciprOCaTeD_tRuzT?}`

Koden min mistet "?" på slutten fordi denne var en bit mindre enn de andre, men fant ut av det da jeg manuelt så på pakkene.
