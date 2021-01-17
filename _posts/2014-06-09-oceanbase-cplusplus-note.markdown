---
layout: article
title: "总结Oceanbase编码中需要注意的一些细节"
date: 2014-06-09 10:38
comments: true
categories: "Oceanbase"
---

1. 所有指针使用之前都需要判断是否为NULL，尤其是如果有IF分支的情况下，如：

		if (it != NULL)
		{
			xxx
		}
		else
		{
			it不能再使用了
		}

1. 不要使用strcpy而应该使用strncpy。

1. 所有成员函数都应该考虑是否为const函数.

1. 所有函数都需要判断传入值是否有效。

1. 有返回值的函数，需要先定义返回值的默认值，不能直接返回中间结果。比如：

		//这样是很容易造成问题的
		int * xxx(xxx)
		{
			int* it = NULL;
			for(int * it =xxx;it != xxx; it ++)
			{}
		}
		//而应该这样
		int * xxx(xxx)
		{
			int* ret = NULL;
			for (int * it = xxx; it != xx; it++)
			{ret = it}
			return ret;
		}

1. 所有的错误码都需要向上抛出。错误码不能被隐藏，任何语句执行的前提条件都是之前没有错误。循环尤其需要注意。如：

		for (int i = 0; i < xx; i++)
		{
			xxx
		}
		//需要改成
		for (OB_SUCCESS == ret && int i = 0; i < xx; i++)
		{
			xxx
		}
		
1. ObArray等动态表结构使用前尽量reserve.

1. 所有不以ret为返回值的地方都要重新指定返回值。

2. 使用to_string的风格打印

2. init失败后，类成员恢复到初始状态

3. 保证函数执行的原子性，要先保存pos，然后用一个临时的pos上序列化，都成功后再改pos

4. 对存储空间要求不严格的地方，建议使用定长序列化encode_i64，以后看binary查问题会简单些
