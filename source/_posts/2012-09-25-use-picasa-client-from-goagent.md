---
title: 通过goagent使用Picasa客户端
author: Harry Chen
layout: post

mkd_text:
  - |
    goagent这一神器就不多说了，配置详见[goagent教程][1]。这里主要探讨picasa客户端使用代理的问题。
    
    <!--more-->
    
    picasa本身的代理设置只有一个用户名和密码，不明所以，所以一直用[hosts文件的方法][2]，但是后来发现配置里还有一项“自动检测网络设置”，勾选之后只要在系统里设置好goagent代理（PS，Internet选项那里，Linux没试，Linux下也没有picasa端吧），就可以使用代理上传照片了。
    
    
    最后吐槽一下：picasa也是google神器了，更有牛逼的人脸识别，但自从picasa相册编程google plus相册之后，就有了很多纠结的问题。比如我只是想把认识的人圈点一下，结果你非要在Google Plus群发一条消息，这如何是我等低调之人所能容忍的。算了，picasa相册还是当网盘使好了。
    
    
    [1]: http://maolihui.com/goagent-detailed-version-of-the-tutorial.html "goagent教程详细版"
    [2]:http://www.williamlong.info/blog/archives/409.html "Picasa相册的HOSTS文件"
dsq_thread_id:
  - 1256532136
categories:
  - 挨踢人生
tags:
  - goagent
  - picasa
format: standard
---
# 

goagent这一神器就不多说了，配置详见[goagent教程][1]。这里主要探讨picasa客户端使用代理的问题。

picasa本身的代理设置只有一个用户名和密码，不明所以，所以一直用[hosts文件的方法][2]，但是后来发现配置里还有一项“自动检测网络设置”，勾选之后只要在系统里设置好goagent代理（PS，Internet选项那里，Linux没试，Linux下也没有picasa端吧），就可以使用代理上传照片了。

最后吐槽一下：picasa也是google神器了，更有牛逼的人脸识别，但自从picasa相册编程google plus相册之后，就有了很多纠结的问题。比如我只是想把认识的人圈点一下，结果你非要在Google Plus群发一条消息，这如何是我等低调之人所能容忍的。算了，picasa相册还是当网盘使好了。

   [1]: http://maolihui.com/goagent-detailed-version-of-the-tutorial.html (goagent教程详细版)
   [2]: http://www.williamlong.info/blog/archives/409.html (Picasa相册的HOSTS文件)
