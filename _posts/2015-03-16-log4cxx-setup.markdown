---
layout: article
title: "Log4cxx安装"
date: 2015-03-16 11:49
comments: true
published: true
categories: "C++"
---
  apache经典的项目，java下有log4j，c++下的实现是log4cxx，安装见[参考文献][1].

  主要有个编译问题，大概是C库和C++库的问题，把出错的地方的头文件都补上就行了。

1. console.cpp ： #include <string.h> #include <stdio.h>
2. socketoutputstream.cpp : #include <string.h>
3. inputstreamreader.cpp: #include <string.h>


[1]: http://www.codelast.com/?p=3211   "[原创] 	log4cxx在Linux下的安装、使用"

###Bibliography:

  \[1] [原创] 	log4cxx在Linux下的安装、使用, <http://www.codelast.com/?p=3211>
