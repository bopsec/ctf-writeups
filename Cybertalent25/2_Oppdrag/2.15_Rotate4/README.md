```
login@corax ~/2_oppdrag/2.15_Rotate4 $ cat LESMEG.md
# Rotate 4

GooodGames har utgitt et nytt spill: Rotate4. De har lagt ut en vinnerpremie til den som klarer å slå de ulike botene deres på ulike vanskelighetsgrader. Vinn over 80% sammenlagt, og man vil få premien. Lykke til.

Vi har også mottatt informasjon om et internt dokument som beskriver avanserte teknikker for utvikling av KI-agenter som er vanskelige å slå. Dette kan vise seg å være av stor operativ verdi for å slå spillet.

PS: Husk å ikke endre noe av logikken i client-skriptet, bare endre agenten som kjører. Vi har også lagt ved en speiling av miljøet som er brukt til å spille Rotate 4, slik at man kan spille spillet med dens regler allerede i `rotate4\_env.py`. Jeg ville ikke endret noe på denne filen, bare importert den.

Koble til turneringen ved bruk av `client.py`. Lag en agent som arver av klassen Agent, slik som i eksempelet RandomAgent i `agent.py`.
```
---


Skrev (med hjelp fra Opus4.5) en minmax AI-agent for Rotate4, som simulerer fremtidige trekk og rotasjoner og velger trekk den tror maksimerer vinnersjanse.


`get_action`: 
```
Henter alle gyldige trekk, sorterer dem basert på preferanse for midtkolonnen (bedre kontroll og raskere pruning)
	For hvert trekk: kloner miljøet, utfører trekket, kjører minmax ned til gitt dybde
Returnerer så trekket med høyest score
```

`minmax`:
```
Rekursiv minmax med alfa-beta-pruning.
Stopper hvis spillet er ferdig
	Stor score hvis agenten vinner, stor negative hvis motstander vinner
Stopper også når maks dybde er nådd og kaller _evaluate
```

`evaluate`:
```
Heuristisk vurdering av brettet
Teller alle 4-på-rad-vinduer for begge spillere
Egen score - (1.1 x motstanderens score)
Bonus for egne brikker i midtkolonnen
Hvis rotasjon snart skjer (moves_until_rotation <= 2):
	Simuler neste rotasjon, evaluerer det roterte brettet med litt lavere vekt
```

`simulate_rotation`:
```
Roterer hele brettet med 90°, og simulerer tyngdekraft på hver kolonne slik at brikkene faller ned etter rotasjonen
```

`score_board` / `score_window`:
```
Går gjennom alle horisontale, vertikale og diagonal vinduer på 4 ruter:
	4 egne = høy score (1000)
	3+1    = 50
	2+2    = 10
	Vinduer med motstanderbrikker ignoreres
```

Måtte kjøre et par ganger før jeg vant med noen små endringer.

```sh
=== ConnectFour90Lite (7x7) ===
Current Player: R
Rotation in: 4
Next Rotation: ACW
    0   1   2   3   4   5   6
0 | . | . | . | . | . | Y | Y |
1 | . | . | . | . | . | R | R |
2 | . | . | . | . | . | R | R |
3 | . | . | . | R | R | R | R |
4 | . | . | . | Y | R | Y | Y |
5 | . | . | . | Y | Y | R | Y |
6 | . | R | Y | Y | R | Y | Y |
----------------------------------

[Stats] W/L/D: 12/8/0 | Win %: 60.00% (Total: 20)

==================================================
CHALLENGE COMPLETE! FINAL RESULTS
-> UNLOCKED FLAG: 2b2aeea4d677f6362a479eca80914175
GAUNTLET WINNER: 87.00% wins! Returning FLAG.
==================================================
```

login@corax ~/storage/2.15 $ scoreboard 2b2aeea4d677f6362a479eca80914175

2.15.1 Rotate4\
Ikke for å lyve altså, men roterende fire på rad er mye vanskeligere enn det ser ut!
