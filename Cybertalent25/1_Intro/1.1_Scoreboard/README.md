# Scoreboard

Gjør deg kjent med scoreboard-kommandoen.

Denne bruker du for å se oversikt over oppgaver du har låst opp og kan løse, sammen med oppgaver du allerede har løst.

For å levere flagg kjører du denne med flagget som et posisjonelt argument.

```sh
login@corax ~ $ scoreboard --help
# Lever flagg og se oversikt over løste oppgaver
#
# Usage: scoreboard [OPTIONS] [INPUT]
#
# Arguments:
#   [INPUT]  Flagg for å levere flagg, eller (blank) for å vise oversikt [default: ]
#
# Options:
#       --reset-environment  Resett miljøet ditt
#   -h, --help               Print help
#
login@corax ~ $ scoreboard
#
# 1. Grunnleggende
# 1.1. [ ] Scoreboard
# 1.2. [ ] Username
# 1.3. [ ] Discord
# 1.4. [ ] FAQ
# 1.5. [ ] SSH-tunnell
# ...
#
# 2. Oppdrag
# ...
#
# 3. Umulig
#
# 4. Skjulte flagg
#
# Du har løst 0 oppgaver og tjent opp 0 poeng.
#
login@corax ~ $ scoreboard e4d8fc322417e82764c82923b9eb4f80
#
# 1.1.1. Scoreboard
#
```

Flagg er på formatet [0-9a-f]{32} (en MD5 hash i heksadesimal) og
kan se slik ut: `e4d8fc322417e82764c82923b9eb4f80`

Prøv å lever det flagget ved å bruke scoreboard-kommandoen!

## `scoreboard --reset-environment`

Dersom du på noe tidspunkt merker at ikke alt er som det skal, kan
du resette miljøet ditt med flagget `--reset-environment`. Det vil
ta opp til 1 minutt før miljøet slettes.

```sh
login@corax ~ $ scoreboard --reset-environment
# Resetter miljøet ditt... Dette kan ta litt tid, og du vil bli nødt til å koble til med SSH igjen.
# login@corax ~ $ command terminated with exit code 137
# Connection to ctf.cybertalent.no closed.
```

Dersom du ønsker å lagre filer du har jobbet med, kan du legge de
i `/home/login/storage/` før du kjører kommandoen. Denne mappen
persisterer og vil la deg lagre inntil 2GB. Verktøy du installerer
kan f.eks. legges her.

--------------------------------------------


Flagget er e4d8fc322417e82764c82923b9eb4f80
