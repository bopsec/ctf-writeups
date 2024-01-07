## Egg
# Minesveiper egg 1
Med en gang minesveiper kom ut la jeg merke til en bug der høyreklikking av der det ville vært en bombe gjorde så "bombecounten" øverst til venstre telte ned.
Så at ingen fant noen flagg så antok at det bare var noe moro og det var en uskyldig bug.
Dagen etter kom det nye modes, antok at det var noen egg. Prøvde det jeg fant dagen før og fant med en gang [første egget](egg_1.png)\
Egg 1:\
`EGG{RETRO}`

# Minesveiper egg 2
Fant [egg nr. 2](egg_2.png)
Skjønte at det var samme greia, prøvde myye forskjellig som braille og å flytte rundt på andre halvdel, flippe det opp ned [.......]
Endte opp med å bare XORe øverste rad med nederste rad, som burde vært noe av det første jeg testet...

Egg 2:\
`EGG{bomber_og_flagg}`

# Ransomware egg 1
Kalenderens første egg ble tilfeldig funnet tidlig i oppgaven. Main-funksjonen i Ransomware kaller en funksjon som enten spiller av morsekode som staver EGGBEEPBOOP, eller spiller musikken fra "coffin dance"

Egg 3:\
`EGG{BEEPBOOP}`

# Ransomware egg 2
Main-funksjonen i Ransomware kaller en funksjon kalt "StartAddress", denne kjøres 64 ganger med en forskjellig verdi (0-64) satt inn som lpThreadParameter hver gang.
Funksjonen bruker denne til sende ut meldinger som "Har du vurdert å gi opp?" "Step, step, step..." osv osv, men hvis lpThreadParameter er mindre enn 38 vil en egen kodesekvens også kjøre, der den blant annet tar noe fra et dword-array.
Fant ut at meldingsboksen som denne delen brukes til hadde meldingen "Hemmelighet"
Testet diverse, implementerte alt det relevante i python (egg_2.py)
(Holdt på i sikkert 4 timer fordi min implementasjon av int32 overflows var litt feil :P)
Koden kan finnes [her](../Dag8-Ransomware/Egg_2.py).

Egg 4:\
`EGG{91d54eb496a1713f5ecdd4d8b1cd636f}`

# Geogjettr egg:
La bildefilen inn i https://www.aperisolve.com
En del som ikke var helt riktig, men satt meg inn i superimposed, green og blue.

Green hadde mange lange tall, mens blue hadde mange korte tall satt i en rekke.
Leste litt gjennom begge, så til slutt at tallene i blue hadde to like "tegn" i posisjon to og tre
Passet for "EGG"
Så også at tegn 4 og siste tegn var speilvendt, så jeg tolket dem som { og }.
Innså til slutt at det skulle tolkes som "antall pixler farget" i pixelart av tegnet.
[Her er bilde av min pixelart](../Dag13-GeoGjettr/Egg.png).

EGG 5:\
`EGG{RUTER_OVERALT}`

Fant ingenting fra [den grønne channelen](../Dag13-GeoGjettr/image_g_1.png).

# Hide and seek egg:
Det fantes referanser til at noen hadde mistet et egg i noe git historikk, sjekket lost-found og fant en commit som inneholdt et stort egg. Egget fantes i midten av [dette store egget](../Dag16-Invasjon/aksjon_2023/.git/lost-found/other/fdfbb6ab8dda68e83853bf372a100e8ff6e8830f).\
EGG 6:\
`EGG{h3ng3r 0g d1ngl3r}`

# Stopp robot armadaen-egg:
Jeg så også at det var referanser til get_egg, men ser ut som at denne ikke kan nåes på samme måte fordi det er to separate cmp-checks.
Fant ut at hvis jeg klarer å glitche over [...]16a2 så vil neste linje være get_egg-funksjonen.

16a2 blir hhv referert til av factory_reset på linje [...]a8c.
Bruker samme strategi fra i sta med å jobbe meg bakover fra det begynner og skrives til USART.
217740 ser ut til å være der F-en skrives i Factory reset complete med `factory_reset KRIPOS{Zipp Zapp, endelig napp!}` og 28 ns bredde.
210320 ns delay funket.

>Entering command handler
>Dumping EGG:
>EGG{3rr0r! Unr34ch4bl3 c0d3 d373c73d!}
>
>Factory reset complete. Resetting MCU.

EGG 7:\
`EGG{3rr0r! Unr34ch4bl3 c0d3 d373c73d!}`
