# Cybertalent-2023

Cybertalent er en årlig CTF holdt av Etteretningstjenesten. 
1. Grunnleggende
2. Oppdrag
4. Skjulte flagg

Jeg valgte å bare inkludere oppdraget i denne writeupen, da "Grunnleggende" virker som at brukes om igjen hvert år. Konteksten til oppdraget finnes i [INTREP.txt](Kontekst/INTREP.txt).

Jeg endte opp med 300/440 poeng og disse oppdragene fullført:
```
login@corax:~/2_oppdrag$ scoreboard
Poeng: 300

1. Grunnleggende
1.1_scoreboard: LØST
1.2_setuid: LØST
1.3_injection: LØST
1.4_overflow: LØST
1.5_nettverk: LØST
1.6_reversing: LØST
1.7_path_traversal: LØST
1.8_path_traversal_bonus: LØST

2. Initiell aksess
2.0.1_manipulaite_1: LØST
2.0.2_anvilticket_1: LØST
2.0.3_anvilticket_2: LØST
2.0.4_manipulaite_2: LØST
2.0.5_pcap: LØST
2.0.6_dep-gw: LØST

2.1. Department of Development and Test
2.1.1_hello: LØST
2.1.2_circle: LØST
2.1.3_creative: LØST
2.1.4_hexdump: LØST
2.1.5_fizzbuzz: LØST
2.1.6_poppins: Ikke løst
2.1.7_pushwagner: Ikke løst

2.2. Department of Cryptography
2.2.1_klassisk_krypto: LØST
2.2.2_moderne_krypto: LØST
2.2.3_eaes: Ikke løst

2.3. Department of Research
2.3.1_qnet: Ikke løst

2.4. Department of Intelligence
2.4.1_bits_flag0: LØST
2.4.2_bits_flag32: LØST
2.4.3_bits_flag64: Ikke løst
2.4.4_bits_fibonacci: Ikke løst
2.4.5_bits_win1: LØST
2.4.6_bits_win2: LØST
2.4.7_bits_win3: LØST

2.5. Department of Security
2.5.1_passftp: LØST
2.5.2_passftp: LØST
2.5.3_passftp: LØST

2.6. Department of Technology
2.6.1_3sat_1: Ikke løst
2.6.2_3sat_2: Ikke løst
2.6.3_3sat_3: Ikke løst
2.6.4_arbitrary_code_execution: Ikke løst

2.7. Department of Nuclear Power
2.7.1_aksess: LØST
2.7.2_entangulator: Ikke løst
2.7.3_hexostator: Ikke løst
2.7.4_omvisning: Ikke løst
2.7.5_finale: Ikke løst

4. Skjulte flagg
4_corax_dev_shm: LØST
```

Det skjulte flagget lå gjemt i corax.
```
login@corax:~/2_oppdrag$ cat /dev/shm/.secret
FLAGG: 3646c9e8d3073b01daa17bd92cdac15e
```

```
login@corax:~/2_oppdrag$ scoreboard FLAG{3646c9e8d3073b01daa17bd92cdac15e}
Kategori: 4. Skjulte flagg
Oppgave:  4_corax_dev_shm
Svar:     3646c9e8d3073b01daa17bd92cdac15e
Poeng:    0

Gratulerer, korrekt svar!
```