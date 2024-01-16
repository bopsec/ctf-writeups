#ifndef COMMANDS_H
#define COMMANDS_H

#include "main.h"

void ls(void);
void quit(void);
void cd(char *command, char *start_dir);
void get(char *command, char *start_dir);
void put(char *command);
void show_help(void);
void shell(void);

#endif // COMMANDS_H
