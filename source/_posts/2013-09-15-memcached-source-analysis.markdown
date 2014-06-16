---
layout: post
title: "memcached源码分析-内存管理"
date: 2013-09-15 18:29
comments: true
categories: memcached源码分析
---

Memcached是一套分布式的缓存系统, 对于WEB应用来讲, Memcached的引入可以减少对于数据库等的请求, 从而减少应用响应时间, 提高吞吐量. 国外类似的实现有Redis等. 国内有淘宝自主研发的tair系统等.

memcached的源码实现很优雅, 相对于其他的开源系统, 比如nginx\apache等, memcached的实现并不复杂, 是一份很好的教材. 这里我们分几部分分析一下memcached的源码. (基于memcached 1.4.0)

###基本源码结构

主要的源码有:

* memcached.c: 系统入口, 并完成初始化等工作, 通过libevent建立连接, 并

//TODO
