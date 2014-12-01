---
layout: post
title: "redis-copy的使用"
date: 2014-12-01 17:01
comments: true
publised: true
categories: "分布式系统"
---

  有时候我们需要迁移redis的数据，从本质上看，这基本上是个rehash的过程。我们这里使用[redis-copy][1]实现。

  简单写一下步骤。首先得有ruby环境，然后直接安装：

  	gem install redis-copy

  可能会遇到几个包缺失的问题，如果有报错，安装如下几个包：

  	gem install redis
  	gem install hiredis
  	gem install recommendify

  简单测试一下redis-copy

  首先建立source和dest redis server：

  	redis-server redis.src.conf //6379 port
  	redis-server redis.dst.conf //6380 port

  redis.conf里面换一下端口就行了。写入几个值

  	redis-cli -h localhost  -p 6379
  	select 1
  	set mykey myvalue

  然后拷贝src里面db1的所有键值到dst的默认db(0).

  	sudo redis-copy localhost:6379/1 localhost:6380

  去dst redis看一下就行了。

  	redis-cli -h localhost -p 6380
  	keys *

  可以看到之前的key-value拷贝过来了。大数据量下的表现明天测一下。

[1]: https://github.com/yaauie/redis-copy   "redis-copy"

###参考文献:

>\[1] redis-copy, <https://github.com/yaauie/redis-copy>