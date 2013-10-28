---
layout: post
title: "关于svn commit fail的问题"
date: 2013-10-12 21:39
comments: true
categories: oceanbase
---

  svn commit失败的时候会产生一个svn-commit.tmp 文件， 打开之后发现里面是commit-message，难道下次提交的时候还需要把消息复制进去么？

  看看 svn help commit, 发现有 -F 可以用, 平常都只有用 -m 'message' 而已。定义如下：

> -F: 会把档案内容读进来, 然后直接 commit, 想当然就用 -F 直接取 svn-commit.tmp 来 commit.

> > * 例: svn ci -F svn-commit.tmp

<!-- more -->

  PS: commit 完后, 还是要手动 rm svn-commit.tmp.

  另一个关于commit的问题是，如果 svn ci 进入填充commit-log的交互界面的时候，突然发现提交文件列表有误怎么办？

  其实很简单，只要不保存退出，就会有提示了。保存退出才会直接提交的。放心。

  钦此。

