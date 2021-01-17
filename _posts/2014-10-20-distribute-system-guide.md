---
layout: article
title: "分布式系统/NOSQL入门书单"
key: distribute-system-guide
date: 2014-10-20 11:26
comments: true
categories: "Oceanbase"
---

  简单记一下我看过的和觉得值得看的。主要是给@赵龙作为参考。

  * 分布式相关

>\[1] 大规模分布式存储系统, <http://book.douban.com/subject/25723658/>
  阿里日照的书，全面介绍了分布式系统的原理和实践，入门不可多得的书

>\[2] 分布式系统原理介绍, <http://blog.sciencenet.cn/home.php?mod=attachment&id=31413>
  百度刘杰的，讲基本的分布式原理，有些笔误什么的。

>\[3] paxos算法相关, <http://cxh.me/2014/08/26/paxos-study/>
  总结了paxos算法一些资料。

>\[5] 分布式数据库系统原理, <http://product.dangdang.com/23466507.html>
  分布式数据库的一本教材。

>\[6] The Raft Consensus Algorithm, <http://raftconsensus.github.io/>
  raft相关的资料，论文和一些实现都能在里面找到，另外有一个图形化的展示很方便。

>\[7] Raft介绍, <http://www.slideboom.com/presentations/956855/Raft%E4%BB%8B%E7%BB%8D>
  raft的一个ppt。

* 数据库相关

>\[1] 数据库系统实现, <http://item.jd.com/10060181.html>
  数据库的一本教材，偏重于实现。

>\[2] 数据挖掘概念与技术, <http://book.douban.com/subject/2038599/>>\[3] 事务相关, <http://cxh.me/2014/07/02/article-on-transaction/>

>\[3] 事务相关, <http://cxh.me/2014/07/02/article-on-transaction/>
  总结了事务相关的一些资料。

* NOSQL相关

>\[1] Dynamo论文, <http://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf>

>\[2] bigtable论文, <http://research.google.com/archive/bigtable-osdi06.pdf>

>\[3] gfs论文, <http://research.google.com/archive/gfs-sosp2003.pdf>

>\[4] map reduce论文, <http://static.googleusercontent.com/media/research.google.com/zh-CN/us/archive/mapreduce-osdi04.pdf>

>\[5] Redis 设计与实现, <http://redisbook.com/en/latest/>
  一本不错的讲redis的书。

>\[6] 数据分析与处理之二（Leveldb 实现原理）, <http://www.cnblogs.com/haippy/archive/2011/12/04/2276064.html>
  leveldb的实现。

>\[7] Memcached 源码剖析笔记, <http://files.cppblog.com/xguru/Memcached.pdf>
  memcache的源码。

* 基础

>\[1] UNIX环境高级编程, <http://book.douban.com/subject/1788421/>

>\[2] UNIX网络编程, <http://book.douban.com/subject/1500149/>

* 一些博客

>\[1] 银河里的星星的博客, <http://duanple.blog.163.com/>
  主要是分布式领域的论文和翻译。

>\[2] 章炎的技术博客, <http://dirlt.com/>

>\[3] 何登成的技术博客, <http://hedengcheng.com/> 大牛不解释

>\[4] 淘宝核心系统团队博客, <http://csrd.aliapp.com/>

>\[5] 吴镝 <http://www.cnblogs.com/foxmailed/> 专注系统，基础架构，分布式系统

  都看还是需要时间的，我只是读完了一部分翻完了一部分，很多还需要再看一遍。分布式系统最好的学习方法当时是实现一个分布式系统，像晓楚[macrakv](https://github.com/raywill/macraykv "Macrakv")这样，但是工程量和难度比较大，退而求其次的办法是看源码，redis/hbase/leveldb/memcached都是不错的例子。

[1]: http://book.douban.com/subject/25723658/ "大规模分布式存储系统"
[2]: http://www.valleytalk.org/wp-content/uploads/2012/07/%E5%88%86%E5%B8%83%E5%BC%8F%E7%B3%BB%E7%BB%9F%E5%8E%9F%E7%90%86%E4%BB%8B%E7%BB%8D.pdf "分布式系统原理介绍"
[3]: http://cxh.me/2014/08/26/paxos-study/ "paxos算法相关"
[4]: http://cxh.me/2014/07/02/article-on-transaction/ "事务相关"
[5]: http://product.dangdang.com/23466507.html "分布式数据库系统原理"
[6]: http://raftconsensus.github.io/ "The Raft Consensus Algorithm"
[7]: http://www.slideboom.com/presentations/956855/Raft%E4%BB%8B%E7%BB%8D "Raft介绍"

[1]: http://item.jd.com/10060181.html "数据库系统实现"
[2]: http://book.douban.com/subject/2038599/ "数据挖掘概念与技术"


[1]: http://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf "Dynamo论文"
[2]: http://research.google.com/archive/bigtable-osdi06.pdf "bigtable论文"
[3]: http://research.google.com/archive/gfs-sosp2003.pdf "gfs论文"
[4]: http://static.googleusercontent.com/media/research.google.com/zh-CN/us/archive/mapreduce-osdi04.pdf "map reduce论文"
[5]: http://redisbook.com/en/latest/ "Redis 设计与实现"
[6]: http://www.cnblogs.com/haippy/archive/2011/12/04/2276064.html "数据分析与处理之二（Leveldb 实现原理）"
[7]: http://files.cppblog.com/xguru/Memcached.pdf "Memcached 源码剖析笔记"

[1]: http://book.douban.com/subject/1788421/ "UNIX环境高级编程"
[2]: http://book.douban.com/subject/1500149/ "UNIX网络编程"

[1]: http://duanple.blog.163.com/ "银河里的星星的博客"
[2]: http://dirlt.com/ "章炎的技术博客"
[3]: http://hedengcheng.com/ "何登成的技术博客"
[4]: http://csrd.aliapp.com/ "淘宝核心系统团队博客"
