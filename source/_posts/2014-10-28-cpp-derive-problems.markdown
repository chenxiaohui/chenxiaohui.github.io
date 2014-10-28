---
layout: post
title: "澄清几个关于C++继承的问题"
date: 2014-10-28 15:56
comments: true
categories: "C++"
---

  之前讨论编码规范的时候遇到过一个问题，继承的类覆盖基类的虚函数，不写virtual关键字是否依然有覆盖（override)的效果。是个基础问题，但是大家的理解好像都不一样。验证如下：

  	#include <stdio.h>
	class Base
	{
	  public:
	    Base (){}
	    virtual ~Base (){}
	    virtual void print() {printf("Base\n");}
	};

	class Middle : public Base
	{
	  public:
	    Middle(){}
	    virtual ~Middle(){}
	    void print() {printf("Middle\n");}
	};

	class Derived : public Middle
	{
	  public:
	    Derived(){}
	    virtual ~Derived(){}
	    void print() {printf("Derived\n");}
	};

	int main(int argc, const char *argv[])
	{
	  Base * p = NULL;
	  Base b;
	  Middle m;
	  Derived d;
	  p = & b;
	  p->print();
	  p = & m;
	  p->print();
	  p = & d;
	  p->print();
	  return 0;
	}
  
<!--more-->

  结果是

	Base
	Middle
	Derived
  
  可见只要定义了virtual关键字，在整个继承体系中这个函数都会成为虚函数。第二个问题是作为一个中间类（Middle)不想覆盖基类的虚函数，默认的情况下有什么影响。猜想应该就默认用了基类的虚函数。不影响后面的继承关系。注释掉Middle的print函数实现。结果如下：

	Base
	Base
	Derived
  
  跟预想一致。水文一篇，可忽略。