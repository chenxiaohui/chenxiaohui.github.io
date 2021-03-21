---
title: inline static的成员初始化
layout: article
key: inline_static_since_c++17
date: 2021-03-21 19:49
---

非静态非const变量当然是通过初始化列表，C++primer会告诉你初始化列表能减少一次初始化，所以不要在构造函数里初始化。

比如

```cpp
#pragma once
class File {
  private:
    const std::string filename;
  public:
    File(): filename("test") {
    }
    void print() const {
      std::cout << filename << std::endl;
    }
};
```


const变量可以直接在定义的时候初始化。这个算是比较简单的构造方式，相当于对初始化列表的优化，可以认为是初始化列表的一个简单的写法。

比如


```cpp
#pragma once
class File {
  private:
    const std::string filename = "test";
  public:
    void print() const {
      std::cout << filename << std::endl;
    }
};
```



而静态变量不太一样。静态变量本身定义跟声明是分开的，这本来也合理，所以在不同的编译单元里面，静态变量可以各自实现，当然相互影响。。一般情况系因为.h和 .cpp的相互对应，也不会出现多次包含之后定义的重复的问题。

但是static变量毕竟是可以寻址的，从这个角度看，一个头文件如果包含了定义和声明，同时被多个编译单元包含，还是会出现multiple definition的问题。

```cpp
#pragma once
class File {
  private:
    static char filename[];
  public:
    void print() const {
      std::cout << filename << std::endl;
    }
};

char File::filename[] = "file.txt";
```

静态的const变量因为不涉及修改，可以认为编译期能确定，所以可以直接在定义的时候声明。同时c++11提供了constexpr来现实说明编译期可以确定。但是constexpr不能支持复杂类型。

比如：

```cpp
#pragma once
class File {
  private:
  static const int file_size = 1025;
  //static constexpr char filename[] = "std::string";//not supported
  public:
    void print() const {
      std::cout << filename << std::endl;
    }
};
```

所以c++17继续从编译器层面支持了多个编译单元对static const的展开，也就是inline变量，是的，不只是函数，变量本身也可以inline了。

比如：

```cpp
#pragma once
class File {
  private:
    // static constexpr std::string filename = "test";//not supported
    inline static const std::string filename = "test";//c++17 supported
  public:
    void print() const {
      std::cout << filename << std::endl;
    }
};

```

同样支持非const的static初始化，比如：

```cpp

#pragma once
class File {
  private:
    static char filename[];
  public:
    void print() const {
      std::cout << filename << std::endl;
    }
};

inline char File::filename[] = "file.txt";

```

感觉并不是很有用，主要是支持了static const std::string的定义初始化?
