# Bekrivelse av qnet-noders API

All kommunikasjon over qnet skjer via QTP over kvantefibre, som er koplet til qnet-noder (herunder 'qnodes'). Enhver qnode skal tilkoples et privat nett med 1 klassisk maskin som kan kontrollere qnoden via et HTTP-api beskrevet i dette dokumentet.

## Konsepter
### Quuid
En quuid er en streng som unikt navngir en bestemt qubit, f.eks. 'θαγε-ζζαθ-βθαε-θζηα'. Om den tilhørende qubit-en overføres til en annen qnode beholder den samme quuid, og for å gjøre en måleoperasjoner e.l. på den må man oppgi quuid-en til qubiten man vil gjøre ting på.

### QTP-adresser
QTP-protokollen brukes til kommunikasjon over kvantefibre. Inngående kjennskap til denne forutsettes ikke for å benytte qnodes. Man må dog vite at hver qnode har en unik QTP-adresse, f.eks. 'qtp://γζ:βα:δγ:γβ', og at denne benyttes for å identifisere f.eks. mottager av qubits man vil sende. Merk at man IKKE benytter denne for å sende HTTP-forespørsler til egen lokale qnode.

### Qubit-decay
Selv om levetiden til qubits stadig øker vil de over tid brytes ned, og etter hvert forsvinner informasjonen i dem. Når dette skjer merker qnoden at de er blitt korrupte, og den tilhørende quuid-en vil ikke lenger regnes som gyldig som argument til noen av endepunktene under. Per i dag kan en qubit forventes å leve i om lag 10 minutter.

## qnode-endepunkter
Alle disse endepunktene nåes via HTTP-forespørsler. Normalt har en qnode hostname på formen qnode_x og kan nåes på port 5000.

### /prepare_states (POST)
Brukes til å initialisere qubits i en bestemt starttilstand, som senere kan endres ved f.eks. å måle dem.

Input: JSON-payload {"states": state_vecs}
state_vecs er en liste av et vilkårlig antall (N) tilstandsvektorer for tilstander på 1 eller flere qubits. En tilstand på M qubits beskrives som en liste med 2^M 2-elementslister, der hver 2-element-liste representerer et komplekst tall (a+bi <-> [a, b]) som er en koeffisient i tilstandsvektoren. Tilstandsvektoren oppgis i standardbasisen, dvs (for en tilstand med 3 qubits) 000, 001, 010, 011, 100, 101, 111. I utrullingsfasen forutsettes det at M ikke er mer enn 10.

Returverdi: JSON-payload {"quuids": quuid_list}
quuid_list er en liste med M lister av quuid-er. quuid-liste nr. M oppgir quuid-ene til qubits-ene i tilstanden med tilstandsvektor state_vecs[M]. Alle disse qubit-ene befinner seg til å begynne med på qnoden som opprettet dem. Merk at ulike qubits i samme tilstand fra nå av ikke behandles som noen enhet, og det går fint å f.eks. sende av gårde den ene og beholde den andre selv.

### /measure_qubits (POST)
Brukes til å måle qubits en qnode selv besitter. (En qnode kan naturligvis ikke måle en qubit som er et helt annet sted.)

Input: JSON-payload {"quuids": quuids, "basis_1s": basis1_vecs, "basis_2s": basis2_vecs}
quuids er en liste av quuid-ene til alle qubit-ene man vil måle. basis_1s og basis_2s oppgir første- og andre-vektoren i basisene man vil måle i. Effekten blir altså at qubit quuids[M] måles i basisen bestående av basis1_vecs[M] og basis2_vecs[M]. Hvert element i basis1_vecs er en liste av lengde 2, der hvert element er en liste som representerer et komplekst tall som beskrevet i /prepare_state. Om man vil måle en qubit i standard-basisen skjer dette altså ved å sende følgende payload:

{"quuid": "some-quuid", "basis1s": [[[1, 0], [0, 0]]], "basis2s": [[[0, 0], [1, 0]]]}

Output: JSON-payload {"measurement_outcomes": outcomes}, der outcomes er en liste med elementer som enten er 0 eller 1. outcomes[M] er 0 dersom målingen av quuids[M] ga basis1_vecs[M], og 1 dersom den ga basis2_vecs[M]. (Andre muligheter finnes naturligvis ikke.) Målingene skjer sekvensielt dersom dette er relevant.

Merk: Det returneres en feilmelding (og ingenting skjer) dersom man forsøker å måle i en basis som ikke er en basis (f.eks. fordi vektorene ikke er ortonormale) eller forsøker å måle en qubit som ikke befinner seg på denne qnode-en (f.eks. fordi man har sendt den av gårde).

### /transmit_qubits (POST)
Brukes for å sende qubits til andre qnodes. De vil da ikke lenger være tilgjengelig for at man kan måle dem selv, men kanskje mottageren har mer glede av dem.

Input: JSON-payload {"recipient_node_id": qaddr, "quuids": quuids}

qaddr er QTP-addressen til mottagernoden, som man antas å være tilkoplet. (Går det ingen direkte kvantefiber vil kallet feile.) quuids er en liste med quuid-er, der hver quuid antas å tilhøre en qubit man selv eier (ellers vil kallet igjen feile). Er alt i orden vil mottager-qnoden få alle qubitene.

Output: Tom JSON-payload ({})

### /query_qubits (GET)
Brukes for å sjekke hvilke qubits man besitter.

Output: JSON-payload {"quuids": quuids}, der quuids er en liste over alle quuid-ene til qubits på denne qnoden. Dersom man forventer å se en qubit her som ikke dukker opp, og man ikke har sendt den av gårde med /transmit_qubits, så kan det hende den har blitt nedbrutt, som beskrevet over.