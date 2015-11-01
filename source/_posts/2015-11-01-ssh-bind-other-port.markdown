---
layout: post
title: "ssh绑定其他端口"
date: 2015-11-01 14:14
comments: true
published: true
categories: "Linux"
---
  首先修改/ssh/sshd_config，把Port 22解注释，然后加一行Port xx。之后修改 /etc/sysconfig/iptables，加入该端口的Rules:

	-A INPUT -m state --state NEW -m tcp -p tcp --dport xx -j ACCEPT  

  重启即可。
 
	/etc/init.d/sshd restart

  这么做的目的是如果出现问题，还有一个端口可以上去修改。登录的时候需要对应的指定一下端口：

    ssh -p xx user@host
    scp -P xx ... user@host