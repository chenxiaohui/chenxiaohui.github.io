---
title: VMware ESXi 网络配置
author: Harry Chen
layout: post
permalink: /vmware-esxi-5-network-configuration/
categories:
  - Others
  - 与技术相关
tags:
  - NAT
  - VMware vCenter
  - WorkStation
  - 桥接
  - 虚拟交换机
---
# 

上一讲忘了扯一下vCenter，大家应该经常会看到Sphere vCenter，这个是用来管理多台ESX(i) Server的，换句话说，是虚拟云的管理端，详见官方白皮书[1]。所以如果你只有一台服务器，大可不必搭理。另外大家应该也经常看到VMware Appliance这种名字，实际上就是装好的VMWare虚拟机镜像，我们可以用VMware Converter安装到远程服务器上。这个之后我们也会提到。

现在我们搭建了好了ESXi Server，同时建立了虚拟机，现在开始为虚拟机配置网络。ESXi的网络理念和VMware WorkStation完全不一样，我们在WorkStation里用的那一套[3]没法在这里用。ESXi Server里，你能看到类似于这样的网络拓扑结构，虚拟交换机的概念替代了之前的三种网络模式，具体概念参见[2]。我们可以简单理解，ESXi把物理交换机完全屏蔽了，你可以建立一台虚拟交换机，然后也不需要考虑这台虚拟交换机的接口问题，直接进操作系统配置你的IP就行了，你可以想想虚拟机就是一台跟物理机一样的机器，甚至这个管理端口Management Network的IP也是可以随便换的，至于为什么ESXi能随意绑定IP，可以想见，应该也是通过了Bridge桥接技术，通过把网卡设置为混杂模式，用类似于ARP欺骗的技术来实现桥接。

![1][1]

样例可参考[4]，需要说明的是，每个适配器相当于一个网卡，虽然你可以不指定，一个操作系统，添加了多个虚拟网络之后，就相当于有了多个网卡，每个网卡按照应该遵循的配置来配置，至于NAT，ESXi默认不支持NAT，所以如果有NAT，一定是路由器给你做的。所以作者在WAN适配器配置外网IP，LAN配置局域网IP，PAN配置服务器内网IP。相当于三块网卡。

下一讲讲ESXi的NAT实现。转载请注明出处。

参考文献：

[1] VMware vCenter Server



[2] VMware Virtual Networking Concepts



[3] VMware网络配置详解



[4] ESXi虚拟网络配置的几点认识



   [1]: http://www.roybit.com/wp-content/uploads/2011/11/1_thumb.png (1)
