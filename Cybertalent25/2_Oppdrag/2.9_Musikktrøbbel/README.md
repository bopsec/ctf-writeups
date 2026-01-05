# Musikktrøbbel

GooodGames har hatt julebord og har lagt ut noter som folk kan lese dersom de ikke har hørt sangene før.

Ryktene sier at de forventer at ansatte kan litt om musikkteori og steganografi.

---
## Jinglebells

La inn i aperisolve og så at øverste halvdel av bildet var veldig noisy i alle channels på bit0

Passord-protected med en Joel.png i mappen\
På bitplane 1,2,3 ser jeg også skjult data\
`Kanskje akkordene kan hjelpe?`

Mapper akkorder C->1 F->3 osv osv med litt testing for de jeg var i tvil på
```
C C C F F G G
1 1 1 4 4 5 5

C C C C F F G
1 1 1 1 4 4 5

G C C C C C F
5 1 1 1 1 1 4

C D G C C C C
1 2 5 1 1 1 1

F C/G G C
4   5 5 1
```

7z x jinglebells.zip -p11144551111445511111412511114551\
Fikk ut Joel.png

---
## Joel

Joel.png har samme støy øverst i bildet, tester diverse men får ikke ut standard, så tar bit 1 0 fra hver pixel i hver channel og setter sammen\
Får en ny zip med "12_days_of_christmas.jpg"

På plane 2 og 3 finner vi \
`Toneart introduseres. F!=4. / betyr basstone (betyr ikke nødvendigvis tall)`\
Litt bruteforcing og testing av diverse, kom frem til denne:
```
F Dm7 C F Bb/F F Bb6 F
1 6   5 1 4    1 4   1

Csus C7 F Dm7 C F Bb/F F Bb6
5    5  1 6   5 1 4    1 4

F Csus7 F F/E Dm Dm/C Gm/Bb Aaug C#o
1 5     1 1   6  6    2     3    3(?)

Dm Dm9/C Bb Gm9 C7 F
6  6     4  2   5  1
```


7z x noel.zip -p16514141551651414151166233664251

---
## Twelve_days_of_christmas

Fikk ut twelve_days_of_christmas.png\
Noe skjult i bits 0, 1, 2, og 3 på alle channels\
Bit 2 har mye mindre data enn de 3 andre (typ 3px height vs 30)\


Hvis du tar bit 2 fra RGBA i de øverste radene, så får du
```
Den siste utfordringen er en del vanskeligere enn de andre, så du skal så en del hjelp også...
Først må du finne zipen. Den er litt rar denne gangen, men kan ha noe å gjøre med bit 0, 1 og 3 i hver piksel.
Musikken er også blitt en del rarere.
Akkorder som kommer rett før en modulasjon, tilhører ny toneart.
Tritonussubstitusjoner er gøy, en akkord har ikke alltid tallet man tror.
(kremt kremt, selv om tonen ikke er i akkorden, betyr ikke det at den ikke kan ha tallet til tonen som ikke er der)
Se etter mønster
```
Hvis du tar bit 1, 3 og 0 i den rekkefølgen, får du en ny zip-fil med en ny png "A_cool_new_christmas_song.png", igjen med et passord

```
A F#m7 Bm7 E7 Amaj C#m D6 Bm7 E7 A6 F° E° D7(b9)
1 6    2   5  1    3   4  2   5  1  6  2  5 		(overgang til G-dur VI - II - V - I)

Gmaj Em7 Am7 D7 Gmaj Am7 D7 G Bm C6 Am7 D7
1    6   2   5  1    2   5  1 3  4  2   5 		(rett frem)

G6 D° Ebm7 Ab7 Db Bbm7 Ebm7 Ab7 Dbmaj Ebm7 Ab7
1  6  2    5   1  6    2    5   1     2    5     	(VI-II-V-I overgang til Db-dur)

Ebm7 Ab7 Db Fm Gb6/Bb Bbb7b5 Ab7 Db6 E° Ab7b5 G9
2    5   1  3  4      2      5   1   4  2     5 	(Bbb -> enharmonisk A, brukes som tritonussub for Eb7 så den mappes til Eb, som er 2 i Db-dur)			(E° kan leses som "rootless C7(b9) som peker mot F (subdominant i C), altså 4. Det er nok dette det "kremt kremt"-hintet refererer til. 
							(Ab7b5 -> 2, tritonussub for D7 i C)
C Am7 Dm7 G7 Cmaj Dm7 G7 Dm7 G7 Dm7 G7
1 6   2   5  1    2   5  2   5  2   5			(rett frem)

C Em F6/A Ab7#5 G7 C
1 3  4    2     5  1 					(Ab7#5 er tritonussub for D7 -> 2, resten rett frem)
```

7z x twelve_hidden.zip -p1625134251625162512513425162516251252513425142516251252525134251

Fikk ut et nytt bilde A_cool_new_christmas_song.png\
Her var det lite data skjult, kun på øverste rad.\
`b1,rgba,lsb,xy      .. text: "Neida, ferdig naa, her er flagget: 11e9746cba401550dc7140e68e355362\n"`\
Takk gud...


login@corax ~ $ scoreboard 11e9746cba401550dc7140e68e355362

2.9.1 Musikktrøbbel\
Ferdig nå, heldivis...



denne satt langt inne
