---
layout: article
title: "关于一个配置项的设计"
key: a-desgin-problem-of-config
date: 2014-06-28 16:27
comments: true
categories: "Oceanbase"
---

  有个需求需要配置每张表的备份SQL语句，我开始想实现如下的效果：

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

	struct TableBackupTransaction
	{
	  static const int OB_MAX_SQL_PER_TRANS = 5;
	  TableBackupSQL sql_list_[OB_MAX_SQL_PER_TRANS];
	};


	TableBackupTransaction table_backup_list_[] =
	{
	  {
	    TableBackupSQL(1, "name", "select * from cs"),
	    TableBackupSQL(2, "name2", "select 2* from cs")
	  },
	  {
	    TableBackupSQL(1, "name", "select * from cs")
	  }
	};
  
  然后用宏美化一下就成这样了：
<!--more-->

	#define TABLE_BACKUP_SINGLE(table_prefix, sql)\
	  { TableBackupSQL(table_prefix##_TID, table_prefix##_TABLE_NAME, sql) }
	#define TABLE_BACKUP(table_prefix, sql)\
	   TableBackupSQL(table_prefix##_TID, table_prefix##_TABLE_NAME, sql)
	#define TABLE_BACKUP_MULTIPLE

	ObInnerTableBackupGuard::TableBackupSQL ObInnerTableBackupGuard::table_backup_list_[][MAX_SQL_PER_TRANS] =
	{
	  TABLE_BACKUP_SINGLE(OB_FIRST_ROOT_TABLE, "select * from %s"),

	  TABLE_BACKUP_MULTIPLE
	  {
	    TABLE_BACKUP(OB_ALL_TABLE, "select * from %s"),
	    TABLE_BACKUP(OB_ALL_COLUMN, "select * from %s"),
	    TABLE_BACKUP(OB_ALL_JOIN_INFO, "select * from %s"),
	    TABLE_BACKUP(OB_ALL_DDL_OPERATION, "select max(schema_version) from %s "),
	  },

	  TABLE_BACKUP_SINGLE(OB_ALL_SYS_STAT, "select * from %s"),
	  TABLE_BACKUP_SINGLE(OB_ALL_SYS_PARAM, "select * from %s"),
	  TABLE_BACKUP_SINGLE(OB_ALL_USER, "select * from %s"),
	  TABLE_BACKUP_SINGLE(OB_ALL_TABLE_PRIVILEGE,  "select * from %s"),
	  TABLE_BACKUP_SINGLE(OB_ALL_CLUSTER, "select * from %s"),
	  TABLE_BACKUP_SINGLE(OB_ALL_TRIGGER_EVENT, "select * from %s"),
	  TABLE_BACKUP_SINGLE(OB_ALL_CLIENT, "select * from %s"),
	  TABLE_BACKUP_SINGLE(OB_ALL_SYS_CONFIG,"select * from %s"),
	  TABLE_BACKUP_SINGLE(OB_ALL_SYS_CONFIG_STAT, "select * from %s"),
	  TABLE_BACKUP_SINGLE(OB_ALL_SERVER, "select * from %s"),
	  TABLE_BACKUP_SINGLE(OB_ALL_CLUSTER_STAT, "select * from %s")
	};

  无奈想法很美好，实际上行不通，至少不开C++11新特性的情况下，不允许这样初始化，退而求其次：
  

	struct TableBackupTransaction
	{
	  static const int OB_MAX_SQL_PER_TRANS = 5;
	  int sql_count_;
	  TableBackupSQL sql_list_[OB_MAX_SQL_PER_TRANS];
	  TableBackupTransaction(const TableBackupSQL * sql_list, int count)
	  {
	    //assert, length sql_list
	    for(int i = 0; i < count; i++)
	    {
	      sql_list_[i] = sql_list[i];
	    }//or memcpy
	    sql_count_ = count;
	  }
	  TableBackupTransaction(const TableBackupSQL & sql_list)
	  {
	    sql_list_[0] = sql_list;
	    sql_count_ = 1;
	  }
	};

	TableBackupTransaction table_backup_list_[] =
	{
	  TableBackupTransaction({
	    TableBackupSQL(1, "name", "select * from cs"),
	    TableBackupSQL(2, "name2", "select 2* from cs")
	  }),
	  TableBackupTransaction({
	    TableBackupSQL(1, "name", "select * from cs")
	  })
	};

  多了一次复制，但是初始化列表{a,b,c...}在不开C++11的时候不能作为函数参数传递，只能这样

	TableBackupSQL table_backup_[] =
	{
	    TableBackupSQL(1, "name", "select * from cs"),
	    TableBackupSQL(2, "name2", "select 2* from cs")
	};
	TableBackupTransaction table_backup_list_[] =
	{
	  TableBackupTransaction(table_backup_, sizeof(table_backup_)/sizeof(TableBackupSQL)),
	  TableBackupTransaction(TableBackupSQL(1, "name", "select * from cs"))
	};

  弱爆了，最后改成二位数组好了：

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
	  bool is_valid() const
	  {
	    return sql_ != NULL && table_name_ != NULL && table_id_ != OB_INVALID_ID;
	  }
	};

	TableBackupSQL table_backup_list_[][5] =
	{
	  {
	    TableBackupSQL(1, "name", "select * from cs"),
	    TableBackupSQL(2, "name2", "select 2* from cs")
	  },
	  {
	    TableBackupSQL(1, "name", "select * from cs")
	  }
	};

  只不过二维数组每个维度只是数组，没有额外的信息，不能扩展，访问只能这样：

	int main(void)
	{
	  TableBackupSQL (*trans)[5] = table_backup_list_;
	  for (int i = 0; i < sizeof(table_backup_list_)/(sizeof(TableBackupSQL)*5); i++, trans++)
	  {
	    for (int j = 0; j < 5; j++)
	    {
	      const TableBackupSQL& desc = *trans[j];
	      if (!desc.is_valid())
	      {
	        break;
	      }
	      printf("%d, %d: %d, %s, %s\n",i ,j , desc.table_id_, desc.table_name_, desc.sql_);
	    }
	  }
	}

或者

	int main(void)
	{
	  for (int i = 0; i < sizeof(table_backup_list_)/(sizeof(TableBackupSQL)*5); i++)
	  {
	    const TableBackupSQL (&trans)[5] = table_backup_list_[i];
	    for (int j = 0; j < 5; j++)
	    {
	      const TableBackupSQL desc = trans[j];
	      if (!desc.is_valid())
	      {
	        break;
	      }
	      printf("%d, %d: %d, %s, %s\n",i ,j , desc.table_id_, desc.table_name_, desc.sql_);
	    }
	  }
	}

  弱爆了....所以我最后决定把Transaction和单条事务直接分开了....
