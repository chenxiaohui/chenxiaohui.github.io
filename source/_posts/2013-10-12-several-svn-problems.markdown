---
layout: post
title: "几个svn的问题"
date: 2013-10-12 19:27
comments: true
categories: oceanbase 
---

### 误用rm删除了未提交文件

经常会遇到这种情况：本地修改了一部分东西，增增改改删删，后来发现已经用svn add过的的文件被删除了，但是这个文件只是加入了版本控制，而并不再版本库里，这时候post-review就会有各种问题。如图（前面有感叹号的文件）：

{% img img-ploaroid center /images/2013-10/before_revert.png "直接用rm删除的文件" "直接用rm删除的文件" %}

解决办法也很简单，我们直接:

	svn revert ob_alive_table_tablet_iter.h

这时候文件并不会被恢复，但是