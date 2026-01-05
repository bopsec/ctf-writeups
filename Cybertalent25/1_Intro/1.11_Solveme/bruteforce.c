#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <pthread.h>

volatile int found = 0;
volatile int total_tried = 0;
char found_pw[5] = {0};
pthread_mutex_t counter_mutex = PTHREAD_MUTEX_INITIALIZER;

#define TOTAL_KEYSPACE (26 * 26 * 26 * 26)

void* search_thread(void* arg) {
    char start = *(char*)arg;
    char pw[5] = {start, 'a', 'a', 'a', 0};
    int pipe_in[2], pipe_out[2];
    
    for (pw[1] = 'a'; pw[1] <= 'z' && !found; pw[1]++) {
        for (pw[2] = 'a'; pw[2] <= 'z' && !found; pw[2]++) {
            for (pw[3] = 'a'; pw[3] <= 'z' && !found; pw[3]++) {
                if (found) return NULL;
                
                pipe(pipe_in);
                pipe(pipe_out);
                
                pid_t pid = fork();
                if (pid == 0) {
                    dup2(pipe_in[0], 0);
                    dup2(pipe_out[1], 1);
                    dup2(pipe_out[1], 2);
                    close(pipe_in[1]);
                    close(pipe_out[0]);
                    execl("./solveMe", "./solveMe", NULL);
                    _exit(1);
                }
                
                close(pipe_in[0]);
                close(pipe_out[1]);
                
                dprintf(pipe_in[1], "SuperSecretPass!\na beautiful pass\nn0PlaceLik3aH0m3\n%s\n", pw);
                close(pipe_in[1]);
                
                char buf[8192] = {0};
                int total_read = 0;
                int n;
                while ((n = read(pipe_out[0], buf + total_read, sizeof(buf) - total_read - 1)) > 0) {
                    total_read += n;
                }
                close(pipe_out[0]);
                waitpid(pid, NULL, 0);
                
                pthread_mutex_lock(&counter_mutex);
                total_tried++;
                pthread_mutex_unlock(&counter_mutex);
                
                // Find the 4th FLAG{ and check if it's followed by valid flag characters
                int count = 0;
                char *p = buf;
                char *fourth_flag = NULL;
                while ((p = strstr(p, "FLAG{")) != NULL) {
                    count++;
                    if (count == 4) {
                        fourth_flag = p;
                        break;
                    }
                    p++;
                }
                
                // Check if 4th flag exists and contains only printable ASCII (valid flag)
                if (fourth_flag != NULL) {
                    int valid = 1;
                    for (int i = 5; i < 40 && fourth_flag[i] != '}' && fourth_flag[i] != '\0'; i++) {
                        unsigned char c = fourth_flag[i];
                        // Valid flag characters: alphanumeric, underscore, common punctuation
                        if (c < 0x20 || c > 0x7e) {
                            valid = 0;
                            break;
                        }
                    }
                    if (valid && strchr(fourth_flag, '}') != NULL) {
                        found = 1;
                        strcpy(found_pw, pw);
                        printf("\nFOUND: %s\n%s\n", pw, buf);
                        return NULL;
                    }
                }
            }
        }
    }
    return NULL;
}

void* progress_thread(void* arg) {
    while (!found) {
        sleep(2);
        if (found) break;
        
        pthread_mutex_lock(&counter_mutex);
        int tried = total_tried;
        pthread_mutex_unlock(&counter_mutex);
        
        double percent = (100.0 * tried) / TOTAL_KEYSPACE;
        printf("\r[%6.2f%%] %d / %d    ", percent, tried, TOTAL_KEYSPACE);
        fflush(stdout);
    }
    return NULL;
}

int main() {
    pthread_t threads[26];
    pthread_t progress;
    char starts[26];
    
    printf("Keyspace: %d\n", TOTAL_KEYSPACE);
    
    pthread_create(&progress, NULL, progress_thread, NULL);
    
    for (int i = 0; i < 26; i++) {
        starts[i] = 'a' + i;
        pthread_create(&threads[i], NULL, search_thread, &starts[i]);
    }
    
    for (int i = 0; i < 26; i++) {
        pthread_join(threads[i], NULL);
    }
    
    found = 1;
    pthread_join(progress, NULL);
    
    return found_pw[0] ? 0 : 1;
}