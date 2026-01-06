# Kryptogram

Er du vår neste Egil Mørk? Tiden skrus tilbake til den mørke dagen 23. november 1935.

Som det vil sees er knekningen av et kryptogram ingen heksekunst,
men det krever litt tålmodighet og at man prøver seg frem og tar fantasien til hjelp.

Benevnelser og arbeidsmetoder kan kanskje virke litt fremmed i første øyeblikk,
men setter man seg inn i saken, er den i virkeligheten enkel.

Du kan hente kryptogrammet her:

```sh
nc kryptogram 1337
```

Besvarelsen du sender inn, finner du i innholdet av meldingen.

--------------------------------------------

```sh
login@corax ~/1_grunnleggende/1.8_Kryptogram $ nc kryptogram 1337
Her er kryptogrammet:
øwbxl hjcbx læxmx fpxfx lmrcb xlpxo rvøpl rlvrc hrjlø cjxøp brdrb xbræs xlxbb xfhxl yxocx lwfxy øvwjf dryxf xjhhy føvæf apxcp jyxjf yxbøb bxfoj jmwfx mjdxf

>
```

Kjørte gjennom dcode cipher identifier, påsto at det var en monoalphabetic substitution, og ga meg noe med en noe realistisk mapping ("aften posten[...]"), bestemte meg for å fortsette med den antagelsen, og testet meg litt frem med mappings for andre bokstaver enn de første\
Innså litt senere at dcode auto decode kun feilet fordi det var æøå i teksten\
Endte opp med:

`aften poste nbeme rkere nmist enkel igakn ingis piona soeak tivit etiby enett erpen delse nfred agfor vider eoppd ragbr ukesk odeor detat terlo omfre mover`

->

`aftenposten bemerker en mistenkelig (ø)kning i spionas(j)eaktivitet i byen etter (h)endelsen fredag for videre oppdrag brukes kodeordet atterloom fremover`\
Teksten inneholdt noen feil selv etter dekoding, men budskapet var klart.

I README star det at besvarelsen er i innholdet av meldingen, så jeg antok at det var kodeordet:

```sh
> atterloom
a812a540b75778ab762af36b7e214182
```

Flagget er a812a540b75778ab762af36b7e214182