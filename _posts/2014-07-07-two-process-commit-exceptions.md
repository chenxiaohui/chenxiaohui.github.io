---
layout: article
title: "两阶段提交协议的异常处理"
key: two-process-commit-exceptions
date: 2014-07-07 11:57
comments: true
categories: "Oceanbase"
---


  两阶段提交的协议大家都比较熟悉了，解释一下每个阶段的异常处理。首先，我们需要持久化协议过程中的状态，这样如果server宕机，那么恢复的时候还能通过日志知道宕机前处于那个阶段。同时，所有对数据的修改都会先写write ahead log，保证宕机重启的之后数据也不会丢失。写日志的顺序假定为:写write ahead log-修改缓冲区-写commit/abort log。

  在这个前提下，我们根据如下的时序图来讨论异常情况和处理方法。

![](/images/2014/2pc.png "两阶段提交协议时序" "两阶段提交协议时序")

  1. 过程a没有成功，即协调者没有收到部分参与者的回应。超时后，协调者发送abort消息给参与者取消事务。参与者存在两种情况：

  	- 过程1失败，网络问题导致参与者没有收到vote request消息或者此时参与者宕机。参与者重启恢复后无需做任何事。
  	- 过程2失败，参与者收到了vote request，网络问题协调者没有收到回复或此时参与者宕机。参与者宕机恢复或等待超时后广播DECISION_REQUEST消息向其他参与者询问是否收到commit/abort消息。

  2. 过程b没有成功，即协调者发送commit消息之后没有收到部分参与者的回应。协调者需要重试，确认参与者的提交完毕消息，如果多次尝试不能联系上，则等待参与者上线之后解决。参与者存在两种情况：

  	- 过程3失败，网络问题导致参与者没有收到commit消息或此时参与者宕机。参与者上线发现在本地日志中发现尚未提交成功，因为到达这里，可以肯定本地已做好提交准备，但是不知道协调者是决定提交，所以向协调者询问，按协调者的回复来进行提交或回滚。如果无法联系上协调者，则向其他参与者询问事务状态，如果有某一个节点已经做了提交或异常终止(说明协调者已发送了相关消息)，则做同样的操作。
  	- 过程4失败，参与者完成了commit/rollback，但是网络问题协调者没有收到回应或者此时参与者宕机。参与者在本地日志中发现已完成本地提交，所以可能由于网络故障导致提交完成消息没有到达协调者。所以直接忽略。这时可能协调者在等待该参与者的提交完成回应消息，所以参与者主动联系协调者告知事务状态。

  3. 过程c没有成功，即参与者发送vote回应消息之后没有等到协调者的commit/rollback消息。这个过程参与者的异常处理已经讨论过了，这里讨论协调者的异常处理。存在两种情况：

  	- 过程2失败，网络问题导致协调者没有收到回复或此时协调者宕机。协调者恢复重启后，发现并未做提交操作，保险操作(因为不知道它是否发送过准备消息，或其他参与者是否做好提交准备)，直接发送abort消息给所有参与者，终止事务
  	- 过程3失败，网络问题导致参与者没有收到commit/rollback消息或者此时协调者宕机。协调者恢复重启后，不能保证所有参与者都已收到了提交消息，所以给所有的参与者发送commit消息，保证事务的正常提交。

<!--more-->

  算法的伪代码可以参考如下代码，摘自《Distributed Systems: Principles and Paradigms》。

  **Actions of Coordinator**

	write("START_2PC tolocal log");
	multicast("VOTE_REQUESTto all participants");
	while(not all votes have been collected)
	{
	  waitfor("any incoming vote");
	  if(timeout)
	  {
	    write("GLOBAL_ABORT to local host");
	    multicast("GLOBAL_ABORT to all participants");
	    exit();
	  }
	  record(vote);
	}
	if(all participants send VOTE_COMMIT and coordinatorvotes COMMIT)
	{
	  write("GLOBAL_COMMIT to local log");
	  multicast("GLOBAL_COMMIT to all participants");
	}
	else
	{
	  write("GLOBAL_ABORT to local log");
	  multicast("GLOBAL_ABORT to all participants");
	}
	
	**Actions of Participants**

	write("INIT to locallog");
	waitfor("VOTE_REQUESTfrom coordinator");
	if(timeout)
	{
	  write("VOTE_ABORT to local log");
	  exit();
	}
	if("participantvotes COMMIT")
	{
	  write("VOTE_COMMIT to local log");
	  send("VOTE_COMMIT to coordinator");
	  waitfor("DESCISION from coordinator");
	  if(timeout)
	  {
	    multicast("DECISION_REQUEST to other participants");
	    waituntil("DECISION is received"); /// remain blocked
	    write("DECISION to local log");
	  }
	  if(DECISION == "GLOBAL_COMMIT")
	  {
	    write("GLOBAL_COMMIT to local log");
	  }
	  else if(DECISION== "GLOBAL_ABORT")
	  {
	    write("GLOBAL_ABORT to local log");
	  }
	}
	else
	{
	    write("GLOBAL_ABORT to local log");
	    send("GLOBAL_ABORT to coordinator");
	}

[1]:http://blog.chinaunix.net/uid-20761674-id-75164.html "两阶段提交(2PC)协议"
#### 参考文献:

  \[1] 两阶段提交(2PC)协议, <http://blog.chinaunix.net/uid-20761674-id-75164.html>
