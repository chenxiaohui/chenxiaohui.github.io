---
layout: article
title: "github/gitcafe pages域名设置"
date: 2014-06-28 18:17
comments: true
categories: "web相关"
---



### A纪录和CNAME

  裸域名只能绑定 DNS 的 A 记录，不能绑定 CNAME 记录。也就是说你不能把裸域设定为另外域名的别名。很多时候这对管理不是很方便，特别是使用第三方托管服务的时候。如果第三方迁移服务器导致 IP 地址变更，你必须自己去更改 DNS 的 A 记录。引用自参考文献[1][1]


### gitcafe pages 域名配置

	  example.com.			1684	IN	A	117.79.146.98

	  www.example.com.		3581	IN	CNAME	example.gitcafe.com.
	  example.gitcafe.com. 560	IN	A	117.79.146.98

  gitcafe文档说：
 	
  如果你想绑定 www 子域名, 你需要将此 www 子域名添加到自定义域名里, 然后在你的域名管理页面增加一条 A 记录, 将它指向 GitCafe 服务器的 IP 地址 117.79.146.98

<!--more-->

### github pages 域名配置


	;example.com
	example.com.   73  IN  A 192.30.252.153
	example.com.   73  IN  A 192.30.252.154

	www.example.com.   xxxx  IN  CNAME example.github.io.
	example.github.io.  xxxx  IN  CNAME github.map.fastly.net.
	github.map.fastly.net.  9 IN  A 103.245.222.133
	  
  同时配置CNAME文件:

  * If your CNAME file contains example.com, then www.example.com will redirect to example.com.
  
  * If your CNAME file contains www.example.com, then example.com will redirect to www.example.com.

  也就是说如果同时配置了A纪录和CNAME，那么对www的访问会重定向到主域名，或者主域名的访问重定向到www。本质上是301 redirect。

### dig和nslookup

    dig www.example.com +nostats +nocomments +nocmd
    nslookup 详见参考文献[2][2]

[1]: http://www.zhihu.com/question/20414602 "为什么越来越多的网站域名不加www了？"
[2]: http://www.ezloo.com/2011/04/a_mx_cname_txt_aaaa_ns.html "常用域名记录解释：A记录、MX记录、CNAME记录、TXT记录、AAAA记录、NS记录"
[3]: https://help.github.com/articles/tips-for-configuring-a-cname-record-with-your-dns-provider "Tips for configuring a CNAME record with your DNS provider"

#### 参考文献:

  \[1] 为什么越来越多的网站域名不加www了？, <http://www.zhihu.com/question/20414602>
 
  \[2] 常用域名记录解释：A记录、MX记录、CNAME记录、TXT记录、AAAA记录、NS记录, <http://www.ezloo.com/2011/04/a_mx_cname_txt_aaaa_ns.html>
 
  \[3] Tips for configuring a CNAME record with your DNS provider, <https://help.github.com/articles/tips-for-configuring-a-cname-record-with-your-dns-provider>
