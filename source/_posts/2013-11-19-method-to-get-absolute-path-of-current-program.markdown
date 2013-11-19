---
layout: post
title: "关于得到当前执行文件所在的目录"
date: 2013-11-19 21:47
comments: true
categories: "Linux"
---

  今天遇到一个问题，程序里面用相对路径引用了同一级目录下的一个文件，shell在上一级目录调用程序的时候，发现当前目录变成了上一级目录，于是程序在上一级目录找那个文件。最简单的办法当然是shell脚本里面加cd操作，但是暂时不方便修改脚本。所以直接通过程序获取绝对路径好了。

  首先，直接 realpath("./") 和 getcwd 获取的都是当前路径，也就是当前shell所在的路径。__FILE__获取的是文件名，不包含路径，而且是编译过程确定的，最简单的办法当然是argv[0]，但是在test_case(gtest)里面不方便传来传去，后来发现最好的办法是这样的：

	#include "libgen.h"
	#define MAX_PATH_SIZE 100
	char current_absolute_path[MAX_PATH_SIZE] = {'\0'};
	if (readlink("/proc/self/exe", current_absolute_path, MAX_PATH_SIZE - 1) < 0)
	{
	  //error
	}
	else
	{
	  sprintf(current_absolute_path, "%s/%s", dirname(current_absolute_path), schema_file_name);
	}

  这样就可以拼合当前程序所在目录和schema_file_name得到这个文件的绝对路径了。这里/proc/self/exe是运行时的当前执行程序软链接。看来proc目录下要好好研究一下啊。
