---
layout: post
title: "mac下ffmpeg的编译"
date: 2015-03-01 11:08
comments: true
published: true
categories: "其他"
---

  基本步骤可以看[这个][1]，说两个问题：

  1. brew的formulae没有celt这个包。忽略了算了。

  2. libaacplus安装的时候，

  	1. 首先这个地址`http://217.20.164.161/~tipok/aacplus/libaacplus-2.0.2.tar.gz`已经失效了，从网上下载的话，这个版本还是有问题，configure的时候会卡住，一些patch丢失了好像。建议直接fork [github上的][2]。
  	2. 这个branch也有问题，frontend链接的时候会提示`ld: symbol(s) not found for architecture x86_64`，直接从Makefile.am里面把frontend去掉算了。

  3. 可以通过brew直接安装：

  		brew install ffmpeg --with-fdk-aac --with-ffplay --with-freetype --with-frei0r --with-libass --with-libvo-aacenc --with-libvorbis --with-libvpx --with-opencore-amr --with-openjpeg --with-opus --with-rtmpdump --with-schroedinger --with-speex --with-theora --with-tools

  4. Besides, 我发现brew可以列出configure选项，如下：

  		brew options xxx

  	手动安装的话，可以通过./configure --help来查看。


[1]: http://www.liaoxuefeng.com/article/0013738927837699a7f3407ea5f4b5caf8e1ab47997d7c5000   "Mac OS X编译ffmpeg"
[2]: https://github.com/Distrotech/libaacplus "Distrotech/libaacplus"