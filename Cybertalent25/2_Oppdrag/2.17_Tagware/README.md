# Tagware

Det er blitt oppdaget en mistenkelig binærfil i forbindelse med et av spillene til Gooodgames.

Klarer du å finne ut av hva det gjør?

---

Hva koden gjør\
awbvck() - Henter MAC-adresse fra nettverksgrensesnitt, hasher den med FNV-1a\
kcsown() - FNV-1a hash-funksjon (0xcbf29ce484222325 og 0x100000001b3)\
jkdewc() - XOR-dekrypterer kommandoen med hashen og kjører:
```c
int fd = socket(AF_INET, SOCK_DGRAM, 0);
for iface in ["eth0","enp0s3","wlan0","wlp2s0"]:
    strncpy(ifr.ifr_name, iface, 0x10);
    if (ioctl(fd, 0x8927, &ifr) == 0)  // SIOCGIFHWADDR
        memcpy(mac, ifr.ifr_hwaddr.sa_data, 6);
```
Deretter bygges buffer:\
buf = MAC[0..5] || 0x00 || 0x00   // 8 bytes

Identifiser hashfunksjon (kcsown):
```c
uint64_t h = 0xcbf29ce484222325;
for each byte b:
    h ^= b;
    h *= 0x100000001b3;
return h;
```
Dette er FNV-1A 64-bit.\
Så key = FNV1A64( MAC || 00 00 )

Symbol-dekryptering
```c
sym = decrypt_string(enc_sym, key);
handle = dlopen(NULL, 0x101);
fn = dlsym(handle, sym);
if (fn) fn();
```

Dekryptering:\
`out[i] = enc[i] ^ ((key >> ((i & 7)*8)) & 0xff)`

-> XOR med 8-bytes nøkkel, roterende.\
Når man dekrypterer strengene finner man:\
Riktig dekryptert symbol = "jkdewc"\
Men kun når uVar1 = 0x42352bac644a\
Dette er derimot ikke hele MACen fordi "jkdewc" er for kort.\
Koden jeg brukte for å finne denne delen av uVar1 kan finnes i [getMacFromJkdewc.py](getMacFromJkdewc.py).

jkdewc() dekrypterer ny streng med samme XOR-mekanisme og kjører:\
system(<dekryptert>)


Kjører litt testing med uVar1 = 0x42352bac644a mot enc_cmd og ser at det ser ut til at den vil kjøre\
`echo [base64] >> ~/.ssh/authorized_keys` 

Fortsetter med denne antagelsen, og leter etter /.ssh/authorized_keys på bruteforce
```sh
KEY: 4a64ac2b3542ebc9
b'echo c3d8379394a4a1924348c2a4e5cabdb9 >> ~/.ssh/authorized_keys'
```

login@corax ~/storage $ scoreboard c3d8379394a4a1924348c2a4e5cabdb9

2.17.1 Tagware\
Godt jobbet! De prøver altså å skaffe persistens på spesifikke maskiner...
