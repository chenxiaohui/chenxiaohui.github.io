---
title: 关于Django url映射的一些小问题
author: Harry Chen
layout: post
permalink: /some-problems-of-django-url-mapping/
mkd_text:
  - |
    之前写Django一直没想着去用patterns的prefix，偶然用的时候发现总不起作用，后来才发觉原来是写法的问题
    
    	:::python
    	urlpatterns = patterns('book.views', 
    		(r'^(\w+).html$', 'default_render'),
    	)
    
    <!--more-->
    
    在这种情况下肯定是没问题的，但是不排除会有同学跟我一样的写成如下的格式
    
    	:::python
    	urlpatterns = patterns('book.views', 
    		(r'^(\w+).html$', default_render),
    	)
    看到差别了吧，只有字符串才可以拼接嘛。
    
    另外是关于Django 1.4之后的路径的问题，每个app被放到跟主project同级的目录，所以引用的时候都变成与project同级的模块。比如有一个叫test的project，那么test里的urls.py必然是test.urls，而某个app里的urls.py显然已经不是test.app.urls而是app.urls了。
    
    纯mark之。水文勿喷....
dsq_thread_id:
  - 1256058711
categories:
  - Python
tags:
  - Django url python
format: standard
---
# 

之前写Django一直没想着去用patterns的prefix，偶然用的时候发现总不起作用，后来才发觉原来是写法的问题


    urlpatterns = patterns('book.views',
        (r'^(\w ).html$', 'default_render'),
    )


在这种情况下肯定是没问题的，但是不排除会有同学跟我一样的写成如下的格式


    urlpatterns = patterns('book.views',
        (r'^(\w ).html$', default_render),
    )


看到差别了吧，只有字符串才可以拼接嘛。

另外是关于Django 1.4之后的路径的问题，每个app被放到跟主project同级的目录，所以引用的时候都变成与project同级的模块。比如有一个叫test的project，那么test里的urls.py必然是test.urls，而某个app里的urls.py显然已经不是test.app.urls而是app.urls了。

纯mark之。水文勿喷….