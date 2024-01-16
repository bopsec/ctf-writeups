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

passFTP> get commands.c
Downloading file commands.c
#include "commands.h"

extern int account_level;

void ls(void) {
    system("ls -l");
}

void quit(void) {
    puts("Goodbye");
    exit(0);
}

void cd(char *command, char *start_dir) {
    if(strlen(command) < 4) {
        puts("Usage: cd <directory>");
        return;
    }

    char *target_dir = command + 3;

    char new_dir[512] = {0};
    snprintf(new_dir, 511, "%s", target_dir);

    if(realpath(new_dir, new_dir) == NULL) {
        puts("Invalid directory");
        return;
    }

    // If we try to go higher than the start directory we don't allow it
    if(strncmp(new_dir, start_dir, strlen(start_dir)) != 0) {
        puts("Not allowed to go higher than start directory");
        return;
    }

    // Check for a file called .pass in the directory if it's there read the password and promt for it
    char pass_file[512] = {0};
    snprintf(pass_file, 511, "%s/.pass", new_dir);
    FILE *fp = fopen(pass_file, "r");
    if(fp != NULL) {
        char password[32] = {0};
        puts("Password protected directory");
        printf("Password: ");
        read(0, password, 32);
        char buffer[32] = {0};
        fread(buffer, 1, 32, fp);
        fclose(fp);
        if(strncmp(password, buffer, 32) != 0) {
            puts("Invalid password");
            return;
        }
    }

    printf("Changing directory to %s\n", target_dir);
    chdir(new_dir);
}

void get(char *command, char *start_dir)
{
    if(strlen(command) < 5) {
        puts("Usage: get <filename>");
        return;
    }

    char *filename = command + 4;

    char full_path[512] = {0};
    snprintf(full_path, 511, "%s", filename);

    if(realpath(full_path, full_path) == NULL) {
        puts("Invalid filename");
        return;
    }

    // If we try to go higher than the start directory we don't allow it
    if(strncmp(full_path, start_dir, strlen(start_dir)) != 0) {
        puts("Not allowed to go higher than start directory");
        return;
    }

    printf("Downloading file %s\n", filename);
    FILE *fp = fopen(full_path, "r");
    if(fp == NULL) {
        puts("Error opening file");
        return;
    }

    char buffer[512] = {0};
    size_t bytesRead;
    while((bytesRead = fread(buffer, 1, 511, fp)) > 0) {
        write(1, buffer, bytesRead);
        memset(buffer, 0, 512);
    }

    fclose(fp);
    putchar('\n');
}

void put(char *command)
{
    char buffer[512] = {0};
    if(account_level < 2) {
        puts("Anonymous users can't upload files");
        return;
    }

    if(strlen(command) < 5) {
        puts("Usage: put <filename>");
        return;
    }

    char *filename = command + 4;

    if(strpbrk(filename, "/.~*") != NULL) {
        puts("Invalid filename");
        return;
    }

    printf("Uploading file %s\nEnter Data: \n", filename);
    gets(buffer);

    FILE *fp = fopen(filename, "w+");
    if(fp == NULL) {
        puts("Error opening file");
        return;
    }

    fwrite(buffer, 1, strlen(buffer), fp);
    fclose(fp);
}

void shell() {
    if(account_level < 3) {
        puts("Only admins can spawn a shell");
        return;
    }
    puts("Spawning shell");
    execve("/bin/bash", NULL, NULL);
}

void show_help(void) {
    puts("Commands:");
    puts("help  - Show this help");
    puts("ls    - List files in current directory");
    puts("get   - Download a file");
    puts("put   - Upload a file");
    puts("quit  - Exit the program");
}