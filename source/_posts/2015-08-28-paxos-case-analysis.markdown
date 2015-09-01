---
layout: post
title: "paxos的一些case分析"
date: 2015-08-28 11:34
comments: true
published: true
categories: "分布式系统"
---


acceptor: a([epoc:4, value:n])  b[epoc:3,value:y]  c[epoc:6,:value:y]

proposor:  x5, x7,   (x4, x3, x6) 

prepare:x5[a, b], x7[b, c]

commit:x[4,n] y[6, y]

一共有5个proposer,
 
1）初始时 x4 (prepare)-> a, x3 (prepare)-> b,x6 (prepare)-> c,
2） x4, x3, x6 挂掉
3）x5(prepare)-> a, b
4）x5(commit[epoc:4, value:n])->a, b
5) x7(prepare) ->b, c
6) x7(commit[epoc:6, value:y])->b, c 
