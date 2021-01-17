---
layout: article
title: "关于sendmail邮件服务器的搭建"
key: something-about-sendmail-setup
date: 2015-04-01 20:14
comments: true
published: true
categories: "Linux"
---

  还是reviewboard的事情，我们需要一个自己的邮件服务器来发通知邮件。sendmail是一个比较好的选择，搭建的方式很简单，安装sendmail，修改配置文件，修改local_host_name就行。如果不需要登陆验证，这样也就直接能用了。现在的问题是reviewboard是必须登陆验证的。至少看报错上是这样。

  	SMTPException: SMTP AUTH extension not supported by server. reviewboard
 
  具体代码没细看，但是应该默认都有认证，只是认证方式不一样。我们telnet到25端口，执行

  	ehlo localhost


 	/usr/sbin/testsaslauthd -u username -p sohutest

    mail -s "test" xxx@xxx.com <content.txt

<!--more-->

  如果邮件不能正常发送可以通过如下方式debug：

  	1. 查看/var/log/messages
  	2. 查看用户mail
  	3. 通过telnet模拟一下登陆发邮件的过程：

			HELO localhost
			AUTH LOGIN 
			aGFycnljaGVu
			password
			MAIL FROM:<test@xxx.com>
			RCPT TO:<username@xxx.com>
			DATA
			To: username@xxx.com
			From:test@xxx.com
			Subject:test mail
			From:test@xxx.com
			test body
			.
			quit

  安装reviewboard的过程还发现一个问题，邮件服务器已经可以正常发邮件了，reviewboard还是失败，看到如下报错：
	
	- Error sending e-mail notification with subject 'Review Request 2: [retrieval-ad][master][NewFeature] Readme' on behalf of '"UserName" <xxx@xxx.com>' to '"UserName" <xxx@xxx.com>,xxx@xxx.com'
	Traceback (most recent call last):
	  File "/opt/xxx/rb/lib/python2.7/site-packages/ReviewBoard-2.0.15-py2.7.egg/reviewboard/notifications/email.py", line 294, in send_review_mail
	    message.send()
	  File "/opt/xxx/rb/lib/python2.7/site-packages/Django-1.6.11-py2.7.egg/django/core/mail/message.py", line 276, in send
	    return self.get_connection(fail_silently).send_messages([self])
	  File "/opt/xxx/rb/lib/python2.7/site-packages/Django-1.6.11-py2.7.egg/django/core/mail/backends/smtp.py", line 87, in send_messages
	    new_conn_created = self.open()
	  File "/opt/xxx/rb/lib/python2.7/site-packages/Django-1.6.11-py2.7.egg/django/core/mail/backends/smtp.py", line 54, in open
	    self.connection.login(self.username, self.password)
	  File "/usr/local/lib/python2.7/smtplib.py", line 613, in login
	    raise SMTPAuthenticationError(code, resp)
	SMTPAuthenticationError: (535, '5.7.0 authentication failed')
  
  跟到如下smtplib.py里面看验证方法，调整了顺序（我这支持AUTH LOGIN PLAIN，没支持PAM)，然后保证用户名密码正确就基本可以使用了。

[1]: http://blog.sina.com.cn/s/blog_6b61ec070101e161.html "CentOS sendmail安装及邮件域名配置"
[2]: http://ju.outofmemory.cn/entry/12533   "testsaslauthd “authentication failed” 解决办法"