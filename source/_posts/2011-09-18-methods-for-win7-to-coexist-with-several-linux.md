---
title: Win7与多Linux并存的安装方法
author: Harry Chen
layout: post
permalink: /methods-for-win7-to-coexist-with-several-linux/
categories:
  - Linux
tags:
  - fedora
  - grub
  - Linux
  - ubuntu
  - win7
  - 多系统
  - 安装
---
# 

网上有很多使用EasyBCD从Win7下安装linux的方法，不过用来用去觉得EasyBCD还是有些问题，比如我装Fedora64就一直报错，而做成安装U盘就可以。而且大多数Linux在EasyBCD安装的时候都要求iso文件存放于Fat32的分区里，作为一个已经装了Win7的孩纸，在硬盘上划出一块Fat32的分区实属令人发指的行为。

这里推荐一个Linux官方的安装方法，首先下载Universal-USB-Installer，这文件很小，但是五脏俱全，包括了你可能见到的所有的Linux的……呃，选项。当然这软件还可以用来做Windows的安装盘。傻瓜化操作就不说了，不过记得每个选项对应一种Linux，包含了各种发行版，下载的iso最好不要改名，免得找不到。

安装的事情仁者见仁，修复Grub的问题智者见智。最简单的办法是先装Win7，因为Win7是不鸟各种Linux的（丫挺的），然后装个个版本的Linux，不过不要装GrubLoader，也就是不要把启动信息写入Mbr，最后装Ubuntu，伟大的乌邦图会识别各种Linux系统然后建立启动菜单。

当然你也可以先安装Ubuntu，然后装其他的Linux，同样不要安装Grub Loader，最后在Ubuntu下手动配置grub.cfg来驱动，不过最好的办法是使用


    sudo update-grub

让Ubuntu自动识别安装的Linux系统，你会看到激动人心的类似于如下界面的结果：![Screenshot-cxh@cxh-ThinkPad-T420_ ~][1]

如果想让Win7默认启动，可以在ubuntu下执行


    sudo mv /etc/grub.d/30_os-prober /etc/grub.d/06_os-prober

然后同上Update Grub就可以了。

   [1]: http://www.roybit.com/wp-content/uploads/2011/09/ScreenshotcxhcxhThinkPadT420__thumb.png (Screenshot-cxh@cxh-ThinkPad-T420_ ~)
