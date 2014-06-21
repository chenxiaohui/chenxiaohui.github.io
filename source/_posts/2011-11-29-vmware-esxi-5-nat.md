---
title: VMware ESXi NAT实现
author: Harry Chen
layout: post

categories:
  - Others
  - 与技术相关
tags:
  - ESXi
  - NAT
  - pfSense
  - VMware
---
# 

  上节我们讲到VMware ESXi默认不支持NAT，但是我们如果只有一个外网端口映射，然后希望通过这个映射，从外网访问两台机器的话，那最好做NAT。这里我们通过一个开源的网络防火墙pfSense来实现NAT[1]。当然也有人通过Zental实现[2]，或SmoothWall神马的[3]。

![logo][1]

  首先建立一个NAT使用的虚拟交换机

![][2]

  弹出如下对话框的时候不要选择任何物理网卡，这个虚拟交换机是专门用来做NAT的。

![][3]

  改个名字

![][4]

  完成之后，你就有了两个可用的虚拟交换机。

![][5]

  然后建立pfSense的虚拟机，我们通过VMConverter来实现，这样更快一些。首先下载VMWare vCenter Converter ()，我们直接在本地运行Converter任务，然后向服务器上上传虚拟机文件，所以选择对应你本地操作系统的版本，安装的时候选择本地安装。然后下载pfSense，注意我们要下载Vmware Appliance版本，还记得之前说的Appliance概念吗，我们这里就通过Appliance简化安装。

![image][6]

  选择虚拟机文件 ，填入用户名，ip，和密码

![image][7]

  剩下的事情就不用操心了。

  启动pfSense虚拟机之前注意为pfSense系统添加网卡，NAT和原来的网络都要添加，![][8]

  之后启动pfSense，配置网络

![][9]

  结果大概是这样，具体的教程见[3]

![][10]

  最后指定虚拟操作系统的网络接口

![][11]

  剩下的NAT配置什么的，参考[4]吧。一系列教程，讲的非常详细了。教程里的图都来自[1]，这哥哥真帮了大忙了。

参考文献：

[1] Configuring NAT on ESX and ESXi,



[2] Configure NAT on Esxi Server,



[3] SmoothWall Express as NAT on ESXi



[4] pfSense学习



   [1]: http://www.roybit.com/wp-content/uploads/2011/11/logo_thumb.png (logo)
   [2]: http://blog.romant.net/wp-content/uploads/2010/07/Step2.png
   [3]: http://blog.romant.net/wp-content/uploads/2010/07/Step3_121.png
   [4]: http://blog.romant.net/wp-content/uploads/2010/07/Step3_13.png
   [5]: http://blog.romant.net/wp-content/uploads/2010/07/Step_last_summary_2.png
   [6]: http://www.roybit.com/wp-content/uploads/2011/11/image_thumb.png (image)
   [7]: http://www.roybit.com/wp-content/uploads/2011/11/image_thumb1.png (image)
   [8]: http://blog.romant.net/wp-content/uploads/2010/07/Step_last.png
   [9]: http://blog.romant.net/wp-content/uploads/2010/07/pfsense_config_2.png
   [10]: http://blog.romant.net/wp-content/uploads/2010/07/pfsense_summary.png
   [11]: http://blog.romant.net/wp-content/uploads/2010/07/client_network.png
