---
layout: article
title: "分布式调试系列之行为模拟"
key: use-mock-to-debug
date: 2013-11-21 17:31
comments: true
categories: "Oceanbase"
---

  最近调试分布式系统，感觉实际上什么看日志的方式都不如带集群调试，当然有些行为是比较难以模拟的，可能的情况下，要么重现环境，要么对部分模块做mock。单测带来的便利性是远超过不做mock省下的时间的，比如与sql相关的逻辑完全可以启动一个完整的sql环境，然后把请求发过去，看回来的响应。至于其他的部分，基本的原则是减少变量。比如两个server之间的通信，同时检测两个server只能看日志，所以最好能mock一个server的行为，这样减少调试的不确定性。

