#define __USE_GNU 1
#include <sys/ucontext.h>

#include <stdlib.h>
#include <stdio.h>
#include <signal.h>

void brek(int si, siginfo_t * sif, ucontext_t * vo) {
  printf("[*] Signal %d", si);
#define r(I,X) printf("\n\t" #X "\t%16llx", vo->uc_mcontext.gregs[I]);
  r(13,rax) r(11,rbx) r(14,rcx) r(12,rdx) r(9,rsi)  r(8,rdi) r(10,rbp) r(15,rsp) 
  r(0,r8) r(1,r9) r(2,r10) r(3,r11) r(4,r12) r(5,r13) r(6,r14) r(7,r15) 
  r(16,rip) r(17,efl) r(18,csgsfs) r(19,err) r(20,trapno) r(21,oldmask) r(22,cr2)
#undef r
  puts(" -- Aborting.");
  fflush(stdout);
  sleep(1);
  _exit(si);
}

__attribute__((constructor)) void brek_on() {
  static char stack[16384];
  stack_t ss = {
    .ss_sp = stack,
    .ss_size = sizeof(stack),
  };
  sigaltstack(&ss, 0);
  for (int i=0; i<100; i++) {
    if (i == SIGCHLD) continue;
    struct sigaction act = {};
    act.sa_sigaction = (void*)brek;
    act.sa_flags = SA_ONSTACK | SA_SIGINFO;    
    sigaction(i, &act, 0);
  }
}
