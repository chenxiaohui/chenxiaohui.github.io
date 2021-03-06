---
layout: article
title: "通过搭建代理来共享网络"
key: linux-proxy-setup
date: 2015-01-11 17:16
comments: true
published: true
categories: "Linux"
---
   遇到这样一个问题，开发机只有一台能上外网，其他的机器上手动更新依赖包简直是要死的感觉。尝试了如下几种方式：

   1. vpn
   	1. [pptp][2]
   	2. [openvpn][1]
   2. ssh反向代理（其实不是干这个事情的貌似）
   3. proxy

   开始一直不想用proxy，毕竟需要为yum什么的单独配置，不是所有的程序都会去读shell的http_proxy配置。但是vpn配置搞了一天都不成功。openvpn能连接，但是不能共享网络，大概是路由配错了，pptp linux下直接链接不上，可能是只用了chap的握手？反正没成功。最后还是配了proxy，配完才觉得proxy简单易行啊，大部分问题能解决，出现了特别的需求就单独为其设置代理好了。问题不大。

   tinyproxy的配置如下：

   	yum install tinyproxy

   	# vi /etc/tinyproxy/tinyproxy.conf
	  Allow 192.168.1.0/24 # 限制可以使用Proxy的来源网段
    ConnectPort 443 
	
  service tinyproxy start

    shell配置：
    export http_proxy='xxx:8888'
    export https_proxy='xxx:8888'

    yum配置：
    vi /etc/yum.conf
	  proxy=http://xxxx:8888

    maven配置:
     <proxies>
     <proxy>
        <id>example-proxy</id>
        <active>true</active>
        <protocol>http</protocol>
        <host>proxy.example.com</host>
        <port>8080</port>
        <username>proxyuser</username>
        <password>somepassword</password>
        <nonProxyHosts>www.google.com|*.example.com</nonProxyHosts>
      </proxy>
    </proxies>

    git配置：
    [http]
      proxy =xxxx:xx
    	

  配置难度真不是一个数量级的，可见有时候能满足大部分情况，就是最好的解决方案了。

  **补充：easy_install和pip是默认读取http_proxy的，但是一直不能连接。尝试了很久之后发现是sudo的问题，sudo环境没有执行.bashrc，所以root的http_proxy和当前用户的http_proxy都没有生效。su到root下就可以了。**

[1]: https://www.digitalocean.com/community/tutorials/how-to-setup-and-configure-an-openvpn-server-on-centos-6 "How to Setup and Configure an OpenVPN Server on CentOS 6 | DigitalOcean"
[2]: http://5323197.blog.51cto.com/5313197/1285738 " centos6.4 安装配置 pptp vpn"