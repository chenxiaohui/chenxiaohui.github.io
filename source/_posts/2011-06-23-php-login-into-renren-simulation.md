---
title: PHP模拟登陆人人
author: Harry Chen
layout: post

dsq_thread_id:
  - 1257043911
categories:
  - PHP
tags:
  - Curl
  - php
  - 人人
  - 模拟登陆
---
# 

PHP的Curl组件可以完成模拟http请求并获取返回结果的功能，并支持SSL和cookie，我们可以用Curl模拟登陆一个网站，并获取登陆后的结果。这里我们用人人做个测试。人人实现了与开心账号互通之后，增加了一个验证服务器，所以需要先到验证服务器验证并获取跳转链接，同时保存cookie，之后请求网页的时候都加上cookie即可。

代码见附件，主要需要注意的几点如下：

  1. 登陆Https网站需要PHP支持SSL并生成服务器认可的证书。
  2. 设置CURLOPT_FOLLOWLOCATION的目的是登陆成功后直接按照返回的跳转值跳转，并抓取之后的页面。
  1. 代码
[这里][1]下载。

  1. 参考文献：

> [1] willko，cURL 二次封装的类库Curl_Manager，
>
> [2] tianxin，php 使用curl模拟登录人人(校内)网，

   [1]: http://www.roybit.com/wp-content/uploads/2011/06/curl.rar (curl)
