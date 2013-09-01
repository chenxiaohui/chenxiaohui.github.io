---
title: C++变量的初始化方式
author: Harry Chen
layout: post
permalink: /ways-to-initialize-variables-in-cplusplus/
categories:
  - 基础理论
tags:
  - 'C#'
  - 初始化
  - 常量
  - 静态
---
# 

写这个问题是受微软今年实习生招聘的一道笔试题启发，上一篇博客好像提到了。之前还真没细想过这些事情。

首先把需要初始化的成员变量分为几类：

> 一般变量(int)
>
> 静态成员变量(static int)
>
> 常量(const int )
>
> 静态常量(static const int)

对应的初始化方式是：

> 一般变量可以在初始化列表里或者构造函数里初始化，不能直接初始化或者类外初始化
>
> 静态成员变量必须在类外初始化
>
> 常量必须在初始化列表里初始化
>
> 静态常量必须只能在定义的时候初始化

举一个简单的例子

> #include 
#include 
using namespace std;
class Test
{
private:
int a;
static int b;
const int c;
static const int d=4;
public:
Test():c(3)//,a(1)或者在初始化列表里初始化
{
a=1;
}
};
int Test::b=2;
>
> void main()
{
Test t;
}