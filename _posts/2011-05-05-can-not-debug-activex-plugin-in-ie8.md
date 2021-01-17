---
title: IE8无法调试ActiveX控件的问题
author: Harry Chen
layout: article

dsq_thread_id:
  - 1256072487
categories:
  - Others
tags:
  - ActiveX
  - IE8
  - 单进程
  - 断点
  - 调试
---

  最近调ActiveX控件，发现总是无法停到一个断点去，这不坑爹呢？

  后来找来找去，发现IE8 默认是多进程工作的，通过修改注册表可以改为单进程工作，多进程的时候，启动的ie进程和加载要调试的ocx的ie进程不是一个进程，所以不能调试。

  注册表操作如下：

> Windows Registry Editor Version 5.00
[HKEY_CURRENT_USER\Software\Microsoft\Internet Explorer\Main]
"TabProcGrowth"=dword:00000000

  参考文献：

[1] VC做的OCX控件，IE下断点调试问题,

[2] IE8调试VC6的OCX控件不能进入断点问题解决方法


