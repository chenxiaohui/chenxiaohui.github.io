---
title: c++17的optional
layout: article
key: cpp17_optional
date: 2021-03-06 13:36
---

最近代码里看到一个optional的头文件，正常用10.2的g++加上c++17无法编译，看了下应该没没有进c++17的标准，比如参考一个例子：

```cpp
#include <optional>
#include <string>
#include <iostream>

// 如果可能的话把string转换为int：
std::optional<int> asInt(const std::string& s)
{
    try {
        return std::stoi(s);
    }
    catch (...) {
        return std::nullopt;
    }
}

int main()
{
    for (auto s : {"42", "  077", "hello", "0x33"}) {
        // 尝试把s转换为int，并打印结果：
        std::optional<int> oi = asInt(s);
        if (oi) {
            std::cout << "convert '" << s << "' to int: " << *oi << "\n";
        }
        else {
            std::cout << "can't convert '" << s << "' to int\n";
        }
    }
}
```

编译的时候需要改成experimental/optional，前缀也加上experimental::

optional简单实现了类似于python的None返回类型的功能，简化了处理逻辑，也就是一个结果是不是有效不需要再增加一个bool返回值来标示了。

当然上面可以改成指针：


```cpp
#include <string>
#include <iostream>
#include <memory>

// 如果可能的话把string转换为int：
std::shared_ptr<int> asInt(const std::string& s)
{
    try {
        return std::make_shared<int>(std::stoi(s));
    }
    catch (...) {
        return nullptr;
    }
}

int main()
{
    for (auto s : {"42", "  077", "hello", "0x33"}) {
        // 尝试把s转换为int，并打印结果：
        std::shared_ptr<int> oi = asInt(s);
        if (oi) {
            std::cout << "convert '" << s << "' to int: " << *oi << "\n";
        }
        else {
            std::cout << "can't convert '" << s << "' to int\n";
        }
    }
}
```

optional可以简化返回复杂类型的时候判断类型是否有效的逻辑：

```cpp
#include <experimental/optional>
#include <string>
#include <iostream>
#include <memory>
struct Ctype {
    int a = 0;
};
// 如果可能的话把string转换为int：
std::experimental::optional<Ctype> asInt(const std::string& s)
{
    try {
        Ctype bt = {.a = 1};
        return bt;
    }
    catch (...) {
        return std::experimental::nullopt;
    }
}

int main()
{
    for (auto s : {"42", "  077", "hello", "0x33"}) {
        // 尝试把s转换为int，并打印结果：
        std::experimental::optional<Ctype> oi = asInt(s);
        if (oi) {
            std::cout << "convert '" << s << "' to int: " << oi->a << "\n";
        }
        else {
            std::cout << "can't convert '" << s << "' to int\n";
        }
    }
}
```
