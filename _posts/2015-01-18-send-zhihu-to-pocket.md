---
layout: article
title: "保存知乎日报到pocket"
key: send-zhihu-to-pocket
date: 2015-01-18 15:30
comments: true
published: true
categories: "web相关"
---
  知乎日报是中国人民喜闻乐见的资讯类应用，Pocket是深受世界人民喜爱的阅读工具。鉴于反碎片化阅读的个人习惯，决定把散落在各个地方的有价值咨询集中到一个应用里面，于是有了如下的工具。

  首先我们要parse知乎日报的URL。按照官方的说法每天三次投放，那抓一次就行了。直接用了[sed工具][1]。

	curl -s http://daily.zhihu.com | sed 's/<a href="\(http:\/\/daily.zhihu.com\/story[^"]*\)"/\n\1\n/g' |grep 'http://daily.zhihu.com/story'

<!--more-->
  
  然后需要打通跟Pocket的渠道。首先去注册Pocket SDK <http://getpocket.com/developer/>

  ![](https://harrychen.oss-cn-beijing.aliyuncs.com/blog-images/2015/pocket.png)

  将会得到如下的几个授权码。我只注册了Web和Desktop

  	NAME	PLATFORM	CONSUMER KEY
	ZhihuDaily2Pocket	Web	xxxx-xxxxxxxxxxxxxxxxxxxx
	ZhihuDaily2Pocket	Desktop (other)	xxxx-xxxxxxxxxxxxxxxxxxxx


  之后先请求pocket的consumer key：

  	curl -s -X POST  -H "X-Accept: Application/json" -H "Content-Type: application/json"  -d '{"consumer_key":"xxxx-xxxxxxxxxxxxxxxxxxxx","redirect_uri":"http://google.com"}'  https://getpocket.com/v3/oauth/request | grep '}' | python -mjson.tool

  这里需要注意Accept头部使用的是X-Accept，这是我之前死活得不到相应的原因。

  返回结果类似于：

	HTTP/1.1 200 OK
	Content-Type: application/x-www-form-urlencoded
	Status: 200 OK

	code=dcba4321-dcba-4321-dcba-4321dc
  
  如果是web应用，这里可以把用户导向一个授权页面了。

	https://getpocket.com/auth/authorize?request_token=dcba4321-dcba-4321-dcba-4321dc&redirect_uri=http://google.com
  
  授权后，我们把code和consumerkey转换成access token：

  	curl -s http://getpocket.com/v3/oauth/authorize -X POST -H "Content-Type: application/json" -H "X-Accept: application/json" -d '{"consumer_key":"xxxx-xxxxxxxxxxxxxxxxxxxx","code":"dcba4321-dcba-4321-dcba-4321dc"}'

  得到类似如下的结果：

	HTTP/1.1 200 OK
	Content-Type: application/x-www-form-urlencoded
	Status: 200 OK

	access_token=5678defg-5678-defg-5678-defg56&
	username=pocketuser

  根据这个access_token可以添加新的url了。

  	curl -s http://getpocket.com/v3/add -X POST -H "Content-Type: application/json" -H "X-Accept: application/json" -d '{"consumer_key":"xxxx-xxxxxxxxxxxxxxxxxxxx", "access_token":"yyyy-yyyy-yyyy-yyyy-yyyy","url":"http://daily.zhihu.com/story/4437286"}'


  之前授权流程完成之后，作为某个特定用户，之后的请求指令就不会变话了。所以程序可以简化到如下：

	curl -s http://daily.zhihu.com | sed 's/<a href="\(http:\/\/daily.zhihu.com\/story[^"]*\)"/\n\1\n/g' |grep 'http://daily.zhihu.com/story' |
	while read line
	do
		curl -s http://getpocket.com/v3/add -X POST -H "Content-Type: application/json" -H "X-Accept: application/json" -d '{"consumer_key":"xxxx-xxxxxxxxxxxxxxxxxxx", "access_token":"yyyy-yyyy-yyyy-yyyy-yyyy","url":"'$line'"}'|python -mjson.tool| grep 'resolved_url'
	done 
  
  添加个定时任务到cron中就行了。

  **当然最后我发现IFTTT是个更简单的方案.....**


[1]: http://coolshell.cn/articles/9104.htm   "sed 简明教程"
[2]: http://getpocket.com/developer/docs "Pocket API Documentation"
#### 参考文献:

  \[1] sed 简明教程, <http://coolshell.cn/articles/9104.htm>
  
  \[2] Pocket API Documentation, <http://getpocket.com/developer/docs>
