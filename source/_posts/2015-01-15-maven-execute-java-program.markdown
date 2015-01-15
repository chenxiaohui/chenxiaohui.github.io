---
layout: post
title: "用maven执行java程序"
date: 2015-01-15 17:08
comments: true
published: true
categories: "Java"
---

  Eclipse中需要执行一个java程序的之后只需要在入口类Run就行，但是有时候需要同时开两个程序，尤其对C/S模式的应用来说。针对这种情况，可以分如下三种方式启动另一个程序：

  1. java -cp 指定的类。shell（或者ZSH才有）下貌似是会有提示如下：

  {% img img-polaroid center /images/2015/javacp.png %}

  以上方式至少需要保证用到的jar都在classpath中。 

  2. 从eclipse中copy执行命令。去调试页面，查看刚才执行的command的属性页面。会看到如下界面，copy命令到shell中执行即可。

  {% img img-polaroid center /images/2015/eclipse_command.png %}

  3. maven execute。 命令类似：
	
		mvn exec:java -Dexec.mainClass=boot.BootStrap

   	注意是第二个exec后是点，不是：，另外如果有多模块，在root project下需要加module:

   		mvn exec:java -pl xxx -Dexec.mainClass=boot.BootStrap 