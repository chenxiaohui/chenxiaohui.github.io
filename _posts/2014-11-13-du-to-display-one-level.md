---
layout: article
title: "du显示只显示一层子目录/文件的大小"
key: du-to-display-one-level
date: 2014-11-13 17:55
comments: true
categories: "Linux"
---
  经常需要看当前目录下的子目录大小，比如开发机被人占满的情况，`du -lh`显示的是递归的所有文件大小，`du -s`又只统计了所有文件/文件夹合起来的大小。正常情况下需要执行：

  	du -lh --max-depth=1

  未免太过麻烦。后来肖总提示发现这样就行了：

  	du -sh *

  果然是学无止境啊