# Legend of Vexillum

Vi har funnet et spill laget av en utvikler som nå jobber i GooodGames. Vedlagt er en forumpost, en manual for spillet og selve spillet.

I følge forumposten er sikkerheten på spillet dårlig implementert. Siden utvikleren nå jobber i GooodGames er det mulig at de har implementert noe liknende.

1. Last ned spillet
2. Kjør spillet med `./game legend-of-vexillum.ctf.cybertalent.no 2000`
3. Finn ut av hvordan sikkerheten til spillet er sårbar og vis at denne kan utnyttes ved å komme til siste rom i spillet

NB: Oppgaven kan ikke løses fra corax.
NB: Dersom du spiller og vinner spillet får du et annet flagg.

---

Testet litt manuelt før jeg skrev en BFS i python, trengte ikke kjøre hele BFS før jeg fant flagget

```
[...]
Exploring: bright_room
    Response: SECRET:{'rooms': {}, 'items': {'coiled rod': <__main__.Item object at 0x7f424e6290f0>}};You are in a small bright room. The light is so strong it's impossible to make out anything. There is a hallway behind you, and a door to your right. In the room there is a bright spark....


Exploring: central_hall
    Response: SECRET:{'rooms': {'eye opening': 'eye_room'}, 'items': {}};You are in a massive central hall, the walls are covered in strange symbols that are pulsating alongside something on a platform above. There is a passageway behind you and a door ahead of you. In the room there is a steel slates, an oozing liquid, and an armor....


Exploring: eye_room
    Response: You are in a small, dark room. The only light comes from above, through the ceiling you can see dcee2dbef8ad3dc077ba21dacafb9a97...
```
Koden kan finnes i [solve.py](solve.py)


Flagget er dcee2dbef8ad3dc077ba21dacafb9a97

Her var det tydeligvis et flagg til, som nevnt i oppgaveteksten, men jeg fant det ikke. Det var også tydeligvis ikke løselig tidlig i konkurransen, så er fullt mulig jeg prøvde før dette ble fikset.