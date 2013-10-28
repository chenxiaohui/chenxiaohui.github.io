---
layout: post
title: "oceanbase的库依赖问题"
date: 2013-09-27 16:15
comments: true
categories: oceanbase
---

  今天遇到一个问题: 写测试用例的时候发现总是找不到符号undefined refrence, 第一反应是我去有个没编译的吧, 但是打印了所有的符号，发现其实编译生成库文件里面完全有对应的符号，命名空间也没有错误。这就是很诡异的问题了，刚好手头另一份代码可以编译链接成功，于是对比了一下午结果，发现最后一个函数在类里实现就能编译，类外实现就不能编译，这个问题就太毁三观了。

  最后请教了 [解伦师兄](http://weibo.com/cangzhou "Leverly") ， 发现其实是库依赖的问题， Libtool制定的链接库列表是有相互依赖关系的，比如：

<!-- more -->

	LDADD = libtest2.a \
			libtest2.a 

  或者gcc命令

	gcc –o test main.c libtest2.a libtest1.a

  这里编译的时候会认为libtest2.a依赖于libtest1.a, libtest2.a可以使用libtest1.a的接口，但是反过来会找不到符号。也就是会有会有"undefined reference to ***”的链接错误。

  找了一下原因，主要是gcc链接顺序的问题，以下引自 [悟空不悟空的博客](http://www.cnblogs.com/wujianlundao/archive/2012/06/06/2538125.html "使用静态库链接程序")

-----------------

  原因是gcc在链接的时候，对于多个静态库或者.o文件是从前往后依次处理的，如果当前的静态库或.o文件中没有使用的符号，则往后继续寻找，而不会再往前查找。

  下面是man gcc看到的说明：

  -l library

  >   Search the library named library when linking.  (The second alternative with the library as a separate argument is only for POSIX compliance and is not recommended.)

  >  It makes a difference where in the command you write this option; the linker searches and processes libraries and object files in the order they are specified.  Thus, foo.o -lz bar.o searches library z after file foo.o but before bar.o.  If bar.o refers to functions in z, those functions may not be loaded.

  所以在使用一些依赖关系比较复杂的静态库时，我们可能会看到这样的使用方式：gcc –o test main.c libtest1.a libtest2.a libtest1.a。在链接序列中，一个静态库可能出现多次，以解决一些循环依赖。

------------------------

  另外的办法是指定Xlinker， 让ld链接的时候全局搜索符号， 但是明显效率会低很多。 所以维护一下依赖关系还是必要的。

  ps: 刚刚看到[晓楚师兄](http://weibo.com/raywill2 "研究员Raywill")的博客里也有[一篇](http://blog.csdn.net/maray/article/details/7666022 "gcc库的链接顺序导致编译出错的问题")说这个事情的....w