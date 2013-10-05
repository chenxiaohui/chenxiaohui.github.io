---
layout: post
title: "oceanbase源码分析-Rowkey相关"
date: 2013-09-16 12:55
comments: true
categories: oceanbase源码分析
---

这里分析一下ObRowkey相关的源码.

 引用[晓楚师兄的一段话](http://blog.csdn.net/maray/article/details/9731113 "OceanBase里面的rowkey是什么概念，是由哪些要素构成的？"):

* Rowkey是OceanBase诞生之初就引入的概念，最终被确立是在OceanBase 0.3。
* 为了便于理解，不妨把OceanBase想象成一个Key-Value系统，Rowkey就是Key，Value就是返回的行数据。
* 如果你对mysql数据库熟悉，那么不妨把Rowkey理解成primary key，它就是那几个主键列的组合，列的顺序与primary key中定义的顺序一致。

<!-- more -->

###ObObjType

定义了OceanBase中支持的基本数据类型,我们可以在ob_obj_type.h中看到其定义


###ObRowkeyColumn
定义了RowKey中的每个列Column


###ObRowkeyInfo
定义了RowkeyColumn的集合

###ObRootTableRow:
存储了RootServer中一行所需要关注的信息，包括了rowkey列的数据和各个replica的版本信息

      void set_min_row(const int64_t rowkey_num);
      // makeout
      int input_tablet_row(const bool start_key, const ObRootTabletInfo & tablet);
      // output
      int output_tablet_row(common::ObScanner & result);
