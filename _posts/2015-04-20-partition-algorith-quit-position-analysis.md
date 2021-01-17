---
layout: article
title: "partition算法的落点讨论"
key: partition-algorith-quit-position-analysis
date: 2015-04-20 21:27
comments: true
published: true
categories: "基础理论"
---
  
  首先这里的partition算法指的是快速排序中把数据分区的算法，算法接受一个数列和一个值，返回一个位置，这个位置之前的元素都小于等于输入值，之后的元素都大于等于输入值。

  算法如下：
   	

  还有一种常见的形式：


  这里我们讨论下落点的情况，如果partition算法可以传入任何的value，而不是快排中那样从序列中随机获得一个值，那么结果就会有多重情况了。
  
