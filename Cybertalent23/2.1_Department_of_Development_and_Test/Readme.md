## 2.1
# 2.1.1_hello
Dette lå allerede som et eksempel i /build.
```
% STD
NEWLINE = 10
PTR = 100
PTR <- #string
loop:
    !*PTR ? NIP <- #HLT
    PRN <- *PTR
    PTR <- INC <- PTR
    NIP <- #loop
string: "MOV to the cloud!", NEWLINE, 0
```
```
login@corax:~/2_oppdrag$ scoreboard FLAG{13f3c0f0ec2d9fff223427fdc54f267c}
Kategori: 2.1. Department of Development and Test
Oppgave:  2.1.1_hello
Svar:     13f3c0f0ec2d9fff223427fdc54f267c
Poeng:    10

Godt jobbet, det kan bli viktig å lære seg hvordan bruke MOV<-16 for å komme seg igjennom infrastrukturen til Utlandia.
```

# 2.1.2_circle
Denne tok litt tid, mest fordi jeg er dårlig på testing, selve logikken var ikke så ille.\
Tok også ekstra 15 minutter fordi DBG-kallene mine gjorde så det ble skrevet for mye output\
Har prøvd å kommentere litt for å gjøre koden mer forståelig.\
Basically det koden min gjør er å lage en boks radius\*radius rundt senteret til sirkelen, deretter går den gjennom hver rute i denne boksen og sjekker om distansen til senter er mindre enn radius.
```
% RAS:0 SIM:13 ALU:1 FPU:2 MDU:3
; Read radius from the input module
; 0,0 is top left remember..
center_x: 128
center_y: 128
radius <- IDA
!radius ? radius <- #1
left_bound: 0
right_bound: 0
top_bound: 0
bottom_bound: 0
dx_sq: 0
dy_sq: 0
distance_sq: 0
radius: 0
; Clear the framebuffer - set all pixels to color 0 (black)
RAC <- #0
center_x <- #128
center_y <- #128

; Define the square region that contains the circle
FPX <- center_x
FPY <- radius
left_bound <- FDF
FPY <- center_x
FPX <- radius
right_bound <- FSM
FPX <- center_y
FPY <- radius
top_bound <- FDF
bottom_bound <- FSM
; DBG <- left_bound
; DBG <- right_bound
; DBG <- top_bound
; DBG <- bottom_bound

; Draw the circle
draw_circle:
    RAX <- left_bound
    circle_loop_x:
        RAY <- top_bound
        circle_loop_y:
            ; Calculate the distance from the center
            ALX <- RAX
            ALY <- center_x
            MUX <- DIF  ; dx = RAX - center_x
            MUY <- DIF
            dx_sq <- UPL

            ALX <- RAY
            ALY <- center_y
            MUX <- DIF  ; dy = RAY - center_y
            MUY <- DIF
            dy_sq <- UPL

            ; Sum dx^2 and dy^2
            ALX <- dx_sq
            ALY <- dy_sq
            distance_sq <- SUM

            ; Compare with radius squared
            MUX <- radius
            MUY <- radius
            ALY <- UPL    ; r^2
            ; DBG <- ALY
            ALX <- distance_sq   ; dist^2
            ; DBG <- ALX
            ULT ? RAW <- #12 ; color 12 for inside
            !ULT ? RAW <- #0  ; color 0 for outside

            ; Check if the end of Y loop is reached
            RAY <- INC <- RAY
            ALX <- RAY
            ALY <- bottom_bound
            !EQU ? NIP <- #circle_loop_y

        ; Check if the end of X loop is reached
        RAX <- INC <- RAX
        ALX <- RAX
        ALY <- right_bound
        !EQU ? NIP <- #circle_loop_x


; Output the framebuffer to the display
RAD <- #0

; Halt the program
NIP <- #HLT
```
```
login@corax:~/2_oppdrag$ scoreboard FLAG{4a48b26054d2a066991cf34435d10d5c}
Kategori: 2.1. Department of Development and Test
Oppgave:  2.1.2_circle
Svar:     4a48b26054d2a066991cf34435d10d5c
Poeng:    10

Veldig bra! MOV<-16 er en viktig del av Utlandias infrastruktur og det kan være nyttig å lære seg hvordan det fungerer.
```

