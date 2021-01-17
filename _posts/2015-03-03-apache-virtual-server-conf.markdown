---
layout: article
title: "Apache的Virtual Server配置"
date: 2015-03-03 20:12
comments: true
published: true
categories: "web相关"
---
  首先，virtual server的概念是说一个apache实例可以模拟出多个server，这些server通过不同的标识来区分（网卡IP/ServerName/端口/ServerPath)，每个虚拟的server最终对应到一个DocumentRoot。

  我们期望如下配置

  		80 	 -> / 	 		网站
  			    /mysite 	子网站mysite
  		8080 ->	/ 			网站news_auth

  配置如下：

<!--more-->

	<VirtualHost *:80>
	    ServerName 127.0.0.1
	    DocumentRoot /var/www/html/mysite/
	    ServerPath /mysite
	    WSGIScriptAlias /mysite /var/www/html/mysite/mysite/wsgi.py
	    <Directory /var/www/html/mysite/>
	        Order deny,allow 
	        Allow from all
	    </Directory>
	    <Location "/static/">
	         SetHandler None
	    </Location>
	</VirtualHost>

	<VirtualHost *:80>
	    ServerName 127.0.0.1
	    DocumentRoot /var/www/html
	    ServerPath /

	    <Directory /var/www/html>
	        Order deny,allow 
	        Allow from all
	    </Directory>

	</VirtualHost>


	<VirtualHost *:8080>
	    ServerName 127.0.0.1
	    DocumentRoot /var/www/html/news_auth
	    ServerPath /

	    WSGIScriptAlias / /var/www/html/news_auth/news_auth/wsgi.py
	    <Directory /var/www/html/news_auth/>
	        Order deny,allow 
	        Allow from all
	    </Directory>

	    <Location "/static/">
	         SetHandler None
	    </Location>
	</VirtualHost>


  一二节的顺序是不能颠倒的，否则apache把/mysite作为路径处理。这里还有个问题，static和其他引用url的处理，django下建议使用[url][1]/[static][2]标签

[1]: http://www.yihaomen.com/article/python/355.htm   "Django url 标签的使用"
[2]: https://docs.djangoproject.com/en/1.7/howto/static-files/ "Managing static files (CSS, images)"