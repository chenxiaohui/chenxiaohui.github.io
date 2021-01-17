---
title: VMware ESXi 管理端口的NAT配置
author: Harry Chen
key: vmware-esxi-5-nat-on-admin-ports
layout: article

dsq_thread_id:
  - 1256549045
categories:
  - Others
tags:
  - ESXi
  - NAT
  - pfSense
  - 管理端口
---
# 

  先复习一下VMWare的基本网络概念。

  VMware ESXi使用桥接（猜测，错了不管）的方式实现网络配置，通过虚拟交换机的概念来模拟物理交换机，这样连接在同一个交换机下的虚拟机相当于处于一个网段之内，如下图所示，管理端口和pfSense（NAT系统）处于一个网段，pfSense添加了两个虚拟交换机，这样就等于接通了两个网段，起NAT的作用，WAN口处于8网段，LAN口在1网段做DHCP，其他两个操作系统（win2k8和RHEL5.4）只连接内网，通过pfSense做NAT到这些虚拟机上。

  ![1.png][1]

  接着说为什么要重做NAT。前几篇文章我们已经实现了一个ESXi上的NAT架构，但新的问题出现了：之前管理端口（8.232）是单独的一个IP，而我们的服务器搭建好之后往往只绑定一个外网IP，然后就远程管理了，这样如果管理端口还使用一个单独的内网IP，我们从外网就没有办法使用Sphere Client管理了。于是需要把管理端口也放到NAT的内网，从NAT映射到管理端口上去。

  首先，ESXi本身使用两个端口（不考虑SSH），一个443端口放一个简单的介绍网页（https），剩下的是Sphere Client使用的端口902（ESX Server好像是903），如果想更改端口，更改方式在下篇文章中再谈。

  这样我们需要做的是，首先在NAT的虚拟交换机中添加VMKernel

  ![1][2]

  设置好内网IP ，更改默认网关

  ![2][3]

  这时候其实就可以进内网的一个操作系统(比如我的win2k8)，telnet一下192.168.1.4的902端口，看看是否可以使用了，如果可以使用，在这个操作系统下就可以用Sphere Client连接ESXi了，只不过有点慢。

  开始的时候我直接在pfSense做了NAT（443和902，到192.168.1.4上），结果发现外网根本telnet不了这两个端口，最后想想干脆把标准交换机0上的那个192.168.8.232的Management Network移除好了，关掉了过程中弹出的几个语气严厉的警告窗口之后，再telnet，就可以使用了。这时候如果到物理服务器上，f2进入ESXi的配置界面，就可以看到Network Configuration那里已经改成了192.168.1.4的IP和192.168.1.1的网关。

  这样，你的管理端口，几个虚拟机就都进入了pfSense的管辖范围里了，也就是说，从公网IP映射到pfSense的WAN口IP，剩下的NAT都是pfSense来做了，无论是ESXi本身，还是其上的虚拟机。最后的网络配置如下，Management Network移除之后不会消失，但是已经没有IP显示了。

  ![3][4]

   [1]: http://www.roybit.com/wp-content/uploads/2011/11/1.png
   [2]: http://www.roybit.com/wp-content/uploads/2012/02/1_thumb.jpg (1)
   [3]: http://www.roybit.com/wp-content/uploads/2012/02/2_thumb.jpg (2)
   [4]: http://www.roybit.com/wp-content/uploads/2012/02/3_thumb.jpg (3)
