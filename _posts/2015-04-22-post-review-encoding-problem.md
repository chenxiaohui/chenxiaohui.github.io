---
layout: article
title: "post-review编码问题"
key: post-review-encoding-problem
date: 2015-04-22 16:08
comments: true
published: true
categories: "其他"
---

  windows下post-review遇到一个问题（不是我，不用windows）。python会报错：

  	UnicodeDecodeError: 'ascii' codec can't decode byte 0xe6 in position xxx: ordinal not in range(128) 	
  又是编码的问题啊，我不想去看post-review的源码，所以还是改默认环境的源码好了。找到rbtools\utils\process.py，import sys后面加两行：

  	reload(sys)
	sys.setdefaultencoding("utf-8") 
  
  Ok.