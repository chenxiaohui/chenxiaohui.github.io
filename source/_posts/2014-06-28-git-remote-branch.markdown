---
layout: post
title: "git远程分支和配置文件详解"
date: 2014-06-28 11:14
comments: true
categories: "其他"
---

  最近同时同步博客到github和gitcafe上，遇到一些问题，我们分如下几个方面来分析一下：

### 推送远程分支到同一个服务器

  比如首先建立git服务器，顺便clone出两个副本

	mkdir server
	cd server
	git init --bare
	cd ..
	git clone server git1
	git clone server git2

  目前git branch是空的。我们提交一点东西建立master分支。

	cd git1
	touch a.txt
	git add .
	git commit -m "init"
	git push origin master

  现在git branch -a 显示:

	* master
	  remotes/origin/master

  当前系统处于master分支，远程origin的repository上也有一个master分支。两个是tracking的。我们切到git2下面

	cd ../git2
	git pull origin

  这时候git2跟git1完全同步了。现在我们开始尝试建立另一个分支并推送到服务器。习惯的，我们还是切回git1

	cd ../git1
	git checkout -b source

  这时候我们已经有了一个本地分支了，如果这个分支不需要共享，那么你可以一直在这个分支上commit但是不push到服务器，直到这个分支被合并回主分支或者丢弃。git branch 显示如下：

	  master
	* source

<!--more-->

  我们最终决定把这个分支push到服务器上与其他人共享，如下：

	git push origin source:source

  这时候git branch -a 能看到当前repository里面所有的分支，包括两个本地的，两个远程的，本地和远程的都处于tracking状态。

	  master
	* source
	  remotes/origin/master
	  remotes/origin/source

  切到另一个副本。
	
	cd ../git2
	git pull origin

  显示如下：

	 * [新分支]          source      -> origin/source

  git branch -a显示本地已经有了一个远程分支的指针，但是没有tracking这个分支的本地分支：

	* master
	  remotes/origin/master
	  remotes/origin/source

  同样我们可以在.git/refs/remotes/origin下看到分支的名字，但是refs/heads下面并没有。我们来检出这个远程分支：
	
	git checkout -b source origin/source

  这时候git branch -a 显示就跟git1一致了。git2下也可以编辑source分支并同步。这些都是比较常见的操作，我们需要注意的是，多分支下默认的参数。比如，在两个分支都修改一点东西：

	cd ../git1
	git checkout master
	//modify 
	git add .
	git commit -m "master modify"
	git checkout source
	//modify
	git add .
	git commit -m "source modify"

  这时候git push origin 是针对当前分支的，所以两个分支同时push更新只能
	
	git push origin
	git checkout master
	git push origin

  pull更新的时候
	
	cd ../git2
	git checkout master
	git pull origin

  这会同时更新两个分支的指针，但是不会merge另一个分支，我们去另一个分支下

	git checkout source
	git pull origin

  但是出错如下：

	You asked to pull from the remote 'origin', but did not specify
	a branch. Because this is not the default configured remote
	for your current branch, you must specify a branch on the command line.

  问题在于没有给当前分支配置merge的路径，git不知道去merge哪个分支。（～～虽然我觉得既然是tracking的不应该不知道啊～）。

  如果你有 1.6.2 以上版本的 Git，--track 选项可以同时配置merge的路径：
	
	git checkout --track origin/serverfix

  这里我们修改配置文件加入branch "source"：

	[core]
		repositoryformatversion = 0
		filemode = false
		bare = false
		logallrefupdates = true
	[remote "origin"]
		url = /media/cxh/backup/work/ceshi/git/server
		fetch = +refs/heads/*:refs/remotes/origin/*
	[branch "master"]
		remote = origin
		merge = refs/heads/master
	[branch "source"]
		remote = origin
	    merge = refs/heads/source

  这意味着每次fetch origin的时候更新所有remotes/origin的头指针到refs/heads/下面，具体可以去.git下查阅这个目录，但是头指针都是只读的。merge是由所在branch定义的。

  我们加了branch "source"的配置指定当前source的merge策略是使用refs/heads/source来合并到当前分支。这样就可以顺利的git pull origin了。

### 推送远程分支到不同服务器

  我们先建立新的repo：

	cd ..
	mkdir server2
	cd server2
	git init --bare
  
  加入git1副本，并提交

	git remote add server xxx/server2
	git push server

  上面过程的本质是提交当前分支头指针到server，相当于拷贝refs/head/xxx到refs/remotes/server/下并提交。git push server会被展开成

	git push server 当前分支名：当前分支名

  我们可以在git2副本同样加入该repository并更新引用

	git remote add server xxx/server2
  	git fetch server

  可以看到refs下目录结构如下：

	├── heads
	│   ├── master
	│   └── source
	├── remotes
	│   ├── origin
	│   │   ├── master
	│   │   └── source
	│   └── server
	│       └── source
	└── tags

### 总结一下

* update

	- fetch操作的本质是更新repo所指定远程分支的头指针(server->refs/remotes/xxx/)

	- merge操作的本质是合并当前分支和指定的头指针(refs/remotes/xxx->refs/heads)
	
	- pull操作的本质是fetch + merge

* commit
	
	- commit的本质是修改了当前分支的头指针(refs/heads)
	
	- push操作本质是提交当前分支头指针到server，顺便也修改了本地存储的server头指针(refs/remotes/xxx)

* checkout
	
	- 复制本地分支的本质是拷贝了refs/heads/下的一个头指针
	
	- push本地分支到server的本质是把这个头指针上传服务器，顺便拷贝了本地存储的server头指针（refs/remotes/xxx)
	
	- tracking远程分支的本质是把refs/remotes/下的指针拷贝到了refs/heads下

> 注：以上过程都没有涉及数据流。

[1]:http://git-scm.com/book/zh/Git-%E5%88%86%E6%94%AF-%E8%BF%9C%E7%A8%8B%E5%88%86%E6%94%AF "Git 分支 - 远程分支"

###参考文献:

>\[1] Git 分支 - 远程分支, <http://git-scm.com/book/zh/Git-%E5%88%86%E6%94%AF-%E8%BF%9C%E7%A8%8B%E5%88%86%E6%94%AF>