---
layout: article
title: "一些python小技巧"
key: python-tricks
date: 2015-05-27 10:54
comments: true
published: true
categories: "Python"
---

1. 生成一个重复列表可以通过如下语句:
	
		[i] * n #这比[ i for _ in range(0,n) ]简洁太多
		同样可以"i" * n来生成字符串

2. map函数。
	
	可以用来分类函数和其调用参数，对于线程池比较有用。比如

		import urllib2 
		from multiprocessing.dummy import Pool as ThreadPool 

		urls = [
		        'http://www.python.org', 
		        # etc.. 
		        ]

		pool = ThreadPool(4) 
		results = pool.map(urllib2.urlopen, urls)
		pool.close() 
		pool.join() 

