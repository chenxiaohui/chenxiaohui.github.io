---
layout: article
title: "reviewboard的安装"
key: review-board-setup
date: 2015-03-28 21:15
comments: true
published: true
categories: "Python"
---

  [reviewboard][1]是群众喜闻乐见的代码review工具。安装过程详见[文档1][2][文档2][3]。这些写一些遇到的问题：

1. 默认支持版本是django 1.6，最新的django1.7不支持。所以最好用virtualenv独立出一个环境来。

2. 官方文档的apache不知道是怎样的目录结构，反正我自己安装的apache和yum install的都跟官方的目录结构不太一样。

	1. copy或者link apache-wsgi.conf到conf.d目录，etc/httpd结构如下

		![](/assets/images/2015/etc_httpd.png)

	2. 配置下PythonHome

		WSGIPythonHome /opt/harrychen/rb
		#WSGIPythonPath /var/www/reviewboard:/opt/harrychen/rb/lib/python2.7/site-packages

	3. WSGIPythonPath [文档][7]里说最好还是配置一下，但是有PythonHome貌似就行了

	4. 按提示给一些目录加权限。

	5. rb-site install，建议直接放到var下，reviewboard的结构跟apache的默认/var/www下类似的。

<!--more-->

3. yum install mod_wsgi所安装的mod_wsgi版本默认对应的还是2.6的python，所以不会去2.7的环境下找site-package，建议手动安装mod_wsgi。apache 安装mod_wsgi的过程参见[文档][4]。网上也看到过[这个问题][5]。

4. apache log报错：couldn't perform authentication. AuthType not set!: /。

	貌似2.4之后才支持 Require all granted ，直接删掉。

5. django报错：ERROR: Invalid HTTP_HOST header: '10.16.10.74'.You may need to add u'10.16.10.74' to ALLOWED_HOSTS.

 	这个问题当然不见得都会遇到，是我安装的时候想随意绑一个域名，然后本地用hosts指过去，再搞搞dns欺骗啥的大家就都可以用这个伪域名了，但是django非debug模式好像对这个要求很严...直接用ip就好。详见[这里][6]

6. the executable "git" is not in the path. 修改/etc/sysconfig/httpd加入环境变量/

	apache没有环境变量。参见[文献8].

7. ServerLog：SMTPException: SMTP AUTH extension not supported by server.

	详见另一篇[文章][9]。

8. 开始搭建的时候post上去总是报错：Got API Error 224 (HTTP code 400): The specified diff file could not be parsed 。

	开始怀疑是git权限，重新申请了git账号，用reviewboard自己生成的私钥公钥，结果一样。而且有的repo是正常的，后来想到可以手动diff，发现diff里面有修改的时候会报错，新增文件不会。网上搜到这个[讨论][9]，发现git（至少我安装的版本）不支持对某个commit下某个文件的访问，而reviewboard的逻辑实际上是先根据diff文件提取base revision，然后打上patch来显示两边的diff，这样就需要根据revisionid和filename来随机访问文件。查阅[文档10][10] 发现gitweb协议支持，按照gitweb和公司github的格式，填写Raw file URL mask，就可以正常访问了。格式大概是：

		git地址：git@github.xxx.com:username/xxx.git

		gitweb地址：http://git.kernel.org/?p=username/xx.git;a=blob_plain;f=\<filename\>;h=\<revision\>




[1]: https://www.reviewboard.org   "Review Board"
[2]: https://www.reviewboard.org/docs/manual/2.5/admin/installation/creating-sites/ "Creating a Review Board Site"
[3]: https://www.reviewboard.org/docs/manual/2.5/admin/installation/linux/ "Installing on Linux"
[4]: http://cxh.me/2015/02/27/django-to-apache/ "Django Mod_wsgi配置的一些问题"
[5]: http://m.oschina.net/blog/341289 "mod_wsgi在多个Python版本下配置apache"
[6]: http://www.zijin5.com/django-1-5-debug-false/ "django 1.5 当DEBUG设置为 False时网页打不开的解决办法"
[7]: https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/modwsgi/ "How to use Django with Apache and mod_wsgi"
[8]: http://serverfault.com/questions/151328/setting-apache2-path-environment-variable "Setting Apache2 PATH environment variable"
[9]: https://groups.google.com/forum/#!msg/reviewboard/13BAerbTT7g/84uAp6VZ6fEJ "Error uploading new diff: fatal: Not a git repository: 'None'"
[10]: https://www.reviewboard.org/docs/manual/2.0/admin/configuration/repositories/ "Repositories"

###Bibliography:

  \[1] Review Board, <https://www.reviewboard.org>

  \[2] Creating a Review Board Site, <https://www.reviewboard.org/docs/manual/2.5/admin/installation/creating-sites/>

  \[3] Installing on Linux, <https://www.reviewboard.org/docs/manual/2.5/admin/installation/linux/>

  \[4] Django Mod_wsgi配置的一些问题, <http://cxh.me/2015/02/27/django-to-apache/>

  \[5] mod_wsgi在多个Python版本下配置apache, <http://m.oschina.net/blog/341289>

  \[6] django 1.5 当DEBUG设置为 False时网页打不开的解决办法, <http://www.zijin5.com/django-1-5-debug-false/>

  \[7] How to use Django with Apache and mod_wsgi" , <https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/modwsgi/>

  \[8] Setting Apache2 PATH environment variable, <http://serverfault.com/questions/151328/setting-apache2-path-environment-variable>

  \[9] Error uploading new diff: fatal: Not a git repository: 'None', <https://groups.google.com/forum/#!msg/reviewboard/13BAerbTT7g/84uAp6VZ6fEJ>

  \[10] Repositories, <https://www.reviewboard.org/docs/manual/2.0/admin/configuration/repositories/>
