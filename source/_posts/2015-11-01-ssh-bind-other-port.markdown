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

  补充两个SSH技巧：

  1. 客户端配置中转，主要是通过跳板机登录：

		Host xx
		HostName 192.168.1.1
		User xx
		ProxyCommand ssh -q xxx@login2.xxx.xx nc %h %p

  2. 保持会话。 ssh会在.ssh目录下生成一个会话选项，下次登录同一个server公用会话，不需要验证。

		Host *
		ControlMaster auto
		ControlPath ~/.ssh/master-%r@%h:%p

	上面会话共享，所以不能关闭会话。可以通过 `ssh -fN xxx` 把第一个会话放到后台不退出

