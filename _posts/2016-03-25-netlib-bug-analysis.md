---
layout: article
title: "记录一个网络库设计的bug"
key: netlib-bug-analysis
date: 2016-03-25 00:14
comments: true
published: true
categories: "Linux"
---
  
   今天遇到一个设计上没考虑好的问题，记录一下。

   之前Libeasy的逻辑如果一个连接上有超时的报文的话，整个连接会destroy掉。考虑网络拥塞的情况，如果AB两个报文同时在等待发送，A报文先进入发送队列（链表，非TCP发送buffer），B后进入，而A超时时间长，B立即超时，那么清理掉B的待发送报文的时候，如果destroy掉连接，那么本来可以发送出去的A报文就被强制失败了。

   考虑这种情况做了一点修改，让超时的报文被清理掉的时候不会destroy连接。这样编码的时候需要指定一个报文被编码出来的buffer是属于哪个会话（session）的，同时记录一下每个session对应的最后一个buffer位置。清理的时候可以从上述位置回溯到不属于当前session的buffer或者到头部为止。看似没啥问题。今天发现了如下的bug：

   考虑如果一个会话编码的多个buffer（或者一个buffer）被部分发送完毕（write返回大小为准），这时候会话超时，这个会话所属的所有编码过的buffer都被干掉，但是连接并没有被destroy，之后的报文继续发送的话，客户端实际上收到了不完整的报文，相当于之后的TCP流都错位了。这种情况下，destroy连接是明显更安全的做法。

   所以还是要考虑周全啊。