---
layout: post
title: "oceanbase源码分析-Rowkey相关"
date: 2013-09-16 12:55
comments: true
categories: oceanbase
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


###ObCellInfo
从结构上可以看出，定义了一个cell的相关信息，主要包括了

      ObString table_name_; //所在表名
      uint64_t table_id_;	//表id
      ObRowkey row_key_;	//所在行row_key_
      uint64_t column_id_;	//列id
      ObString column_name_;//列名
      ObObj value_;			//cell值

如下两个类与之有关联，一并写在这里

###ObRootTableRow:

存储了RootTable中一行的信息，包括了rowkey列的数据和各个replica的版本信息

      // 方法
      int input_tablet_row(const bool start_key, const ObRootTabletInfo & tablet);
      int output_tablet_row(common::ObScanner & result);
      // 成员
      common::ObObj rowkey_objs_[common::OB_MAX_ROWKEY_COLUMN_NUMBER];
      common::ObCellInfo row_cells_[common::OB_MAX_COLUMN_NUMBER];

着重分析一下input_tablet_row方法，首先拷贝rowkey，没有做深拷贝

    // copy the range end key as rowkey
    rowkey_column_num_ = rowkey_len;
    for (int64_t i = 0; i < rowkey_column_num_; ++i)
    {
      rowkey_objs_[i] = input_key.ptr()[i];
    }
然后填充row_cells_，RootTable中一行的各个列信息，

    ADD_REPLICA_SERVER(normal_column_num_, i, replica->server_, replica->version_);

ADD_REPLICA_SERVER的定义如下：

	#define ADD_REPLICA_SERVER(column, index, server, version) \
	{ \
	    ObRowkey rowkey; \
	    rowkey.assign(rowkey_objs_, rowkey_column_num_); \
	    row_cells_[column].row_key_ = rowkey; \
	    row_cells_[column].table_name_ = ObString::make_string("temp"); \
	    row_cells_[column].column_name_ = ObString::make_string("version_"#index); \
	    row_cells_[column].value_.set_int(version); \
	    column++; \
	    row_cells_[column].row_key_ = rowkey; \
	    row_cells_[column].table_name_ = ObString::make_string("temp"); \
	    row_cells_[column].column_name_ = ObString::make_string("port_"#index); \
	    row_cells_[column].value_.set_int(server.get_port()); \
	    column++; \
	    row_cells_[column].row_key_ = rowkey; \
	    row_cells_[column].table_name_ = ObString::make_string("temp"); \
	    row_cells_[column].column_name_ = ObString::make_string("ip_"#index); \
	    row_cells_[column].value_.set_int(server.get_ipv4()); \
	    column++; \
	}
同时填充了三个cell，分别是version，port，ip，对应了RootTable的表结构，这里顺便说一下RootTable内部表化之后的表结构定义：

range默认前开后闭，也就是说从检索tablet的时候的如果刚好有个tablet是以此endkey结尾的，那么这个tablet会被检索出来。如果检索的关键字是rowkey的话，那么这个rowkey所对应的tablet就是这个tablet而不是下一个tablet（如果tablet没有出现空洞的话），这个是系统里的约定，也是比较基础的规则了。

举个例子，如下的函数负责从一堆tablet里面找到刚好对应当前rowkey的tablet,我们来看函数的逻辑。

int ObRootTabletUtil::find_right_tablet(const ObRootTabletList & list, const uint64_t table_id,
    const ObRowkey & rowkey, ObRootTabletInfo & tablet)
{
  int ret = OB_ENTRY_NOT_EXIST;
  for (int64_t i = 0; i < list.list_.count(); ++i)
  {
    tablet = list.list_.at(i);
    TBSYS_LOG(DEBUG, "iterator tablet:%s", to_cstring(tablet.meta_info_.range_));
    if (tablet.meta_info_.range_.table_id_ < table_id)
    {
      continue;
    }
    else if (tablet.meta_info_.range_.table_id_ > table_id)
    {
      break;
    }
    else if (tablet.meta_info_.range_.end_key_ < rowkey)
    {
      continue;
    }
    else
    {
      if (tablet.meta_info_.range_.start_key_ > rowkey)
      {
        break;
      }
      else if (tablet.meta_info_.range_.start_key_ == rowkey)
      {
        // find the first root tablet
        if (rowkey.is_min_row())
        {
          ret = OB_SUCCESS;
        }
        break;
      }
      else
      {
        ret = OB_SUCCESS;
        break;
      }
    }
  }
  if (ret != OB_SUCCESS)
  {
    // find the next tablet but not find the suitable tablet
    if (list.list_.count() > 0)
    {
      TBSYS_LOG(WARN, "not find the tablet in root table has hole:rowkey[%s], tablet[%s]",
          to_cstring(rowkey), to_cstring(tablet.meta_info_.range_));
    }
  }
  return ret;
}


###表名

First Root Table 的 Table ID 为 111(固定值,暂定 111)
User Meta Table 和 User Root Table 为 User Table 的衍生 Table, 对外不可见, 在 User Table 创建时自动创建， Table Name 和 Table
ID 取值约定如下:要求 User Table ID 从 3000 以后取值。

如下所示：

Table Type 			Table Name 				Table ID
User Table 			User Table Name 		User Table ID
User Meta Table 	__User Table ID.META 	User Table ID – 1
User Root Table 	__User Table ID.ROOT 	User Table ID – 2
First Root Table 	__first_root_table 		111

Rowkey构成规则

Table Type  		Table Rowkey
User Table 			User Table Rowkey Columns
User Meta Table 	Cluster ID + User Table ID + User Table Rowkey Columns
User Root Table 	Cluster ID + User Meta Table ID + User Table ID + User Table Rowkey Columns
First Root Table 	Cluster ID + User Root Table ID

表结构比较多，只捡主要的说：

FirstRootTable

###ObScanner
