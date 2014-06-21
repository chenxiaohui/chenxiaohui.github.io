---
title: '&ldquo;违反并发性: UpdateCommand 影响了预期1条记录中的0条&rdquo;原因分析'
author: Harry Chen
layout: post

dsq_thread_id:
  - 1266432130
categories:
  - .Net
  - 与技术相关
tags:
  - UpdateCommand
  - 影响了
  - 违反并发性
  - 预期
---

  该问题出现在使用DataAdapter自动对DataTable(或DataSet)进行更新的时候，具体情形是：通过界面添加了一条记录，然后调用DataAdapter的Update方法更新了数据，之后又修改或删除了这条记录。

  原因网上有很多说法，大部分的分析我感觉是扯淡，其实主要的原因是自增长字段的值没有跟数据库同步[1]，即前台的记录里添加了一条记录，但是程序不知道自增长的ID字段应该填充多少，用户也不可能指定这个ID，更新了之后数据库自动填充了自增长ID，但是前台对应的DataTable(或DataSet)里却没有同步更新，从而导致DataAdapter不知道根据什么字段来定位修改的记录，因而出错。

  具体的解决方法参考[1]一文中给出了一种方法，即每次插入记录的时候去服务器查询自增长种子值，然后把结果放到DataTable对应自增长ID列的AutoIncrementSeed属性里，主要的问题有如下两点：

  1. 我不知道怎么获取……SQLServer里可以用DBCC CheckIdent([User],NoReseed)语句，但是这个语句在代码里貌似是不返回结果的。
  2. 如果两个用户同时操作，比如A添加了一条记录未提交，B也添加了一条记录，这时两个用户的AutoIncrementSeed是一样的，之后也会存在更新的并发问题。

  其实最简单的解决方法就是每次更新之后把新的记录返回一下，替换当前DataTable，问题不就解决了么。参见[代码][1]

参考文献：

> [1] Access自动编号 违反并发性原因解析,
>
> 

   [1]: http://www.roybit.com/wp-content/uploads/2011/02/UpdateID.rar