# 2.1.3_creative
Latskap lenge leve. Her lå det to forskjellige bilder som eksempler i Raster-module delen av MOV16-101 Programming guide. Hver av dem alene var for simple, men å legge dem sammen var godkjent.\
Her er det fullstendige programmet jeg endte opp med, fjernet bare linjen som overskrev hele bildet i Example 2 fra Programming guide.\
Denne hadde nok ikke vært så ille å gjøre ordentlig hvis jeg hadde løst den etter 2.1.2_circle.
```
% STD RAS:0
; Start at 0,0
RAP <- #0
loop:
; Combine x and y using bitwise or
 ; and write the pixel
ALX <- RAX
ALY <- RAY
RAI <- ORR
; RAI will increment RAP, so loop until
; it reaches 0 again
RAP ? NIP <- #loop

; Set x and y to 0
RAP <- #0
; Fill the image with color 1
loop2:
; Decrement y
RAY <- DEC <- RAY
; Set x to y
RAX <- RAY
; Draw a pixel with color 2
RAW <- #2
; Invert the x coordinate and draw a
; pixel with color 3
RAX <- NOT <- RAX
RAW <- #3
; Loop until y reaches 0 again
RAY ? NIP <- #loop2
; Send the image to the monitor
RAD <- #0
; Stop
NIP <- #HLT 
; Send the image to the monitor
RAD <- #0
; Stop
NIP <- #HLT 
```
[Her er bildet haha](https://i.imgur.com/i8BTsNN.png)
```
login@corax:~$ scoreboard FLAG{1ee10ed0e76f3b55c0255e3c9ff68b83}
Kategori: 2.1. Department of Development and Test
Oppgave:  2.1.3_creative
Svar:     1ee10ed0e76f3b55c0255e3c9ff68b83
Poeng:    10

Bra jobba! Det ble et kreativt bilde!
```

# 2.1.4_hexdump
Igjen, ser ut til at det ligger et eksempel i Programming guide...
`This example reads words from the Serial Input Module and writes the words
as hexadecimal numbers to the printer.`

Manglet kun funksjonalitet for å sette space etter hver 4 letter, newline etter hvert 16 ord, pluss at eksemplet manglet D som hex char.

```
% PRI:14 SIM:13 ALU:12
cntr: 0
cntr <- #00
linecheck: 16
spacecheck: 0
spacecheck <- #16

NIP <- #loop

should_halt:
  NIP <- #print_newline
  NIP <- #HLT

print_space_or_newline:
  cntr <- INC <- cntr
  ALX <- cntr
  ALY <- linecheck
  !DIF ? NIP <- #print_newline
  DIF ? PRN <- #' '
  NIP <- #loop

print_newline:
  PRN <- #10
  cntr <- #00

loop:
; Stop if there is no more input
!ICO ? NIP <- #HLT
; Read one word into RES
RES <- IDA
; Print the 4 hex digits of RES
NIP <- #rotate_and_print_digit
NIP <- #rotate_and_print_digit
NIP <- #rotate_and_print_digit
NIP <- #rotate_and_print_digit

; Print newline and halt if we should halt
!ICO ? NIP <- #should_halt

; Print space or newline...
NIP <- #print_space_or_newline
; Jump back to loop
NIP <- #loop

rotate_and_print_digit:
; Rotate RES 4 times to the left
RES <- LRO <- LRO <- LRO <- LRO <- RES
; Add the lower 4 bits to the address of
; hex_chars and print the character
ALX <- RES
ALY <- #$000F
ALX <- AND
ALY <- #hex_chars
PRN <- *SUM
; Return to the caller
NIP <- PIP
hex_chars:
"0123456789ABCDEF" 
```

```
login@corax:~$ scoreboard FLAG{ecef83cc785dd9fd506d99c8edbb619a}
Kategori: 2.1. Department of Development and Test
Oppgave:  2.1.4_hexdump
Svar:     ecef83cc785dd9fd506d99c8edbb619a
Poeng:    10

Dette klarte du bra!
```

# 2.1.5_fizzbuzz
Her var oppgaven å lage et FizzBuzz-program ved kun å bruke MPU og printeren. Altså ingen matematiske operasjoner.\
Dette var ikke så ille når man hadde tilgang til `?`-operatoren for å sjekke om en verdi var lik null eller ikke.\
Lagde en teller som telte ned fra 3, og en annen fra 5. Hvis en av disse var 0 ble det printet enten "Fizz" og/eller "Buzz".\
\
Denne oppgaven var morsom, selv om koden er noe av det værste jeg har skrevet...\
Hvis bare PRN <- counter hadde funket så hadde dette vært en 5 minutters jobb :P\
Jaja, koden ligger [her](2_1_5_fizzbuzz.txt).\

```
login@corax:~$ scoreboard FLAG{de2ac3129aa802f2690117e8f9b30c9f}
Kategori: 2.1. Department of Development and Test
Oppgave:  2.1.5_fizzbuzz
Svar:     de2ac3129aa802f2690117e8f9b30c9f
Poeng:    10

Utmerket! Dette var ikke noe problem for deg!
```
Huff

# 2.1.6_poppins
Ikke løst.

# 2.1.7_pushwagner
Ikke løst.