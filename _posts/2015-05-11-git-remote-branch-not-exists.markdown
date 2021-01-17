---
layout: article
title: "Git远程分支不存在的问题"
date: 2015-05-11 12:11
comments: true
published: true
categories: "Linux"
---

  建立了一个远程分支，提交到origin上之后，发现之前有一个同样的远程Repository存在，而且名字一样，这就比较D疼了，git branch -a 显示的分支里面的分支提交到了另一个Repository，但是这个Repository已经改名字了，虽然地址一样。

  搞来搞去之后发现git checkout远程分支的时候报不存在的问题，删除这个分支的时候同样有这个问题：

  	unable to delete 'refactor': remote ref does not exist

  导致这个分支就这么存在着删不掉了。查stackoverflow有人给出[如下的方案][1]：

  	git fetch -p origin

  问题是能解决了，但是不太理解为什么。


[1]: http://stackoverflow.com/questions/10292480/when-deleting-remote-git-branch-error-unable-to-push-to-unqualified-destinatio   "When deleting remote git branch “error: unable to push to unqualified destination”"
