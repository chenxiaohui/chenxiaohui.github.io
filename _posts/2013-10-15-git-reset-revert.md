---
layout: article
title: "git reset和git revert"
key: git-reset-revert
date: 2013-10-15 14:50
comments: true
categories: oceanbase
---

### git reset 作用

  git reset 主要完成到版本库某个特定版本的回退，分为如下三种方式

![](img-ploaroid center /images/2013/git-reset.png "git-reset三种方式" "git-reset三种方式")

>* git reset –mixed：此为默认方式，不带任何参数的git reset，即时这种方式，它回退到某个版本，只保留源码，回退commit和index信息
* git reset –soft：回退到某个版本，只回退了commit的信息，不会恢复到index file一级。如果还要提交，直接commit即可
* git reset –hard：彻底回退到某个版本，本地的源码也会变为上一个版本的内容

### git revert 作用

  git revert从字面的理解上跟git reset是一样的，不同之处在于git revert生成一个反向的差异（特定版本-当前版本）然后提交到版本库，相当与做了之前操作的逆操作，这个操作是可以直接在版本库中看到并使用git reset回退的。

### 撤销之后恢复

  git-reset如果执行之后，再想回退到指定版本。//TODO


