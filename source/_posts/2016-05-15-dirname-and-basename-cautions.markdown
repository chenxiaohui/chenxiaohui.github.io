---
layout: post
title: "dirname和basename的一些细节"
date: 2016-05-15 14:42
comments: true
published: true
categories: "Linux"
---

  作为获取文件名和文件路径的函数，dirname和basename的签名是：

    #include <libgen.h>

    char *dirname(char *path);

    char *basename(char *path);

  之前没注意的地方是这个函数的输入输出都不是const的，也就意味着这个函数调用过程可能会修改char*指向的string内容。所以直接输出一个不可变字符串是不行的，同理，也要考虑这个非const函数会破坏入参。也就是：

  	char *str = "/abc/def";
  	printf("%s\n", dirname(str));

  会core掉。而

	#include <stdio.h>
	#include <libgen.h>
	int main(int argc, const char *argv[]) {
	  char str[] = "/abc/def";
	  printf("%s\n", dirname(str));
	  printf("%s\n", basename(str));
	  printf("%s\n", str);
	  return 0;
	}

  输出结果是：

    /abc
	abc
	/abc

  还有一个更有意思的问题....如果对同一个path先后调用dirname和basename，那么返回的只有一个是对的....因为源已经被修改了。反过来可以。
  
  path在执行过程中被修改了。C系的函数很多面临这个问题，如果不这么做的话要申请一块额外的内存，然后返回，而释放这块内存的工作得调用方完成，这种情况下，内存泄露的可能性很大，所以很多c库函数的选择是用全局变量（getopt等)或者修改入参（basename等）。
