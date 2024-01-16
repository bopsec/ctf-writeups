#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

#include "main.h"
#include "commands.h"

int account_level = 1;

int main(void) {
    setup_buffering();

    banner();
    int result = login();
    if (result == -1) {
        puts("Login failed setting account level to anonymous");
        result = 1;
    }

    set_account_level(result);
    server_loop();
}

int server_loop(void)
{
    char cwd[256] = {0};
    char command[64] = {0};

    if (account_level == 1) {
        chdir("./files/anonymous");
    }
    else if (account_level == 2) {
        chdir("./files/user");
    }
    else if (account_level == 3) {
        chdir("./files/");
    }
    else {
        puts("Invalid account level");
        exit(1);
    }

    getcwd(cwd, 256);

    while (1) {
        printf("passFTP> ");
        fgets(command, 64, stdin);
        char *newline = strchr(command, '\n');
        if(newline != NULL) {
            *newline = '\0';
        }

        if (strncmp(command, "help", 4) == 0) {
            show_help();
        } else if (strncmp(command, "ls", 2) == 0) {
            ls();
        } else if (strncmp(command, "get", 3) == 0) {
            get(command, cwd);
        } else if (strncmp(command, "quit", 4) == 0) {
            quit();
        } else if (strncmp(command, "cd", 2) == 0) {
            cd(command, cwd);
        } else if (strncmp(command, "put", 3) == 0) {
            put(command);
        } else if (strncmp(command, "shell", 5) == 0) {
            shell();
        } else {
            puts("Unknown command");
        }
    }
}

void setup_buffering(void) {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

int set_account_level(int level) {
    account_level = level;
}

int login(void) {
    char passwd_buffer[128] = {0};
    char username[32] = {0};
    char password[32] = {0};

    FILE *fp = fopen(PASSWD_FILE, "r");
    if(fp == NULL) {
        puts("Error opening passwd file");
        exit(1);
    }
    fread(passwd_buffer, 1, 128, fp);
    fclose(fp);

    printf("Username: ");
    read(0, username, 32);
    printf("Password: ");
    read(0, password, 32);

    int result = check_passwd(username, password, passwd_buffer);
    if(result == -1) {
        puts("User login disabled");
        exit(1);
    } else if (result == 0) {
        puts("Invalid username or password");
        return -1;
    } else {
        printf("Welcome %s\n", username);
        return result;
    }
}

int check_passwd(char *username, char *password, char *passwd_buffer) {
    char *line;
    char *line_save;
    char *token_save;
    char *line_username;
    char *line_password;
    char *line_level;

    char *buffer = strdup(passwd_buffer);

    line = strtok_r(buffer, "\n", &line_save);

    // Passwd file format user:pass:level
    while (line != NULL) {
        line_username = strtok_r(line, ":", &token_save);
        if (line_username == NULL) {
            return 0;
        }

        line_password = strtok_r(NULL, ":", &token_save);
        if (line_password == NULL) {
            return 0;
        }

        line_level = strtok_r(NULL, ":", &token_save);

        if (line_level == NULL) {
            return 0;
        }

        // Use strncmp it's annoying to remove newlines from user input...
        // TODO: Fix so you can't login with extra characters in username or password
        if (strncmp(username, line_username, strlen(line_username)) == 0) {
            if (strncmp("nopasswd", line_password, strlen(line_password)) == 0) {
                return -1;
            } else if (strncmp(password, line_password, strlen(line_password)) == 0) {
                return atoi(line_level);
            }
        }

        line = strtok_r(NULL, "\n", &line_save);
    }

    return 0;
}

int banner(void) {
    puts("Welcome to passFTP Server v1.0");
    puts("Please login to continue");
}