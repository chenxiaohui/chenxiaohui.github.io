---
layout: article
title: "有关coredump没有符号的问题"
key: glibc-no-symbol-problem
date: 2016-06-06 15:02
comments: true
published: true
categories: "Linux"
---

  线上server core掉了，看dmesg能看到core的日志，

    s3store[16586]: segfault at 2a28000 ip 00007fda20543b58 sp 00007fd9e9894128 error 4 in libc-2.12.so[7fda204ba000+18a000]

  但是/proc/sys/kernel/core_pattern指向的位置并没有core文件，改一下core_pattern再跑应该能core出来，不过并不是稳定复现的。所以只能先凭这条日志来分析了。从core的位置看，大概率应该是malloc里面的问题。用

    addr2line -e xxx  00007fda20543b58

  看到的结果是??:0。怀疑是glibc没有调试信息。看一下系统的glibc版本：
  
	rpm -qa |grep glibc
	glibc-common-2.12-1.166.el6_7.7.x86_64
	glibc-static-2.12-1.166.el6_7.7.x86_64
	glibc-2.12-1.166.el6_7.7.x86_64
	glibc-devel-2.12-1.166.el6_7.7.x86_64
	glibc-debuginfo-common-2.12-1.166.el6_7.7.x86_64
	glibc-headers-2.12-1.166.el6_7.7.x86_64
	glibc-debuginfo-2.12-1.166.el6_7.7.x86_64

  去centos网站上下对应版本的glibc debuginfo并安装
  
    http://debuginfo.centos.org/6/x86_64/
    wget http://debuginfo.centos.org/6/x86_64/glibc-debuginfo-2.12-1.166.el6_7.7.x86_64.rpm
    wget http://debuginfo.centos.org/6/x86_64/glibc-debuginfo-common-2.12-1.166.el6_7.7.x86_64.rpm
    rpm -ivh glibc-debuginfo-common-2.12-1.166.el6_7.7.x86_64.rpm
    rpm -ivh  glibc-debuginfo-2.12-1.166.el6_7.7.x86_64.rpm

  之后继续addr2line -e xxx 00007fda20543b58还是没有...
 
  我擦嘞。改天继续。