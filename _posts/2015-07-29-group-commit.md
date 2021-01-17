---
layout: article
title: "关于group commit"
key: group-commit
date: 2015-07-29 17:25
comments: true
published: true
categories: "分布式系统"
---
  最近突然想到这个东西，以前Oceanbase的UpdateServer提交的时候是做了group commit的。基本思路如下：

  1. 并发小的时候，超过一个时间窗口就直接提交
  2. 并发大的时候，等请求填满一个buffer再一起提交。

  实现上可以考虑如下伪代码：

  	while true:
  		start timer
  		if buffer full or timer reach limit:
  			commit
  			reset timer
  		else
  			wait and receive

  广泛运用在一些需要组合请求的地方，比如一些rpc因为历史原因（嗯）一直单条请求，不能改协议的情况下，可以考虑转发一下，做个缓冲。当然这种情况下一般是通过队列来缓冲请求压力。
