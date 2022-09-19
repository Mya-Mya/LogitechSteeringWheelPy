#include <stdio.h> 
#include <stdlib.h> 
#include <unistd.h> 
#include <string.h> 
#include <sys/types.h> 
#include <sys/socket.h> 
#include <arpa/inet.h> 
#include <netinet/in.h> 

#include "state.h"

#define PORT 8000
#define STATE_SIZE sizeof(DIJOYSTATE2_t)

int main() {
  int sockfd;
  char buffer[STATE_SIZE + 1];

  struct sockaddr_in servaddr = { 0 };

  if ((sockfd = socket(AF_INET, SOCK_DGRAM, 0)) < 0) {
    perror("failed to create socket");
    exit(EXIT_FAILURE);
  }

  servaddr.sin_family = AF_INET;
  servaddr.sin_port = htons(PORT);
  servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");

  if (bind(sockfd, (const struct sockaddr *) &servaddr, 
            sizeof(servaddr)) < 0) {
    perror("bind failed");
    exit(EXIT_FAILURE);
  }

  DIJOYSTATE2_t state;

  while(1) {
    printf("Wait recv\n");
    int n, len;
    n = recvfrom(sockfd, (char*) buffer, STATE_SIZE, MSG_WAITALL,
                  (struct sockaddr *) &servaddr, &len);
    buffer[n] = 0;
    int res;
    printf("Received: %s\n", buffer);
    memcpy(&res, buffer, sizeof(int));
    printf("First int: %d\n", res);
    memcpy(&state, buffer, STATE_SIZE);
  }

  return 0;
}
