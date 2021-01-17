---
title: Windows下64位PHP+Mysql+Apache的安装配置
author: Harry Chen
key: php-apache-mysql-configuration-under-windows-x64
layout: article

dsq_thread_id:
  - 1272359189
categories:
  - PHP
tags:
  - apache
  - mysql
  - php
  - x64
  - 配置
---

  实际上和32的差别并不大，写这篇文章的主要目的是给出可行的下载地址。


> PHPx64
>
> 
>
> Apachex64
>
> 
>
> Mysqlx64
>
> [http://dl-sh-ocn-1.pchome.net/0t/fw/mysql-essential-5.0.90-winx64.rar
][1]

  然后安装mysql，apache和php直接解压就行，php.ini做如下几处修改


    #扩展目录
    extension_dir = "../php/ext"
    #mysql扩展
    extension=php_mysql.dll
    #剩下的酌情自己配置

  httpd.conf做如下几处修改


    #主目录
    ServerRoot "D:/Program Files/httpd-2.2-x64"
    #LoadPHP的模块
    LoadModule php5_module "D:/Program Files/php/php5apache2_2.dll"
    PHPIniDir "D:/Program Files/php/"
    #文档目录
    DocumentRoot "d:/temporary/php"
    #文档目录的权限配置
    
    #默认访问文件名
    DirectoryIndex index.php default.php index.html
    #解析文档类型，这里很重要，否则无法解析php
    AddType application/x-httpd-php .php  .php4 .php5 .html

  拷贝libmysql.dll（mysql的bin目录下）到system32和apache的bin目录。

  以管理员身份运行命令行，执行如下命令

    httpd -k install

  在执行 httpd -k install 的时候，显示 The Apache2.2 service is successfully installed 表明已经安装成功。

  然后执行

    httpd -k start

  启动apache即可。


   [1]: http://dl-sh-ocn-1.pchome.net/0t/fw/mysql-essential-5.0.90-winx64.rar (http://dl-sh-ocn-1.pchome.net/0t/fw/mysql-essential-5.0.90-winx64.rar)
