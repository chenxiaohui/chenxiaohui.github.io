---
layout: post
title: "oceanbase源码分析-RootTable"
date: 2013-09-02 12:55
comments: true
categories: oceanbase源码分析
---

#Replica和TabletInfo

分析一下Replica类和TabletInfo类的结构

#ObObjType
	
定义了OceanBase中支持的基本数据类型,我们可以在ob_obj_type.h中看到其定义

		enum ObObjType
		{
       ObMinType = -1,
 
       ObNullType,   // 空类型
       ObIntType,
       ObFloatType,              // @deprecated
 
       ObDoubleType,             // @deprecated
       ObDateTimeType,           // @deprecated
       ObPreciseDateTimeType,    // =5
 
       ObVarcharType,
       ObUnknownType,    // For sql prepare
       ObCreateTimeType,
 
       ObModifyTimeType,
       ObExtendType,
       ObBoolType,
 
       ObDecimalType,            // aka numeric
       ObMaxType,
     };



#ObRowkeyColumn
定义了RowKey中的每个列Column


#ObRowkeyInfo
定义了RowkeyColumn的集合
