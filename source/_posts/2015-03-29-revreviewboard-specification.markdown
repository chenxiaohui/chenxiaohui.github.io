---
layout: post
title: "ReviewBoard客户端配置和代码review流程"
date: 2015-03-29 20:17
comments: true
published: true
categories: "其他"
---

## Postreview 客户端配置

  reviewboard是群众喜闻乐见的代码review工具。本文主要涉及客户端配置和review流程，server端配置见[文档1][1]。

  首先安装python（必须的），之后安装post-review插件:

  	pip:
  		pip install --allow-external RBTools --allow-unverified RBTools RBTools
  	easy_install：
  		easy_install -U RBTools
  	LinuxRPM:
  		sudo yum install RBTools
  	直接安装：
  		git clone git://github.com/reviewboard/rbtools.git
  		cd rbtools
  		python setup.py

  旧版的post-review有一个post-review的命令，新的只有rbt了，命令格式不太一样。

    post - Posts changes to Review Board
    diff - Displays the diff that will be sent to Review Board
    land - Lands a change in a local branch or on a review request
    patch - Patches your tree with a change on a review request
    setup-repo - Sets up RBTools to talk to your repository

  首先配置review board，HOME目录下简历.reviewboardrc如下：

  	REVIEWBOARD_URL = 'http://10.16.10.74/'
	  REPOSITORY = 'adrd-service'

  或者在代码目录执行rbt setup-repo，会生成上述文件。REPOSITORY原则上不配置也行。

## PostReview流程。

　原则上git commit 之后，git push之前要提交post-review，保证代码修改相关人都知悉并ship修改才能提交。基本流程是：

  	git add xx
  	git commit -m "message"
  	rbt post

  对同一个更改post之后如果要再次修改，可以：

  	rbt post -r <post_id>

  post-id是每个post的url/r/后面的数字。post-review标题原则上按照如下规范：

  	[repository_name][branch_name][NewFeature|BugFix|Refactor|Log] post-review title

  groups/people添加的人员原则上包括：

  	1. 技术主管[mentor]
  	2. 合作者[partner]
  	2. 其他需要知悉修改的人[related]

  post-review旧版和svn的整合见[文档2][2]。
  post-review在svn和git同时托管的情况下处理冲突的方法见[文档3][3]。
  一个post-review的vim插件见[文档4][4]。




[1]: http://cxh.me/2015/03/28/review-board-setup/   "Reviewboard的安装"
[2]: http://cxh.me/2013/10/15/svn-vim-integration/ "Svn Vim 整合方案"
[3]: http://cxh.me/2013/10/11/post-review-conflict-under-git-svn/ "Post-review在svn和git共同存在下的冲突问题"
[4]: http://cxh.me/2014/06/21/ppost-review-plugin/ "Post-review插件"
###Bibliography:

  \[1] Reviewboard的安装, <http://cxh.me/2015/03/28/review-board-setup/>

  \[2] Svn Vim 整合方案, <http://cxh.me/2013/10/15/svn-vim-integration/>

  \[3] Post-review在svn和git共同存在下的冲突问题, <http://cxh.me/2013/10/11/post-review-conflict-under-git-svn/>

  \[4] Post-review插件, <http://cxh.me/2014/06/21/ppost-review-plugin/>
