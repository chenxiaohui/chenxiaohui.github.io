---
layout: post
title: "Python2/Python3中文编码"
date: 2015-03-19 15:03
comments: true
published: true
categories: "Python"
---
  python2中需要区分另种不同形式的string，字符串和字节串（严格意义上讲，string就是字符串，字节串是bytes）。默认情况下，直接输入字符串格式为str，编码由文件编码指定，可以理解为ascii存储的某种形式，编码由编码方式决定。而python字符串是unicode内码的字符流，无论采用什么编码，长度都是由字符个数决定的，字符是最基本的操作对象。
  
  转换上，最终字符"xx"的编码由文件编码决定，u"xx"统一被转成unicode字符，对于某种编码的bytes，decode或者unicode函数把编码转成字符，对于unicode的字符，encode把字符编码为字节。

  命令行打印上看，字符直接打印的时候，程序会按照sys.defaultencoding编码输出字符，如果打印字节，需要保证编码跟terminal/IDE的默认编码一致。输入的时候应该不存在这个问题，terminal会按照编码sys.defaultencoding把输入转成unicode字符。

  python3中不存在这两种不同的编码形式了。string统一变成了unicode。略浪费。

  详见[参考文献][1]。

  [1]: http://wklken.me/posts/2013/08/31/python-extra-coding-intro.html   "PYTHON-进阶-编码处理小结"
  [2]: