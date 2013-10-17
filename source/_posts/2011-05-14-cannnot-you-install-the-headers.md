---
title: 万水千山总是情，预装下header行不行？
author: Harry Chen
layout: post

categories:
  - Linux
tags:
  - glibc-headers
  - preprocessor fails sanity check
  - RedHat
  - rpm
---
# 

晚上安装Ngix总是遇到一个问题，如下图

![image][1]

也就是"**C preprocessor "/lib/cpp" fails sanity check”**错误，网上怎么说的都有，随便一搜索就是一堆问题，历尽千辛万苦，装了一堆乱七八糟的rpm包（我是RedHat AS4），差点就换个内核了，最后在发现是glibc-headers没装，最后在RedHat第三张盘里发现了glibc-headers的rpm，如下

![image][2] 问题是这么重要的东西，为什么就不预装一下，甚至软件管理那里都没有它的选项….

哎，万水千山总是情，预装下header行不行？

   [1]: http://www.roybit.com/wp-content/uploads/2011/05/image_thumb.png (image)
   [2]: http://www.roybit.com/wp-content/uploads/2011/05/image_thumb1.png (image)
