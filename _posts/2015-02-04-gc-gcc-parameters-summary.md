---
layout: article
title: "gcc命令行参数总结"
key: gc-gcc-parameters-summary
date: 2015-02-04 11:36
comments: true
published: true
categories: "C++"
---
   总结一下混乱的GCC命令行参数，帮助写Makefile:

1. 编译阶段
	1. 预编译E->生成汇编S(ccl)->生成机器码c(as)->链接生成目标程序(ld)

1. 输出类型：

	1. -E 只执行到预编译
	2. -S 只执行到汇编阶段。生成汇编代码。
	3. -c 只执行到编译。输出目标文件。
	4. 空。生成链接目标代码。
	5. -o 指定输出文件名。

2. 输入类型：

	1. 每个阶段可以接受之前阶段的中间结果（可跨越）。比如：

			gcc -E hello.c -o hello.i
			gcc -S hello.i -o hello.s
			顺序可以换：
			gcc -c -o hello.o hello.c

3. 优化调试相关

	1. -g 生成调试信息
	2. -s 去掉调试和符号信息
	3. -O[1|2|3..] 编译优化
	4. -W[all] 开启额外警告

4. 链接相关：

	1. -l, 指定所使用到的函数库
	2. -L, 指定函数库所在的文件夹。
	3. -I, 指定头文件所在的文件夹


[1]: http://robbinfan.com/blog/9/gcc-linker-basic-usage   "Linux平台gcc和动态共享库的基础知识"
[2]: http://www.cppblog.com/deane/articles/165216.html "Linux下Gcc生成和使用静态库和动态库详解（转）"
###Bibliography:

  \[1] Linux平台gcc和动态共享库的基础知识, <http://robbinfan.com/blog/9/gcc-linker-basic-usage>
