// Copyright (c) 2017 Yule Fox
// All rights reserved

#include "http.h"

int main(void)
{
  http_init();
  for (;;) {
    http_loop();
  }
  http_fini();
  return 0;
}
