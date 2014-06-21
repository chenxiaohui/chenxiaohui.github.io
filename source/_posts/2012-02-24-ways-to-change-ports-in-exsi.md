---
title: ESXi修改默认端口的方法(zz)
author: Harry Chen
layout: post

dsq_thread_id:
  - 1257520092
categories:
  - Others
tags:
  - ESXi
  - 修改
  - 默认端口
---
# 

  转载自网络，找不到出处了，没试过，应该是对的。

  修改默认端口的方法： 端口 80 (http) 443 (https)
  root登录后

     vi /etc/vmware/hostd/proxy.xml

找到下添加以下内容

    custom port #
    custom port #

  保存文件

  重新启动vmware-hostd服务

        # service mgmt-vmware restart

  例子：添加以下为分别改为81 444

    81
    444

  ESX 4.0测试通过
