---
layout: article
title: "c/c++的不定参数"
date: 2014-07-17 14:42
comments: true
categories: "C++"
---

  c/c++可以通过va_arg等宏实现不定参数。一个例子如下(c++)：

	void ar_cnt(int cnt,...);
	int main(int argc, char* argv[])
	{
	    ar_cnt(4,1,2,3,4);
	    return 0; 
	}
	void ar_cnt(int cnt,...)
	{
	    int arg_cnt = cnt;
	    va_list arg_ptr;
	    va_start(arg_ptr, cnt);
	    for(int i=0; i < cnt;i++)
	    {
	        int value=va_arg(arg_ptr,int);
	        printf("posation %d=%d\n", value, i+1);
	    }
	    va_end(arg_ptr);
	}

  其实原理是比较简单的，依赖于编译器对函数调用的压栈顺序，但是目测现有的调用方式压栈都是从右向左，所以va_start定位第一个参数的位置，va_arg每次在之前的位置上加一个偏移值，从而得到每个传入参数。这就是说va_start要求传入不定参数的函数不能只传入一个...，至少要有一个固定的参数，用来获取栈指针位置。

<!--more-->

  调用方式这个东西好像只有在VC里才探讨，不太清楚gcc这里的处理是怎么样的，vc下主要分了如下几种：

  - STDCALL/PASCAL/WINAPI/CALLBACK
  	1. 参数从右向左压入堆栈
  	2. 函数自身修改堆栈 
  	3. 函数名自动加前导的下划线，后面紧跟一个@符号，其后紧跟着参数的尺寸
 
  - CDECL
  	1. 调用约定的参数压栈顺序是和stdcall是一样的，参数由右向左压入堆栈。
  	2. 调用者负责清理堆栈。
  	3. 由于这种变化，C调用约定允许函数的参数的个数是不固定的，这也是C语言的一大特色。

  - FASTCALL
  	1. 函数的第一个和第二个DWORD参数（或者尺寸更小的）通过ecx和edx传递，其他参数通过从右向左的顺序压栈 
  	2. 被调用函数清理堆栈 
  	3. 函数名修改规则同stdcall 

  - THISCALL
  	1. 参数从右向左入栈
  	2. 如果参数个数确定，this指针通过ecx传递给被调用者；如果参数个数不确定，this指针在所有参数压栈后被压入堆栈 

  - NAKEDCALL 
  	1. 这是一个很少见的调用约定，一般程序设计者建议不要使用。 
  	2. 编译器不会给这种函数增加初始化和清理代码，更特殊的是，你不能用return返回返回值，只能用插入汇编返回结果
  	3. 这一般用于实模式驱动程序设计



[1]:http://blog.csdn.net/fly2k5/article/details/544112 "cdecl、stdcall、fastcall函数调用约定区别 "
[2]:http://www.cppblog.com/kenny/archive/2011/04/19/144539.html "函数调用的区别：_cdecl以及_stdcall"
[3]:http://www.cnblogs.com/wangyonghui/archive/2010/07/12/1776068.html "透析C语言可变参数问题"

#### 参考文献:

  \[1] cdecl、stdcall、fastcall函数调用约定区别 , <http://blog.csdn.net/fly2k5/article/details/544112>
  
  \[2] 函数调用的区别：_cdecl以及_stdcall, <http://www.cppblog.com/kenny/archive/2011/04/19/144539.html>
  
  \[3] 透析C语言可变参数问题, <http://www.cnblogs.com/wangyonghui/archive/2010/07/12/1776068.html>
