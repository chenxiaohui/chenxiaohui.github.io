---
layout: article
title: "一个关于宏的问题"
key: a-macro-problem
date: 2014-06-26 10:53
comments: true
categories: "C++"
---

  写了一段代码，我想实现宏里面拼接一个变量然后取得这个变量的值的效果，但是没有成功：

	#define OB_FIRST_ROOT_TABLE_TID 21
	#define OB_INVALID_ID INT_MAX
	const char* OB_FIRST_ROOT_TABLE_TABLE_NAME  =  "__first_root_table";

	struct TableBackupSQL
	{
	  uint64_t table_id_;
	  const char* sql_;
	  const char * table_name_;
	  TableBackupSQL()
	  {
	    sql_ = NULL;
	    table_name_ = NULL;
	    table_id_ = OB_INVALID_ID;
	  }
	  TableBackupSQL(uint64_t table_id, const char* table_name, const char* sql)
	  {
	    sql_ = sql;
	    table_name_ = table_name;
	    table_id_ = table_id;
	  }
	};


	#define TABLE_BACKUP_(table_prefix, table_name)\
	TableBackupSQL(table_prefix##_TID, table_prefix##_TABLE_NAME, "select * from "#table_name)
	#define TABLE_BACKUP(table_prefix)\
	TABLE_BACKUP_(table_prefix, table_prefix##_TABLE_NAME)

	TableBackupSQL table_backup_list_[] =
	{
	  TABLE_BACKUP(OB_FIRST_ROOT_TABLE)
	};


	int main(void)
	{
	  for (int i = 0; i < sizeof(table_backup_list_)/sizeof(TableBackupSQL); i++)
	  {
	    TableBackupSQL& desc = table_backup_list_[i];
	    printf("%d, %s, %s\n", desc.table_id_, desc.table_name_, desc.sql_);
	  }
	}

  期望的结果是

	21, __first_root_table, select * from __first_root_table

  实际的结果是
	
	21, __first_root_table, select * from OB_FIRST_ROOT_TABLE_TABLE_NAME

<!--more-->

  拼出来的OB_FIRST_ROOT_TABLE_TABLE_NAME没有被替换，当然有很多方法绕开。我试图两次展开宏但是没有成功，这个跟[这里][1]说的问题毕竟不是一个。不知道C++11里面有没有解决方法。
  
  另外，我才发现一个struct直接赋值是C++11才允许的。比如：

	TableBackupSQL table_backup_list_[] =
	{
	  {21, "__first_root_table", "select * from __first_root_table"}
	};

  不加-std=c++0x或者 -std=gnu++0x的时候会报错。c语言支持。

  后来发现我遗忘了一个事实，宏替换是发生在预编译期的，这时候都没有做语法词法分析，程序不知道一个变量应该如何替换，所以变量实际上没有被替换成值，这跟函数定义是不一样的。比如：

	#define wrap(value) value
	int a  = 1;
  	int b = wrap(a);

  我们用gcc打印展开之后的结果如下：
  	
  	int a = 1;
  	int b = a;
  
  这里是不会展开成 int b = 1;的。而连接符\#的作用也只是把宏替换后的字面值加上引号，比如：

  	#define wrap(value) #value
  	int a  = 1;
  	const char * b = wrap(a);

  展开结果是：

    int a = 1;
  	const char * b = "a";

  而连接符\#\#的作用就更简单了，就是提供一个标示宏传入参数的作用，比如

	#define wrap(value) a##value
    int ab = 2;
  	int b = wrap(b);

  如果不写\#\#就变成了avalue，无法区分输入参数，如果写a(value)就会替换成a(b),如果写a value就会替换成a b，所以想替换成ab只能用\#\#。

  至于上面那个问题，如果我们table的名字都是宏定义的字符串，那就好办多了：

  	const char* OB_FIRST_ROOT_TABLE_TABLE_NAME  =  "__first_root_table";
  	#define TABLE_BACKUP_(table_prefix, table_name)\
	TableBackupSQL(table_prefix##_TID, table_prefix##_TABLE_NAME, "select * from " table_name)

  感谢郁白师兄的指导。

[1]: http://blog.csdn.net/maray/article/details/11096459 "介绍一个C++奇巧淫技"