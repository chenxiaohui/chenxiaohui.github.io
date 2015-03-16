---
layout: post
title: "关于Linux 安装和卸载tar ball形式的程序"
date: 2015-03-16 12:11
comments: true
published: true
categories: "Linux"
---
  源码安装的一些NOTE:

1. 首先./configure --helps是可以看到所有编译选项的。
2. centos下，`yum install xx.rpm`，可以安装依赖，ubuntu下：`apt-get build-dep xx`
3. zsh下，./configure tab是会提示所有的编译选项的。
4. Makefile如果没有uninstall选项，更合理的办法似乎是：
	
	1. 先install到一个单独目录：

		find . -exec rm 安装目录/{} \;

	文件夹自然会失败。