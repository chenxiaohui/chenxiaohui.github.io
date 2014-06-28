---
layout: post
title: "github/gitcafe pages域名设置"
date: 2014-06-28 18:17
comments: true
categories: "web相关"
---



# A纪录和CNAME

  裸域名只能绑定 DNS 的 A 记录，不能绑定 CNAME 记录。也就是说你不能把裸域设定为另外域名的别名。很多时候这对管理不是很方便，特别是使用第三方托管服务的时候。如果第三方迁移服务器导致 IP 地址变更，你必须自己去更改 DNS 的 A 记录。引用自参考文献[1][1]


### gitcafe pages 域名配置

	  cxh.me.			1684	IN	A	117.79.146.98

	  www.cxh.me.		3581	IN	CNAME	chenxiaohui.gitcafe.com.
	  chenxiaohui.gitcafe.com. 560	IN	A	117.79.146.98


### github pages 域名配置

	  cxh.me

	  www.cxh.me.   xxxx  IN  CNAME chenxiaohui.github.io.
	  chenxiaohui.github.io.  xxxx  IN  CNAME github.map.fastly.net.
	  github.map.fastly.net.  9 IN  A 103.245.222.133
	  
  同时配置CNAME文件，内容是裸域名

	  cxh.me

### dig和nslookup

    dig www.example.com +nostats +nocomments +nocmd
    nslookup 详见参考文献[2][2]

[1]: http://www.zhihu.com/question/20414602 "为什么越来越多的网站域名不加www了？"
[2]: http://www.ezloo.com/2011/04/a_mx_cname_txt_aaaa_ns.html "常用域名记录解释：A记录、MX记录、CNAME记录、TXT记录、AAAA记录、NS记录"

###参考文献:

>\[1] 为什么越来越多的网站域名不加www了？, <http://www.zhihu.com/question/20414602>

>\[2] 常用域名记录解释：A记录、MX记录、CNAME记录、TXT记录、AAAA记录、NS记录, <http://www.ezloo.com/2011/04/a_mx_cname_txt_aaaa_ns.html>

