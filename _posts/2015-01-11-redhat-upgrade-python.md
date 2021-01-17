---
layout: article
title: "redhat下升级python"
key: redhat-upgrade-python
date: 2015-01-11 18:56
comments: true
published: true
categories: "Python"
---
  偶然发现服务器上的python是2.4的，好多语法都不支持。遂决定升级。

  首先yum升级是可以升级到2.6的：

  	yum install python26
  	yum install python26-devel
  	yum install python26-setuptools
  	ln -s /usr/bin/python2.6 /usr/bin/python

  升级之后发现yum不能用了。yum应该是跟python版本绑定了，于是把yum头部改成：

  	#!/bin/python2.4

  之后发现2.6还是不行...我是用了多新的语法啊...就是几个dict comprehension。于是决定升级到2.7。源里面没有，只能手动。

  	#wget http://python.org/ftp/python/2.7.3/Python-2.7.3.tar.bz2  
  	#tar -jxvf Python-2.7.3.tar.bz2
  	#cd Python-2.7.3  
  	#./configure  
	#make all             
	#make install
	#ln -s /usr/local/bin/python2.7 /usr/bin/python  

  安装setup-tools

  	wget https://pypi.python.org/packages/source/s/setuptools/setuptools-11.3.1.zip --no-check-certificate
  	unzip setuptools-11.3.1.zip
  	cd setuptools-11.3.1
  	python setup.py install

  yum不用动了。