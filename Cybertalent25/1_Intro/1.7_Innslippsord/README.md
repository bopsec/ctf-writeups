# Innslippsord

Finner du ordet?

--------------------------------------------
Gjorde litt dynamisk analyse før jeg bare gjorde objdump\
Fant ut at det funket slik (se kommentarer)
```sh
00000000000011fe <check_pw>:
[...]
    121b:       31 c0                   xor    %eax,%eax
    121d:       48 b8 b5 48 17 2f b2    movabs $0xa3555b22f1748b5,%rax // xor p1
    1224:       55 35 0a
    1227:       48 ba 30 80 c9 ba 01    movabs $0x4030201bac98030,%rdx // xor p2
    122e:       02 03 04
    1231:       48 89 45 b0             mov    %rax,-0x50(%rbp)
    1235:       48 89 55 b8             mov    %rdx,-0x48(%rbp)
    1239:       48 b8 05 06 07 08 09    movabs $0xc0b0a0908070605,%rax // xor p3
    1240:       0a 0b 0c
    1243:       48 ba 0d 0e 0f 10 11    movabs $0x14131211100f0e0d,%rdx // xor p4
    124a:       12 13 14
    124d:       48 89 45 c0             mov    %rax,-0x40(%rbp)
    1251:       48 89 55 c8             mov    %rdx,-0x38(%rbp)
    1255:       48 b8 09 f9 79 f1 90    movabs $0x3a2a1890f179f909,%rax // enc 1
    125c:       18 2a 3a
    125f:       48 ba 04 ce ff fd 66    movabs $0x309ad966fdffce04,%rdx // enc 2
    1266:       d9 9a 30
    1269:       48 89 45 d0             mov    %rax,-0x30(%rbp)
    126d:       48 89 55 d8             mov    %rdx,-0x28(%rbp)
    1271:       48 b8 cc fc 23 e3 4d    movabs $0x3cb79b4de323fccc,%rax // enc 3
    1278:       9b b7 3c
    127b:       48 ba 6a e0 63 52 84    movabs $0x27921d845263e06a,%rdx // enc 4
    1282:       1d 92 27
    1285:       48 89 45 e0             mov    %rax,-0x20(%rbp)
[...]
```

```sh
python3 1.7.py
Passord: 168065a0236e2e64c9c6cdd086c55f63
```
Koden kan finnes i [1.7.py](1.7.py)
```sh
login@corax ~/1_grunnleggende/1.7_Innslippsord $ ./innslippsord
=== Password Checker ===
System Ready.
Please enter password:
> 168065a0236e2e64c9c6cdd086c55f63
Correct password!
Flag = Password
```

Flagget er 168065a0236e2e64c9c6cdd086c55f63