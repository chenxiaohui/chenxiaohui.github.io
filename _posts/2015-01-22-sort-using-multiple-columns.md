---
layout: article
title: "sort多列排序"
key: sort-using-multiple-columns
date: 2015-01-22 13:38
comments: true
published: true
categories: "Linux"
---
  遇到这样一个需求，希望按照第二列排序，第二列相同的情况下按照第一列排序，数据如下：

  	b   2   c
	c   2   b
	a   1   b
  
  习惯性的用:

  	sort -k 2 -k 1 input.txt

  输出结果是：

  	a   1   b
	c   2   b
	b   2   c
  可以看到实际上先按照第二列排序，第二列相同按照第三列排序了。问题在于sort -k默认是按照顺序排序到末尾的。如果要打破默认，需要指定从哪个列到哪个列。

  	sort -k 2，2 -k 1 input.txt

  换个角度说，`sort -k 1 -k 2` 的效果跟 `sort -k 1` 是一样的。所以最好还是让数据按照排序列生成，这样看起来也最直观。