# Eye of the tiger

Vi har fanget opp noe vi tror er en hemmelig kommunika(tt)sjonskanal Gooodgames bruker.

Dessverre er alt vi finner bare kattebilder.

https://eye-of-the-tiger.ctf.cybertalent.no

---




Klikk på en spesifik pixel i venstre øye\
```js
let svgObject = document.querySelector('object');
let svgDoc = svgObject.contentDocument;
let n1 = svgDoc.getElementById('n1');
```

Så kommer man til en hemmelig side med flagget :)\
Pixelen var heldigvis en annen farge så var ikke vanskelig å finne og trykke, bare zoome litt inn på siden.


![hidden_channel.png](hidden_channel.png)