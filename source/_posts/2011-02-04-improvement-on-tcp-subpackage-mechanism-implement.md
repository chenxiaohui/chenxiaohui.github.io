---
title: '对&ldquo;基于长度和定界符带校验的TCP分包方式&rdquo;的一些改进'
author: Harry Chen
layout: post
permalink: /improvement-on-tcp-subpackage-mechanism-implement/
dsq_thread_id:
  - 1294433066
categories:
  - .Net
  - 与技术相关
tags:
  - 分包
  - 改进
  - 校验
  - 长度
---
# 

“长度、分隔符加校验的TCP分包设计(C#)”[1]一文提出了一种综合长度和特殊字符定界两种TCP分包方式的新的分包方式，原文给出的实现没有考虑长度字符被分开两次传播的情况，同时原算法没有明确的算法描述，基于多种情况的综合，容易遗漏，这里给出改进后的算法：

  1. 如果WaitForLength置位，则拼上原来的字段，凑齐长度字段信息。
  2. 如果LeftLength不为0，则判断剩余缓冲区是否包含了报文剩余部分，如果包含则拼合字段，判断结尾是不是结束定界符>，否则拼合剩余缓冲区，LeftLength更新。
  3. 找到一个开始定界符，否则拼合剩余缓冲区，等待下次数据到达。

总的来说，就是通过开始定界符标定一个报文的开始，通过长度字段得到报文的结尾位置，通过结尾位置是不是结束定界符>判断一个报文是不是完整，如不完整则继续找寻下个开始定界符。

报文的正确新校验仍通过C#的反序列化机制。源码只更新了[Client.cs][1]，测试代码如下：


    byte[] buffer1 = new byte[] { 60, 0, 0, 0, 10, 44, 43, 43, 43, 43, 44, 62, };//第一个报文
    byte[] buffer2 = new byte[] { 60, 0, 0, };//第二个报文
    byte[] buffer3 = new byte[] { 0, 7, 43, 43, 43, 62, 60, 0, 0, 0, 10, 44, 45, 45, 45, 45, 44, 62 };//第三个报文

    //第一个报文
    Array.Copy(buffer1, 0, client.m_receiveBuffer, 0, buffer1.Length);//拷贝到接收缓冲区
    client.ResolveSessionBuffer(buffer1.Length);
    Array.Clear(client.m_receiveBuffer,0,client.m_receiveBuffer.Length);

    //第二个报文
    Array.Copy(buffer2, 0, client.m_receiveBuffer, 3, buffer2.Length);//拷贝到接受缓冲区
    client.ResolveSessionBuffer(buffer2.Length);
    Array.Clear(client.m_receiveBuffer, 0, client.m_receiveBuffer.Length);

    //第三个报文
    Array.Copy(buffer3, 0, client.m_receiveBuffer, 3, buffer3.Length);//拷贝到接收缓冲区
    client.ResolveSessionBuffer(buffer3.Length);
    Array.Clear(client.m_receiveBuffer, 0, client.m_receiveBuffer.Length);

参考文献：

> [1] 长度、分隔符加校验的TCP分包设计(C#)，
>
> 

   [1]: http://www.roybit.com/wp-content/uploads/2011/02/Client.cs
