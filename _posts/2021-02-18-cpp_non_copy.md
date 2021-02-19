---
title: c++禁止拷贝
layout: article
key: cpp_non_copy
date: 2021-02-18 11:25
---

最近突然想一个事情，如果只是控制了赋值预算和拷贝构造，在这种情况下移动构造是否还能默认生成呢？

写了个例子：
```c++
#include <iostream>
class NonCopy
{
public:
    explicit NonCopy () {}
    virtual ~NonCopy () {}

private:
     NonCopy& operator=(const NonCopy&);
     NonCopy(const NonCopy&);
};

int main(int argc, char *argv[])
{
    NonCopy a, b;
    // a = b;
    // NonCopy c = b;

    //a = std::move(b);
    //NonCopy c = std::move(b); 

    return 0;
}
```
证明实际上封禁了全部的拷贝操作。也就是没有生成默认的移动构造。当然手动添加一个移动构造是OK的。private构造的方式在c++11之后也被delete声明取代了。

```c++
#include <iostream>
class NonCopy
{
public:
    explicit NonCopy () {}
    virtual ~NonCopy () {}
    NonCopy& operator=(NonCopy&&) {
        return *this;
    }
    NonCopy(NonCopy&&) {
    }

    NonCopy& operator=(const NonCopy&) = delete;
    NonCopy(const NonCopy&) = delete;
};

int main(int argc, char *argv[])
{
    NonCopy a, b;
    // a = b;
    // NonCopy c = b;

    a = std::move(b);
    NonCopy c = std::move(b);

    return 0;
}
```
