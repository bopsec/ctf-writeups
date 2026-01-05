#define _GNU_SOURCE
#include <string.h>
#include <sys/utsname.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdarg.h>
#include <sys/syscall.h>

static void *(*real_dlsym)(void *, const char *) = NULL;

__attribute__((constructor))
static void init() {
    real_dlsym = dlvsym(RTLD_NEXT, "dlsym", "GLIBC_2.2.5");
}

FILE *fake_fopen(const char *path, const char *mode) {
    FILE *(*orig_fopen)(const char *, const char *) = real_dlsym(RTLD_NEXT, "fopen");
    if (strcmp(path, "/etc/os-release") == 0) {
        return orig_fopen("/tmp/fake-os-release", mode);
    }
    return orig_fopen(path, mode);
}

int fake_access(const char *path, int mode) {
    if (strcmp(path, "/usr/bin/apt") == 0) return 0;
    if (strcmp(path, "/usr/bin/hollywood") == 0) return 0;
    if (strstr(path, "hollywood") != NULL) return 0;
    int (*orig_access)(const char *, int) = real_dlsym(RTLD_NEXT, "access");
    return orig_access(path, mode);
}

char *fake_getenv(const char *name) {
    char *(*orig_getenv)(const char *) = real_dlsym(RTLD_NEXT, "getenv");
    if (strcmp(name, "I_CAST") == 0) return "FIREBALL";
    return orig_getenv(name);
}

long fake_sysconf(int name) {
    if (name == 84) {
        return 6;
    }
    long (*orig_sysconf)(int) = real_dlsym(RTLD_NEXT, "sysconf");
    return orig_sysconf(name);
}

void *dlsym(void *handle, const char *symbol) {
    if (!real_dlsym) {
        real_dlsym = dlvsym(RTLD_NEXT, "dlsym", "GLIBC_2.2.5");
    }
    if (strcmp(symbol, "fopen") == 0) return (void *)fake_fopen;
    if (strcmp(symbol, "access") == 0) return (void *)fake_access;
    if (strcmp(symbol, "getenv") == 0) return (void *)fake_getenv;
    if (strcmp(symbol, "sysconf") == 0) return (void *)fake_sysconf;
    return real_dlsym(handle, symbol);
}

long syscall(long number, ...) {
    long (*orig_syscall)(long, ...) = real_dlsym(RTLD_NEXT, "syscall");
    va_list args;
    va_start(args, number);
    
    if (number == SYS_uname) {
        struct utsname *buf = va_arg(args, struct utsname *);
        va_end(args);
        long ret = orig_syscall(number, buf);
        strcpy(buf->release, "5.10.0-25-amd64");
        strcpy(buf->nodename, "AmogOS");
        return ret;
    }
    
    void *a1 = va_arg(args, void *);
    void *a2 = va_arg(args, void *);
    void *a3 = va_arg(args, void *);
    void *a4 = va_arg(args, void *);
    void *a5 = va_arg(args, void *);
    void *a6 = va_arg(args, void *);
    va_end(args);
    return orig_syscall(number, a1, a2, a3, a4, a5, a6);
}

int uname(struct utsname *buf) {
    int (*orig)(struct utsname *) = real_dlsym(RTLD_NEXT, "uname");
    int ret = orig(buf);
    strcpy(buf->release, "5.10.0-25-amd64");
    strcpy(buf->nodename, "AmogOS");
    return ret;
}

int gethostname(char *name, size_t len) {
    strncpy(name, "AmogOS", len);
    return 0;
}
