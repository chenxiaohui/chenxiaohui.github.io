---
layout: post
title: "java/c++变量作用域的一点小区别"
date: 2014-07-17 11:16
comments: true
categories: "C++"
---

  偶然遇到一个问题，java里面这么写是有问题的
	
	int x = 1;
		{
			int x = 2;
		}

  作为一个写了多年C++的人，不能忍啊。java子域里的变量看样子不会覆盖父域。但是这样是没问题的，可见子域的生命周期还是局限于子域里面。

		{
			int x = 2;
		}
  	int x = 1;

  C++里面这样是没问题的

	  int x = 1 ;
	  {
	    int x  = 2;
	  }

  相对于脚本语言，这种限制似乎就宽多了。这样都可以。

  	for i in range(1,10):
    	pass
	print i
