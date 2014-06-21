---
title: 深入解析C++输入输出运算符重载
author: Harry Chen
layout: post
categories:
  - MFC
tags:
  - 'C#'
  - CArchive
  - 输入输出
  - 运算符重载
format: standard
---

  其实算不上什么深入解析，只不过最近看CArchive类的实现，其中一些写法完全颠覆了我对输入输出运算符重载的一些理解，所以在这里mark一下。

  我们以输出运算符为例。首先输出运算符重载的一般形式是

    :::cpp
    friend ostream& operator<<(ostream& o,const ClassName& c);[1]

<!--more-->

  ostream是c++流输出的类，至于友元，只记得说输入输出运算符必须用友元重载，因为ostream是受保护的。今天看CArchive类实现的时候，里面有如下的定义

    :::cpp
    friend CArchive& AFXAPI operator>>(CArchive& ar, CObject*& pOb);

  于是才发觉ostream并不是必需的，换句话说，从语法上讲，ostream的位置放什么类都可以，只不过语义上要行得通。而友元的重载从语法上讲也不是必须的，比如可以依然用成员函数重载，函数定义变成如下的格式

    :::cpp
    ostream& operator>>(ostream& o);

  使用的时候只能用object>>cout（或者cout>>object这就太别扭了）形式了，并且不可能连续使用了（比如obj1>>obj2>>cout），这违背了C++规范，但是语法上是的过得去的。

  举一个简单而诡异的例子（原谅我这里诡异的代码风格，只是个演示）

    :::cpp
    #include "stdafx.h"
    #include <iostream>
    using namespace std;
    class output
    {
    public:
        output& operator<<(int i);
    };

    output& output::operator<<( int i )
    {
        cout<<i;
        return *this;
    }
    class CComplex
    {
        int x;
        int y;
    public:
        CComplex(int _x,int _y):x(_x),y(_y){}
        output& operator>>(output& o);

    };

    output& CComplex::operator>>( output& o )
    {
        o<<x<<y;
        return o;
    }

    int _tmain(int argc, _TCHAR* argv[])
    {
        CComplex c(1,2);
        c>>output();
    }

  绕了两个圈圈，只是为了说明输入输出运算符语法上讲完全可以像普通运算符一样重载，但是语义上看输出运算符<<里，ostream只能做左值，而ostream不能让你去添加一个成员函数，所以只能用友元重载，输入运算符里，istream也只能做左值，因而同样只能用友元重载。

  最后，需要注意两个问题。首先是为什么一定要返回一个ostream&或者类似的引用？我们可以从这个例子来想

    :::cpp
    cout<<obj1<<obj2<<endl;

  编译器求值的时候按优先级从左向右进行，cout<<obj1相当于调用函数[1]，结果为ostream的引用才能继续进行右边的<<obj2，这也解释了为什么如下语句是编译不过去的（CArchive里没有对ostream对象的输出运算符重载，因而ar<<obj1返回CArchive&引用之后下一步就报错了）。

    :::cpp
    CArchive ar(&file,CArchive::store);
    ar<<obj1<<endl;

  其次，函数参数里的ostream& o不能加const，因为你实现里几乎一定会写o<<….，这里相当于调用ostream对应的重载函数修改ostream，因而编译的时候会报错。
