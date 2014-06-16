---
title: >
  区分一下强制类型转换运算符重载/赋值运算符重载/对象定义的赋值
author: Harry Chen
layout: post

mkd_text:
  - |
    这三个名字可能很绕，看着也很不一样，但其实是三个很容易混淆的概念，并且经常在实际编程中遇到。这里拿出来比较一下。
    
    首先是强制类型转换运算符的重载，作用是当前对象向其他类型的转换，常见的形式是
    
    	:::cpp
    	operator int();
    	Integer::operator int()
    	{
    		return x;
    	}
    
    <!--more-->
    
    调用方式类似于
    
    	:::cpp
    	Integer c(10);
    	int a=c;
    
    在函数调用的时候，类型转换的重载也会被隐式调用，比如下面一种情况
    
    	:::cpp
    	void print(int n)
    	{
    		cout<<n<<endl;
    	}
    	Integer i(10);
    	print(i);
    
    与之相对应的是赋值运算符重载，赋值运算符是从别的类型转换成当前对象，常见的形式如下：
    
    	:::cpp
    	Integer operator=(int n);
    	Integer Integer::operator=( int n )
    	{
    		return Integer(n);
    	}
    
    调用方式类似于
    
    	:::cpp
    	Integer c;
    	c=11;
    
    最后是对象定义时的赋值，如果你定义了如下的一个构造函数
    
    	:::cpp
    	Integer(int _x):x(_x){}
    
    那么你可以用这种方式定义一个对象
    
    	:::cpp
    	Integer c=11;
    
    需要特别区别的是，定义时的赋值是会不会调用赋值运算符重载的。另外，如果需要限制隐式类型转换，可以使用explicit关键字，见参考文献[1].
    
###参考文献
    
    >C++笔记（1）explicit构造函数
    
    ><http://www.cnblogs.com/cutepig/archive/2009/01/14/1375917.html>
categories:
  - MFC
tags:
  - 强制类型转换
  - 构造函数
  - 赋值运算符
  - 运算符重载
format: standard
---
# 

这三个名字可能很绕，看着也很不一样，但其实是三个很容易混淆的概念，并且经常在实际编程中遇到。这里拿出来比较一下。

首先是强制类型转换运算符的重载，作用是当前对象向其他类型的转换，常见的形式是


    operator int();
    Integer::operator int()
    {
        return x;
    }


调用方式类似于


    Integer c(10);
    int a=c;


在函数调用的时候，类型转换的重载也会被隐式调用，比如下面一种情况


    void print(int n)
    {
        cout
