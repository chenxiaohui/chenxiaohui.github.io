---
layout: post
title: "table_tablet_iterator"
date: 2013-10-21 16:26
comments: true
categories: 
---
所有迭代器的类图如下所示：

{% img img-polaroid center /images/2013-10/iterator.png "iterator类图" "iterator类图" %}

## ObRootTabletIterator

所有tablet类迭代器，也就是ObRootTableIterator, ObTableTabletIterator等的直接父类，定义了迭代接口。

<!-- more -->

## ObTableTabletIterator

最基本的迭代器，继承ObRootTabletIterator, 负责迭代一个表的所有（或者某个指定range里面的）Tablet。

###实现机理 :

从Rowkey::MINROWKEY开始，每次迭代的tablet的endkey（加一个ObRowkey::MIN_OBJECT防止找到同一个）作为下次迭代的起始值。

###错误码与错误原因对应

**断言失败**：

1. 接受返回值的传入参数tablet存在分配器（allocator）或者手动制定了其他的分配器（而不是由上次本迭代器制定的range_allocator)

2. sql查询结果为空

**OB_ITER_END**：

1. 迭代正常结束，必须保证tablet是以MAX结束的（或者以ScanRange的endkey结束）。

2. 如果有一个表没有任何tablet，同样返回OB_ITER_END，而不是OB_NO_RESULT错误码（更新，争议的地方）。

**OB_NOT_INIT**: 

没有初始化，目前是没有传入RootTableService指针，或者指针为空。

**OB_ROOT_NOT_INTEGRATED**：

scan_range出错，当前end_key不再scan_range的范围里，

**OB_ERR_UNEXPECTED**：

tablet本身错误，start_key > end_key

####其他从root_table层得到的错误码：

**OB_MEM_OVERFLOW**： 内存错误

**OB_TABLE_NOT_EXIST**：

1.获得表schema的时候发现schema中不存在这张表

2.查询到的结果有空洞（某个范围下没有当前表的tablet）

**OB_NO_RESULT**：按照指定的条件，proxy查询不到结果，主要是table没有tablet的情况和tablet范围未封闭（没有max)，否则总会找到结果，即使没有对应的tablet，也应该返回OB_ENTRY_NOT_EXIST

**OB_ERROR**：可能情况

1. 当前表的元数据表没有指定

2. 获取root_table_name的时候写入失败

3. proxy读取tablet的时候结果加入返回列表的时候失败。

4. proxy构建内部表读取sql语句的时候失败（内存错误或者schema错误或者sql字符串填充失败）

**OB_ENTRY_NOT_EXIST**：

1. 当前表的元数据表schema不存在。

2. tablet范围里面有空洞，按照rowkey查找一定范围的tablet之后找不到rowkey所刚好对应的tablet

**OB_SCHEMA_ERROR**：

proxy生成sql语句的时候add_rowkey_column_value失败

**OB_ERR_NULL_VALUE**：

proxy生成sql语句的时候add_rowkey_column_value失败

**OB_ERR_SQLCLIENT**：

主要是一些sql调用失败。

**OB_ALLOCATE_MEMORY_FAILED**：

主要是deep copy range失败

**以上错误码都会直接返回到上层，只不过部分需要单独处理，比如OB_ENTRY_NOT_EXISTS 和OB_NO_RESULT是否继续迭代还是个问题。**

##ObRootTableIterator

继承ObRootTabletIterator，实现迭代所有表的所有tablet的功能，如果有table完全没有tablet，则返回OB_NO_TABLET，调用者决定是否继续迭代。

###实现机理

通过ObTableSchemaIterator迭代所有table, 每次生成一个table的TableTabletIterator,迭代此iterator直到end，然后继续迭代下一个表。如果遇到tablet_iter的错误，返回错误，除OB_NO_TABLET错误外，调用者应中止迭代。

###错误码与错误对应原因

**OB_ITER_END**：迭代所有表的tablet结束。

**OB_NO_TABLET**： 从一个表里没有迭代出任何一个tablet，之后仍可继续迭代。

其他错误码来自ObTableSchemaIterator和TableTabletIterator


##ObServerTabletIterator

继承ObRootTableIterator（仔细看不是tablet）,实现一个server上所有tablet的迭代。

###实现机理

迭代所有tablet直到找到有副本分布在这个server上的tablet，然后返回。如果出错，一概中断。

###错误码与错误原因对应

OB_ITER_END：所有tablet迭代结束。

其他错误码来自root_table_iterator


##ObAliveRootTableIterator

继承ObRootTableIterator（仔细看不是tablet),返回所有表的所有tablet，但是剔除不存活的版本，所以依赖一个ObChunkServerManager指针。


##ObTableTabletFilterVersionIterator

继承ObTableTabletIterator，返回所有表的所有tablet，但是剔除版本不等于指定版本的replica。


###错误码及错误原因对应

OB_NOT_INIT：未初始化。

OB_INVALID_ARGUMENT： 初始化参数不合法。

###ObIteratorUtility

工具类，无状态，负责一些iterator数据处理：如剔除不存活的副本（strip_dead_replicas），筛选符合version条件的副本（filter_replica_version）等。


<hr/>

##ObRootReplicaIterator

所有replica类迭代器，目前只有ObServerReplicaIterator，定义了迭代接口。包含一个ObRootTableIterator的迭代对象，即所有replica迭代器都是基于RootTableIterator迭代所有表的所有tablet的基础上实现的。

##ObServerReplicaIterator

迭代某个server上的所有replica(副本)

###实现机理

迭代所有tablet，直到得到一个tablet里面的分布在该server上的副本。没有就继续迭代。有错误一概中断。

##ObReplicaIteratorCalculator

合并两个replica类迭代器的结果，并返回当前吐出的replica（replica参数）是属于哪个迭代器的（type参数/LEFT_ITER/RIGHT_ITER/BOTH_ITER三种)

###实现机理

1. 首先置type为both_iter,两个迭代器都前进一步
2. 如果left_iter的结果> right_iter，吐出right_iter的结果，置type为LEFT_ITER，保存两个结果。
3. 同理如果right>left,吐出right_iter的结果，置type为RIGHT_ITER,保存两个结果。
4. 如果right==left，吐出随便哪个结果（左边），置type为BOTH_ITER,保存两个结果。
5. 之后每次next判断type，type=LEFT_ITER则迭代LEFT_ITER，跟right_iter上次的结果比较，决定吐出哪个，并置位type=left/right/both。RIGHT/BOTH同理。
6. 如果有单边迭代器中止，比如左边，则置type=RIGHT_ITER, 迭代到结束，反之亦然。
7. 正常中止条件：两边迭代器都中止。
8. OB_ITER_END情况下type返回值决定了哪边先结束。

