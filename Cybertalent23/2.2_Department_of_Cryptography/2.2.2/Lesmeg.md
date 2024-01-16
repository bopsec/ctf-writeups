# Moderne krypto

*Office for Modern Ciphers* benytter moderne computerteknologi hvor MOV<-16 står sentralt. De har laget et program som beskytter flagget med et passord. Vi har hørt at terminalene de bruker er utdaterte og støtter bare store bokstaver, men det trenger du muligens ikke å bry deg om?

Vi har ikke fått tak i kildekoden til programmet, bare binærfila. Heldigvis har vi klart å disassemble programmet og det ser ut som koden både kompilerer og kjører fint.

``` assembly
% PRI:14 SIM:13 ALU:12
                LSH <- IDA                      ; $0000: $3FFA $3FD1
                LSH <- LSH                      ; $0002: $3FFA $3FFA
                LSH <- LSH                      ; $0004: $3FFA $3FFA
                LSH <- LSH                      ; $0006: $3FFA $3FFA
                LSH <- LSH                      ; $0008: $3FFA $3FFA
                LSH <- LSH                      ; $000A: $3FFA $3FFA
                LSH <- LSH                      ; $000C: $3FFA $3FFA
                LSH <- LSH                      ; $000E: $3FFA $3FFA
                ALX <- LSH                      ; $0010: $3FC0 $3FFA
                ALY <- IDA                      ; $0012: $3FC1 $3FD1
                L_022A <- ORR                   ; $0014: $022A $3FC8
                LSH <- IDA                      ; $0016: $3FFA $3FD1
                LSH <- LSH                      ; $0018: $3FFA $3FFA
                LSH <- LSH                      ; $001A: $3FFA $3FFA
                LSH <- LSH                      ; $001C: $3FFA $3FFA
                LSH <- LSH                      ; $001E: $3FFA $3FFA
                LSH <- LSH                      ; $0020: $3FFA $3FFA
                LSH <- LSH                      ; $0022: $3FFA $3FFA
                LSH <- LSH                      ; $0024: $3FFA $3FFA
                ALX <- LSH                      ; $0026: $3FC0 $3FFA
                ALY <- IDA                      ; $0028: $3FC1 $3FD1
                L_022B <- ORR                   ; $002A: $022B $3FC8
                LSH <- IDA                      ; $002C: $3FFA $3FD1
                LSH <- LSH                      ; $002E: $3FFA $3FFA
                LSH <- LSH                      ; $0030: $3FFA $3FFA
                LSH <- LSH                      ; $0032: $3FFA $3FFA
                LSH <- LSH                      ; $0034: $3FFA $3FFA
                LSH <- LSH                      ; $0036: $3FFA $3FFA
                LSH <- LSH                      ; $0038: $3FFA $3FFA
                LSH <- LSH                      ; $003A: $3FFA $3FFA
                ALX <- LSH                      ; $003C: $3FC0 $3FFA
                ALY <- IDA                      ; $003E: $3FC1 $3FD1
                L_022C <- ORR                   ; $0040: $022C $3FC8
                LSH <- IDA                      ; $0042: $3FFA $3FD1
                LSH <- LSH                      ; $0044: $3FFA $3FFA
                LSH <- LSH                      ; $0046: $3FFA $3FFA
                LSH <- LSH                      ; $0048: $3FFA $3FFA
                LSH <- LSH                      ; $004A: $3FFA $3FFA
                LSH <- LSH                      ; $004C: $3FFA $3FFA
                LSH <- LSH                      ; $004E: $3FFA $3FFA
                LSH <- LSH                      ; $0050: $3FFA $3FFA
                ALX <- LSH                      ; $0052: $3FC0 $3FFA
                ALY <- IDA                      ; $0054: $3FC1 $3FD1
                L_022D <- ORR                   ; $0056: $022D $3FC8
                L_00AA <- #L_00AC               ; $0058: $00AA $80AC
                L_00AB <- #$0004                ; $005A: $00AB $8004
L_005C:         STT <- L_022A                   ; $005C: $3FF3 $022A
                STT <- L_022B                   ; $005E: $3FF3 $022B
                STT <- L_022C                   ; $0060: $3FF3 $022C
                STT <- L_022D                   ; $0062: $3FF3 $022D
                NIP <- #L_00BC                  ; $0064: $3FFF $80BC
                ALX <- L_022A                   ; $0066: $3FC0 $022A
                ALY <- *L_00AA                  ; $0068: $3FC1 $40AA
                *L_00AA <- XOR                  ; $006A: $40AA $3FC9
                INC <- L_00AA                   ; $006C: $3FFD $00AA
                L_00AA <- INC                   ; $006E: $00AA $3FFD
                ALX <- L_022B                   ; $0070: $3FC0 $022B
                ALY <- *L_00AA                  ; $0072: $3FC1 $40AA
                *L_00AA <- XOR                  ; $0074: $40AA $3FC9
                INC <- L_00AA                   ; $0076: $3FFD $00AA
                L_00AA <- INC                   ; $0078: $00AA $3FFD
                ALX <- L_022C                   ; $007A: $3FC0 $022C
                ALY <- *L_00AA                  ; $007C: $3FC1 $40AA
                *L_00AA <- XOR                  ; $007E: $40AA $3FC9
                INC <- L_00AA                   ; $0080: $3FFD $00AA
                L_00AA <- INC                   ; $0082: $00AA $3FFD
                ALX <- L_022D                   ; $0084: $3FC0 $022D
                ALY <- *L_00AA                  ; $0086: $3FC1 $40AA
                *L_00AA <- XOR                  ; $0088: $40AA $3FC9
                INC <- L_00AA                   ; $008A: $3FFD $00AA
                L_00AA <- INC                   ; $008C: $00AA $3FFD
                DEC <- L_00AB                   ; $008E: $3FFE $00AB
                L_00AB <- DEC                   ; $0090: $00AB $3FFE
                L_00AB ? NIP <- #L_005C         ; $0092: $80AB $3FFF $805C
                L_00AA <- #L_00AC               ; $0095: $00AA $80AC
                L_00AB <- #$0010                ; $0097: $00AB $8010
L_0099:         PRN <- *L_00AA                  ; $0099: $3FE0 $40AA
                INC <- L_00AA                   ; $009B: $3FFD $00AA
                L_00AA <- INC                   ; $009D: $00AA $3FFD
                DEC <- L_00AB                   ; $009F: $3FFE $00AB
                L_00AB <- DEC                   ; $00A1: $00AB $3FFE
                L_00AB ? NIP <- #L_0099         ; $00A3: $80AB $3FFF $8099
                PRN <- #$000A                   ; $00A6: $3FE0 $800A
                NIP <- #HLT                     ; $00A8: $3FFF $FFFF
L_00AA:         $0000                           ; $00AA
L_00AB:         $0000                           ; $00AB
L_00AC:         $F781                           ; $00AC
                $53B0                           ; $00AD
                $9EAA                           ; $00AE
                $C15B                           ; $00AF
                $5543                           ; $00B0
                $D3EB                           ; $00B1
                $2377                           ; $00B2
                $BB85                           ; $00B3
                $A907                           ; $00B4
                $7FD3                           ; $00B5
                $DD00                           ; $00B6
                $4910                           ; $00B7
                $D03F                           ; $00B8
                $9F48                           ; $00B9
                $36B3                           ; $00BA
                $E02E                           ; $00BB
L_00BC:         L_0229 <- STT                   ; $00BC: $0229 $3FF3
                L_0228 <- STT                   ; $00BE: $0228 $3FF3
                L_0227 <- STT                   ; $00C0: $0227 $3FF3
                L_0226 <- STT                   ; $00C2: $0226 $3FF3
                STT <- PIP                      ; $00C4: $3FF3 $3FFF
                L_022A <- #$0123                ; $00C6: $022A $8123
                RRO <- #$159D                   ; $00C8: $3FFB $959D
                RRO <- RRO                      ; $00CA: $3FFB $3FFB
                L_022B <- RRO                   ; $00CC: $022B $3FFB
                RRO <- #$1357                   ; $00CE: $3FFB $9357
                L_022C <- RRO                   ; $00D0: $022C $3FFB
                L_022D <- #$CDEF                ; $00D2: $022D $CDEF
                NIP <- #L_01D4                  ; $00D4: $3FFF $81D4
                ALY <- L_0226                   ; $00D6: $3FC1 $0226
                L_022E <- SUM                   ; $00D8: $022E $3FC2
                NIP <- #L_01C6                  ; $00DA: $3FFF $81C6
                NIP <- #L_01D4                  ; $00DC: $3FFF $81D4
                ALY <- L_0227                   ; $00DE: $3FC1 $0227
                LRO <- SUM                      ; $00E0: $3FFC $3FC2
                LRO <- LRO                      ; $00E2: $3FFC $3FFC
                LRO <- LRO                      ; $00E4: $3FFC $3FFC
                L_022E <- LRO                   ; $00E6: $022E $3FFC
                NIP <- #L_01C6                  ; $00E8: $3FFF $81C6
                NIP <- #L_01D4                  ; $00EA: $3FFF $81D4
                ALY <- L_0228                   ; $00EC: $3FC1 $0228
                LRO <- SUM                      ; $00EE: $3FFC $3FC2
                LRO <- LRO                      ; $00F0: $3FFC $3FFC
                LRO <- LRO                      ; $00F2: $3FFC $3FFC
                LRO <- LRO                      ; $00F4: $3FFC $3FFC
                LRO <- LRO                      ; $00F6: $3FFC $3FFC
                LRO <- LRO                      ; $00F8: $3FFC $3FFC
                L_022E <- LRO                   ; $00FA: $022E $3FFC
                NIP <- #L_01C6                  ; $00FC: $3FFF $81C6
                NIP <- #L_01D4                  ; $00FE: $3FFF $81D4
                ALY <- L_0229                   ; $0100: $3FC1 $0229
                LRO <- SUM                      ; $0102: $3FFC $3FC2
                L_022E <- LRO                   ; $0104: $022E $3FFC
                NIP <- #L_01C6                  ; $0106: $3FFF $81C6
                NIP <- #L_01E4                  ; $0108: $3FFF $81E4
                ALY <- L_0226                   ; $010A: $3FC1 $0226
                LRO <- SUM                      ; $010C: $3FFC $3FC2
                LRO <- LRO                      ; $010E: $3FFC $3FFC
                LRO <- LRO                      ; $0110: $3FFC $3FFC
                LRO <- LRO                      ; $0112: $3FFC $3FFC
                L_022E <- LRO                   ; $0114: $022E $3FFC
                NIP <- #L_01C6                  ; $0116: $3FFF $81C6
                NIP <- #L_01E4                  ; $0118: $3FFF $81E4
                ALY <- L_0227                   ; $011A: $3FC1 $0227
                LRO <- SUM                      ; $011C: $3FFC $3FC2
                LRO <- LRO                      ; $011E: $3FFC $3FFC
                LRO <- LRO                      ; $0120: $3FFC $3FFC
                LRO <- LRO                      ; $0122: $3FFC $3FFC
                LRO <- LRO                      ; $0124: $3FFC $3FFC
                LRO <- LRO                      ; $0126: $3FFC $3FFC
                LRO <- LRO                      ; $0128: $3FFC $3FFC
                L_022E <- LRO                   ; $012A: $022E $3FFC
                NIP <- #L_01C6                  ; $012C: $3FFF $81C6
                NIP <- #L_01E4                  ; $012E: $3FFF $81E4
                ALY <- L_0228                   ; $0130: $3FC1 $0228
                LRO <- SUM                      ; $0132: $3FFC $3FC2
                LRO <- LRO                      ; $0134: $3FFC $3FFC
                L_022E <- LRO                   ; $0136: $022E $3FFC
                NIP <- #L_01C6                  ; $0138: $3FFF $81C6
                NIP <- #L_01E4                  ; $013A: $3FFF $81E4
                ALY <- L_0229                   ; $013C: $3FC1 $0229
                LRO <- SUM                      ; $013E: $3FFC $3FC2
                LRO <- LRO                      ; $0140: $3FFC $3FFC
                LRO <- LRO                      ; $0142: $3FFC $3FFC
                LRO <- LRO                      ; $0144: $3FFC $3FFC
                LRO <- LRO                      ; $0146: $3FFC $3FFC
                L_022E <- LRO                   ; $0148: $022E $3FFC
                NIP <- #L_01C6                  ; $014A: $3FFF $81C6
                NIP <- #L_01F6                  ; $014C: $3FFF $81F6
                ALY <- L_0226                   ; $014E: $3FC1 $0226
                L_022E <- SUM                   ; $0150: $022E $3FC2
                NIP <- #L_01C6                  ; $0152: $3FFF $81C6
                NIP <- #L_01F6                  ; $0154: $3FFF $81F6
                ALY <- L_0227                   ; $0156: $3FC1 $0227
                LRO <- SUM                      ; $0158: $3FFC $3FC2
                LRO <- LRO                      ; $015A: $3FFC $3FFC
                LRO <- LRO                      ; $015C: $3FFC $3FFC
                LRO <- LRO                      ; $015E: $3FFC $3FFC
                LRO <- LRO                      ; $0160: $3FFC $3FFC
                L_022E <- LRO                   ; $0162: $022E $3FFC
                NIP <- #L_01C6                  ; $0164: $3FFF $81C6
                NIP <- #L_01F6                  ; $0166: $3FFF $81F6
                ALY <- L_0228                   ; $0168: $3FC1 $0228
                LRO <- SUM                      ; $016A: $3FFC $3FC2
                LRO <- LRO                      ; $016C: $3FFC $3FFC
                L_022E <- LRO                   ; $016E: $022E $3FFC
                NIP <- #L_01C6                  ; $0170: $3FFF $81C6
                NIP <- #L_01F6                  ; $0172: $3FFF $81F6
                ALY <- L_0229                   ; $0174: $3FC1 $0229
                LRO <- SUM                      ; $0176: $3FFC $3FC2
                LRO <- LRO                      ; $0178: $3FFC $3FFC
                LRO <- LRO                      ; $017A: $3FFC $3FFC
                LRO <- LRO                      ; $017C: $3FFC $3FFC
                LRO <- LRO                      ; $017E: $3FFC $3FFC
                LRO <- LRO                      ; $0180: $3FFC $3FFC
                LRO <- LRO                      ; $0182: $3FFC $3FFC
                L_022E <- LRO                   ; $0184: $022E $3FFC
                NIP <- #L_01C6                  ; $0186: $3FFF $81C6
                NIP <- #L_020E                  ; $0188: $3FFF $820E
                ALY <- L_0226                   ; $018A: $3FC1 $0226
                LRO <- SUM                      ; $018C: $3FFC $3FC2
                LRO <- LRO                      ; $018E: $3FFC $3FFC
                LRO <- LRO                      ; $0190: $3FFC $3FFC
                LRO <- LRO                      ; $0192: $3FFC $3FFC
                L_022E <- LRO                   ; $0194: $022E $3FFC
                NIP <- #L_01C6                  ; $0196: $3FFF $81C6
                NIP <- #L_020E                  ; $0198: $3FFF $820E
                ALY <- L_0227                   ; $019A: $3FC1 $0227
                LRO <- SUM                      ; $019C: $3FFC $3FC2
                L_022E <- LRO                   ; $019E: $022E $3FFC
                NIP <- #L_01C6                  ; $01A0: $3FFF $81C6
                NIP <- #L_020E                  ; $01A2: $3FFF $820E
                ALY <- L_0228                   ; $01A4: $3FC1 $0228
                LRO <- SUM                      ; $01A6: $3FFC $3FC2
                LRO <- LRO                      ; $01A8: $3FFC $3FFC
                LRO <- LRO                      ; $01AA: $3FFC $3FFC
                LRO <- LRO                      ; $01AC: $3FFC $3FFC
                LRO <- LRO                      ; $01AE: $3FFC $3FFC
                LRO <- LRO                      ; $01B0: $3FFC $3FFC
                L_022E <- LRO                   ; $01B2: $022E $3FFC
                NIP <- #L_01C6                  ; $01B4: $3FFF $81C6
                NIP <- #L_020E                  ; $01B6: $3FFF $820E
                ALY <- L_0229                   ; $01B8: $3FC1 $0229
                LRO <- SUM                      ; $01BA: $3FFC $3FC2
                LRO <- LRO                      ; $01BC: $3FFC $3FFC
                LRO <- LRO                      ; $01BE: $3FFC $3FFC
                L_022E <- LRO                   ; $01C0: $022E $3FFC
                NIP <- #L_01C6                  ; $01C2: $3FFF $81C6
                NIP <- STT                      ; $01C4: $3FFF $3FF3
L_01C6:         L_022A <- L_022D                ; $01C6: $022A $022D
                L_022D <- L_022C                ; $01C8: $022D $022C
                L_022C <- L_022B                ; $01CA: $022C $022B
                ALX <- L_022E                   ; $01CC: $3FC0 $022E
                ALY <- L_022B                   ; $01CE: $3FC1 $022B
                L_022B <- SUM                   ; $01D0: $022B $3FC2
                NIP <- PIP                      ; $01D2: $3FFF $3FFF
L_01D4:         ALX <- L_022B                   ; $01D4: $3FC0 $022B
                ALY <- L_022C                   ; $01D6: $3FC1 $022C
                ALX <- XOR                      ; $01D8: $3FC0 $3FC9
                ALY <- L_022D                   ; $01DA: $3FC1 $022D
                ALX <- XOR                      ; $01DC: $3FC0 $3FC9
                ALY <- L_022A                   ; $01DE: $3FC1 $022A
                ALX <- SUM                      ; $01E0: $3FC0 $3FC2
                NIP <- PIP                      ; $01E2: $3FFF $3FFF
L_01E4:         ALX <- L_022B                   ; $01E4: $3FC0 $022B
                NOT <- L_022D                   ; $01E6: $3FCA $022D
                ALY <- NOT                      ; $01E8: $3FC1 $3FCA
                ALX <- ORR                      ; $01EA: $3FC0 $3FC8
                ALY <- L_022C                   ; $01EC: $3FC1 $022C
                ALX <- XOR                      ; $01EE: $3FC0 $3FC9
                ALY <- L_022A                   ; $01F0: $3FC1 $022A
                ALX <- SUM                      ; $01F2: $3FC0 $3FC2
                NIP <- PIP                      ; $01F4: $3FFF $3FFF
L_01F6:         ALX <- L_022B                   ; $01F6: $3FC0 $022B
                ALY <- L_022D                   ; $01F8: $3FC1 $022D
                STT <- AND                      ; $01FA: $3FF3 $3FC7
                ALX <- L_022C                   ; $01FC: $3FC0 $022C
                NOT <- L_022D                   ; $01FE: $3FCA $022D
                ALY <- NOT                      ; $0200: $3FC1 $3FCA
                ALX <- AND                      ; $0202: $3FC0 $3FC7
                ALY <- STT                      ; $0204: $3FC1 $3FF3
                ALX <- ORR                      ; $0206: $3FC0 $3FC8
                ALY <- L_022A                   ; $0208: $3FC1 $022A
                ALX <- SUM                      ; $020A: $3FC0 $3FC2
                NIP <- PIP                      ; $020C: $3FFF $3FFF
L_020E:         ALX <- L_022B                   ; $020E: $3FC0 $022B
                ALY <- L_022C                   ; $0210: $3FC1 $022C
                STT <- AND                      ; $0212: $3FF3 $3FC7
                NOT <- L_022B                   ; $0214: $3FCA $022B
                ALX <- NOT                      ; $0216: $3FC0 $3FCA
                ALY <- L_022D                   ; $0218: $3FC1 $022D
                ALX <- AND                      ; $021A: $3FC0 $3FC7
                ALY <- STT                      ; $021C: $3FC1 $3FF3
                ALX <- ORR                      ; $021E: $3FC0 $3FC8
                ALY <- L_022A                   ; $0220: $3FC1 $022A
                ALX <- SUM                      ; $0222: $3FC0 $3FC2
                NIP <- PIP                      ; $0224: $3FFF $3FFF
L_0226:         $0000                           ; $0226
L_0227:         $0000                           ; $0227
L_0228:         $0000                           ; $0228
L_0229:         $0000                           ; $0229
L_022A:         $0000                           ; $022A
L_022B:         $0000                           ; $022B
L_022C:         $0000                           ; $022C
L_022D:         $0000                           ; $022D
L_022E:         $0000                           ; $022E
```