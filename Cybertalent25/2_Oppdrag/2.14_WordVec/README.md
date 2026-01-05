# WordVec

GooodGames har lagt ut enda et KI-spill. Her er målet å traverse fram til ordet "flagg".

Vi har ekstrahert et internt dokument som forklarer hvordan spillet fungerer, og hvordan man skal traverse gjennom de ulike ordene. Lykke til!

https://wordvec.ctf.cybertalent.no

---

"Spilte" litt manuelt frem til jeg fikk noen ord jeg trudde kunne bli nyttige, så lagde jeg en BFS-søker som lette etter spesifike ord (feks symbol, emblem, land, osv) som jeg så for meg kunne lett gi meg "Flagg" hvis kombinert med riktige ord.\
Etter at jeg kjørte solveren en stund fant den emblem, og rett fra emblem så fikk vi flagget\
Solver script ligger i [solver.js](solver.js), jeg har mistet vektorene jeg brukte for å starte, men noen få ligger i [vectors.txt](vectors.txt)


```sh
[...]
VM675:232 
Step 3: Attempt solve
VM675:162 
Attempting solve with: (16)['land', 'tyskland', 'sverige', 'symbol', 'norge', 'merke', 'nasjon', 'stat', 'rike', 'emblem', 'norsk', 'svensk', 'dansk', 'frankrike', 'spania', 'england']
VM675:206 
Searching semantically near Norwegian words...
VM675:209 Searching near norge...
VM675:209 Searching near nasjon...
VM675:209 Searching near symbol...
VM675:209 Searching near land...
VM675:209 Searching near merke...
VM675:236 
Step 4: Deep search from found vectors
VM675:238 
Searching from land...
VM675:97 [0] Exploring: land
VM675:97 [2] Exploring: landene
VM675:97 [3] Exploring: lands
VM675:97 [4] Exploring: landet
VM675:97 [5] Exploring: Norge
VM675:97 [8] Exploring: nasjonene
[...]
VM675:238 
Searching from emblem...
VM675:97 [0] Exploring: emblem
VM675:75 FOUND FLAGG!
VM675:77 🚩 FLAG: {flag: '2bda9d2137c819b6f65b59c5a0698fd8'}flag: "2bda9d2137c819b6f65b59c5a0698fd8"[[Prototype]]: Object
```

Flagget er 2bda9d2137c819b6f65b59c5a0698fd8


login@corax ~/2_oppdrag/2.14_WordVec $ scoreboard 2bda9d2137c819b6f65b59c5a0698fd8

2.14.1 WordVec\
Klikk klikk klikk... FLAG!