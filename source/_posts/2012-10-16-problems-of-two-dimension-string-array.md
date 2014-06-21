---
title: 二维字符串数组的问题
author: Harry Chen
layout: post

dsq_thread_id:
  -
categories:
  - C++
tags:
  - 字符串数组
format: standard
---
  随手写了个字符串的程序，才发现自己好像对字符串数组的理解一直似懂非懂。

  先举一个int二维数组简单的例子：

<!--more-->

    :::cpp
    void foo(int (*p)[3],int n)
    {
        for(int i=0;i<n;i++)
        {
            for(int j=0;j<3;j++)
                cout<<p[i][j]<<" ";
            cout<<endl;
        }
    }
    int arr[][3]=
    {
        {1,2,3},
        {4,5,6},
        {7,8,9},
    };
    foo(p,3);

  这个例子还是比较好理解的，int(*p)[3]是指向数组的指针，指向的每个元素是int[3]，详见[这里][1]

  所以对应的字符串二位数组的写法是：

    :::cpp
    void foo(char* (*p)[3],int n)
    {
        for(int i=0;i<n;i++)
        {
            for(int j=0;j<3;j++)
            {
                cout<<p[i][j]<<" ";
            }
            cout<<endl;
        }
    }

    char* str[][3]=
    {
        {"abc","abc","abc"},
        {"dfs","dfs","dfs"},
        {"bcs","bcs","bcs"},
    };
    foo(str,3);

  乍一看还是很晕的，但是其实把char*当成一个类型，形式上就完全一样了。而且其实foo函数可以直接用模板的:


    :::cpp
    template<class T>
    void foo(T (*p)[3],int n)
    {
        for(int i=0;i<n;i++)
        {
            for(int j=0;j<3;j++)
            {
                cout<<p[i][j]<<" ";
            }
            cout<<endl;
        }
    }
    foo<char*>(str,3);

[1]: http://www.roybit.com/archives/830 "针数组，数组指针与函数指针"
