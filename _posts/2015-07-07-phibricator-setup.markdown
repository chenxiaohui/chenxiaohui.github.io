---
layout: article
title: "Phibricator搭建过程总结"
date: 2015-07-07 17:45
comments: true
published: true
categories: "PHP"
---

  [Phibricator][1]是Facebook开源的一体化项目管理、代码review工具，主要特点是集成度高、界面漂亮。根据搭建的经验看，确实做的非常完善，各种细节用起来像是商业产品，不会像其他的开源产品那么难以配置。这里把配置过程根据回忆写一下：

  官方给出过一个一键安装的脚本，但是下载的时候感觉有点问题吧，下载完不是sh而是网页，而且我只有一台机器，环境都已经预先有了，也不想再搭一套LAMP。这里我们以centos5为例：

  首先安装httpd + mysql + php，由于centos5的版本太低，yum源里的mysql和php均低于phibricator要求的版本，我们需要先升级yum源，参见[参考文献][2]， 不过好像安装的时候没有php53u，而是直接php53

  之后把对应的扩展也装了:

  	yum install php53-mbstring
	yum install php53-mysql

<!--more-->

  升级mysql到mysql5.5，参见[参考文献][3]。中间遇到两个问题:

1. mysql 启动失败，提示没有权限创建pid。su到mysql用户下发现/var/run目录mysql用户没有execute的权限：
	
	usermod +x /var/run

	给目录加execute的权限

2. mysql_upgrade失败，直接提示FATAL ERROR:Upgrade failed，发现用户名密码的问题，root@localhost密码没变，root@127.0.0.1在升级之后好像没有密码了

	SET PASSWORD FOR 'root'@'127.0.0.1' = PASSWORD('newpass');	

	重新设置密码。

  之后去/var/www/html安装源码:
  	
  	$ git clone https://github.com/phacility/libphutil.git
	$ git clone https://github.com/phacility/arcanist.git
	$ git clone https://github.com/phacility/phabricator.git

  顺便装上一些别的php扩展：
  
  	sudo yum install pcre-devel
  	sudo yum install php-pear
  	sudo yum install php53-process
	sudo pecl install apc
 
  主要是提升性能的。然后配置httpd.conf


	<VirtualHost *>
	  # Change this to the domain which points to your host.
	  ServerName phabricator.example.com

	  # Change this to the path where you put 'phabricator' when you checked it
	  # out from GitHub when following the Installation Guide.
	  #
	  # Make sure you include "/webroot" at the end!
	  DocumentRoot /path/to/phabricator/webroot

	  RewriteEngine on
	  RewriteRule ^/rsrc/(.*)     -                       [L,QSA]
	  RewriteRule ^/favicon.ico   -                       [L,QSA]
	  RewriteRule ^(.*)$          /index.php?__path__=$1  [B,L,QSA]
	</VirtualHost>
  
  最后一个Rule的B在我的httpd下不识别，所以直接去掉了，貌似没什么影响...重启之后到phibricator的源码目录执行：

  	phabricator/ $ ./bin/storage upgrade

  按照提示可以配置mysql 用户名密码，之后可以看到建立了数据库结构。这时候访问host就能看到界面了。先注册管理员进去，能够看到一系列的TIPs，说明需要配置的地方。Phibricator在这方面非常人性化，按照提示一点点配置就可以了。直到解决大部分的warning。剩下的问题就是注册用户和邮件了。

  首先在auth上开启认证方式，这里我们还是比较传统，选择了用户名密码的方式，你也可以选择其他账号体系打通的方式。一个用户注册之后，管理员需要批准用户，这个用户才能登陆。我找了好久，才发现原来批准在这位置：

  ![](/images/2015/approval-queue.png)


  最后是配置邮件服务器。首先你需要有个本地的或者其他提供商提供的邮件服务器。可以参考[这里][4]，PHP Mailer设置：

	phpmailer.mailer: set to "smtp".
	phpmailer.smtp-host: smtp.xxx.com
	phpmailer.smtp-port: 25
	phpmailer.smtp-user: xxxx
	phpmailer.smtp-password: xxxx

  之后重启daemon应该就能发送邮件了。删除用户非常有意思，ph只允许从命令行删除

  	phabricator/ $ ./bin/remove destroy @harrychen
  
  之后会有一个有意思的界面：

![](/images/2015/delete-user.png)



[1]: http://phabricator.org/   "Phibricator官网"
[2]: http://zengrong.net/post/1595.htm "升级CentOS 5.x中的PHP 5.1到5.3"
[3]: http://www.ha97.com/4145.html "RHEL/CentOS 5.x使用yum快速安装MySQL 5.5.x"
[4]: http://blog.csdn.net/lihongxun945/article/details/9030753 "phabricator 邮件服务配置 备忘"
