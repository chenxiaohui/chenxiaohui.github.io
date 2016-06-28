---
layout: post
title: "用timecat来定位日志"
date: 2016-06-28 14:33
comments: true
published: true
categories: "Linux"
---
  

  介绍一个日志grep的神器。
  做系统开发的人都有从海量日志里面定位bug的经历，大家一般用如下几种方法：

1. head -n xxx|tail -n 1，大概定位位置
2. 直接grep日志来找到对应的行号并用sed cut一段出来。
3. 把日志灌倒hive等ETL工具里面。

  但是如上几种方式要么太慢，要么太复杂。最近突然想到有没有二分·grep的工具，搜到如下一个工具timcat:

  安装：

  	pip install timecat

  使用：

  	timecat -d '2016-01-02' -s '20:13:14' -e '20:14:13' LOGFILE1.log LOGFILE2.log ...
    timecat -s '2016-01-02 20:13:14' -e '2016-01-02 20:14:13' LOGFILE1.log LOGFILE2.log ...
	  For more: timecat -h

  非常快。

  作者的[博客][1]讲解如下：

###参考文献:

>\[1] 如何对日志文件进行二分查找？开源文件二分查找工具『timecat』介绍, <http://blog.reetsee.com/archives/502>

[1]: http://blog.reetsee.com/archives/502 "如何对日志文件进行二分查找？开源文件二分查找工具『timecat』介绍"