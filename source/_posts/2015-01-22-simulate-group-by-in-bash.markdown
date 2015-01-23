---
layout: post
title: "bash下模拟group by功能"
date: 2015-01-22 15:56
comments: true
published: true
categories: "Linux"
---
  遇到这样一个问题：有一堆数据，需要统计相同key下相同的column的重复出现次数，实际上就是数据库里面的group by功能，但是建表导入然后计算未免麻烦，何况数据是临时数据，导入计算完毕之后就不需要了。这里用shell下的一些命令来完成。

  数据格式

  	user			tag_id  type		time
	AAAAAAAAAAA		tag1	Click		2015:13:37:16
	AAAAAAAAAAA		tag1	Click		2015:13:37:16
	AAAAAAAAAAA		tag2	Click		2015:13:37:16
	BBBBBBBBBBB		tag2	Click		2015:13:37:16
	BBBBBBBBBBB		tag2	Click	    2015:13:37:16
	BBBBBBBBBBB		tag2	EXPOSURE	2015:13:37:16


  目的：

  	统计同一个用户下，同一个tag的点击次数：

  实现如下：

  1. 排序

    首先对数据进行排序。这是最基本的，见[上篇文章][1]。

  	    sort -k 1 

  2. 过滤不需要的行和列。

  	    awk '{print $1, $2, $3}' |grep "Click" 

  3. 这时候出现了一些重复列了，这也就是我们要做group by的数据。

        uniq -c | awk {'print $2, $3, $1'} 

  后面awk只是调了一下位置。合并起来就是：

 	sort -k 1  test.txt|awk '{print $1, $2, $3}' |grep "Click"|uniq -c | awk {'print $2, $3, $1'} 

  输出结果：

    AAAAAAAAAAA tag1 2
  	AAAAAAAAAAA tag2 1
  	BBBBBBBBBBB tag2 2


[1]: http://cxh.me/2015/01/22/sort-using-multiple-columns/   "Sort多列排序"
