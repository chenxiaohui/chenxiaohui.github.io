---
layout: article
title: "关于ubuntu gnome下crontab运行的问题"
key: ubuntu-gnome-crontab
date: 2015-03-24 13:54
comments: true
published: true
categories: "Linux"
---

  今天想在gnome下运行一个自动关机前的提示，发现crontab根本不起作用啊。以为是路径和root权限的问题，但是路径没问题，而且root的crontab必须要sudo crontab -e的，也就是说crontab还是执行在当前用户下。

  后来发现对图形界面程序来讲，crontab的进程需要指定输出到哪个显示的，也就是

   	export DISPLAY=:0 #:0指第一个显示终端，ctrl+alt+f7那个
	/usr/bin/notify-send "亲，该去运动了！！一分钟后关机，请保存所有未保存的Job."
	sudo shutdown -h 1


  或者直接在crontab -e中指定环境变量：

   	DISPLAY=:0
	30 20 * * * /home/cxh/repo/scripts/shutdown.sh

  可以顺便制定一下其他变量

	SHELL=/bin/bash
	PATH=/sbin:/bin:/usr/sbin:/usr/bin
	MAILTO=cxh #如果出现错误，或者有数据输出，数据作为邮件发给这个帐号
	HOME=/home/cxh #使用者运行的路径,这里是根目录

  crontab出错的信息会发邮件到对应用户，mail或者cat /var/mail/$USER查看。d *清理。

