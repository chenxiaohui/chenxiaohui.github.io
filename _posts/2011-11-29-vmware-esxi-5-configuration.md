---
title: VMware ESXi 5安装配置部分
author: Harry Chen
layout: article

dsq_thread_id:
  - 1256850131
categories:
  - Others
  - 与技术相关
tags:
  - Dell R710
  - iDRAC
  - Sphere Client
  - VMware ESXi
  - 安装配置
---
# 

  折腾了两天，终于搞懂了是怎么回事了。这里写一下详细配置，给其他像我这样的小白一个参考。

  首先明确一下ESXi是干嘛的。

> VMware ESXi是VMware的嵌入式hypervisor。ESXi没有服务控制台，可以说是一个精简版的ESX。对于由于成本和硬件还没有开始实施虚拟化的组织来说，使用免费的VMware ESXi hypervisor不失为着手虚拟化的好方式。[3]
>
> ![VMware ESXi ¥i¦bµw¥ó¤Wª½±µ¹B¦æ][1]
>
> 图1：VMware ESX系列架构[1]

  而ESXi可以看做ESX Server的轻量化版本。

  两者的区别见文献[2]，还有一个非常不错的专题[3]

  我在一台Dell R710服务器上搭建了一个ESXi Server，同时运行两台服务器，一台RHEL5.4，一台Win2K8。详细过程如下：

  首先需要注意的是很多服务器购买的时候，内置软件有远程管理模块。比如DELL的iDRAC，实际上来讲，用处不大，而且iDRAC占用着一些端口（比如HTTPS 443），导致我安装了ESXi之后一度连接不上也看不到web提示页面。这里我们先禁用iDRAC。从System Setup进入Dell内置管理系统，然后不给iDRAC配置IP地址（原则上讲开始是没有配置IP的，但是大部分人的习惯是进去把IP配置了，I suppose）。之后在管理系统里建立RAID，注意RAID1是热备份的，相当于你只有一半硬盘空间可用。然后选择安装操作系统，系统类型选择ESXi 4，放入系统光盘。实际上我从官网下载（[https://www.vmware.com/cn/tryvmware/?p=free-esxi5&lp=default][2]）了ESXi5，但不影响。ESXi安装可以参考[4]，绝对通俗易懂。

  进入ESXi之后可以选择开启SSH和ESXiShell，这样你就可以远程登陆到ESXi做点很底层的事情，至于ESXiShell，这是个定制的Shell，里面只保留了一部分的Linux命令，然后加入了一部分ESXi自己的命令。传说ESXi需要用账号unsupported登陆，而这个unsupported本身是不受服务支持的，改坏了自己负责。但是实际上用root登陆就行了。

  其实最常用的还是VMware Sphere Client，虽然官方有命令行工具Sphere CLI，但是大部分人不会去使用。安装完ESXi之后，浏览器输入IP应该就能看到一个页面了。然后用Sphere Client登陆之后可以做相应操作，比如安装操作系统什么的。

  这里一定要注意一个问题，安装操作系统的时候不能断开Sphere Client，我在这问题上2了很久，后来才想到原来是这个原因。就像远程桌面连接拷东西的时候不能退出一样，这东西不会后台自动运行的，退出，就没了。

  下一讲讲一下ESXi的网络配置，欢迎关注。转载请注明出处。

参考文献：

[1] 產品方案 – VMware – ESXi 入門教學，


[2] ESX还是ESXi？这也是个问题，


[3] 虚拟化hypervisor：VMware ESXi全面解析，


[4]Vmware_ESXI_4.0_安装详解(图文)，

