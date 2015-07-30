---
layout: post
title: "log4cxx安装"
date: 2015-07-30 15:55
comments: true
published: true
categories: "Linux"
---

  log4cxx是apache基金会的log开源项目，log4j的c++实现，安装的时候遇到一个小问题：

  首先正常安装：

  	wget http://mirrors.cnnic.cn/apache/logging/log4cxx/0.10.0/apache-log4cxx-0.10.0.tar.gz
	tar zxvf apache-log4cxx-0.10.0.tar.gz
	cd apache-log4cxx-0.10.0
	./configure
	make
   
   报错libdb-4.3.so 格式错误。开始以为是文件损坏了，查了一下这个文件

   	yum provides */libdb-4.3.so

   提示在db4里面，重新安装db4

   	yum reinstall db4

   回去还是报错。后来看了一下格式，貌似链接到了32位版本。修改软连接：

   	cd /usr/lib/
   	rm libdb-4.3.so
 	ln -s ../../lib64/libdb-4.3.so .

   同样处理另外一个库
 	
 	rm libexpat.so
 	ln -s ../../lib64/libexpat.so.0.5.0 libexpat.so

   应该就OK了。