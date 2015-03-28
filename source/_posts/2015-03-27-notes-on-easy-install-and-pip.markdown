---
layout: post
title: "easy_install和pip的注意事项"
date: 2015-03-27 11:13
comments: true
published: true
categories: "Python"
---
   
  关于安装目录：

    dist-packages instead of site-packages. Third party Python software installed from Debian packages goes into dist-packages, not site-packages. This is to reduce conflict between the system Python, and any from-source Python build you might install manually.

    dist-packages取代了site-packages。从Debian安装包安装的第三方的Python软件 被 安装到 dist-packages,不是 site-packages.这是为了减少，系统自带python 和 你手动安装的python 之间的冲突。

    不过我感觉都在site-packages下...

  删除包：

  	pip uninstall packageName
  	#自动删除
  	easy_install -mxN packageName
  	#手动删除

  显示安装的包：

  	pip list
  	easy_install只能去安装目录看了。实际上是共享的。

  另外需要注意的就是不同的Python版本下会有不同的easy_install和pip，比如easy_install3/pip3等。

    pip -V 可以显示当前pip是针对哪个Python版本的

  可以用virtualenv来分离不同的环境。