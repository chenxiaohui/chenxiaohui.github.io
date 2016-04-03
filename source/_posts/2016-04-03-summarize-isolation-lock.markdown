---
layout: post
title: "数据库锁和隔离级别的总结"
date: 2016-04-03 19:34
comments: true
published: true
categories: "Oceanbase"
---


  最近在琢磨MVCC和悲观乐观锁的问题，感觉有些以前学习的点没有串联起来，主要是隔离级别和锁相关的，这里总结思考一下：

  1. 两阶段锁解决了什么问题

  	两阶段锁主要解决事务调度的可串行化，保证了调度是正确的。一个简单的例子参考[度娘][1]这里。

  2. 实现两阶段锁对应了什么隔离级别。

  	两阶段锁保证了基本的隔离级别正确性，RC之上的隔离级别（包含RC）都需要至少保证两阶段锁。一个例外是如果wher条件不走索引的话，是可能全表加锁的，这种情况下mysql为了性能提前解锁了不满足条件的行，参见[这里][2]。

  3. 各个隔离级别对应的加锁策略。

  	这个比较简单了：

  	RU：读加S锁，写加X锁，完成即可释放。
  	RC：读加S锁，写加X锁，读锁完成可释放，写锁一直到事务完成再释放。
  	RR：读加S锁，写加X锁，读写锁都一直到事务完成再释放。
  	SE: RR基础上再加范围锁。

  4. select如何防止丢失更新。

  	按照[何等成][2]博客里面的定义，可以区分MVCC下两种读。

  	快照读
  	select * from table where ?;

  	当前读。
  	select * from table where ? lock in share mode;
	select * from table where ? for update;
	insert into table values (…);
	update table set ? where ?;
	delete from table where ?;

    快照读级别下，写事务可能丢失更新，因为select并不阻塞写，两个读写事务可能基于同一个快照点。当前读级别下，写阻塞读，所以涉及同一行的读写事务一定是串行的。不会丢失更新。

    基于乐观锁的方式下，也不会丢失更新，因为检查到更新可能被覆盖的操作都会回滚（打回重试）了。

  4. MVCC和锁（悲观乐观）的实现方式下，隔离级别是怎么实现的？

  	MVCC主要针对冲突数据的处理，乐观锁、悲观锁决定了最终原子的更新一行的方式。
  	
  	MVCC加乐观锁的方式基本思路如下：

  		定义一个keyValueSet，Conditional Update在此基础上加上了一组更新条件conditionSet { … data[keyx]=valuex, … }，即只有在D满足更新条件的情况下才将数据更新为keyValueSet’；否则，返回错误信息。[引用][3]

  	MVCC加悲观锁主要是提供了不加锁的读。按[何等成][2]的文章里看，就是快照读+当前读。快照读级别下，直接按照版本读就行，当前读级别下，如果有锁冲突还是要加锁。

  	在ob里的实现上看比较明显，行的修改增量组织为一棵B树，历史版本表现为B树叶子节点上挂的链表。链表的按照版本号串接起所有历史版本，全局Publish version决定了当前可见的最新版本。

  	在快照读级别下，select不需要加锁，只需要每次按照publish version去链表遍历，找到可见的结果并返回。如果不修改transaction consistency set的情况下，这种读取可能导致两次读结果不一致，不满足RR或者SI(Snapshot Isolation)。OB0.5增加了一个readonly snapshot的级别，可以提供对一个快照的只读操作，保证了多次读取的一致，但是没有snapshot级别不加锁的读写事务（快照写），毕竟基于一个旧的快照做写操作可能使新的提交丢失。这里要么类似乐观锁验证一下版本，要么加锁来延迟读写。

  	当前读级别下，select也要加锁直到事务结束释放，跟mysql的实现一致。

  	总结来讲，如果把当前读看成写事务的话，那么ob事实上是读操作只看版本号，写操作只看锁。如果只考虑当前读和写操作的话，那么相当于有冲突的时候读锁延迟了写操作，写锁延迟了读操作，保证了调度的串行。这种情况下，多次读取的结果是一致的。

  5. select for update在mvcc下如何实现。

     道理是一样的，跟mvcc没什么关系，select for update实际上相当于写事务（select的时候加写锁，直到事务结束再释放，update操作本身也是一样的过程，先检索符合条件的记录加锁，再修改并提交，这样才能保证是原子的）

[1]: http://baike.baidu.com/view/3798716.htm "两阶段封锁"
[2]: http://hedengcheng.com/?p=771#_Toc374698312 "MySQL 加锁处理分析"
[3]: http://coolshell.cn/articles/6790.html "多版本并发控制(MVCC)在分布式系统中的应用"