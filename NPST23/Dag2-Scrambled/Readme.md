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