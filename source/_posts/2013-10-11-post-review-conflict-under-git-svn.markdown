---
layout: post
title: "post-review在svn和git共同存在下的冲突问题"
date: 2013-10-11 21:24
comments: true
categories: 
---

  有时候我们会同时用多种版本管理工具进行管理，或许这听着很eggache，但是有时候确实会发生，比如

* 不习惯某种版本管理工具，希望通过另一种熟悉的版本管理工具进行管理
* 有些特性是其他的版本管理工具所没有的
* 开发的版本管理和自己的分支管理策略之间有冲突，开发的版本库不允许随便建立测试分支

<!-- more -->

  具体到一种情况下，比如我们有一个svn的版本库，版本管理策略比较严格，而我们需要做一些有风险的本地开发的时候，都原意建立一个test分支，开发确定没有问题之后再合并到master分支，但是现实的情况不允许我们随便建立丢弃分支。这样就可以通过加入一个git的版本管理来实现。

  比如我们建立了一个新的版本库（repository）

  	mkdir repository.git && cd repository.git && git init --bare

  然后checkout了版本并使当前项目加入版本管理，这里我只会一个笨办法，checkout一个空的，然后mv .git目录进去，有空再研究别的方法。

  之后所有的修改都可以通过git进行管理了，git的version control文件只存在于根目录下，所以也不会污染原有版本库。

  但是post-review的时候就有问题了我们明明有修改，但是post-review总是报错：

	  There don't seem to be any diffs!
  
  这到底是什么问题呢，启动debug模式运行post-review，结果如下：

  	>>> RBTools 0.5
	>>> Python 2.6.6 (r266:84292, May  1 2012, 13:52:17) 
	[GCC 4.4.6 20110731 (Red Hat 4.4.6-3)]
	>>> Running on Linux-2.6.32-220.el6.x86_64-x86_64-with-redhat-6.2-Santiago
	>>> Home = /xxx
	>>> Current Directory = /xxx
	>>> Checking the repository type. Errors shown below are mostly harmless.
	DEBUG:root:Checking for a Bazaar repository...
	DEBUG:root:Checking for a CVS repository...
	DEBUG:root:Checking for a ClearCase repository...
	DEBUG:root:Checking for a Git repository...
	DEBUG:root:Running: git rev-parse --git-dir
	DEBUG:root:Running: git config core.bare
	DEBUG:root:Running: git rev-parse --show-toplevel
	DEBUG:root:Running: git symbolic-ref -q HEAD
	DEBUG:root:Running: git config --get branch.master.merge
	DEBUG:root:Running: git config --get branch.master.remote
	DEBUG:root:Running: git config --get remote.origin.url
	DEBUG:root:repository info: Path: /xxx.git, Base path: , Supports changesets: False
	>>> Finished checking the repository type.
	>>> HTTP GETting api/info/
	DEBUG:root:Running: git merge-base origin/master refs/heads/master
	DEBUG:root:Running: git diff --no-color --full-index --no-ext-diff --ignore-submodules --no-renames 43351ae337ca18c3f00660c9d565b18a5e904e66..refs/heads/master
	There don't seem to be any diffs!
  
  可以看到，git的检测优先于subversion，这样当前版本库被当作git管理的版本库来处理了，所以才没有变更。

  解决办法有两个，要么修改RBTool的代码，更改检测优先级，或者post-review之前运行

  	mv .git git

  这足够骗过RBTool了。

  钦此。