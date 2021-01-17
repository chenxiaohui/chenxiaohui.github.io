---
title: 关于const和指针的专题
author: Harry Chen
key: about-const-and-pointer
layout: article

categories:
  - 与技术相关
  - 基础理论
tags:
  - const
  - 微软
  - 指针
  - 面试
---
#

  const和指针的问题是笔试里经常出现的问题。这里综合一下各种不同的情况。

  首先是几种const与指针组合的区分，比如：

	int b = 500;
	const int* a = &b; [1]
	int const *a = &b; [2]
	int* const a = &b; [3]
	const int* const a = &b; [4]

  [1]和[2]其实是一样的，都是指向int型常量的指针，而[3]是int型常量指针，两者的区别是指向常量的指针本身可以指向别的，所指向的数据不能被修改，而常量指针本身不能被修改。[4]就不用说了，啥都甭想改。

  至于例子，可以举下面的一个例子（以[1]为例）。这里小小的牵扯了一点优先级的问题。

	#include
	using namespace std;

	int main(int argc,char* argv[])
	{
	int a=1;
	const int *b=&a;
	*b ;//成立
	(*b) ;//编译器错误
	}

  那么我们能不能突破const去修改一个值呢？虽然这件事情本身并没有多大意义，但是还是可以做的。我们可以用const_cast来去掉一个const或者volatile限制。const_cast的作用主要分如下三种：

> 转化一个常量指针为非常量指针
>
> 转化一个常量引用为非常量引用
>
> 转化一个常量对象为非常量对象

  至于例子

  我们举如下一个例子：

	#include
	using namespace std;

	class Test
	{
	public:
	const int a ;
	Test(int b):a(b)
	{

	 }
	};

	 int main(int argc,char* argv[])
	{
	Test t(1);
	//t.a=2;//出错
	int b=const_cast(t.a);
	int& c=const_cast(t.a);
	int* d=const_cast(&t.a);
	b=2;
	c=3;
	cout
