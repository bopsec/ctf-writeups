# NN Logic

Vi har blitt oppmerksom på en svakhet i det nye login-systemet til Goood Games.

Ryktet sier at de har byttet ut den klassiske login-logikken med KI, hvor det sannsynligvis finnes sårbarheter vi kan utnytte.

Vi har også fått tilgang til interne dokumenter som beskriver den nye KI-en som brukes.

Kom deg forbi login-siden som `admin` slik at vi får full tilgang til nettsiden.

https://$USERID-nn-logic.ctf.cybertalent.no

**Merk:** Du må legge til dette domenet i `/etc/hosts` før du kan få tilgang.

---

Så fra NN.pdf at man kunne trene AIen via /train/step-endepunktet\
Trente det med 1,0 -> 0 noen tusen ganger i parallell frem til riktig brukernavn og feil passord ble godkjent.\
Tok ikke mer enn et minutt, glad det ikke var noe rate limiting :P

```sh
python3 retraining.py
[*] Training (1,0) -> 1 in parallel...
  Step 100: loss = 8.287844
  Step 200: loss = 8.108612
[...]
  Step 8700: loss = 0.010582
  Step 8800: loss = 0.009542
  ✓ Converged!

[*] Attempting login as admin...
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Login Result</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="stylesheet" href="/static/style.css">
</head>
<body>

  <div class="login-wrapper">
    <main class="login-card">


        <h2 style="color: #4ade80;">✅ Login successful</h2>
        <p>Welcome, <strong>admin</strong>!</p>
        <div style="background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-top: 10px;">
           <code style="color: #fff; font-family: monospace;">42fd918e97c0c839ec8d669bd40267e3</code>
        </div>



    </main>
  </div>

</body>
</html>
```
Retraining-koden ligger i [retraining.py](retraining.py)

login@corax ~/2_oppdrag/2.4_NN_Logic $ scoreboard 42fd918e97c0c839ec8d669bd40267e3

2.4.1 NN Logic\
Velkommen tilbake, Admin!
