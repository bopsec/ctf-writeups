#ifndef MAIN_H
#define MAIN_H

#define _GNU_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#define PASSWD_FILE "passwd.txt"

extern int account_level;

void setup_buffering(void);
int banner(void);
int login(void);
int check_passwd(char *username, char *password, char *passwd_buffer);
int server_loop(void);
int set_account_level(int level);

#endif // MAIN_H
