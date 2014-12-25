---
layout: post
title: "关于eclipse里面override上的warning"
date: 2014-12-08 16:53
comments: true
publised: true
categories: "其他"
---

  写一个Thrift的调用。生成的Thrift代码在eclipse里面打开就报错。如下：

  {% img center /images/2014/method_callback.png   %}

  看AsyncMethodCallback的代码，没有任何问题啊：

  {% img center /images/2014/async_callback.png   %}

  后来发现当前项目JRE的版本是1.5，貌似1.5的JRE有个bug。切到1.6以上版本就可以了。

  如果依然有问题，可以直接改一下Compliance Level：

  {% img img-polaroid center /images/2014/compliance.png %}