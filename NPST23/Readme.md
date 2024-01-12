# NPST Julekalender 2023
mal er stjålet fra unblvr :eyes:

Første CTF der jeg har puttet inn en innsats etter dag 4, så tenkte jeg kunne skrive en writeup med mine løsninger..\
ChatGPT er brukt en del for å skrive kode når jeg vet hva som trengs, så hvis kodestilen endrer seg kan det være derfor.

- [Dag 1 - Mobildetektiven](#dag-1---mobildetektiven)
- [Dag 2 - Kongelig brøler](#dag-2---scrambled)
- [Dag 3 - Redacted](#dag-3---redacted)
- [Dag 4 - Pinneved](#dag-4---pinneved)
- [Dag 5 - Muldvarpjakt](#dag-5---muldvarpjakt)
- [Dag 6 - Kaker kontroll](#dag-6---kaker-kontroll)
- [Dag 7 - Alle gode ting er tre](#dag-4---alle-gode-ting-er-tre)
- [Dag 8 - Ransomware](#dag-8---ransomware)
- [Dag 9 - Kronolokalisering](#dag-9---kronolokalisering)
- [Dag 10 - Alvesortering](#dag-10---alvesortering)
- [Dag 11 - Informasjonsdeling](#dag-11---informasjonsdeling)
- [Dag 12 - Pakkestorm](#dag-12---pakkestorm)
- [Dag 13 - Geogjettr](#dag-13---geogjettr)
- [Dag 14 - Bokorm](#dag-14---bokorm)
- [Dag 15 - Bit-råte](#dag-15---bit-raate)
- [Dag 16 - Invasjon](#dag-16---invasjon)
- [Dag 17 - Innebygde ord](#dag-17---innebygde-ord)
- [Dag 18 - Melding fra antikken](#dag-20---melding-fra-antikken)
- [Dag 19 - Hide and seek](#dag-19---hide-and-seek)
- [Dag 20 - Rudolf's eventyr](#dag-18---rudolfs-eventyr)
- [Dag 21 - Rudolph "The Stag"](#dag-21---rudolph-the-stag)
- [Dag 22 - Gavelisteendringer](#dag-22---gavelisteendringer)
- [Dag 23 - Kvu dokumenter](#dag-23---kvu-dokumenter)
- [Dag 24 - Stopp robot armadaen](#dag-24---stopp-robot-armadaen)



## Dag 1 - Mobildetektiven

```
Emne: Mobil-detektiven

Her får du den første oppgaven!

Under etterforskningen av hendelsen på jule-verkstedet har vi oppdaget noe rart. Et av meldingssystemene som sender varslinger til beredskapsvaktene for verkstedet har sendt en SMS til et ukjent nummer. Meldingen er dessverre helt uleselig for oss, så vi trenger dine mobildetektiv-egenskaper. Når du finner ut av det, send meg svar på formatet PST{ditt svar her}.

7-4 9-3 7-4 8-1 3-2 6-1 0-1
4-3 6-2 3-3 4-3 7-4 3-2 7-3
8-1 0-1 4-1 7-3 8-2 6-2 5-2
3-2 7-3 0-1 4-3 6-2 2-3 6-3
6-1 4-3 6-2 4-1
- Tastefinger
```

Brukte [dcode's multitap abc cipher](https://www.dcode.fr/multitap-abc-cipher), input

7777 999 7777 8 33 6 0 \
444 66 333 444 7777 33 777 8 0 \
4 777 88 66 55 33 777 0 \
444 66 222 666 6 444 66 4 \
Result\
SYSTEM INFISERT GRUNKER INCOMING

Flagg: \
`NSM{SYSTEM INFISERT GRUNKER INCOMING}`


## Dag 2 - Scrambled

```
Emne: Scrambled

Over natten har det vært store utfordringer knyttet til en av maskinene i verkstedet. En serie feilproduserte leker har kommet på rullende bånd. Vi prøver å finne ut hva som har skjedd. Graver du ned i det her?

- Mellomleder

📎Bilde
```

Så på odelagte_leker_fix.png, så at det var en "utbrettet" rubiks kube.\
Googlet litt rundt og fant flere som hadde gjort lignende det samme, men ingen tools som kunne gjøre dette veldig lett.

Endte opp med å sette inn kubens farger i en [rubik's cube solver](https://rubiks-cube-solver.com).\
Ga med alle trekkene jeg trengte for å fullføre kuben

Deretter implementerte jeg hvert trekk i python, og lagde en 3x3 matrise for hver side\
Gikk gjennom hver turn i løsningen og fant

```
{'Top': [['P', 'L', 'P'], ['_', 'S', 'S'], ['M', 'U', 'E']], 
'Front': [['E', 'E', 'O'], ['D', 'N', 'S'], ['_', 'N', '_']], 
'Bottom': [['_', 'S', '{'], ['D', 'T', 'L'], ['U', 'E', 'Ø']], 
'Left': [['W', 'Y', 'T'], ['B', 'O', 'S'], ['R', 'G', 'P']], 
'Right': [['L', 'L', 'R'], ['L', 'E', 'E'], ['I', '_', 'L']], 
'Back': [['U', '?', '}'], ['K', 'E', ')'], ['_', 'B', ':']]}
```

Tok bare noen minutter før jeg skjønte hvordan jeg skulle finne rekkefølgen for hver side.\
Kunne sikkert bruteforcet hver side raskere

Flag:\
"WYBORG"+\
`PST{LØSTE_DU_DENNE_SOM_PUSLESPILL_ELLER_KUBE?:)}`

## Dag 3 - Redacted

```
Emne: Redacted

Det er krise! Filene på alvemaskinene har blitt kryptert, og vi har ingen backups tilgjengelig!

På nissens skrivebord fant vi det vedlagte brevet, sammen med en kryptert fil.

Det er ubeskrivelig viktig at vi får åpnet denne filen igjen umiddelbart, da Jule NISSEN ikke klarer å huske innholdet!

- Mellomleder

📎 Mitt utpressingsbrev.docx
📎 huskeliste.txt.enc
```

Flyttet vekk "REDACTED" i Word\
Fant nøkkelen: dda2846b010a6185b5e76aca4144069f88dc7a6ba49bf128\
Flyttet bildet som beskrev "krypteringsmåten" med "Cut"-funksjonen i Word.\
Fant [dette](Dag3-Redacted/skjult_info.png)\
IVen er UtgangsVektor123, funnet av Edit log i dokumentet.

Brukte informasjonen fra bildet og løste som AES-CTR med ROT-13 på IVen.\
Flagg:\
`KRIPOS{Husk å se etter spor i snøen!}`


Hele outputen er [her](Dag3-Redacted/huskeliste.txt).


## Dag 4 - Pinneved

```
Emne: Pinneved

Alvebetjentene på Jule NISSEN sitt verksted våknet i dag til et fryktelig syn; Julenissens slede er sprengt i fillebiter. Vi har satt folk på saken for å finne ut av hvem som er ansvarlig for ødeleggelsen, men det er kritisk at sleden blir reparert slik at vi får testet den før Jule NISSEN skal levere pakkene.

Alvebetjentene har samlet vrakrestene, samt verktøyet de mistenker at sabotørene har brukt.

Vi trenger at du rekonstruerer sleden så fort som mulig!

- Tastefinger

📎 pinneved.py
📎 pinneved.txt
```

Leste bare gjennom koden for å prøve å skjønne hva den gjorde. Tok noen iterasjoner av [pinneved_reversed.py](Dag4-Pinneved/pinneved_reversed.py) før jeg fikk ASCII-art [slede-reversed.txt](Dag4-Pinneved/slede_reversed.txt).

Flagg:\
`PST{ASCII_art_er_kult}`


## Dag 5 - Muldvarpjakt

```
Emne: Muldvarpjakt

Gjennom temmelig hemmelige innhentingsmetoder har vi fanget opp en melding om et nært forestående møte på Fastlands-Norge mellom en mistenkt kildefører som jobber for sydpolare tjenester og et ukjent objekt vi mistenker kan være en muldvarp.

For at våre spaningsalver skal settes i stand til å observere møtet og identifisere det ukjente objektet må vi vite hvor vi skal sende våre alver.

Vi prøvde å spørre OSINT-alvene våre, men de var travelt opptatt med å saumfare sosiale medier etter snille og slemme barn. De mumlet noe om at vi kunne fikse det selv med “turbo overgang”.

Kan du ut fra meldingen finne ut hvor de skal møtes?

`Ta bussen og gå av på holdeplassen rett ved begravelsesbyrået som ligger inntil en sjømatbutikk. Jeg vil stå klar ved fontenen noen titalls meter fra bussholdeplassen. Når du har kommet frem til fontenen, vil vi sammen gå til det nærliggende biblioteket som ligger under 50 meter fra fontenen og gjennomfører overføringen.`

Svar meg med navnet på møtestedet og på formen PST{BERGEN LUFTHAVN}

- Tastefinger
```

Gjennom "De mumlet noe om at vi kunne fikse det selv med “turbo overgang”."\
Så fant jeg verktøyet [overpass-turbo](https://overpass-turbo.eu/) \
Brukte litt tid på å lære meg syntax osv, endte opp med denne:
```
\\[out:json][bbox:{{bbox}}][timeout:800];

node[highway=bus_stop]->.bus;
(
  node[amenity=fountain];
  way[amenity=fountain];
  rel[amenity=fountain];
)->.fun; 

(
  node[amenity=library];
  way[amenity=library];
  rel[amenity=library];
)->.lib; // library xd

(
  node[shop=funeral_directors];
  way[shop=funeral_directors];
  rel[shop=funeral_directors];
)->.funr;

(
  node.lib(around.fun:100);
  way.lib(around.fun:100);
  rel.fun(around.fun:100);
)->.libs;

(
  node.funr(around.libs:100);
  way.funr(around.libs:100);
  rel.funr(around.libs:100);
)->.funs;

(.funs;);

// return node, ways, relations as determined above
out geom meta;\\
```


[Dette](https://i.imgur.com/C6hmGx4.png) var resultatet av søket.\
Zoomet inn og fant Frogn Bibliotek i Drøbak.

Flagg:\
`PST{FROGN BIBLIOTEK}`

## Dag 6 - KAKER-kontroll
```
Emne: KAKER-kontroll
I en standard KAKER-kontroll (Kontroll Av Kommuniké med Eksport-Restriksjoner) har det blitt tatt en kopi av dette dokumentet. Vi syns det er snodig at akkurat denne personen har hatt med seg dokumentet siden personen har hatt anti-jul-holdninger tidligere, og vi vil derfor at du tar en nærmere kikk for å se etter uhumskheter.

- Tastefinger

PE‍PPERKAKER {
    POR‍SJONER {
        20 kaker
    }
    ‍TYPE ‍{
        julekake
    }
    INGREDIENSER {
        KAKEDEIG {
            2 ts ‍Pepper
            2 ts Malt ing‍efær
            0,5 ts Malt nellik
            3 dl Mørk siru‍p
            300 g Smør
            2 ts Malt kanel
            4 ts Natron
            2 stk. Egg
            300 g Sukker
            ca. 900 g Hvetemel
        }
        MELISGLASUR {
            ca. 250 g Melis
            1 stk. Eggehvite
            0,5 ts Sitronsaft
        }
    }
    OPPSKRIFT {
        STEG1 { Bland smør, siru‍p og sukker i en kjele. Varm opp til sukkeret er sm‍eltet. Tilsett nellik, ingefæ‍r, pepper og kanel, og rør godt sammen. }
        STEG2 { Ta ‍kjelen av platen og avkjøl bl‍andingen noe. Rør inn egg. }
        STEG3 { Ha i natron, og si‍kt inn mel. Rør alt sammen til ‍en jevn deig. Deigen skal væ‍re ganske myk og klissete, den vil bli mye hardere når den blir kald! }
        STEG4 { Hell deigen over i en bolle og dryss litt hvetemel på toppen. Dekk til med litt plastfolie og sett deigen kaldt noen timer, gjerne over natten. }
        STEG5 { Skjær løs et stykke av deigen. Plasser resten av deigen tilbake i kjøleskapet. ‍Elt deigen forsiktig. Tilsett litt me‍r mel om den virker for myk. }
        STEG6 { ‍Mel en flate, ‍og kjevle deigen ut til ca 3 mm tykkelse. Det er enklest når deigen er myk som plas‍tilina. Stikk ut pepperkakefigurer og flytt dem over på et ‍bakepapirkledd stekebrett. Samle restene av deigen og legg den kaldt. Skjær ut et n‍ytt stykke av ‍deigen og gjenta prosessen. Deigen blir vanskelig å jobbe med når den blir for varm, så da kan d‍en få hvile i kjøleskapet igjen. }
        STEG7 { Stek kakene midt i stekeovnen på 175 °C i ca. 10 minutter. Avkjø‍l kakene helt på rist. }
        STEG8 { Bland sammen mel‍is, eggehvite og sitronsaft til en tykk ‍glasur, og dekorer kaken‍e. }
    ‍}
}
```

Kopierer kakeoppskrift for å se om det var noe skjult der, fant noen zero-width-joiners\
Rotet litt rundt, og endte opp med "første tegn etter ZWJ"\
Pythonkoden kan finnes [her](Dag6-Kaker-kontroll/dag6.py).

Flagg:\
`PST{PepperkakerErMotbydelige}`

## Dag 7 - Alle gode ting er tre
```
Emne: Alle gode ting er tre

Alveresepsjonen fant en mystisk lapp i postboksen til Nissens verksted i dag tidlig. Vanligvis er dette noe Ronny, Shahana og Ada fra alvdeling for kryptografi ville tatt seg av. Dessverre er alle tre bortreist på en viktig konferanse i San Francisco for å høre om den siste utviklingen innen eksponenter og modulær aritmetikk. Kan du steppe inn for dem og finne ut av hva denne beskjeden egentlig er for noe?

- Mellomleder

📎msg.txt
```

Leste oppgaveteksten og så at navnene til kryptografene stavet RSA\
Gikk til en [RSA cipher solver](https://www.dcode.fr/rsa-cipher).

Cipher message
`0X755040806D1D699C76CF2B3FFFC28AD8831A8667E1B064297A43733B89F6272483A5A728B725D02B069F8FC65EB51D89CE9133DF8F5F2D5E13F63C5423021EB2B56EEB91B11D78717528DFCE169450A08D40F5AB451C8AC1F8C6875CFFBD4D70259D436ED70BAEAE37B9BDAFC5965`

Public key E
`3`

Public key N
`0X5993C05EAC819AA17AE7E4E4B9F75B2D6FDBAEC913E0B2D6F4BA585A991B62279ED9AC53AEADEE3327321E02C0C06ECDA184952DF5D1CC8B3024643C0AFDD9BBD52BF2D830F54D6E59E76844394EB0FFC498995DD270B9B95BF1614984472A3EF12D8C1BAD64529BE7B638C5D0FCCF61C5AC2AB4564E5215748EB2533D4D949AFD9486426DBF0C06A07C2C0F6D482E4F8CF3052E6AB9DF20878B747936D590C3B8BB0219A378CBEC03BAEE4EA8D0641C57BCC18706BBE92C3F2D7569C424062D9B79464958419B4000E3E31C077BBA27EF2FC6ED15B7EBDCDB41D1CBF7708737E200904015D341EF94C537A916F1FEC61E0B1BF64762E5A97BAFDDE290B939C3`

Flagg:\
`NSM{af0dbd13cee45990593c182b213f978d}`

## Dag 8 - Ransomware

```
Emne: Sort på Hvitt

Skjermen på en av datamaskinene på NISSENS verksted ble plutselig dekket av mange meldinger om at viktige filer var blitt kryptert. Et team av alver klarte å finne igjen denne filen sammen med en høyst mistenkelig fil, men klarer ikke å dekryptere filen. De har delt filene i et ZIP-arkiv med infected som passord. Klarer du å få tilbake den viktige filen?

- Tastefinger

📎mistenkelig_beslag.zip
```

Denne tok meg et par dager..\
Hadde tidlig funnet ut at første linjen var noe med nøkkelen i RSA. Fant senere ut at dette var N.
`0xF92B7110BA05839D0EC18DE9BA8DE489048B2A0C2AAE3FF1FAC83AB7799E8B45747E0D698DDDB424BE09C34B3CCFAFE88D4CB46F73701696E39B04298AA115438C152C0666D08858B8F46C29039CE3AC978A4EB2EADE7D113DC3691F52D3707E9F7A11C19514071EDA4A3534BC530DC54BD7EB4A4DB94F0B0B9784828768B5305AFF932F836F340A140162AA0C7FF97660B4B314C4D03D95B0ECF82A192193CA137FF0F6C6094AE6E3DE4B60E475F56277373FF73973F1F71D61A567F250BA24755D29D8B5DCE41F6A91117EC09981F1598BB5387D111CCBD3D8F465A4842D052155C638C0DB8674389986F46BD5DE61643854B6724901986E2D2111464383FB87494E2626082089C8A5A80A0BB6F994A0DA2FCD366DFB3F1003E4A20D5549CD1F6DB4D70E5151D5B70A2AEE02139953247E6B6E242A1777BD8042BCF81C7BBB2236EA3DE36764A3CC5430FC2A8828C7A86504F0D9E9C939ACE73C7B853F4582EA39496BDC9B074410EE19FC4A4828C9720E49F311479E59AC6964971A923483DE36BFBEBAE8E3E02F60ED4944A1C58D9FDA1DD091CC47E681608D99012DD5FA086396BA98D8BF76ADB2762D0C6AA878A5E74AB8674DD4FC90DAF04BFF71BA2B2C4452A3C81A293286A085A97398EE65FB54C932C0464CAA400DCB52821E06451811C2C0BC0EAB2DC0A6F5E44F48C4DA701BC05D9B75311B8243EFB4DF9FBB35`\
Ciphertext oversatt til hex ble så til, som var samme lengde:
`0xE882A3043D36478FE9DCBD5D18A2CE2D631D5FC7C54212C0AECF205ECC6C73BDBDAB3E5AA054C69A9B8EE9478A7AD4DE0E6B364BD6EECB12F270FF2E8331C29E8E2DA55EEA261B1537D0DD669B08A13E971DAF3E8C22C697ED7495627867E06B45E8875B9A80290449327433D3AF4FE1332FF10686927CC334F47C3E65994186D2FEC7FA980D1A797BF07DFF4E0807A62DDD47D246FF8FB2C32221E5017BB5F512D0AB4CC67A9C785AD8A4ECC9B2C64453DF81826B623B07F505C6FFFE8034C8CAF7DF67778E287B993D0178646689432FCB1C82E19A55AEB832BC720A78EF690166A1A442074AD172A29AE83CFCA3F4EC528290D6EDA561343387A024DD77D1D9C25B7E88FDCB26301DD4AFED8D8B19D3570F3550B4039BEB73DADEFD9883EC4636E6BBAD764AEAB4E89DA2860238ADBBD043F497C1139CD656D25FB7745E8821525A62AE004427D45F5CEB2A5811A9D1D92241DA5B187BC7B6DC6C969828E21D086DF3BA28009E4467E3C65FCED7CDF141E40F5700498FED5073D3E69D2641F1E0547F8F26E647B9C877C8FF5D49CE1AB7066C67EF7068E09AA33B0EDCED9D466EE2F8D4EA45BCDC0DA3EF965487A5AE88552280D8AC682E85C7F36403B1D35D0699B14E5BACD2F6A5CA9A4D6DB74638697B003124E54BEAF4713A7B9659D3C182C8AA4B50C037EA1EE94D52FD6B4C0B13A4B1483C99407D926E92BA43343B`

Sjekket etter noen dager om N tilfeldigvis var et primtall, noe som er usannsynlig men gjør det ihvertfall mulig å løse oppgaven ved RSA's svakhet når N er prime.

Prøvde å bruke disse verdiene sammen med svakheten til RSA når N er primtall, og kom til slutt frem til flagget.

Flagg:\
`NSM{65d77649dcd02ab0fed102c3e3d3d33faba1874038c7bda737c40604021034b4}`

# Egg 1

Kalenderens første egg ble tilfeldig funnet tidlig i oppgaven. Main-funksjonen kaller en funksjon som enten spiller av morsekode som staver EGGBEEPBOOP, eller spiller musikken fra "coffin dance"

EGG:\
`EGG{BEEPBOOP}`

# Egg 2

Main-funksjonen kaller en funksjon kalt "StartAddress", denne kjøres 64 ganger med en forskjellig verdi (0-64) satt inn som lpThreadParameter hver gang.\
Funksjonen bruker denne til sende ut meldinger som "Har du vurdert å gi opp?" "Step, step, step..." osv osv, men hvis lpThreadParameter er mindre enn 38 vil en egen kodesekvens også kjøre, der den blant annet tar noe fra et dword-array.\
Fant ut at meldingsboksen som denne delen brukes til hadde meldingen "Hemmelighet"\
Testet diverse, implementerte alt det relevante i python (egg_2.py)\
(Holdt på i sikkert 4 timer fordi min implementasjon av int32 overflows var litt feil :P)\
Koden kan finnes [her](Dag8-Ransomware/Egg_2.py).

EGG:\
`EGG{91d54eb496a1713f5ecdd4d8b1cd636f}`

## Dag 9 - Kronolokalisering

```
Gjennom et beslag har vi fått tak i et papirark. På den ene siden står det “Oppmøtested for den topphemmelige sydpolinfiltrasjonen 2023, rekognosering 23. november”. På den andre siden av arket er det et bilde. For å kunne hente inn overvåkingsbilder og identifisere hvem som har planlagt arrangementet trenger vi det nøyaktige tidspunktet bildet er tatt.

Send meg svar på denne eposten som KRIPOS{tidspunkt}, f.eks. KRIPOS{23:35}, rundet av til nærmeste fem minutter.

- Mellomleder

📎 bilde.jpeg
```

Så på bildet, ante ikke hvor det er tatt. Prøvde reverse image search og fant ut at det var Europol HQ i Haag.\
Antok at det ble tatt 23. November fra oppgaveteksten.

Fant stedet på Google Maps. Tegnet en linje for Nord, Øst og Vest for å indikere solas posisjon ved klokka ~1200, ~1800 og ~0600. \
Tok hensyn til endring i solas posisjon basert på dato, men forskjellen var ganske liten\
Brukte dette sammen med skyggene på bildet for å line opp en approksimering av hva klokka ville vært med skyggens posisjon. Kom frem til ganske nøyaktig midt mellom 1430 og 1200, som var 1315\
Testet 13:15 og 13:20.

Flagg:\
`PST{13:20}`


## Dag 10 - Alvesortering

```
De strenge alvene har skrevet ned et julekodeord, men i den ivrige sorteringen av pakker har det skjedd en horribel feil og alt er blitt rot! Ordet har blitt borte i det som ser ut som et virrvarr av tilfeldig tekst! Nå trenger de hjelp til å gjenfinne ordet. De har null peiling på hvor langt ordet er. Kan du å gjenfinne ordet?

- Mellomleder

📎random_text.bin
```

Så kjapt referansen til "null", kjørte litt statistisk analyse på teksten og fant at det var 100024 "null"-bytes. Sjekket også litt annet og fant ut at det kun var 1 \} og 1 \{. Fant ut at disse var rett etter null-bytes.

Splittet hele dokumentet på null-bytes. Så til slutt at det var referanser til "hvor langt ordet er" og prøvde å sortere på lengde.

Koden kan finnes [her](Dag10-Alvesortering/splitAndSort.py), og [output her](Dag10-Alvesortering/output.txt).

Flagg:\
`PST{julenisseStreng0Alv}`

## Dag 11 - Informasjonsdeling

```
Emne: Informasjonsdeling

NISSENS verksted har mottatt en mystisk melding og litt kode for å dekryptere meldingen. Noen alver i førstelinjen har sett på det, og blir ikke helt kloke. De mistenker at kun denne ene hemmeligheten ikke er nok. Kanskje er det andre som sitter på mer info?

- Mellomleder
```

Løste denne ved å skaffe alle tre hemmeligheten fra alle tre organisasjonene, XORet dem sammen og brukte det som key.\
Hintet til av oppgavenavnet som var "Informasjonsdeling"\
(det kan hende jeg lagde to nye brukere for å skaffe de to andre hemmelighetene..)\
Koden kan finnes i [dekrypter_melding.py](Dag11-Informasjonsdeling/dekrypter_melding.py).\
Hemmelighetene finnes i samme mappe.

Flagg:\
`NSM{9c7cac722d55da1dbfa13025d85efeed45e9ddea2796c0e5ea2fda81ea4de17d}`


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
Fikk bare 34 pakker med Reserved Bit til true, hentet ut disse med [dette pythonscriptet](Dag12-Pakkestorm/extract_data.py).

Flagg:\
`PST{I_cAn_HaZ_rEciprOCaTeD_tRuzT?}`

Koden min mistet "?" på slutten fordi denne var en bit mindre enn de andre, men fant ut av det da jeg manuelt så på pakkene.

## Dag 13 - Geogjettr

```
Emne: Geogjettr

Ledelsen har fått dilla på GeoGjettr og jeg er med i en konkurranse, men klarer ikke finne ut av hvilken by bildet her er fra. Kan du hjelpe meg litt fort?

Svar meg med KRIPOS{navn på by}.

- Mellomleder

📎bilde.jpg
```

Så kjapt QR-koden i bildet.\
Tenkte det kom til å kreves noe "rebuild" av QR-koden i bildet. Men viste seg at telefonen skannet den helt fint.\
Fant noe med Wifi og The State Buildings, googlet the state buildings og fant ut at det var i Perth, Australia.

Flagg:\
`KRIPOS{Perth}`

# Egg
La bildefilen inn i https://www.aperisolve.com \
En del som ikke var helt riktig, men satt meg inn i superimposed, green og blue.

Green hadde mange lange tall, mens blue hadde mange korte tall satt i en rekke.\
Leste litt gjennom begge, så til slutt at tallene i blue hadde to like tegn i posisjon to og tre\
Passet for "EGG"\
Så også at tegn 4 og siste tegn var speilvendt, så jeg tolket dem som { og }.\
Innså til slutt at det skulle tolkes som "antall pixler farget" i pixelart av tegnet.\
[Her er bilde av min pixelart](Dag13-GeoGjettr/Egg.png).\
\
EGG:\
`EGG{RUTER_OVERALT}`\
\
Viste seg at [den grønne channelen](Dag13-GeoGjettr/image_g_1.png) bare ga en annen måte å få samme egget (horisontalt istedenfor vertikalt).

## Dag 14 - Bokorm

```
Emne: Bokorm

En snok vi mistenker å stå i ledetog med Pen GWYN har blitt arrestert etter å ha brutt seg inn i NordPolarBiblioteket og stjålet noen bøker. Vi mistenker at de har vært ute etter noe spesifikt, men vi blir ikke helt kloke på hva det er. Snoken ble tatt med en stabel bøker og et notat.

Bøkene har vi gitt tilbake til biblioteket, men her er en liste av dem som ble stjålet:

Norrøn arverett og samfunnsstruktur
Radium og radioaktive stoffer, samt nyere opdagelser angaaende straaler
Undertrykking av objekter med høy luminans ved hjelp av en romlig lysmodulator under avbildning med CCD- og lysforsterkningskamera
Om den yngre Jernalder i Norge : 1. afdeling
Storlogens Konstitution og Tillægslove
Sild- og saltfiskretter
Notatet inneholdt dette her:
(55, 1, 2, 1), (65, 17, 6, 3), (19, 3, 8, 1), (13, 5, 6, 2), (14, 11, 4, 8), (27, 32, 12, 2), (9, 7, 12, 3), (82, 5, 2, 8), (78, 3, 11, 1), (71, 5, 1, 8), (76, 1, 6, 2), (92, 1, 1, 1), (50, 2, 1, 5), (15, 1, 1, 1), (82, 16, 10, 4), (23, 6, 1, 1), (34, 16, 7, 1), (92, 11, 3, 2), (50, 5, 6, 1), (1, 3, 5, 12), (42, 2, 1, 1), (15, 3, 1, 3), (23, 8, 1, 2), (90, 2, 5, 1), (83, 1, 1, 2), (59, 29, 9, 4), (93, 4, 1, 16), (82, 8, 3, 5), (39, 1, 1, 8), (77, 7, 9, 1), (93, 8, 6, 8), (1, 1, 3, 6), (83, 10, 8, 1), (23, 1, 1, 1), (69, 2, 9, 2), (76, 12, 3, 4), (7, 1, 3, 1), (3, 9, 9, 2), (19, 1, 6, 10), (93, 14, 7, 5), (13, 31, 7, 10), (3, 1, 9, 2), (7, 2, 6, 1), (23, 19, 4, 3), (50, 6, 5, 11)

Send svar til meg om du finner ut av det.

- Tastefinger
```

Lignet på Sidetall, Linje, Ord, Bokstav i bøker, sett lignende før\
Sjekket gjennom noen av bøkene på nett, fant ingenting i Radium og radioaktive stoffer, flere av bøkene fant jeg ikke på nett i det hele tatt\
Fant [Om den yngre Jernalder i Norge : 1. Afdeling](https://www.nb.no/items/ca795dec965d2fb7abb5dffa71a7f81c)\
Testet noen bokstaver og fant PST som de første tre, så tenkte at dette måtte være riktig bok for starten ihvertfall. Viste seg at alt var fra denne boka.

Flagg:\
`PST{bokstavjakt}`

Sidetall, linje, ord, bokstav
```
(55, 1, 2, 1), P
(65, 17, 6, 3), S
(19, 3, 8, 1), T
(13, 5, 6, 2), k
(14, 11, 4, 8), r
(27, 32, 12, 2), ø
(9, 7, 12, 3), l
(82, 5, 2, 8), l
(78, 3, 11, 1), p
(71, 5, 1, 8), a
(76, 1, 6, 2), r
(92, 1, 1, 1), a
(50, 2, 1, 5), n
(15, 1, 1, 1), t
(82, 16, 10, 4),e 
(23, 6, 1, 1), s
(34, 16, 7, 1), b
(92, 11, 3, 2), o
(50, 5, 6, 1), k
(1, 3, 5, 12), s
(42, 2, 1, 1), t
(15, 3, 1, 3), a
(23, 8, 1, 2), v
(90, 2, 5, 1), j
(83, 1, 1, 2), a
(59, 29, 9, 4), k
(93, 4, 1, 16), t
(82, 8, 3, 5), k
(39, 1, 1, 8), r
(77, 7, 9, 1), ø
(93, 8, 6, 8), l
(1, 1, 3, 6), l
(83, 10, 8, 1), p
(23, 1, 1, 1), a
(69, 2, 9, 2), r
(76, 12, 3, 4), a
(7, 1, 3, 1), n
(3, 9, 9, 2), t
(19, 1, 6, 10), e
(93, 14, 7, 5), s
(13, 31, 7, 10), S
(3, 1, 9, 2), l
(7, 2, 6, 1), U
(23, 19, 4, 3), t
(50, 6, 5, 11), t
```
\
Sjekket noen av de andre for å lete etter egg, men fant ingenting i de jeg fant og gadd ikke sjekke resten


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
Scriptet ligger [her](Dag15-Bitraate/document_reconstruction_script.py).

Flagg:\
`PST{e32ba07d1254bafd1683b109c0fd6d6c}`

## Dag 16 - Invasjon

```
Emne: Invasjon

Gjennom temmelig hemmelige innhentingsmetoder har vi fått tak i det vedlagte dokumentet som avslører den egentlige hensikten bak løsepengeangrepet: Sydpolare aktører planlegger å invadere Nordpolen for å stoppe julen én gang for alle!

I dokumentet nevnes det at aktørene har plantet deep-cover agenter i blant oss, og at de har hemmelige koder for å etablere kontakt med disse. Analyser materialet og se om du klarer å avsløre de hemmelige kodene slik at vi kan få disse agentene på kroken!

I mellomtiden iverksetter vi umiddelbare mottiltak for å stanse invasjonen.

- Tastefinger

📎aksjon_2023.zip
```

Sjekket litt gjennom git branches, fant "ikke commit før julaften" der det står
```
Author: Pen Gwyn <p1@spst.no>
Date:   Mon Sep 25 11:11:11 2023 +0200

    Placeholder for eksfil av feltagenter

    Prosedyre for kodegenerering vil bli implementert senere for å beskytte
    våre agenter
```
Samt en fil som het feltagenter_kontaktmanual.md med noen KODE_PLACEHOLDERs for 3 agenter.\
Kjørte `grep -R feltagenter_kontaktmanual.md .` for å se om det var noen flere referanser til dette. Fant [pre-merge-commit](Dag16-Invasjon/aksjon2023/_.git/hooks/pre-merge-commit) som skulle gjøre noen endringer, oversatte base64 jeg fant inne i filen

> Unnskyld, vet du veien til biblioteket? <RESPONS>. Sa jeg biblioteket? Jeg mente fiskeforhandleren, kan du vagge bort med meg

> Ikke god jul.

> KRIPOS{Flagg i alle kriker og kroker}

Flagg:\
`KRIPOS{Flagg i alle kriker og kroker}`


# Egg
Det fantes referanser til at noen hadde mistet et egg, sjekket lost-found og fant en commit som inneholdt et stort egg. Egget fantes i midten av [dette store egget](Dag16-Invasjon/aksjon_2023/_.git/lost-found/other/fdfbb6ab8dda68e83853bf372a100e8ff6e8830f).

EGG 4:\
`EGG{h3ng3r 0g d1ngl3r}`


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
Pythonscriptet mitt kan finnes [her](Dag17-Innebygde-ord/dag17.py).

Flagg:\
`pst{nede for telling}`

## Dag 18 - Melding fra antikken

```
Emne: Melding fra antikken

I riktig gamle dager hadde NISSEN flere regionskontor spredt rundt i verden. Disse kontorene fungerte både som mottak for ønskelister og distribusjonssenter for gaver. Da som nå var det ikke alle som oppførte seg like pent fram mot jul, og ifølge historiebøkene var spesielt organisasjonen PERSIUS (ledet av den onde Dr. Xerxes) stadig vekk på spion- og toktforsøk mot ett av NISSENs regionkontor. På sitt verste var det angivelig hele 300 alvebetjenter i sving for å forsvare gaver og ønskelister. De særs tapre alvene til tross, NISSEN var reelt bekymret for at viktig informasjon og gaver skulle havne på avveie. Siden den gang har derfor all julesensitiv informasjon blitt kryptert.

Takket være noen alvorlige logistikkproblemer (og muligens en streik eller to) har plutselig en slik gammel melding dukket opp. Julelovens paragraf §133-syvende ledd er imidlertid krystallklar

Enhver julesensitiv informasjon må analyseres og vurderes før den avgraderes høytid.

Imidlertid er det ingen av Alvene som aner hvordan denne gamle meldingen skal leses. Kan du hjelpe dem?

- Mellomleder

📎melding.txt
```

Gikk dypt ned i rabbit-holet og antok at alt av informasjonen i oppgaveteksten var relevant.\
Fant ikke noe spesielt med hverken tallene eller informasjonen.

Testet noe på en whim, kjørte bare "hent hver nte bokstav" på teksten fra 1 til 500. Visste at første tegn alltid ville være p så spesifiserte at jeg bare ville ha "pst[...]"\
Pythonskriptet kan finnes [her](Dag18-Melding-fra-antikken/everyNthCharacter.py).

Flagg:\
`pst{var_julenissen_kong_leonidas}`


## Dag 19 - Hide and seek

```
Emne: Hide and Seek

Som følge av et stadig økende trusselbilde, spesielt ifra sydligere strøk, har Nordpolar sikkerhetstjeneste etablert en intern enhet som skal beskytte tjenestens egne digitale systemer mot angrep. Enheten består av nøye selekterte tidligere alveteknologer som har god erfaring med bekjempelse av sydpolare aktører.

Grunnet tidligere prestasjoner på Nordpolen har NISSEN selv navngitt enheten til Julens Utvalgte Lærde Elektronisk databehandlende Sikkerhets og Operative Center, forkortet JULESOC. JULESOCen kan blant annet bidra til å finne ondsinnede fugler i datasystemene til Julenissens verksted, grave i sildcoin transaksjoner og analyse av speilglatte kopier.

JULESOC har nylig mottatt en speilkopi av en arbeidsstasjon lokalisert på Julenissens verksted. Det er mistanke om at noen uautoriserte har vært inne på maskinen og tukla. Vi trenger at du graver frem noen spor.

- Mellomleder

📎image.raw.gz
```

Måtte først dele image.raw i tre partisjoner med kpartx.\
En av delene hadde en mappe /hemmelig/ med en "code"-fil, denne inneholdt bare masse tall i et array.\
Den andre delen inneholdt noen tomme mapper, en python-fil som så ut til å lage "code"-filen, og et stort tekstdokument\
Den tredje delen inneholdt kun et bilde av en [QR-kode](Dag19-Hide-and-seek/Partisjoner/qr-kode.png) som bare var "blindspor dessverre, let videre"\
Tenkte bare prøve å bruke tallene fra code-filen som indeks til tegnene i tekstdokumentet.

Flagg:\
`PST{TheGrinchWouldHateThis}`

[1817, 1004, 2238, 1709, 18, 714, 2499, 3069, 2148, 854, 1480, 831, 2441, 373, 276, 374, 844, 2725, 736, 2204, 1107, 1478]\
Fant en annen array med indekser pluss en annen [nissetekst-lignende fil](Dag19-Hide-and-seek/nissetekst_2), men fant ingenting fra disse to..\
Kan hende det finnes et egg? Enn så lenge fikk jeg "eaf t ndpnc hhneteti p"...

## Dag 20 - Rudolfs Eventyr

```
Julefreden har begynt å senke seg over Nordpolen, og alvene har blitt hekta på på et retro spill. I følge noen av alvene er det visstnok mye hemmeligheter her!

Et lite avbrekk i julestria må da være lov?

- Tastefinger

📎rudolfs_eventyr.gba
```

Så det var en game boy advanced spill-fil, kjørte den i mGBA. Veldig morsom oppgave :P\
Første man finner i spillet er første del av flagget på en lapp i rommet man starter\
`NSM{`

Fant deretter en alv som sa at en del av flagget lå i VRAM. Åpnet opp forskjellige bakgrunner i mGBA og fant [dette](https://i.imgur.com/weVQe9B.png).\
FLAGG DEL 2:\
`RUDO`


Gikk deretter rundt i de forskjellige husene og fant et hus med en lapp med braille \
https://i.imgur.com/UbGmYVT.png som sier \
DEL 4 AV FLAGGET: \
`EDDE`
\
Fant deretter en alv som spilte kron eller mynt og sa at hvis man vant 100 ganger på rad så fikk man hemmeligheten hans\
Lastet ned cheat engine og fant [denne](https://i.imgur.com/XmB9GM9.png) verdien som sa "streaken" man hadde\
Satt den til 99 og vant en gang\
Flagg siste del: \
[la!}](https://i.imgur.com/UR87qG1.png)\
\
Hadde nå\
NSM{RUDOxxxxEDDExxxxla!}\
RUDO er nok starten på RUDOLF_ ihvertfall\
Gjetta {Rudolf_redder_jula!}\
\
Visste at det fantes et rom med noe som minte om morsekode, men syns det var vanskelig å skrive ned så jeg bare ignorerte det frem til nå.\
Morsekoden var del 3, altså LF_R.\
\
Manglende del "R_JU" vet jeg finnes inne i en dør som må åpnes ved å endre på noe i SRAM (ref en av alvene utenfor døra) men denne har jeg ikke klart enda.\
[Noe med yolo..?](https://i.imgur.com/lIWl9oO.png)\
\
Flagg:\
`NSM{RUDOLF_Redder_jula!}`

## Dag 21 - Rudolf "The Stag"

```
Emne: Rudolf "The Stag"'s Pepperkaker

Nasjonens sikkerhetsalver leter febrilsk etter sin temmelig hemmelige pepperkakeoppskrift, men det peker til at Rudolf "The Stag" kanskje har spist opp denne. Klarer du skanne "The Stag"'s kropp og lese av denne før den går sin naturlige gang og blir borte for alltid?

- Mellomleder

📎rudolph.7z
```

Her er jeg fullstendig blank... Denne hadde ingen løst før hintet vi mottok 3. Januar:
```
Emne: The Stag's Analyse

Hei,

Jeg sjekket opp på en av alveanalytikerne våre som har låst seg inn på kontoret sitt og jobbet med tolkingen av bildet av Rudolf og pepperkakeoppskriften. Jeg tror ikke det går så veldig bra med han.

Kontoret var fylt med halvspiste pepperkakebiter arrangert på rekker, og han mumlet noe om adventspekere før han jaget meg ut av kontoret.

Jeg er bekymret for at han har fått i seg noe dårlig julegløgg. Kan du gi han en hånd og hjelpe han med det problemet?

- Tastefinger
```

Hadde allerede satt meg litt inn i "peker" fra originalmeldingen, men visste ikke hva jeg skulle med det.\
Halvspiste biter så jeg for meg at refererte til de siste 4 bits av hver byte, dette passer også godt med at det er her man ser en "strek" øverst i blå og rød. Grønn derimot har ikke denne.\
Jeg tenkte kanskje bruke de siste 4 bits fra blå og rød som en "pointer" til å hente ut en pixel fra bildet.\
Jeg fant ingenting fra dette, testet diverse annet uten hell.

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
Hentet ut UUID fra denne med [dette pythonscriptet](Dag22-Gaveliste-endring/categorize_modification.py).

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
Åpnet bildet i [aperisolve](https://www.aperisolve.com), fant [image_b_4.png](Dag23-KVU-dokumenter/image_b_4.png) med en tekststreng skjult. Brukte denne (e24f52497bcf4c332f1283ec925f77a1) som nøkkel i dekrypteringsskriptet.\
Cashflow ble dekryptert, og fikk en budsjettoversikt. I månedlige inntekter fant jeg PST{alternativ_pengestrøm} på 1000 kr.\
\
Flagg:\
`PST{alternativ_pengestrøm}`

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


## Egg
# Minesveiper egg 1
Med en gang minesveiper kom ut la jeg merke til en bug der høyreklikking av der det ville vært en bombe gjorde så "bombecounten" øverst til venstre telte ned.
Så at ingen fant noen flagg så antok at det bare var noe moro og det var en uskyldig bug.
Dagen etter kom det nye modes, antok at det var noen egg. Prøvde det jeg fant dagen før og fant med en gang [første egget](egg/egg_1.png)\
Egg 1:\
`EGG{RETRO}`

# Minesveiper egg 2
Fant [egg nr. 2](egg/egg_2.png).
Skjønte at det var samme greia, prøvde mye forskjellig som braille og å flytte rundt på andre halvdel, flippe det opp ned [.......]
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
Koden kan finnes [her](Dag8-Ransomware/Egg_2.py).

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
[Her er bilde av min pixelart](Dag13-GeoGjettr/Egg.png).

EGG 5:\
`EGG{RUTER_OVERALT}`

Fant ingenting fra [den grønne channelen](Dag13-GeoGjettr/image_g_1.png).

# Hide and seek egg:
Det fantes referanser til at noen hadde mistet et egg i noe git historikk, sjekket lost-found og fant en commit som inneholdt et stort egg. Egget fantes i midten av [dette store egget](Dag16-Invasjon/aksjon_2023/_.git/lost-found/other/fdfbb6ab8dda68e83853bf372a100e8ff6e8830f).\
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
