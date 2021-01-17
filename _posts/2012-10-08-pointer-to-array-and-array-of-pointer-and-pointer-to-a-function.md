---
title: 指针数组，数组指针与函数指针
author: Harry Chen
key: pointer-to-array-and-array-of-pointer-and-pointer-to-a-function
layout: article

categories:
  - 随笔
tags:
  - 'C#'
format: standard
---
  指针数组是指由指针组成的数组，这个比较好理解；数组指针是指向一个数组的指针，其实字面上也比较好理解。容易混淆的地方在于书写形式有些类似

    :::cpp
    int *p[n];  //array of pointers
    int (*p)[n];//pointer to an array

<!--more-->

  指针数组可以像普通数组一样使用，只不过每个元素是指针而已，数组指针可直接指向一个数组，从而用来遍历一个数组，一个简单的例子如下：

    ::cpp
    void PrintLine(int *p,int n)
    {
        for(int i=0;i<n;i++)
            printf("%*d",2,p[i]);
        printf("\n");
    }
    int main(int argc, const char *argv[])
    {
        int a[4][4];
        for(int i=0;i<4;i++)
            for(int j=0;j<4;j++)
                a[i][j]=i*j;
        int (*p)[4]=a;
        PrintLine(p[1],4);
        PrintLine(p[2],4);
    }

  另一个容易混淆的对象是函数指针，函数指针本身的形式如下

    :::cpp
    int (*p)(int);

  但是经常会有各种各样的变化，比如

    :::cpp
    int* (*p)(int *);//参数和返回值都是指针的函数指针
    int (*p[10])(int);//一个指针数组，每个元素都是指向一个函数的指针（返回值和参数都是int)
    int* (*p[10]);//等同于int**p[10]，二维指针数组
    int* (*p)[10];//数组指针，指向一个数组，每个元素都是int指针
    int(*(*f)(int))(int);//f是一个函数指针，指向一个参数为int返回值为一个函数指针（参数和返回值都是int）
