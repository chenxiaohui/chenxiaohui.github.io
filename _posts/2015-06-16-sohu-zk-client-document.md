---
layout: article
title: "基于zookeeper的配置管理客户端"
key: sohu-zk-client-document
date: 2015-06-16 16:28
comments: true
published: true
categories: "分布式系统"
---



### 名词解释：
  
  SeviceConfig:
    一个服务的所有配置存在一个目录下
  BucketConfig:
     Bucket的配置存在一个单独的子目录中

### 配置项类型：

  - Integer
  - Long
  - Short
  - Float
  - Double
  - Byte[]
  - Boolean
  - String
  - 自定义配置项 ConfigObject

###使用说明：

####POM：

    <dependency>
      <groupId>com.sohu.adrd</groupId>
      <artifactId>sohu-zk-client</artifactId>
      <version>1.0.1</version>
    </dependency>

####初始化 

  ServiceConfig.Instance().init("ConnectString", "serviceName");//如果做测试可以用10.16.3.61:2181
  
  ServiceConfig.Instance().init("serviceName"); 默认使用肖永磊的zk地址

####配置项使用

  先给默认值

    private static long exploitDiscardTimespan = 7 * 86400L;

  可以保存个Instance()的引用

    private ServiceConfig serviceConfig = ServiceConfig.Instance();

  所有引用到的地方，通过如下方式取配置项（这是默认config）：

   serviceConfig.getLong("exploitDiscardTimespan", exploitDiscardTimespan)

  如果是BucketConfig(bucketConfig会在zookeeper上根目录下再增加一个Node，名字是bucket的名字，在此之下存储config)

   serviceConfig.Bucket("bucketName").getLong("exploitDiscardTimespan", exploitDiscardTimespan)

  这样server端更新配置的时候，serviceConfig会根据通知刷新自己的配置缓存，下次使用getLong的时候就得到了新的配置。

  上述getLong的过程包含了：

  1. 如果是Bucket配置，从Bucket中获取，如果找不到，从Service的配置获取，如果还是没有，返回默认值。

  2. 对于返回默认值的情况，写回Zookeeper。

  3. 如果Zookeeper端有修改，Zkclient会收到消息，重新update本地配置项的缓存。

  4. 如果定义了handler调用handler，如下所述：

  如果需要根据配置修改的通知来做出响应（这是默认事件，node_data_change)：

    ServiceConfig.Instance().addEventListener("task_period", new IEventHandler() {
      @Override
      public void process(ZkEvent event) {
        logger.info("update task period.");
        setDeclaredField(TimerTask.class, ServerTasks.this, "period", ServiceConfig.Instance().getLong("task_period", period));  
      }
    });

  如果需要删除的通知：

      ServiceConfig.Instance().addEventListener("task_period", EventType.NodeDeleted, new IEventHandler() {
      @Override
      public void process(ZkEvent event) {
        logger.info("update task period.");
        setDeclaredField(TimerTask.class, ServerTasks.this, "period", ServiceConfig.Instance().getLong("task_period", period));  
      }
    });


#### 结合SpringFramework：

    基本不变，只不过SpringFramework会先填充InitializingBean的域，这些值只有在出默认值的时候才会被采用。