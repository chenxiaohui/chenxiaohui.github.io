---
layout: post
title: "Thrift依赖和Slf4j"
date: 2014-12-25 18:24
comments: true
publised: true
categories: "其他"
---
  
  用Thrift做一个分布式系统的RPC，发现跑起来的时候总提示`Failed to load class org.slf4j.impl.StaticLoggerBinder`，看了看maven依赖感觉没啥问题啊，slf4j-api-xx.jar好好的在呢。分析了maven的依赖，eclipse的问题，最后发现都没问题啊。最后发现还是不了解slf4j，以为跟log4j一样的，其实作为一个proxy，slf4j-api只是一套接口，实现的依赖没有添加进来。

   Thrift的依赖加进来的时候（如下），Dependency Hierachy解析会添加相关的包，但是只添加了slf4j-api，动态编译也不会出错，毕竟接口都有了，但是运行时从classpath找不到对应的包。

	  <dependency>
	  	<groupId>org.apache.thrift</groupId>
	  	<artifactId>libthrift</artifactId>
	  	<version>0.8.0</version>
	  </dependency>

  在上面的基础上要加入一个任意一个slf4j-api的实现：

	Placing one (and only one) of slf4j-nop.jar, slf4j-simple.jar, slf4j-log4j12.jar, slf4j-jdk14.jar or logback-classic.jar on the class path should solve the problem.

  每个实现详见[参考文献2][2]

[1]: http://www.slf4j.org/codes.html#StaticLoggerBinder   "SLF4J warning or error messages and their meanings"
[2]: http://blog.csdn.net/robert_mm/article/details/8197108 " slf4j-api、slf4j-log4j12以及log4j之间什么关系？"