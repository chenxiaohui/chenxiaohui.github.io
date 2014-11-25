---
layout: post
title: "kafka配置入门"
date: 2014-11-20 14:21
comments: true
categories: "分布式系统"
---

producer
metadata.broker.list=localhost:9092,localhost:9093


consumer group


bin/zookeeper-server-start.sh config/zookeeper.properties >/dev/null 2>&1 &
env JMX_PORT=9999 bin/kafka-server-start.sh config/server1.properties >/dev/null 2>&1 &
env JMX_PORT=10000 bin/kafka-server-start.sh config/server2.properties >/dev/null 2>&1 &
sleep 5
bin/kafka-topics.sh --zookeeper localhost:2181 --create --topic mytopic --partitions 2 --replication-factor 2
 #bin/kafka-console-producer.sh --broker-list localhost:9092,localhost:9093 --topic mytopic
#bin/kafka-console-consumer.sh --zookeeper localhost:2181 --topic mytopic --from-beginning
