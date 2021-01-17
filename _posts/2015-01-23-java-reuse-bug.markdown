---
layout: article
title: "java中重用对象的bug"
date: 2015-01-23 11:15
comments: true
published: true
categories: "Java"
---
  
  首先这不是java编译器的问题，就是写代码的时候大意了。

  有这样一个函数
  	
  	int parse(String msg, Message out)；

  解析一个String，返回一个结构体。这么做的目的主要是避开try catch的性能问题，通过返回码来处理异常。这里就很容易出现这样的用法了：

  	Message msg = new Message();
  	for (xxxx){
  		if (0 == parse(str, msg))

  	}

  当时觉得还挺好，复用了一个对象。实际明显有问题的，这个对象的生命周期不见得只在for循环内部，一旦引用被传递出去，就会有悬挂（java里是不是不这么叫）的问题。多个引用指向了一个对象，计算结果是不可预测的。

  主要问题是java里面默认都是传引用的，所以要时刻保持对gc机制的警惕。或者直接实现clone接口。