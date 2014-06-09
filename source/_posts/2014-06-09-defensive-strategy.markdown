---
layout: post
title: "常见的防御性编程策略"
date: 2014-06-09 11:51
comments: true
categories: "Oceanbase"
---

  针对出错之后不能恢复的情况，最好的办法是写另外一个对象，确认成功之后原子的交换对象。同时也能避免对一个对象的修改持锁时间过长。这种思路广泛用在很多地方。

  1. 保存备份文件，当前的文件有可能有人在读在写，所以每次线程都写一个单独的备份文件，最后原子的覆盖之前的文件。
  2. 升级系统。自动升级的时候下载了新的可执行文件，然后删除原来的文件，替换成下载文件。当然估计不会有人直接覆盖之前的文件。
  3. 一些NOSQL的冻结。OB里面比较典型的就是UpdateServer的内存冻结，当然是copy on write实现的，最后原子的切换B树的根指针。主要是为了minor fqreeze的时候依然能提供写入服务。
  4. =运算符重载的时候，如果当前类持有的对象先释放了，但是又没能成功复制需要拷贝的对象，就会有悬空的风险。effective c++里面给了一种实现方式，就是先生成一份拷贝，再swap。

一个简单的例子如下：

	int do_checkpoint()
	{
	  int ret = OB_SUCCESS;
	  if (enable_backup_)
	  {
	    if (OB_SUCCESS != (ret = write_to_file(tmp_file_path_)))
	    {
	      TBSYS_LOG(WARN, "failed to write schema backup file:ret[%d]", ret);
	    }
	    else
	    {
	      //copy tmp to schema.ini
	      unlink(schema_file_path_);
	      if (0 == rename(tmp_file_path_, schema_file_path_))
	      {
	        TBSYS_LOG(INFO, "save schema to backup succ. refresh_times_:%ld", refresh_times_);
	      }
	      else
	      {
	        TBSYS_LOG(WARN, "rename new schema file failed:ret[%d]", ret);
	        ret = OB_ERR_UNEXPECTED;
	      }
	    }
	  }
	  return ret;
	}
