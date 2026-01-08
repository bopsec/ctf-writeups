# SolveMe

Finn passordene for å dekryptere flaggene


---

# 1.
```
/1_Intro/1.11$ strings solveme -n 10
[...]
SuperSecretPass!
You made it! Here is your prize:
What a beautiful password you have chosen for yourself!
Here is your prize:
Do you always remember all your passwords that well?
Do not waste my time!
Please try again...
If there is no flag, the password might be wrong.. Try again!
Invalid character detected!
Is there a prize here?
Enter your first password, please:
Enter your second password, please:
Enter your third password, please:
Enter your fourth password, please:
_GLOBAL__sub_I_flag1
_Z14checkPassword3NSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
_Z14checkPassword4NSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
_Z14checkPassword2NSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
_Z14checkPassword1NSt7__cxx1112basic_stringIcSt11char_traitsIcESaIcEEE
[...]
```

Fant "SuperSecretPass!". \
Testet på pass 1, funket

```sh
Enter your first password, please: SuperSecretPass!

You made it! Here is your prize:
FLAG{Strings_are_all_you_need}
```
Solveme 1: FLAG{Strings_are_all_you_need}

---

# 2. 
Sjekket litt i gdb, fant substring som startet fra 5, sjekket i ghidra disassemble og fant
```c
  std::__cxx11::string::string<>
            (local_a8,"What a beautiful password you have chosen for yourself!",&local_b1)

for (local_b0 = 0; local_b0 < 0x10; local_b0 = local_b0 + 1) {
    pcVar2 = (char *)std::__cxx11::string::operator[]((ulong)param_1);
    cVar1 = *pcVar2;
    pcVar2 = (char *)std::__cxx11::string::operator[]((ulong)local_a8);
    if (cVar1 != *pcVar2) {
        exit(1);
    }
}
```
len 0x10 (16)\
Starter fra index 5 i strengen `What a beautiful password you have chosen for yourself!`\
-> a beautiful pass

```
Enter your second password, please: a beautiful pass
What a beautiful password you have chosen for yourself!

Here is your prize:
FLAG{Start_the_day_on_the_right_offset}
```
Solveme 2: FLAG{Start_the_day_on_the_right_offset}

---
# 3. 
```c
  lVar3 = std::__cxx11::string::length();
  if (lVar3 != 0x10) {
                    /* try { // try from 00103024 to 00103289 has its CatchHandler @ 00103444 */
    poVar4 = std::operator<<((ostream *)std::cout,"Do not waste my time!");
    std::ostream::operator<<(poVar4,std::endl<>);
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
```
Length 16

```c
local_c8[0] = -0x708baa70;   // = 0x8f745590
local_c8[1] = 0x6b838889;
local_c8[2] = 0x8c5d8485;
local_c8[3] = 0x6283616a;

local_e8 = 0;
for (local_e4 = 0; local_e4 < 4; local_e4 = local_e4 + 1) {
    local_dc = local_e8 * 0x1010101 + 0x10203;
    local_e8 = local_e8 + 4;
    if (local_c8[local_e4] != (local_dc ^ *(uint *)(local_d0 + (long)local_e4 * 4)) + 0x23232323) {
        // fail
    }
}
```
i=0: local_e8=0, counter = 0 * 0x1010101 + 0x10203 = 0x00010203\
i=1: local_e8=4, counter = 4 * 0x1010101 + 0x10203 = 0x04050607\
i=2: local_e8=8, counter = 8 * 0x1010101 + 0x10203 = 0x08090a0b\
i=3: local_e8=12, counter = 12 * 0x1010101 + 0x10203 = 0x0c0d0e0f

Sjekken er: hardcoded == (counter ^ input) + 0x23232323

```py
hardcoded = [0x8f745590, 0x6b838889, 0x8c5d8485, 0x6283616a]
counters = [0x00010203, 0x04050607, 0x08090a0b, 0x0c0d0e0f]

password = b""
for i in range(4):
    val = (hardcoded[i] - 0x23232323) & 0xFFFFFFFF
    val ^= counters[i]
    password += val.to_bytes(4, 'little')

print(password)
```
Koden er også i flag3.py
```sh
python3 flag3.py
b'n0PlaceLik3aH0m3'
```
```
Enter your third password, please: n0PlaceLik3aH0m3
Do you always remember all your passwords that well?

Here is your prize:
FLAG{Don't_get_lost_on_your_way_home}
```

Solveme 3: FLAG{Don't_get_lost_on_your_way_home}

---
# 4.

```asm
cmp    $0x4,%rax      ; lengdesjekk på 4 chars
...
cmp    $0x7a,%al      ; sammenlign med 'z' (122)
jg     ...            ; feil hvis > 'z'
...
cmp    $0x60,%al      ; sammenlign med '`' (96)
jg     ...            ; OK hvis > '`' (altså >= 'a')
```

Mellom lowercase a og lowercase z

Finner ingenting mer angående hva som inneholder i passordet, annet enn at det blir konkatenert sammen 4 ganger.
Altså passordet abcd -> faktisk key er abcdabcdabcdabcd.

Siden keyspace er såpass lite kan jeg bare bruteforce det, 26^4 = 456976 muligheter

```sh
./bruteforce
Keyspace: 456976
[  4.95%] 22620 / 456976
FOUND: qbit
```
Koden kan finnes i [bruteforce.c](bruteforce.c).
```
Enter your first password, please:
You made it! Here is your prize:
FLAG{Strings_are_all_you_need}
Enter your second password, please: What a beautiful password you have chosen for yourself!

Here is your prize:
FLAG{Start_the_day_on_the_right_offset}
Enter your third password, please: Do you always remember all your passwords that well?

Here is your prize:
FLAG{Don't_get_lost_on_your_way_home}
Enter your fourth password, please: If there is no flag, the password might be wrong.. Try again!

Is there a prize here?
FLAG{Brutus_doesnt_remember_passwords}
```

Solveme 4: FLAG{Brutus_doesnt_remember_passwords}

---
# Bonus

Mens jeg lette etter de andre flaggene under dynamisk analyse, la jeg merke til at flagstrengen var lenger enn det som ble printet. \
Etter hvert flagg fant jeg dette:\
FLAG{Strings_are_all_you_need}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;FLAG{A_sparkling_hidden_gem} 	(flag1 + bonus flagg)\
FLAG{Start_the_day_on_the_right_offset}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Life is full of paths. (flag2 + bonus text)\
FLAG{Don't_get_lost_on_your_way_home}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Sometimes you dont know  (flag3 + bonus text)\
FLAG{Brutus_doesnt_remember_passwords}&nbsp;&nbsp;that you missed something.(flag4 + bonus text)

Solveme bonus: FLAG{A_sparkling_hidden_gem}
