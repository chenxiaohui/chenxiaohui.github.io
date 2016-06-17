---
layout: post
title: "使用nfs挂载网络磁盘"
date: 2016-06-17 11:58
comments: true
published: true
categories: "Linux"
---

  分布式环境下经常需要到各个节点启动server，常见的方式推的方式，比如scp到各个结点，但是有时候更新的文件少儿需要scp的文件比较多。这时候可以选择nfs挂载的方式把编译好的文件放到网络磁盘上，然后共享到其他的服务器，这样可以按需使用。

  首先配置一下nfs服务器。假设系统都是centos：

    yum install -y nfs-utils
    yum install -y portmap
    rpm -qa | grep nfs
   
  事实上看centos6.5以上portmap应该被rpcbind替代了，而已安装nfs-utils的时候应该顺便安装了rpcbind。之后配置一下需要挂载的磁盘：

    文件/etc/exports:
    /tmp rz*(rw,async) yf*(ro)

  简单解释一下： /tmp是挂载的目录路径，后面跟权限控制，可以是主机名或者ip，rz*表示rz开头的主机，括号里面是权限。整条语句表示把/tmp目录共享以rw权限和async方式共享给rz开头的机器，同时以ro权限共享给yf开头的机器。

  之后启动nfs服务：

    service nfs start

  需要挂载机器上同样安装客户端：

    yum install -y nfs-utils
  
  挂载到指定的目录：

    mkdir fs && mount -t nfs xxx.xxx.xx.xx:/tmp ./fs

  xxx指定机器名或者ip
