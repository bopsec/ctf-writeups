# Apollo

Vi har satt opp en server der vi kan kryptere vilkårlige meldinger og dekryptere chiffertekst, men med en vri.

Klarer du å benytte en kjent angrepstype for å avdekke innholdet?

Kjør `uv run --script chall.py` for å teste lokalt.

```sh
nc apollo 1337
```
---

```
login@corax ~/1_grunnleggende/1.14_apollo $ nc apollo 1337
En symmetrisk krypteringsalgoritme er nå implementert for deg.
Du kan bruke den til å kryptere og dekryptere meldinger.

Flagget er: 168643db19ee10ae1450bb6eae5c9186a3ebcbc30d0333b32430a3915413501f3173db056a1f89a133ca327c83fc3f82b44f56b6053303d3f17adced80bd0492

For å kryptere en melding, velg 1 (encrypt) og skriv inn meldingen.
For å dekryptere en melding, velg 2 (decrypt) og motta den dekrypterte meldingen.

>
```

Sjekket koden i chall.py, typisk padding oracle, gjetter bare byte for byte bakover frem til jeg har hele flagget.


```
[+] Opening connection to apollo on port 1337: Done
CT blocks: 4

=== Blokk 3 ===
  Byte 15: 0xe
  Byte 14: 0xe
  Byte 13: 0xe
  Byte 12: 0xe
  Byte 11: 0xe
  Byte 10: 0xe
  Byte 9: 0xe
  Byte 8: 0xe
  Byte 7: 0xe
  Byte 6: 0xe
  Byte 5: 0xe
  Byte 4: 0xe
  Byte 3: 0xe
  Byte 2: 0xe
  Byte 1: 1
  Byte 0: 9
P3: b'91\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e'

=== Blokk 2 ===
  Byte 15: 0
  Byte 14: 0
  Byte 13: d
  Byte 12: 3
  Byte 11: 2
  Byte 10: 5
  Byte 9: 0
  Byte 8: d
  Byte 7: 3
  Byte 6: 7
  Byte 5: 6
  Byte 4: 0
  Byte 3: 4
  Byte 2: d
  Byte 1: c
  Byte 0: 6
P2: b'6cd40673d0523d00'

=== Blokk 1 ===
  Byte 15: 6
  Byte 14: a
  Byte 13: 5
  Byte 12: 6
  Byte 11: a
  Byte 10: d
  Byte 9: a
  Byte 8: b
  Byte 7: 1
  Byte 6: 5
  Byte 5: a
  Byte 4: 4
  Byte 3: b
  Byte 2: f
  Byte 1:
  Byte 0: :
P1: b': fb4a51bada65a6'

=== FLAGG ===
Blokk 1: b': fb4a51bada65a6'
Blokk 2: b'6cd40673d0523d00'
Blokk 3: b'91\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e'
[*] Closed connection to apollo port 1337
login@corax ~/1_grunnleggende/1.14_apollo $
```
Koden kan finnes i [apollo.py](apollo.py)

Flagget er fb4a51bada65a66cd40673d0523d0091
