---
layout: article
title: "关于eclipse里面override上的warning"
date: 2014-12-08 16:53
comments: true
published: true
categories: "java"
---

  写一个Thrift的调用。生成的Thrift代码在eclipse里面打开就报错。如下：

  ![](center /images/2014/method_callback.png  )

  看AsyncMethodCallback的代码，没有任何问题啊：

  ![](center /images/2014/async_callback.png  )

  后来发现当前项目JRE的版本是1.5，~~貌似1.5的JRE有个bug~。切到1.6以上版本就可以了。原因如下：

	Eclipse is defaulting to Java 1.5 and you have classes implementing interface methods (which in Java 1.6 can be annotated with @Override, but in Java 1.5 can only be applied to methods overriding a superclass method).

  如果依然有问题，可以直接改一下Compliance Level：

  ![](/images/2014/compliance.png)
