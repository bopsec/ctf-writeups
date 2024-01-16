CC = gcc

all: passFTP

passFTP: main.c commands.c
        mkdir -p bin
        $(CC) -static -fno-stack-protector -no-pie -o ./bin/passFTP main.c commands.c

