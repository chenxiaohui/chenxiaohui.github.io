---
title: C++ Primer 读书笔记
author: Harry Chen
layout: post
permalink: /cplusplus-primer-book-review/
mkd_text:
  - |
    今天遇到一个c++的问题，上网查了查，发现答案的出处其实就是C++ Primer，想想这本经典的书其实没怎么细度过，很多细节其实模棱两可，所以决定每天读一点，务必求细致，不为速度，写点读书笔记权当是打卡了。
    
    <!--more-->
    
    1. 关于初始化变量和未初始化变量
    
    >这里有个很蛋疼的例子，VC我没试过，gcc下有匪夷所思的输出
    
    
    	:::cpp
    	int a;
    	int b;
    	int c;
    	printf("a=%d  b=%d  c=%d\n", a, b, c);
    
    2.块注释不能嵌套
    
    3.两种初始化方式
    
    	int ival(1024);//直接初始化
    	int ival=1024; //复制初始化
    
    >c++中初始化不是赋值，初始化指创建变量并赋值，赋值则是擦去对象当前值并用新值代替
    
    >初始化语句中前面定义的变量可以用来初始化后面的值，所以如下语句是合法的
    
    	:::cpp
    	double salary=9999.99,wage(salary+0.01);
    
    4.const作用域也不能出文件
    
    5.const引用是指向const对象的引用，是一种语法规则限制。另外const引用可以初始化为不同类型的对象或右值，例如：
    
    	:::cpp
    	double dval=3.14;
    	const int &ri=dval;//编译器会转换代码为：int temp=dval;const int &ri=temp;
    
    	const int &r=42;
    	const int &r2=r+i;
    
    6.string的连接：+操作符左右操作数必须至少有一个是string类型的，但是鉴于+操作符是从左到右求值的，所以这种是合法的：
    
    	:::cpp
    	string s1="b";
    	string s2="a"+s1+"c";
    
    6.还有一件事情:大写字母的ascii码值小于小写字母，切记
dsq_thread_id:
  - 1292767832
categories:
  - C++
tags:
  - 'C#'
  - Primer
format: standard
---
# 

今天遇到一个c 的问题，上网查了查，发现答案的出处其实就是C Primer，想想这本经典的书其实没怎么细度过，很多细节其实模棱两可，所以决定每天读一点，务必求细致，不为速度，写点读书笔记权当是打卡了。

  1. 关于初始化变量和未初始化变量

> 这里有个很蛋疼的例子，VC我没试过，gcc下有匪夷所思的输出


    int a;
    int b;
    int c;
    printf("a=%d  b=%d  c=%dn", a, b, c);

2.块注释不能嵌套

3.两种初始化方式


    int ival(1024);//直接初始化
    int ival=1024; //复制初始化

> c 中初始化不是赋值，初始化指创建变量并赋值，赋值则是擦去对象当前值并用新值代替
>
> 初始化语句中前面定义的变量可以用来初始化后面的值，所以如下语句是合法的


    double salary=9999.99,wage(salary 0.01);

4.const作用域也不能出文件

5.const引用是指向const对象的引用，是一种语法规则限制。另外const引用可以初始化为不同类型的对象或右值，例如：


    double dval=3.14;
    const int &ri=dval;//编译器会转换代码为：int temp=dval;const int &ri=temp;

    const int &r=42;
    const int &r2=r i;

6.string的连接： 操作符左右操作数必须至少有一个是string类型的，但是鉴于 操作符是从左到右求值的，所以这种是合法的：


    string s1="b";
    string s2="a" s1 "c";

6.还有一件事情:大写字母的ascii码值小于小写字母，切记