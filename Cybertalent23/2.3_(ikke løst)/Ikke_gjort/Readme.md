# Velkommen til forskningsministeriet-qkd-staging

*Department of research* er for tiden opptatt med testing og utrulling av en nytt system for kvante-nøkkelutveksling (QKD) som benytter kvantesammenfiltring for å kommunisere på måter som vil være fysisk umulig å knekke. Dette muliggjøres som de fleste vet av kvante-internettet vi akkurat rullet ut. Kvante-nodene i dette nettverket kjører ekstremt spesialisert hardware, og utviklere henvises til QNET_API. QKD-testmiljøet består p.t. av tre vanlige noder A, B, C, som hver naturligvis har sin egen kvanteboks (qnode) qA, qB, qC som de gjør kvante-kommunikasjon med:

- Node A, der qA har QTP-addresse qtp://αε:ηβ:εα:βε
- Node B, der qA har QTP-addresse qtp://βδ:θδ:ζα:δθ
- Node C, denne maskinen, der qC har QTP-addresse qtp://γζ:βα:δγ:γβ, og kan nåes på http://qnet_node_c.utl:5000

Av kostnadshensyn har A og B i første omgang kun fått lagt kvantefibre til C, så all kommunikasjon (både QTP og HTTP) går via C og qC. Heldigvis er QKD-varianten vi bruker (E91) nettopp laget for å være robust mot MitM-angrep, så A og B kan utveksle sensitiv informasjon selv om noen mot formodning skulle komme inn på denne maskinen og bruke verktøy som tcpdump til å følge med på kommunikasjonen eller tukle med den.

QKD-utviklere henvises til ./qkd_software_dev for utvikling av programpakkene.

Her er et enkelt nettverksdiagram:
```
QA <~~> QC <~~> QB
↑       ↑       ↑
|       |       |
↓       ↓       ↓
A <---> C <---> B
```