---
layout: post
title: "logrotate版本问题"
date: 2016-05-18 16:02
comments: true
published: true
categories: "Linux"
---

  线上运维过程中切日志用了logrotate，但无奈日志打的太多，一天的日志几十G难以分析，遂决定改成每小时切分一次日志。从logrotate的说明看有hourly的支持，但是直接把daily改成hourly之后启动报错：

   	unknown option 'hourly'

  感觉是logrotate 3.8.7的版本不支持hourly语法

  rpm安装logrotate高版本的包提示缺少fillup和其他的依赖，同时glibc的版本也要求高版本。于是下载了logrotate的源码安装，以最新版本3.9.2为例

    ./autogen.sh
    ./configure
  
  提示缺少libpopt头文件，下载了libpopt 1.5的源码安装，提示libtool版本不对。我擦嘞。

  后来突然想到libpopt是debian下的命名，试一下centos下

    yum install popt-devel -y

  搞定。于是继续源码安装，直接用logrotate的官网版本好了。

    yum install popt-devel -y
    wget https://fedorahosted.org/releases/l/o/logrotate/logrotate-3.8.6.tar.gz
    tar zxvf  logrotate-3.8.6.tar.gz
    cd logrotate-3.8.6 && make && make install

  这个版本是可以稳定使用的。中间试了几个别的版本，3.8.3还是不支持hourly语法，3.8.5支持了语法，但是测试的时候

    logrotate -d /etc/logrotate.conf

  有core，跟进源码去感觉是依赖bug，换到3.8.6终于ok了...回去看作者更新日志：

    3.8.4 -> 3.8.5
         - Improved rotation during daylight saving time and between timezone
           changes.
         - Fixed ACL setting problem caused by ext3 erroneously reporting ENOSYS
           instead of ENOSUP.
         - Do not continue with rotation if state file is corrupted.
         - Make logrotate.status creation atomic.
         - Allow "hourly" rotation. See manpage for more information.
         - Use "/bin/echo" in tests. Fixes tests execution in Dash.
         - Do no try to parse config files bigger than 16MB.
         - Improved manpage consistency and formatting.
         - Fix race condition between acl_set_fd() and fchmod().
