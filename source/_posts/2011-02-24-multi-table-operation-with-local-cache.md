---
title: '基于本地缓存的多表级联操作的实现（C#）'
author: Harry Chen
layout: post

dsq_thread_id:
  - 1255514081
categories:
  - .Net
  - 与技术相关
tags:
  - 事实表
  - 多表级联
  - 本地缓存
  - 维表
---

  背景：数据库操作中我们经常会遇到级联修改的问题，在之前的一篇文章[1]里我们探讨了多表级联的一种实现方式，这篇文章我们将探讨另一种实现方式，即通过本地缓存的方式，避免不必要的存储过程。

定义：

> 事实表：中央表，它包含联系事实与维度表的数字度量值和键。简单说，事实表包括各个维度的ID。
>
> 维表：述事实数据表中的数据。维度表包含创建维度所基于的数据。

  首先，我们的条件是，级联不是很复杂，存在一张事实表和若干维表，通过单ID将事实表和维表进行级联。思路是：首先本地缓存维表的所有数据，然后将事实表的数据绑定到DataGridView上，将ID列设置为DataGridViewComboBoxColumn，绑定相应的维表，指定值字段和显示字段，让结果自动对应。

  举个简单的例子：订单数据库，包含Customers，Products和Orders三个表，之间的逻辑关系如图1所示：

![视图结构][1]图1 数据库表结构关系

  程序运行截图如图2所示：

![程序][2]

图2 程序运行截图

  具体的见[代码][3]，不再赘述。

参考文献：

> [1] 多表级联增删查改操作的实现，
>
> 

   [1]: http://www.roybit.com/wp-content/uploads/2011/02/thumb1.png (视图结构)
   [2]: http://www.roybit.com/wp-content/uploads/2011/02/thumb2.png (程序)
   [3]: http://www.roybit.com/wp-content/uploads/2011/02/testDataUpdate.rar
