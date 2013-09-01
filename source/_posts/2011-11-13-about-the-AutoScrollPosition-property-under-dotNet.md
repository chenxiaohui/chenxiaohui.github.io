---
title: 关于.NET中的AutoScrollPosition属性
author: Harry Chen
layout: post
permalink: /about-the-AutoScrollPosition-property-under-dotNet/
categories:
  - .Net
tags:
  - AutoScrollPosition
---
# 

今天写一个能滚动的PictureBox，PictureBox默认没有滚动条，所以又两种实现方式，要么在PictureBox外套一个规定大小的Panel，然后设置Panel有滚动条，要么单独做一个UserControl，自己管理重绘。

但是都发现一个问题，我写拖动的代码的时候，获得了两次拖动事件之间的移动距离，然后想加到AutoScrollPosition属性上，控制滚动，但是总会跳回原点。经过了无数次艰苦卓绝的测试，最后发现一个哭笑不得的问题。

.Net实在太智能了，智能的你都想不到他智能哪里去了。

> Point p = new Point(20, 0);
panel1.AutoScrollPosition = p;

上面这句会设定有滚动20个像素

> Point p = new Point(-20, 0);
panel1.AutoScrollPosition = p;

下面这句会调回原点，原因是你设置AutoScrollPosition=20的时候，.NET自动给20加了一个符号，AutoScrollPosition变成了-20，这都好理解，问题是你累加AutoScrollPosition的时候，开始是20，取出来就变成-20，于是你再加20，刚好回原点。这是一个多么奇葩的结果，你跟一个人说，滚，然后他努力的每次向前移动20cm，结果他在原地振动了……