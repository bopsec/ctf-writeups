## Dag 24 - Stopp robot-armadaen

```
Emne: Stopp robot-armadaen

Hei {{brukernavn}},

Julegavemaskinen ved nissens verksted har over en lengre periode ikke produsert annet enn smokingkledde roboter med vaggende gange. Nå har endelig maskineriet blitt reparert, men det vagger fortsatt et par titalls tusen robot-pingviner rundt i kontorene her som truer vår suverenitet over Nordpolen.

Vi har vanligvis et innebygget override passord i alle brikkene våre for slike nødtilfeller, men det ser ut til at passordet har blitt endret!

Undersøkelsene våre viser at noen har tuklet med maskineriet, og lastet opp ukjent fastvare til mikrokontrollerene som vanligvis styrer lekene. I tillegg var produksjonssettings-pipelinen kompromittert, hvor vi fant en ukjent enhet koblet til USART-grensesnittet som utfører den endelige konfigurasjon av mikrokontrollerene. Dessverre gikk denne enheten opp i røyk da vi prøvde å koble den fra, så den er totaldestruert.

Etter noen innledende eksperimenter tror vi at disse brikkene kan være sårbare mot fault injection angrep, og KRIAPOS har latt oss få remote tilgang til elektronikk-laben deres for å jobbe videre med dette:

kriapos.no

Laben er allerede satt opp med en brikke som vi har tatt ut av en robot-pingvin. Se om du klarer å få tak i dataen fra denne slik at vi kan se hva override passordet har blitt satt til.

Vi har delt all dataen dere trenger med de samarbeidende etatene allerede, så du vil motta disse fra din kontaktperson veldig snart.

Svar meg på denne eposten når du finner ut av dette!
```
```
Emne: Robot-armada: {{tjeneste}}
Hei alle sammen!

Vi har fått utdelt noen filer i forbindelse med Nisse-saken, og jeg har blitt bedt om å dele disse videre til relevant personnel. Filene ligger vedlagt.

Vi fikk også denne beskjeden sammen med filene:

Vedlagt ligger den ondsinnede fastvaren som er ekstrahert fra julegavemaskinen: “mykepakkervare.bin”, samt databladet for NISSE32-brikken. Vi tror også kanskje at de har bygget videre på vår vanlige fastvare, så alvdelingen for fastepakkervare har ordnet en debug-variant av fastvaren vi vanligvis bruker: “fastepakkervare.elf”.

Jeg fikk noe pakketap da jeg lastet ned filene, men det har sikkert gått fint. Eventuelt har vel dere teknikere kommunikasjon på tvers av etatene på discord? OBS! Ikke stol blindt på filer du mottar fra andre; dobbeltsjekk hashen i md5sum.txt og bruk gjerne en VM.
```

Hver av NISM, KRIAPOS og NPST fikk sin egen del. Hhv datasheet.pdf, fastepakkervare.elf og mykepakkervare.bin\
Linken leder til dette https://i.imgur.com/kFnwZZl.png .\
Refererer til bruk av fault injection for å "glitche" over instruksjoner.\
Viste et eksempel med å skippe en bne etter en cmp-check. Datasheet.pdf hintet også til at vi skulle glitche inn i flash_dump for å finne passordet.\
\
Testet litt rundt, fant ut at 28ns som glitch bredde funket, og at programmet kjører i 200 og noe ms.\
\
Ved hjelp av "USART output før glitch:" fant jeg fort ut hvor ting begynte å bli skrevet.\
dump_flash asdasd, 28 ns width og 192920 fant jeg ut glitcher akkurat på der W i "Wrong override password" blir skrevet.\
Jobber meg litt bakover derfra, finner ut at det er 120-130 linjer fra bne til W. Bruteforcer bare 192920 - 20*(120-130) ns på delay.\
Virker som at det varierer litt?
```
Entering command handler
Commencing flash dump:
OVERRIDE_PASSWORD=KRIPOS{Zipp Zapp, endelig napp!}

Start limb control sequence
```

Flagg:\
`KRIPOS{Zipp Zapp, endelig napp!}`

# Egg
Jeg så også at det var referanser til get_egg, men ser ut som at denne ikke kan nåes på samme måte fordi det er to separate cmp-checks.
Fant ut at hvis jeg klarer å glitche over [...]16a2 så vil neste linje være get_egg-funksjonen.

16a2 blir hhv referert til av factory_reset på linje [...]a8c.\
Bruker samme strategi fra i sta med å jobbe meg bakover fra det begynner og skrives til USART.\
217740 ser ut til å være der F-en skrives i Factory reset complete med `factory_reset KRIPOS{Zipp Zapp, endelig napp!}` og 28 ns bredde.\
210320 ns delay funket.
```
Entering command handler
Dumping EGG:
EGG{3rr0r! Unr34ch4bl3 c0d3 d373c73d!}

Factory reset complete. Resetting MCU.
```
\
Egg:\
`EGG{3rr0r! Unr34ch4bl3 c0d3 d373c73d!}`


Det var også noe binærkode skjult i bevegelsen til roboten(e).
JULEGAVER, BJELLEKLANG, NISSELUER og egg finner du et annet sted ;) i .elf-filen
red herring,LEMMAO!, ikke, god, jul i .bin-fila.
Ingen fler egg her virker det som.
