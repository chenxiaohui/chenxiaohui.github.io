---
layout: post
title: "关于sendmail邮件服务器的搭建"
date: 2015-04-01 20:14
comments: true
published: true
categories: "Linux"
---

  还是reviewboard的事情，我们需要一个自己的邮件服务器来发通知邮件。sendmail是一个比较好的选择，搭建的方式很简单，安装sendmail，修改配置文件，修改local_host_name就行。如果不需要登陆验证，这样也就直接能用了。现在的问题是reviewboard是必须登陆验证的。至少看报错上是这样。

  	SMTPException: SMTP AUTH extension not supported by server. reviewboard
 
  具体代码没细看，但是应该默认都有认证，只是认证方式不一样。我们telnet到25端口，执行

  	ehlo localhost

  发现250 AUTH没有支持



[1]: http://ju.outofmemory.cn/entry/12533   "testsaslauthd “authentication failed” 解决办法"
[2]: