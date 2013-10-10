---
layout: post
title: "霸气风骚的系统监视器htop"
date: 2013-10-10 20:12
comments: true
categories: Linux
---

做测试和运维的同学都比较熟悉top工具，top工具提供了强大的系统性能监视能力，但是top毕竟比较简陋，而服务器端又不能运行需要X的程序，所以需要一款更人性更强大的系统监视器。HTOP就是一个很好的选择。

###介绍

> htop 是Linux系统中的一个互动的进程查看器，一个文本模式的应用程序(在控制台或者X终端中)，需要ncurses。

> 与Linux传统的top相比，htop更加人性化。它可让用户交互式操作，支持颜色主题，可横向或纵向滚动浏览进程列表，并支持鼠标操作。

> 与top相比，htop有以下优点：

> * 可以横向或纵向滚动浏览进程列表，以便看到所有的进程和完整的命令行。
> * 在启动上，比top 更快。
> * 杀进程时不需要输入进程号。
> * htop 支持鼠标操作。

> htop 官网：http://htop.sourceforge.net/

###截图

{% img img-ploaroid /images/2013-10/htop.png  "htop截图" "htop截图" %}

###安装

####Ubuntu

	sudo apt-get install htop

####RHEL/CentOS

#####CentOS 5.x
	
	32位系统选择：
	rpm -ivh http://download.fedoraproject.org/pub/epel/5/i386/epel-release-5-4.noarch.rpm
	64位系统选择：
	rpm -ivh http://download.fedoraproject.org/pub/epel/5/x86_64/epel-release-5-4.noarch.rpm
	导入key
	rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL

#####CentOS 6.x

	32位系统选择：
	rpm -ivh http://download.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm
	64位系统选择：
	rpm -ivh http://download.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
	导入key：
	rpm --import /etc/pki/rpm-gpg/RPM-GPG-KEY-EPEL-6

最后执行

	yum install htop

####源码安装

	wget http://nchc.dl.sourceforge.net/project/htop/htop/1.0.1/htop-1.0.1.tar.gz
	tar zxvf htop-1.0.1.tar.gz
	cd htop-1.0.1
	./configure
	make
	make install

###参考文献：

> [1] （原创）htop：一款比top强悍好用的进程管理监控工具, http://www.ha97.com/4075.html