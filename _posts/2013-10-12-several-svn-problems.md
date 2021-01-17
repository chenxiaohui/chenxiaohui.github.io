---
layout: article
title: "几个svn的问题"
key: several-svn-problems
date: 2013-10-12 19:27
comments: true
categories: oceanbase 
---

### 误用rm删除了未提交文件

  经常会遇到这种情况：本地修改了一部分东西，增增改改删删，后来发现已经用svn add过的的文件被删除了，但是这个文件只是加入了版本控制，而并不再版本库里，这时候post-review就会有各种问题。如图（前面有感叹号的文件）：

![](img-ploaroid center /images/2013/before_revert.png "直接用rm删除的文件" "直接用rm删除的文件")

<!-- more -->

  解决办法也很简单，我们直接:

	svn revert ob_alive_table_tablet_iter.h

  这时候文件并不会被恢复，但是svn status上已经显示删除了，post-review不会再报错，如下图所示：

![](img-ploaroid center /images/2013/after_revert.png "revert之后" "revert之后")


### 版本控制中移除文件

  经常会遇到错误的把文件加入了版本控制的情况，比如我加了一个Makefile.in到版本控制里（如图），但是svn rm 会同时从版本库和本地删除这个文件，这是我所不希望的，毕竟我还要再跑一遍automake。

![](img-ploaroid center /images/2013/before-rm.png "错误的把Makefile.in加入版本控制" "错误的把Makefile.in加入版本控制")

  其实 svn rm 提供了keep-local选项来保留本地副本：

	svn rm Makefile.in --keep-local

  执行之后的版本库状态如下图：

![](img-ploaroid center /images/2013/before-rm.png "版本控制的状态" "版本控制的状态")

  从文件管理里面看，这个本地副本依然存在，如下图：

![](img-ploaroid center /images/2013/ll-result.png "文件管理里的情况" "文件管理里的情况")

