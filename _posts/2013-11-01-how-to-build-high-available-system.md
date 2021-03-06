---
layout: article
title: "如何构建按高可用系统（分享的笔记）"
key: how-to-build-high-available-system
date: 2013-11-01 18:42
comments: true
categories: "Oceanbase"
---

版权所有：[解伦师兄][1]

###介绍篇

**可用性vs可靠性**

  可用性主要是从时间的角度看，可靠的时间。可靠性主要是看不可用的频率。如果一个系统1小时宕机1ms，可用性非常高，可靠性非常低。

  可用性可靠性是系统的工程，设计开发，管理，运维等等。

  宕机几大因素：软件-硬件-网络-人为

  data loss的最大因素：drop table, 所以要做好充分的容错。

<!-- more -->

###设计篇

**减少故障发生的可能**

  避免单点故障，防止扩散，有效的监控运维配合


  常见的**冗余**设计。

>* RAID,Replica,Erasure Code
* BackUp, Reassign,Retry
* Master-Slave,Mirror,RAC..

  减少对外部系统强依赖

>  * 缓存
  * 异步替代同步

  对外部依赖不信任

>  * 结果进行
  * 失败情况下failover（重试时间次数需要控制）

  有效的内部监控

**减少故障恢复时间**

  无状态最好

>  * 有状态定期做持久化（checkpoint/commitlog)

  有效的故障隔离

>  * 故障检测，黑白名单，流量分配
  * 黑名单要有恢复机制

**减少损失**

  过载保护

>  * 发现故障，并限制资源

  应用降级

>   * 关闭部分不重要的功能(某些情况下用户也感觉不出来)

  有个故事：二战的时候（好背景），坦克设计的时候每次发射炮弹，都会有电磁波导致所有软件挂掉，所以故障恢复就很重要。

###案例篇

**Twitter**

  世界杯的时候twitter经常会时常挂掉

>  * memcache规划的问题
*   cache也要注意设计

**Foursquare**

  数据不均，mongodb数据量超过内存之后性能非常差(mmap的问题)

>  * 数据迁走之后有空洞，页不释放
  * 还好毕设的时候数据量不大

**Amazon**

  EBS主网络走数据，备网络走控制，操作失误，主网络切到备网络

>  * 相应超时，认为丢失副本
  * 副本复制，继续加剧网络问题

**Weibo**

  热点存在，cache失效，一瞬间所有访问db

>  * 加锁，一个人获取内容回填cache之后就不会有人去访问db了

**Facebook**

  cache没取到就删除了原cache

**OB**

  客户端要做分流，业务高峰，超时严重，把cluster都加入黑名单，重试风暴

###总结篇

**可用性**

>  * BASE:基本可用
  * CAP:No CAP, No CP, A是很重要的
  * [20 Key High Availability Design Principles][2]

[1]:
[2]:
[3]:

