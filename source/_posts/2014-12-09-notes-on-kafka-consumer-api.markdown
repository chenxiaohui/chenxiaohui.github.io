---
layout: post
title: "kafka Consumer API几个问题"
date: 2014-12-09 10:12
comments: true
published: true
categories: "分布式系统"
---


  一直不理解这里的topicCountMap是什么意思。kafka的High Level Consumer API设计实在是比较费解。源码又比较费解。

	Map<String, Integer> topicCountMap = new HashMap<String, Integer>();
	topicCountMap.put(topic, new Integer(1));
	Map<String, List<KafkaStream<byte[], byte[]>>> consumerMap = consumer.createMessageStreams(topicCountMap);
	List<KafkaStream<byte[], byte[]>> streams = consumerMap.get(topic);

  后来查阅到这是跟线程相关的，指定消费每个topic的线程数，然后kafka consumer connector会建立对应的stream流。每个线程对应于一个KafkaStream。一个多线程消费的例子见[参考文献][1].

[1]: http://www.cnblogs.com/fxjwind/p/3794255.html   "Kafka Consumer接口"

###参考文献:

>\[1] Kafka Consumer接口, <http://www.cnblogs.com/fxjwind/p/3794255.html>
