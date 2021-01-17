---
layout: article
title: "gcc的格式化字符串检查"
date: 2016-07-04 14:53
comments: true
published: true
categories: "C++"
---
  
  之前很好奇为什么printf参数类型跟格式化字符串不匹配的时候为啥有时候可以报错，有时候不能报错。printf的时候如果不匹配经常会看到这种错误：

  	 format ‘%s’ expects type ‘char *’, but argument 12 has type ‘struct S3ListHead * const’

  很多core是因为这种问题导致的，所以能放到编译期检查的话，确实有助于提高代码质量。后来白哥指点gcc有单独的attribute来指定检查匹配。作为一个编译器，真是良心啊。

  	format (archetype, string-index, first-to-check)
	The format attribute specifies that a function takes printf, scanf, strftime or strfmon style arguments which should be type-checked against a format string. For example, the declaration:
	          extern int
	          my_printf (void *my_object, const char *my_format, ...)
	                __attribute__ ((format (printf, 2, 3)));
  
  这样自定义的函数也可以依赖gcc做参数检查了。

  详细的参见[这里][1]

#### 参考文献:

>\[1] Declaring Attributes of Functions, <https://gcc.gnu.org/onlinedocs/gcc-3.2/gcc/Function-Attributes.html>

[1]: https://gcc.gnu.org/onlinedocs/gcc-3.2/gcc/Function-Attributes.html "Declaring Attributes of Functions"
