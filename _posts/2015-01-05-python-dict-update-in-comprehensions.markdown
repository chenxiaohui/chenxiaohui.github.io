---
layout: article
title: "在Python字典解析中进行update"
date: 2015-01-05 13:25
comments: true
published: true
categories: "Python"
---

  遇到这样一个事情，从一个Thrift源取回部分数据，结构是一个对象数组，根据其中所有的Id字段从数据库又取回另一部分数据，结构是一个字典数组。那么问题来了，~~挖掘机技术哪家强~~如何按照id合并两份数据?

  这其实就是JOIN，也就两种做法，nested loop join和hash join（这些词都是在ob的时候听到的，其实道理很简单）。做nested loop join的话，最好按排序，做hash join的话，就需要把其中一份数据的变成以id字段为key的字典。这里我们选择后一种，python代码实现起来比较简洁。前一种貌似只能for循环搞下标，不知道有没有直接的built in function。

  代码比较简单，就是遇到了一个有代表性的问题：

	results = [result.update(items[result['id']])) for result in results]
  
  id字段是join的key，results是从数据库取到的，items是从thrift取到的。关键问题在于update的结果是None，result是被原地修改的。所以需要改成下面：

	results = [dict(result.items() + items[result['id']].items()) for result in results]
