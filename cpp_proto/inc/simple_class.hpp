#ifndef SIMPLE_CLASS_HPP
#define SIMPLE_CLASS_HPP

#include <iostream>

class SimpleClass {
 public:
  SimpleClass(){};

  template <typename T>
  void Display(T &value) {
    std::cout << "My value is " << value << "\n";

    return;
  }

 private:
};

#endif  // SIMPLE_CLASS_HPP