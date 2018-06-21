#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>          /* See NOTES */
#include <sys/socket.h>
#include <arpa/inet.h>
#include <strings.h>
#include <string.h>
#include <unistd.h>
#include <signal.h>
#include <errno.h>
#include <dirent.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <time.h>
#include <seccomp.h>

#define BUFSIZE 4096
#define MAXFILES 40

/*
 * error - wrapper for perror used for bad syscalls
 */
void error(char *msg) {
  perror(msg);
  exit(1);
}

int randomFile(char * path) {
  DIR * dirp;
  struct dirent * entry;
  char files[MAXFILES][256];
  int file;
  int result;
  int file_count = 0;
  int dirfd;
  dirfd = open(path, O_RDONLY);
  dirp = fdopendir(dirfd);
  if (dirp == NULL) {
    error("Cannot open directory");
  }
  while ((entry = readdir(dirp)) != NULL) {
    if (entry->d_type == DT_REG) { /* If the entry is a regular file */
     file_count++;
     strncpy(files[file_count-1], entry->d_name, 256);
    }
  }
  srand(time(NULL));
  file = rand()%file_count;
  result = openat(dirfd, files[file], O_RDONLY);
  closedir(dirp);
  return result;
}




/* http://man7.org/tlpi/code/online/dist/sockets/read_line.c.html
  Read characters from 'fd' until a newline is encountered. If a newline
  character is not encountered in the first (n - 1) bytes, then the excess
  characters are discarded. The returned string placed in 'buf' is
  null-terminated and includes the newline character if it was read in the
  first (n - 1) bytes. The function return value is the number of bytes
  placed in buffer (which includes the newline character if encountered,
  but excludes the terminating null byte). */

ssize_t
readLine(int fd, void *buffer, size_t n)
{
    ssize_t numRead;                    /* # of bytes fetched by last read() */
    size_t totRead;                     /* Total bytes read so far */
    char *buf;
    char ch;

    if (n <= 0 || buffer == NULL) {
        errno = EINVAL;
        return -1;
    }

    buf = buffer;                       /* No pointer arithmetic on "void *" */

    totRead = 0;
    for (;;) {
        numRead = read(fd, &ch, 1);

        if (numRead == -1) {
            if (errno == EINTR)         /* Interrupted --> restart read() */
                continue;
            else
                return -1;              /* Some other error */

        } else if (numRead == 0) {      /* EOF */
            if (totRead == 0)           /* No bytes read; return 0 */
                return 0;
            else                        /* Some bytes read; add '\0' */
                break;

        } else {                        /* 'numRead' must be 1 if we get here */
            if (totRead < n - 1) {      /* Discard > (n - 1) bytes */
                totRead++;
                *buf++ = ch;
            }

            if (ch == '\n')
                break;
        }
    }

    *buf = '\0';
    return totRead;
}


int setup_seccomp() {
    scmp_filter_ctx ctx;
    ctx = seccomp_init(SCMP_ACT_KILL);
    int calls[] = {SCMP_SYS(close),    SCMP_SYS(read),      SCMP_SYS(write),
                   SCMP_SYS(open),     SCMP_SYS(fstat),     SCMP_SYS(fcntl),
                   SCMP_SYS(brk),      SCMP_SYS(getdents),  SCMP_SYS(openat),
                   SCMP_SYS(shutdown), SCMP_SYS(exit_group)};
    int calls_length = sizeof(calls) / sizeof(calls[0]);
    int i;

    if (ctx == NULL) {
        return -1;
    }

    for (i = 0; i < calls_length; i++) {
        if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, calls[i], 0) < 0) {
            seccomp_release(ctx);
            fprintf(stderr, "adding rule %d failed \n", i);
            return -1;
        }
    }

    if (seccomp_load(ctx) < 0) {
        seccomp_release(ctx);
        fprintf(stderr, "loading seccomp failed\n");
        return -1;
    }
    return 0;
}


void process(int fd, struct sockaddr_in *clientaddr){
  char buf[BUFSIZE];
  const char * randomcatrequest = "GET /randomcat ";
  const char * hellorequest = "GET / ";
  const char * helloresponse = "HTTP/1.0 200 OK\r\nContent-Type: text/html\r\nConnection: close\r\n\r\nRandom cat image server!";
  const char * randomcatresponse = "HTTP/1.0 200 OK\r\nContent-Type: image/jpeg\r\nConnection: close\r\n\r\n";
  const char * notfound = "HTTP/1.0 404 Not Found\r\nConnection: close\r\n\r\n";
  int filefd;
  ssize_t length;

  // Add Seccomp rules
  if (setup_seccomp() == -1){
    error("Failed to add seccomp rules");
  }
    
  
  length = readLine(fd, buf, BUFSIZE);
  if (length <= 0) {
    error("Failed to read request");
  }
  if (strncmp(buf, hellorequest, strlen(hellorequest)) == 0) {
    write(fd, helloresponse, strlen(helloresponse));
  } else if (strncmp(buf, randomcatrequest, strlen(randomcatrequest)) == 0) {
    printf("Random cat\n");
    write(fd, randomcatresponse, strlen(randomcatresponse));
    filefd = randomFile("images");
    if (filefd < 0) {
      error("Cannot open file");
    }
    int bytesRead = read(filefd, buf, BUFSIZE);
    while (bytesRead > 0) {
      write(fd, buf, bytesRead);
      bytesRead = read(filefd, buf, BUFSIZE);
    }
  } else {
    write(fd, notfound, strlen(notfound));
  }
  shutdown(fd, SHUT_WR);
  close(fd);
  return;
}

int main(int argc, char** argv) {
  int parentfd;          /* parent socket */
  int childfd;           /* child socket */
  struct sockaddr_in serveraddr; /* server's addr */
  struct sockaddr_in clientaddr; /* client addr */
  socklen_t clientlen;         /* byte size of client's address */
  int optval;            /* flag value for setsockopt */
  pid_t pid;

  if (signal(SIGCHLD, SIG_IGN) == SIG_ERR) {
    perror(0);
    exit(1);
  }

  //srand(time(NULL));


  /* open socket descriptor */
  parentfd = socket(AF_INET, SOCK_STREAM, 0);
  if (parentfd < 0)
    error("ERROR opening socket");

  /* allows us to restart server immediately */
  optval = 1;
  setsockopt(parentfd, SOL_SOCKET, SO_REUSEADDR,
       (const void *)&optval , sizeof(int));

  /* bind port to socket */
  bzero((char *) &serveraddr, sizeof(serveraddr));
  serveraddr.sin_family = AF_INET;
  serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
  serveraddr.sin_port = htons((unsigned short)5000);
  if (bind(parentfd, (struct sockaddr *) &serveraddr,
     sizeof(serveraddr)) < 0)
    error("ERROR on binding");

  /* get us ready to accept connection requests */
  if (listen(parentfd, 5) < 0) /* allow 5 requests to queue up */
    error("ERROR on listen");

  /*
   * main loop: wait for a connection request, parse HTTP,
   * serve requested content, close connection.
   */
  clientlen = sizeof(clientaddr);
  while (1) {
    /* wait for a connection request */
    childfd = accept(parentfd, (struct sockaddr *) &clientaddr, &clientlen);
    printf("New connection: %d\n", childfd);
    if (childfd < 0)
      error("ERROR on accept");
    pid = fork();
    if (pid < 0) {
      error("Cannot fork");
    }
    if (pid == 0) {
      // child
      close(parentfd);
      process(childfd, &clientaddr);
      return 0;
    } else {
      close(childfd);
    }
  }

}
