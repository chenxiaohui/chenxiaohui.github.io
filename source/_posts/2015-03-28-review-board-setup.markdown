---
layout: post
title: "reviewboard的安装"
date: 2015-03-28 21:15
comments: true
published: true
categories: "Python"
---
  
  [reviewboard][1]是群众喜闻乐见的代码review工具。安装过程详见[文档1][2][文档2][3]。这些写一些遇到的问题：

1. 默认支持版本是django 1.6，最新的django1.7不支持。所以最好用virtualenv独立出一个环境来。

2. 官方文档的apache不知道是怎样的目录结构，反正我自己安装的apache和yum install的都跟官方的目录结构不太一样。 

3. yum install mod_wsgi所安装的mod_wsgi版本默认对应的还是2.6的python，所以不会去2.7的环境下找site-package，建议手动安装mod_wsgi。apache 安装mod_wsgi的过程参见[文档][4]。网上也看到过这个问题[]

4. 










[1]: https://www.reviewboard.org   "Review Board"
[2]: https://www.reviewboard.org/docs/manual/2.5/admin/installation/creating-sites/ "Creating a Review Board Site"
[3]: https://www.reviewboard.org/docs/manual/2.5/admin/installation/linux/ "Installing on Linux"
[4]: http://cxh.me/2015/02/27/django-to-apache/ "Django Mod_wsgi配置的一些问题"
[5]: http://m.oschina.net/blog/341289 "mod_wsgi在多个Python版本下配置apache"