---
layout: article
title: "分布式消息队列的消息消费逻辑"
key: message-queue-consume-semantics
date: 2014-11-07 14:54
comments: true
published: false
categories: "分布式系统"
---

  引用一段，出处在找：
  
  对于JMS实现,消息传输担保非常直接:有且只有一次(exactly once).在kafka中稍有不同,对于consumer而言:
    1) at most once: 最多一次,这个和JMS中"非持久化"消息类似.发送一次,无论成败,将不会重发.
    2) at least once: 消息至少发送一次,如果消息未能接受成功,可能会重发,直到接收成功.
    3) exactly once: 消息只会发送一次.
    at most once: 消费者fetch消息,然后保存offset,然后处理消息;当client保存offset之后,但是在消息处理过程中consumer进程失效(crash),导致部分消息未能继续处理.那么此后可能其他consumer会接管,但是因为offset已经提前保存,那么新的consumer将不能fetch到offset之前的消息(尽管它们尚没有被处理),这就是"at most once".
    at least once: 消费者fetch消息,然后处理消息,然后保存offset.如果消息处理成功之后,但是在保存offset阶段zookeeper异常或者consumer失效,导致保存offset操作未能执行成功,这就导致接下来再次fetch时可能获得上次已经处理过的消息,这就是"at least once".
    exactly once: kafka中并没有严格的去实现(基于2阶段提交,事务),我们认为这种策略在kafka中是没有必要的.
    因为"消息消费"和"保存offset"这两个操作的先后时机不同,导致了上述3种情况,通常情况下"at-least-once"是我们搜选.(相比at most once而言,重复接收数据总比丢失数据要好).

    to be continued.