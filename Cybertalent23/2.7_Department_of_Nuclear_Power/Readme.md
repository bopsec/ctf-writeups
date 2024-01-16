# 2.7_Department_of_Nuclear_Power

## 2.7.1_aksess
Denne var ikke spesielt vanskelig med [ACCESS16 User Manual](2.7.1/ACCESS16%20User%20Manual.pdf).\
Åpnet hexedit av access16_update.bin og sjekket hvor forskjellige ting ble endret, så at det var noen deler for å sette PIN, noen deler for å fjerne access og en for å gi access. Bare la til 05199377 i sett-PIN-delen. Og la til 0519FFFF i gi access for å sette access til alle dører.\
```
Status Code: 200
Response JSON:
{'flag': 'FLAG{6b2809f4e7f618d2b2581900d5871dca}', 'printer_output': 'ADIAMAAyADQALQAwADEALQAxADEAIAAxADAAOgAwADAAOgAwADAAIABTAHQAYQByAHQAaQBuAGcAIABBAEMAQwBFAFMAUwAxADYAIAB2ADEALgA2AAoAMgAwADIANAAtADAAMQAtADEAMQAgADEAMAA6ADAAMAA6ADAAMAAgAEQAbwBvAHIAIABBACAAQwBhAHIAZAAgADUAMgA4ADoAIABJAG4AdgBhAGwAaQBkACAAUABJAE4ACgAyADAAMgA0AC0AMAAxAC0AMQAxACAAMQAwADoAMAAwADoAMQAzACAARABvAG8AcgAgAEEAIABDAGEAcgBkACAAMgAzADMAOgAgAEQAbwBvAHIAIABvAHAAZQBuAGUAZAAKADIAMAAyADQALQAwADEALQAx[......]
```
```
login@corax:~/2_oppdrag/7_department_of_nuclear_power/1_aksess$ scoreboard FLAG{6b2809f4e7f618d2b2581900d5871dca}
Kategori: 2.7. Department of Nuclear Power
Oppgave:  2.7.1_aksess
Svar:     6b2809f4e7f618d2b2581900d5871dca
Poeng:    10

Veldig bra! Vi har fått beskjed om at agenten har kommet seg inn lagerbygget og fått tak i entangulatoren.

Ny fil: /home/login/2_oppdrag/7_department_of_nuclear_power/2_entangulator/LESMEG.md
```

## 2.7.2_entangulator

## 2.7.3_hexostator

## 2.7.4_omvisning

## 2.7.5_finale