---
layout: post
title: "vim编译错误：PyUnicodeUCS4_AsEncodedString"
date: 2016-03-06 14:45
comments: true
published: true
categories: "vim"
---

  换了个ubuntu的环境想编译一下vim，为了防止不兼容手动编译了python2.7，之后把改过的vim源码放上去编译发现有问题：

	undefined symbol: PyUnicodeUCS4_AsEncodedString

  于是换回标准的vim源码还是一样的问题，我擦嘞。上网搜一下说Python模式是UnicodeUCS2的支持，从源码里面直接grep一下这个函数发现是有的：

  	Include/unicodeobject.h:# define PyUnicode_AsEncodedString PyUnicodeUCS4_AsEncodedString

  那只可能是没有开启编译选项了，./configure --help发现有如下一项：

  	  --enable-unicode[=ucs[24]]
                          Enable Unicode strings (default is ucs2)
  
  configure到ucs4重新编译python2.7，完美。没毛病。

  

