---
layout: article
title: "记一个实际中遇到的覆盖问题"
key: an-overwrite-problem-in-cplusplus
date: 2014-06-10 19:32
comments: true
categories: "C++"
---

  工作中遇到一个继承结构如下：

	ObServerSchemaService : init_core_schema(const ObSchemaManagerV2 &schema)
	         |
	ObRootSchemaSerivice : init_core_schema()

  基类的init_core_schema接收一个核心表的schema，而这个schema往往是从rootserver传过来的，所以下面的子类RootSchemaService不需要传参，直接自己生成就好了。

  问题是如果在ObRootSchemaService的对象上想要调用ObServerSchemaService的init_core_schema函数会报错。因为命名空间上Root的会覆盖Server的，哪怕只是同名的数据成员也会隐藏基类的成员函数。比如：

	struct TableSchema
	{
	  const static int version_ = 1;
	  int mem_version()
	  {
	    return version_;
	  }
	};

	struct ExTableSchema: TableSchema
	{
	  int mem_version;
	};
	int main(void)
	{
	  ExTableSchema schema;
	  schema.mem_version();
	}


  解决方法很简单，直接指明命名空间就行了
	
	schema.TableSchema::mem_version();