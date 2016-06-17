---
layout: post
title: "union和struct相互嵌套时的初始化"
date: 2016-05-26 11:01
comments: true
published: true
categories: "C++"
---


	typedef union {
	volatile int64_t atomic;
		struct{
		  int32_t pid;
		  int32_t atomic32;
		};
	} S3Atomic;

	int main(int argc, const char *argv[]) {
		S3Atomic atomic = {{.pid = 2, .atomic32 = 1}};
		printf("%x\n", atomic.pid);
		printf("%x\n", atomic.atomic32);
		printf("%lx\n", atomic.atomic);
		return 0;
	}



[参考如下代码][1]


	/* 
	 * This sample shows definition and initiation of a struct and a union in a struct.
	 * using GCC to compile this C file
	 * Author: Jay Ren 
	*/

	#include <stdio.h>

	int main(int argc, char *argv[]) {
		struct my_struct1 {
			int num1;
			union {
				int num2;
				char ch;
			};
		};
		
		struct my_struct1 my_st1 = {
			.num1 = 111,
			/* the following commented line will cause a syntax error. */
			/* .num2 = 123456,*/
		};

		/* num2 or ch in the union of the struct can't be initiated before. */
		my_st1.num2 = 123456;

		printf("my_st1.num1 = %d\n", my_st1.num1);
		printf("my_st1.num2 = %d\n", my_st1.num2);
		
		struct my_struct2 {
			int num1;
			union my_union {
				int num2;
				char ch;
			} my_u;
		};
		
		struct my_struct2 my_st2 = {
			.num1 = 222,
			/*  the following line for initiating num2 works fine. */
			.my_u.num2 = 123456,
		};

		printf("my_st2.num1 = %d\n", my_st2.num1);
		printf("my_st2.num2 = %d\n", my_st2.my_u.num2);

		return 0;
	}


[1]: http://smilejay.com/2011/12/gcc_union_in_struct/ "联合体(UNION)在结构体(STRUCT)中的初始化（GCC语法）"

###参考文献:

>\[1] 联合体(UNION)在结构体(STRUCT)中的初始化（GCC语法）, <http://smilejay.com/2011/12/gcc_union_in_struct/>