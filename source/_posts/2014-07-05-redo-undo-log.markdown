---
layout: post
title: "undo 日志和redo 日志"
date: 2014-07-05 21:20
comments: true
categories: "Oceanbase"
---

  具体的可以看[这里][1]，解释几个作者没解释清楚的问题：

1. 只用REDO日志为什么数据修改要每次修改刷盘

	如果不刷盘，不会导致数据不一致，但是数据修改过程相当于写redo日志-修改内存-写commit日志（修改内存的顺序也无所谓了），这个过程结束已经应答用户了，但是修改没有刷下去断电恢复的话也无法通过redolog恢复到当前状态，所以会丢失修改。

2. 修改数据和写redo/undo log/commit log之间的关系是什么

	任何对磁盘的数据修改落实之前都需要先写log，无论是redo还是undo。undo保证了一旦数据写了一半（脏数据）能够回滚，redo保证了写了日志的事务能够回放出来。

	只使用undo的时候commit日志要等待刷盘成功，写了commit的事务不会再回滚。

	只使用redo的时候需要先写commit日志再修改数据，因为数据有刷盘和不刷盘的可能，写完commit日志意味着修改已经完整记录下来了不会丢失。否则，没有commit的日志不会回放，如果之前修改数据并刷盘了，系统不知道处于哪个阶段：写了一半的log？写成功log?修改了一半数据？成功修改全部数据？。如果修改不刷盘，那么如果在修改数据阶段宕机，就丢失了此条本来可以写成功的数据，好在这时候也没有回复用户。

	其实看来如果修改不刷盘的话，那么可以先修改内存再写commit，只不过没有必要做这个区分（对否？）

[1]: http://blog.csdn.net/ggxxkkll/article/details/7616739 "数据库日志文件-- undo log 、redo log、 undo/redo log"

###参考文献:

>\[1] 数据库日志文件-- undo log 、redo log、 undo/redo log, <http://blog.csdn.net/ggxxkkll/article/details/7616739>