# Pet gallery

Vi har informasjon om at visse dyr i Pet Gallery kan gi oss nøkkelinformasjon.
Kan du hjelpe oss med å få tilgang til de nødvendige bildene?

https://pet-gallery.ctf.cybertalent.no

---

Ganske rett frem, hvis base64 av bildenavnet inneholder substrengen "DeW" så vil bildet ikke vises på nettsiden og heller byttes ut med "Forbidden".\
Neon Cyber Cat var bildet som viste forbidden, sjekket base64 av navnet, og så at det inneholdt "DeW".\
Prøvde lowercase "neon cyber cat" b64 "bmVvbiBjeWJlciBjYXQ=", inneholder ikke DeW, og ga flagget.


![neon-cyber-cat.png](neon-cyber-cat.png)

Flagget er 37396e8b6cc51a0b54c94ebf4144bfa5.
