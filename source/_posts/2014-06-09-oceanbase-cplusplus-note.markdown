---
layout: post
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

2. 不要使用strcpy而应该使用strncpy。

3. 所有成员函数都应该考虑是否为const函数.

4. 所有函数都需要判断传入值是否有效。

5. 有返回值的函数，需要先定义返回值的默认值，不能直接返回中间结果。比如这样是很容易造成问题的：
	
	int * xxx(xxx)
	{
		int* it = NULL;
		for(int * it =xxx;it != xxx; it ++)
		{}
	}

而应该这样

	int * xxx(xxx)
	{
		int* ret = NULL;
		for (int * it = xxx; it != xx; it++)
		{ret = it}
		return ret;
	}

4. 所有的错误码都需要向上抛出。错误码不能被隐藏，任何语句执行的前提条件都是之前没有错误。循环尤其需要注意。如：

	for (int i = 0; i < xx; i++)
	{
		xxx
	}

需要改成

	for (OB_SUCCESS == ret && int i = 0; i < xx; i++)
	{
		xxx
	}
