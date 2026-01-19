---
layout: article
title: "Eclipse调试的时候出现class not found"
key: eclipse-class-not-found
date: 2015-01-05 09:50
comments: true
published: true
categories: "java"
---
  昨天遇到这样一个问题：

  ![](https://harrychen.oss-cn-beijing.aliyuncs.com/blog-images/2015/classnotfound.png)

  开始以为是依赖的问题，更新了所有的jar包和Maven依赖，发现没有什么问题。怀疑是eclipse，写了一个简单的程序，发现一样找不到class。

  解决办法是先把breakpoint里面的ClassNotFoundException: caught and uncaught去掉了。不知道为什么会造成这个结果。

  ![](https://harrychen.oss-cn-beijing.aliyuncs.com/blog-images/2015/breakpoint.png)