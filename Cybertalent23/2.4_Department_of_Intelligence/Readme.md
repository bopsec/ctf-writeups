## 2_4_Department_of_Intelligence

# 2_4_1_flag0
Etter at jeg testet forferdelig mye forskjellige uten hell for å finne høyde/bredde osv så kom jeg frem til at - siden dette er et BITMAP bilde uten encryption - så kan jeg bare eksperimentere med høyde og bredde frem til jeg ser hva bildet utifra 0 og 1-ene...\
[Her er flagget...](https://i.imgur.com/2WSHb8U.png)
FLAG{83911047f89fff0424210dff6e81d2aa}
```
login@corax:~/2_oppdrag/4_department_of_intelligence$ scoreboard FLAG{83911046f89fff0424210dff6e81d2aa}
Kategori: 2.4. Department of Intelligence
Oppgave:  2.4.1_bits_flag0
Svar:     83911046f89fff0424210dff6e81d2aa
Poeng:    10

Godt jobbet, du fant informasjonen!
```
Visste at jeg måtte finne en måte å finne bredde og høyde uansett, men brukte løsningen min for å hjelpe meg selv med å lage noe kode som fant den riktige bredden og høyden :P\
Fant senere ut at grunnen til at jeg ikke fant bredde og høyde var fordi jeg glemte å ta hensyn til length.\

# 2_4_2_flag32
Visste at 32 bit crypto ikke ville ta mer enn ~20 min å bruteforce, så jeg bare satt opp en kjøring i bakgrunnen der jeg kjørte crypt på en 000[..]-streng av lengde 802, sammen med de første 802 bitene fra ciphertext som fulgte etter length, type, width og height til flag32. Lengde, type, bredde og høyde var ikke kryptert.\
Fant nøkkelen etter 10-15 minutter på `2920247797`\
I ettertid lagde jeg et .cpp program for å teste effektiviteten. Dette brukte ikke mer enn 30 sekunder iirc.
Lagde en basic decrypt-funksjon fra den originale crypt-funksjonen i BITS.txt\
```
def decrypt(bitstream, initial_key, size=32, g=3):
    k = size - 1
    mask = (1 << size) - 1
    key = initial_key
    decrypted = []
    for b in bitstream:
        decrypted_bit = (key >> k) ^ b
        decrypted.append(decrypted_bit)
        key = (g * key) & mask
    return decrypted
```
FLAG{11053f8124886b02695deb0a2e0a5046}, i [samme format](https://i.imgur.com/nbkbvow.png) som forrige oppgave.

```
login@corax:~/2_oppdrag/4_department_of_intelligence$ scoreboard FLAG{11053f8124886b02695deb0a2e0a5046}
Kategori: 2.4. Department of Intelligence
Oppgave:  2.4.2_bits_flag32
Svar:     11053f8124886b02695deb0a2e0a5046
Poeng:    10

Veldig bra jobbet, du klarte å finne informasjonen i bildet! Informasjonen inneholder en zip-fil. Vi har lagt den i oppdragsmappen din på corax. Kanskje du får bruk for den i Department of Nuclear Power?

Ny fil: /home/login/2_oppdrag/hexostator-images.zip
```

# 2_4_3_flag64
Løste ikke denne.

# 2_4_5_win1
GameOfWIN lignet veldig på NIM, så tenkte at det var lurt å ta en titt på strategier for å vinne i dette\
Fant diverse på nett som viste til NIM numbers/[Nimbers](https://en.wikipedia.org/wiki/Nimber), implementerte noe lignende og vant etter noen iterasjoner og litt testing.\
Å vinne i de to andre spillene var bare snakk om å utvide funksjonen til å ta inn et større brett, da spillet er nøyaktig det samme.
```
You win! FLAG{fec671c7e8306ab4d4bc10481c33642b}
login@corax:~/2_oppdrag/4_department_of_intelligence$ scoreboard FLAG{fec671c7e8306ab4d4bc10481c33642b}
Kategori: 2.4. Department of Intelligence
Oppgave:  2.4.5_bits_win1
Svar:     fec671c7e8306ab4d4bc10481c33642b
Poeng:    10

Gratulerer, du slo BITS-serveren deres!
```

# 2_4_6_win2
Se 2_4_5_win1.
```
You win! FLAG{66f1bd3f3b50209edbedf8a56e0f57c0}
login@corax:~/2_oppdrag/4_department_of_intelligence$ scoreboard FLAG{66f1bd3f3b50209edbedf8a56e0f57c0}
Kategori: 2.4. Department of Intelligence
Oppgave:  2.4.6_bits_win2
Svar:     66f1bd3f3b50209edbedf8a56e0f57c0
Poeng:    10

Imponerende, BITS-serveren deres kan ikke stoppe deg!
```

# 2_4_7_win3
Se 2_4_5_win1.
```
You win! FLAG{60b264c1408b2fc3b07f16c98de727aa}
login@corax:~/2_oppdrag/4_department_of_intelligence$ scoreboard FLAG{60b264c1408b2fc3b07f16c98de727aa}
Kategori: 2.4. Department of Intelligence
Oppgave:  2.4.7_bits_win3
Svar:     60b264c1408b2fc3b07f16c98de727aa
Poeng:    10

Fantastisk, du har vunnet over BITS-serveren deres på det vanskeligste nivået!
```
