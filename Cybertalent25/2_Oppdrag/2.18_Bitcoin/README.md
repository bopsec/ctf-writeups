# bitcoin

Våre operatører har fanget opp noe vi mener er en nettbasert transaksjon.

Vi har grunn til å tro at avsenderen har kryptert en datamengde du kan være interessert i, ved å bruke privatnøkkelen sin som en éngangsnøkkel (OTP).

Kjør følgende kommando for å koble til endepunktet og motta den krypterte datamengden samt transaksjonen:

```sh
nc bitcoin 8333
```

Flagget består av de første 16 bytene av det dekrypterte innholdet.

---
```
login@corax ~/2_oppdrag/2.18_Bitcoin $ nc bitcoin 8333
Her er den krypterte datamengden:
fac04a6616e28cd43c1ebaa992fe08a7835aefe1b9943785d6f2ca534dc8c558

Trykk Enter for å se transaksjonen...

============================================================

{
  "txid": "4a70cfc431ef40398f83975effb8e0c65f5143c519f731ba5d7f83abb2775554",
  "size": 555,
  "version": 1,
  "locktime": 0,
  "fee": 50000,
  "inputs": [
    {
      "coinbase": false,
      "txid": "0a56efc7deeee4fb0eb346cc52310bd3e0603c56953cdab7901259a029553332",
      "output": 1,
      "sigscript": "47304402205cd879ed58c689be87083e847eb61f8b782d147420532cb320ead9f63221560502200a549c03865abd5856fad8edf92b17c66203f45493947fcb084a9d2450dba95f014104dede3591d6a58bf1be284a2884f98b629403cc13464a6b3a176af4a658822aa28921a8a5f01d3d719aec5ddb165854cda6ff442e80bd525d93b3c852ef16fb77",
      "sequence": 4294967295,
      "pkscript": "76a9143512b6d99f0ada742710e786c8666105ea71974a88ac",
      "value": 130000,
      "address": "15qdETUYSwtb8UJEKtRkoXcTm199KMMHzx",
      "witness": []
    },
    {
      "coinbase": false,
      "txid": "1812edc870824c1a68062909ba03e3a6d8a0e1c11471692c5d997a804dced220",
      "output": 1,
      "sigscript": "47304402205cd879ed58c689be87083e847eb61f8b782d147420532cb320ead9f632215605022009a8fe0d1b20e9d41eae2f3c11a7b19b4cc4975c17279168b179736fe36612ae014104dede3591d6a58bf1be284a2884f98b629403cc13464a6b3a176af4a658822aa28921a8a5f01d3d719aec5ddb165854cda6ff442e80bd525d93b3c852ef16fb77",
      "sequence": 4294967295,
      "pkscript": "76a9143512b6d99f0ada742710e786c8666105ea71974a88ac",
      "value": 120000,
      "address": "15qdETUYSwtb8UJEKtRkoXcTm199KMMHzx",
      "witness": []
    }
  ],
  "outputs": [
    {
      "address": "15qdETUYSwtb8UJEKtRkoXcTm199KMMHzx",
      "pkscript": "76a9143512b6d99f0ada742710e786c8666105ea71974a88ac",
      "value": 200000,
      "spent": true,
      "spender": {
        "txid": "b760f15a3a6a13fa92ee705543b0fe2f8e86ef86a265abf24c7fed6ce6c3e6a1",
        "input": 0
      }
    }
  ],
  "block": {
    "height": 316433,
    "position": 11
  },
  "deleted": false,
  "time": 1408435732,
  "rbf": false,
  "weight": 1887
}
```



Sigscripts for begge er det samme, nonce reuse

Input 1 sigscript:\
`4830450220585ab36f9f554049f045bd9c9347a4045aa7ad5f666dc4e72c19c4ba7921ac36022100a663a41bd336c5730010ea8ad1a6284dcfcd77237797d740774b7e7146aa723d01...`

Input 2 sigscript:\
`4830450220585ab36f9f554049f045bd9c9347a4045aa7ad5f666dc4e72c19c4ba7921ac36022100916b7958e8ea912b960766502afaa16b28ade3e30239bbef430acec974ba46c101...`


Begge signaturene har:\
`r = 585ab36f9f554049f045bd9c9347a4045aa7ad5f666dc4e72c19c4ba7921ac36`\
`s1 = a663a41bd336c5730010ea8ad1a6284dcfcd77237797d740774b7e7146aa723d`\
`s2 = 916b7958e8ea912b960766502afaa16b28ade3e30239bbef430acec974ba46c1`


ECDSA nonce reuse:
- k = (z1 - z2) / (s1 - s2) mod n
- private_key = (s * k - z) / r mod n
- Hvor z1 og z2 er meldingshashes (transaction sighashes)


```sh
python3 bitcoin.py
Recovered private key: 0x742661af80da42acea27c71638e4bc93e24fe95f4c56cb5f721e2a6530b6261e
Decrypted (hex): 0340ae9cd240604f47e7773ec2791abd0340ae9cd240604f47e7773ec2791abd

First 16: 0340ae9cd240604f47e7773ec2791abd
```

Flagget er 0340ae9cd240604f47e7773ec2791abd
