---
layout: post
title: "django mod_wsgi配置的一些问题"
date: 2015-02-27 13:39
comments: true
published: true
categories: "web相关"
---

  安装apache不说了，用apache做django容器的时候（详见[参考文献1][1])遇到如下几个问题，记录一下：

1. apxs找不到。centos上直接装的httpd-2.2.3-83.el5_10，默认没有apxs。想源码编译一个apache，结果发现源里面有。

  	yum install -y httpd-devel

2. /usr/local/lib/libpython2.7.a: could not read symbols: Bad value

    错误提示里面已经说了，libpython2.7.a没有动态编译。下了一个python2.7的源码，重新编译安装一下。
        ./configure --prefix=/usr/local/  –enable-shared CFLAGS=-fPIC
        make
        make install

3. ImportError: libpython2.7.so.1.0: cannot open shared object file: No such file or directory

    库路径问题，要么配置LD_LIBRARY_PATH，要么修改ld.so.conf然后ldconfig

4. / not found.

    httpd.conf配置：
        WSGIScriptAlias / /var/www/html/mysite/mysite/django.wsgi
        <Directory /var/www/html/mysite>
            Order allow,deny
            Allow from all
        </Directory> 


5. log/errro_log中 No module named mysite.settings。

    wsgi配置：
        import sys
        sys.path.append("/var/www/html/mysite/")

  6. Cannot load /etc/httpd/modules/mod_ldap.rso into server: /etc/httpd/modules/mod_ldap.so: undefined symbol: apr_ldap_ssl_init

    大概是说httpd编译的apr版本和系统的版本不一致，查看httpd -V 显示：

        Server loaded:  APR 1.4.6, APR-Util 1.5.2
        Compiled using: APR 1.2.7, APR-Util 1.2.7

    尝试降级apr：

        yum downgrade apr-util

    或者指到别的apr版本上去，修改环境变量：

        export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64 

    我不知道httpd是否会去加载当前环境变量，所以顺便删了/etc/ld.so.conf里面的两行
        
        /usr/local/apr/lib
        /usr/local/apr-util/lib
        然后ldconfig   

    让apr走系统的版本。





[1]: http://www.cnblogs.com/fengzheng/p/3619406.html   "Linux下安装Apache并以mod_wsgi方式部署django站点"

###Bibliography:

  \[1] Linux下安装Apache并以mod_wsgi方式部署django站点, <http://www.cnblogs.com/fengzheng/p/3619406.html>
