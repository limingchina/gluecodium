#define _DEFAULT_SOURCE
#define _POSIX_C_SOURCE 200809L
#include <errno.h>
#include <fcntl.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/resource.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <time.h>
#include <unistd.h>

static volatile sig_atomic_t child = -1;
static volatile sig_atomic_t expired = 0;
static void timeout_handler(int sig) {
    (void)sig;
    expired = 1;
    if (child > 0) kill(-(pid_t)child, SIGKILL);
}
int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: supervisor SECONDS LOG COMMAND [ARG...]\n"); return 2; }
    char *end; long seconds = strtol(argv[1], &end, 10);
    if (*end || seconds < 1) return 2;
    int log = open(argv[2], O_WRONLY | O_CREAT | O_TRUNC, 0600);
    if (log < 0) { perror("open log"); return 2; }
    struct sigaction action = {0}; action.sa_handler = timeout_handler; sigemptyset(&action.sa_mask);
    if (sigaction(SIGALRM, &action, NULL) != 0) return 2;
    struct timespec start, finish;
    if (clock_gettime(CLOCK_MONOTONIC, &start) != 0) return 2;
    pid_t pid = fork();
    if (pid < 0) { perror("fork"); return 2; }
    if (pid == 0) {
        setpgid(0, 0);
        if (dup2(log, 1) < 0 || dup2(log, 2) < 0) _exit(126);
        close(log); execv(argv[3], argv + 3); perror("execv"); _exit(127);
    }
    child = pid; setpgid(pid, pid); close(log);
    struct itimerval timer = {0}; timer.it_value.tv_sec = seconds;
    if (setitimer(ITIMER_REAL, &timer, NULL) != 0) { kill(-pid, SIGKILL); return 2; }
    int status; struct rusage usage;
    while (wait4(pid, &status, 0, &usage) < 0) { if (errno != EINTR) { perror("wait4"); return 2; } }
    sigset_t blocked; sigemptyset(&blocked); sigaddset(&blocked, SIGALRM);
    sigprocmask(SIG_BLOCK, &blocked, NULL);
    struct itimerval disarm = {0}; setitimer(ITIMER_REAL, &disarm, NULL);
    clock_gettime(CLOCK_MONOTONIC, &finish);
    double wall = (finish.tv_sec-start.tv_sec) + (finish.tv_nsec-start.tv_nsec)/1e9;
    double user = usage.ru_utime.tv_sec + usage.ru_utime.tv_usec/1e6;
    double system = usage.ru_stime.tv_sec + usage.ru_stime.tv_usec/1e6;
    int code = WIFEXITED(status) ? WEXITSTATUS(status) : -WTERMSIG(status);
    printf("{\"wall_seconds\":%.9f,\"user_seconds\":%.6f,\"system_seconds\":%.6f,\"peak_rss_kib\":%ld,\"exit_code\":%d,\"timeout\":%s}\n", wall, user, system, usage.ru_maxrss, code, expired ? "true" : "false");
    return 0;
}
