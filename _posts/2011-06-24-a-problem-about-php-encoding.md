---
title: 关于php编码一个弱弱的问题
author: Harry Chen
key: a-problem-about-php-encoding
layout: article

categories:
  - PHP
tags:
  - php
  - xpath
  - 编码
---

  晚上调Xpath的一个程序，从网页里读出来的数据然后显示到网页一直是乱码……乱码啊乱码……都快疯了，最后发现从来没想过这个问题：

  你echo回来的网页，浏览器凭什么知道你的编码?

  于是乎，指定一下header，保证跟你echo到网页的编码一致，就OK了……这个问题好囧。

>
>     header("Content-type: text/html; charset=gb2312");
