---
layout: post
title: "总结STL的通用算法基本形式"
date: 2014-06-19 09:58
comments: true
categories: "C++"
---


stl的通用算法基本有如下四种形式：

1. alg(beg, end, params)：使用源输入作为输出
2. alg(beg, end, dest, params) ：使用dest作为输出，需要保证有足够的空间，所以往往使用inserter
3. alg(beg, end, beg2, other params)：beg2作为输出，假定beg2开始的范围至少跟beg和end指定的范围一样大。
4. alg(beg, end, beg2, end2, params)：beg2 end2作为输出

举例：

第一种比如：
	find(beg, end, search_value);
	sort(beg, end);
	accumulate(beg, end, original_value);
	fill(beg, end, value); //特殊的：fill_n(begin, count, n)
	replace(beg, end, value, replace_value);
	unique(beg, end);
	count(beg, end, value);
	stable_sort(beg, end);
	reverse(beg, end);

第二种比如：
	
	copy(beg, end, back_inserter(vector));

第三种比如：
	
	replace_copy(beg, end, beg2, value, replace_value);
	unique_copy(beg, end, beg2);
	reverse_copy(beg, end, beg2);

第四种比如：
	
	find_first_of(beg, end, beg2, end2);

另外，有的算法支持谓词，比如
	
	sort(beg, end, comp)
	find_if(beg, end, comp)
	count_if(beg, end, comp)

有的算法有copy和非copy版，比如
	
	replace(beg, end, value, replace_value);
	unique(beg, end);

	replace_copy(beg, end, beg2, value, replace_value);
	unique_copy(beg, end, beg2);	