---
title: '面向对象语言的编译过程&#8211;以C++为例(二)'
author: Harry Chen
key: compile-process-of-object-oriented-language-take-cplusplus-as-an-example-2
layout: article

dsq_thread_id:
  - 1301103271
categories:
  - 基础理论
---

  摘要:

  概述面向对象语言的重要概念和实现技术

  以C 语言为例，介绍如何将C 程序翻译成C程序

  实际的编译器大都把C 程序直接翻译成低级语言程序

  编译器对于继承的处理，往往是父类包含子类的对象，例如


        struct Base

        {

            int a;

        };

        struct Derived

        {

            Base base;

            int b;

        };

  再深入的偶也不会了………

  下面我们讨论对面向对象多态特性的处理。多态是面向对象语言最为精彩的地方，可以说是诞生无数神奇的特性，多态给了我们极大的自由，让我们可以在一套类的体系结构中自由游走，可以写很少的代码，但是完成复杂的功能，可以在别人的基础上做二次开发……

  好了，不打广告了，下面举一个简单的例子说明编译器对多态的处理。首先介绍一下虚函数表。大多数编译器实现多态都是通过虚函数表，虚函数表是一个保存了多个函数指针的表，其中每个函数对应着一个虚函数（非虚函数不参与），调用一个虚函数的时候，编译器通过虚函数表查找相应位置的函数，所以编译时编译器不知道这个函数会调用到基类的函数还是派生类的函数，所以叫动态绑定或运行时绑定。

  以下是一个简单的多态实例程序，有了虚函数所以可以在基类指针指向派生类对象的时候运行派生类的函数。


      #include

      using namespace std;

      class Base

      {

      public:

      virtual void Hello();

      };

      void Base::Hello()

      {

      cout
