---
title: 关于Const指针的一点补充
author: Harry Chen
layout: post
categories:
  - Others
tags:
  - const
  - define
  - typedef
  - 宏替换
  - 指针
  - 编译器
format: standard
---
# 

  OsChina上一个朋友给出的例子，很能说明问题：


    typedef char * CharPtr;
    const CharPtr mycharptr = "Hello, World";
    mycharptr[0]='h'; //OK[1]
    mycharptr = "It's Wrong"; //Err[2]


  如果把CharPtr替代掉的话，那么似乎[1]是错的，[2]是对的，因为const char _是指向const char的指针，指针可以指向别的，但是指向的内容不能变。实际上，const只是编译器的一种规范，所以编译的时候只按照语法检查是不是改变了，char_被typedef之后，可以当成一种简单类型看，那么const CharPtr 就只一个CharPtr型的常量，对它的赋值肯定会引起编译错误，而[0]这种寻址并不影响。

  不过，如果把typedef 改为宏替换（如下），事情就不一样了，毕竟宏替换只是一种替换而已，不会引起编译器的检查，编译之前，CharPtr就已经被替换掉了。


    #define CharPtr char *
    const CharPtr mycharptr = "Hello, World";
    mycharptr[0]='h'; //Err
    mycharptr = "It's Wrong"; //OK
