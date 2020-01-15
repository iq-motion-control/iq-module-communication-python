
#include <iostream>

#include "simple_class.hpp"

int main(int argc, char *argv[]) {
  SimpleClass sc = SimpleClass();

  uint8_t value1 = 5;
  sc.Display(value1);

  int value2 = -5;
  sc.Display(value2);

  return 0;
}
