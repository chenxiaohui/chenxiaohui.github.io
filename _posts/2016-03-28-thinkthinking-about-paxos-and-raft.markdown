---
layout: article
title: "关于Paxos和Raft的一些思考"
date: 2016-03-28 23:33
comments: true
published: true
categories: "分布式系统"
---
   
   最近在总结一些协议这么设计的原因，比较杂，纯做记录：

 1. 选主过程相当于Paxos的prepare过程：

  	选出的Leader得到了多数派的同意，相当于Paxos一阶段完成，由于当前Term下投过票的Server保证不再接受小于等于当前Term的，所以保证了选主最终只能选出一个。

  	不同于Paxos的地方在于这一轮Term下，follower除非Lease过期，否则不会发起新的选主，也就是发起Epoc更大的提案。Raft可以认为MultiPaxos的一种应用，MultiPaxos可以认为是合并了Prepare阶段的SingleDegreePaxos.

 2. raft读一致性和选主timeout

    raft协议本身由于主只是续约了follower的lease，所以正常情况下follower不会在lease过期前发起新的选主，但是master网络分区情况下，master本身不维护自己的lease，follower lease过期会发起新的选主从而产生新的主。这时候旧主的写一定不能成功，但是旧主的读不受影响。

    以前在ob的时候阳老师设计的选主协议里面通过主lease来解决了这个问题，只是当时没体会到原因在这里。协议要求补充限制：主在自己的lease过期后放弃主的身份，主维持心跳的过程中续约follower的lease，根据rpc的返回，只有收到多数派的回应并且term没有更大的才续约自己的lease。新启动的server在follower状态至少等一个lease周期才发起选主，来让可能的旧主过期。

 3. paxos是两阶段提交的一种场景。

    两阶段提交的一阶段也是获得所有参与者的同意。只不过是所有而不是多数派，一阶段通过之后，相当于决议已经形成，所以后一阶段不会产生新的决议。2阶段可以完全异步来做，如果2阶段失败，不影响形成的决议。这意味着两阶段提交是非抢占式的。

    

