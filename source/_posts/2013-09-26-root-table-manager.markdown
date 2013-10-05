---
layout: post
title: "oceanbase源码分析-root_table_manager相关"
date: 2013-09-26 12:15
comments: true
categories: oceanbase源码分析 
---
 
记录一下root_table_manager相关类的阅读和心得。

<!-- more -->

###ObTableNameIterator

一个Iterator, 用于获取所有的TableName

* init

  初始化并调用scan_tables执行查询表名的sql语句   

* scan_tables

  执行sql语句 "select table_name, table_id from __all_table" 来得到所有表的表名

* get_next

  获取下一个表名, 如果 table_idx_ < 3 获取的是内部表的信息, 否则从sql执行结果中迭代返回普通表名

  table_idx_对应的表名分别是:

  ....

* internal_get

  获取内部表名

* normal_get

  获取普通表名 

###	ObTableIdName

顾名思义, TableId 和 TableName 的组合

### ObTableSchemaIterator

获取TableSchema的迭代器

### ObRootSchemaService

RootServer的Schema服务类, 提供rootserver所需的schema操作, 主要是读操作. 

成员
	
方法

	init
	写入
### RootTableService

RootServer

