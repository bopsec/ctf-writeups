# Flagle

Bare gjett flagget.

```sh
ssh play@flagle
```
---

Bare testet litt rundt, og innså at en gang iblant hvis jeg kjørte flere spill i parallell, så ville det være flere spill som hadde same flagg.\
Kjørte da bare 6 spill i parallell, og brukte resultatet fra de første 5 for hvert av gjettene i det siste.

```sh
login@corax ~/storage/2.8_Flagle $ python3 flagle.py
=== Run 0 ===
Connected 6 sessions
Session 0 got flag: c8de9fd3e85f3a082bfdc5330381a787
Session 1 got flag: 436adb3ae79d95bc75665b0f25ee06a4
Session 2 got flag: 412574427066ef126b33c911dbd86a6b
Session 3 got flag: 436adb3ae79d95bc75665b0f25ee06a4
Session 4 got flag: 436adb3ae79d95bc75665b0f25ee06a4
Session 5 got flag: c8de9fd3e85f3a082bfdc5330381a787
Got 3 unique flags
Submitting guess 1: c8de9fd3e85f3a082bfdc5330381a787
Submitting guess 2: 436adb3ae79d95bc75665b0f25ee06a4
Submitting guess 3: 412574427066ef126b33c911dbd86a6b

=== Run 1 ===
Connected 6 sessions
Session 0 got flag: 7473a860fbd22d4843d4e2f8f556b962
Session 1 got flag: af07ee152c09e0cb4f98ff4d38cd253c
Session 2 got flag: 7473a860fbd22d4843d4e2f8f556b962
Session 3 got flag: 3d1ee88cdee9add8fd805d0b44116529
Session 4 got flag: 7473a860fbd22d4843d4e2f8f556b962
Session 5 got flag: 3d1ee88cdee9add8fd805d0b44116529
Got 3 unique flags
Submitting guess 1: 7473a860fbd22d4843d4e2f8f556b962
Submitting guess 2: af07ee152c09e0cb4f98ff4d38cd253c

Game ended!
=== FLAG: 998cb4814307061b319dd166aa1c7418 ===
```


login@corax ~/storage/2.8_Flagle $ scoreboard 998cb4814307061b319dd166aa1c7418

2.8.1 Flagle
Godt gjettet!
