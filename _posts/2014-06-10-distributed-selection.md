---
layout: article
title: "分布式选主-笔记"
key: distributed-selection
date: 2014-06-10 21:08
comments: true
categories: "Oceanbase"
---
### 数据库主备复制

同步模式

- 备机是否写盘之后应答
- 性能收主备机之间通讯距离，网络抖动影响

异步模式

- 主机不等待备机的应答
- 性能最优，可能造成数据丢失不一致

半异步

- 超过多数成功则返回
- 奇数台机器才可以
- 3/5 > 2/3 > 2/2

<!--more-->

### 网络

- 任意两个进程可以传递消息
- 进程有本地物理时钟 时钟使用NTP同步
- 超时有上限
- 进程不会发错误的消息

### 分布式选举基本问题

不可靠的机群实现可靠的协议，通过投票的方案

- 任意时刻只能有一个主 
- 要容忍网络分区
- Leader Lease，选主要等待上个主的lease过期
- Lease周期的长短

Paxos要求

1. 成员不能说假话（非拜占庭）
2. 单个成员说话不能相互矛盾（投票给A了不能投票给B）
2. 修改需要多数成员同意

实现

1. 记住自己在lease周期的投票
2. 重启等待一个lease周期不投票
3. 多个人都想成为主的时候




