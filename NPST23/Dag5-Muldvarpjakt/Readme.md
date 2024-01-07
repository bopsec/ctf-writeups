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