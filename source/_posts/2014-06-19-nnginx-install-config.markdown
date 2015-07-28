---
layout: post
title: "Nginx 安装配置总结"
date: 2014-06-19 11:57
comments: true
categories: "web相关"
---


具体的可以看参考文献里面的三篇博客，中间遇到一个问题，nignx提示无法找到php文件。主要有两个原因：

1. 确定nginx工作线程的启动用户有权限访问www-root，需要修改nginx.conf的这里：

		user  www-data;

2. 确定www-root配置正确，需要修改这里：           

		fastcgi_param  SCRIPT_FILENAME  $document_root$fastcgi_script_name;




[1]: http://www.nginx.cn/591.html   "nginx配置入门"
[2]: http://www.nginx.cn/install "Nginx安装"
[3]: http://www.nginx.cn/231.html "nginx php-fpm安装配置"

###参考文献:

  \[1] nginx配置入门, <http://www.nginx.cn/591.html>

  \[2] Nginx安装, <http://www.nginx.cn/install>

  \[3] nginx php-fpm安装配置, <http://www.nginx.cn/231.html>
