---
title: '多表级联增删查改操作的实现（C#）'
author: Harry Chen
key: curd-operation-of-multi-table
layout: article

dsq_thread_id:
  - 1262711033
categories:
  - .Net
  - 与技术相关
tags:
  - DataAdapter
  - DataSet
  - DataTable
  - 增删查改
  - 多表
  - 更新
  - 级联
---

  本文背景：

  我们经常会遇到这样的问题：从数据库里通过几个表级联查询数据，然后显示到界面上，用户修改了这些级联之后的数据后，如何将数据更新到数据库里去？我们查询的时候完全可以使用视图，但是视图不支持增删查操作。如何实现视图的可更新呢？

  本文的实现主要采用了.Net DataTable(和DataSet)，使用DataAdapter可更新数据的特性，底层通过存储过程更新数据。逻辑结构如图1所示：

![未命名][1]

图 1 逻辑结构

  基本的想法是：

  * 通过视图进行数据的查询操作，而且这样可以通过SQLServer等工具自动生成视图。
  * 删除，插入和修改分别实现存储过程（或Sql语句），然后构建DataAdapter，将DataAdapter的InsertCommand,UpdateCommand,SelectCommand,DeleteCommand分别置为之前的四种操作。
  * 通过DataAdapter的Update操作更新DataTable（或DataSet）

  举一个简单的例子，目前有四个数据库，之间的关系如图2所示，其中Orders（订单）通过Order_id与Customers（客户）表关联，OrderDetails（订单细节）通过ProductID与Products（商品）表关联，Orders与OrderDetails明显冗余了（一对一），中间做的时候改动了不少东西，所以到最后成了这个样子，算了，懒得改了：

![未2命名][2]

图2 数据库各个表之间的关系

  类图如图3所示，主要是一个数据库连接类，一个表操作基类和两个派生类。派生类主要是覆盖基类方法并填写DataAdapter的四个Command，其中InsertCommand是必须填写的，如果只涉及一个表的操作的话，那么其他三个Command可以用CommandBuilder自动构造：

![testData][3] 图3 类图

  数据库里的操作主要是写存储过程和创建视图，如图4所示：

![数据库][4] 图4 数据库里的操作

  程序执行的截图如图5所示：

![ui][5] 具体的详见[代码][6]，请自行修改连接字符串。

参考文献：

 [1]:SQLServer 存储过程简介与使用方法，

 [2]:使用DataSet更新数据库的两种方式，

