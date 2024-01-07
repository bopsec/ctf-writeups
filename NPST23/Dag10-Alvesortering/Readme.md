## Dag 10 - Alvesortering

```
De strenge alvene har skrevet ned et julekodeord, men i den ivrige sorteringen av pakker har det skjedd en horribel feil og alt er blitt rot! Ordet har blitt borte i det som ser ut som et virrvarr av tilfeldig tekst! Nå trenger de hjelp til å gjenfinne ordet. De har null peiling på hvor langt ordet er. Kan du å gjenfinne ordet?

- Mellomleder

📎random_text.bin
```

Så kjapt referansen til "null", kjørte litt statistisk analyse på teksten og fant at det var 100024 "null"-bytes. Sjekket også litt annet og fant ut at det kun var 1 \} og 1 \{. Fant ut at disse var rett etter null-bytes.

Splittet hele dokumentet på null-bytes. Så til slutt at det var referanser til "hvor langt ordet er" og prøvde å sortere på lengde.

Koden kan finnes [her](splitAndSort.py), og [output her](output.txt).

Flagg:\
`PST{julenisseStreng0Alv}`
