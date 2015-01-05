---
layout: post
title: "Linux上的远程log监控"
date: 2015-01-04 17:34
comments: true
published: true
categories: "Linux"
---

  名字太大，其实只是遇到了一个问题，想远程实时看一个log文件的变化。开始是这么做的。

  	vim 里面 :e scp://xxx@xxx//filePath
  	:e! 来刷新
   
   太low了。直接用ssh：

   	ssh xx@xxx "less filePath"

   发现less直接就退出了。 换成:

   	ssh -t xx@xxx "less filePath"

   也不能实时刷新。测试less 本地一个文件同时写入，发现less没有实时刷新的功能。看来是在ob的时候deploy给我的错觉啊。

   换tail:

    ssh -t xx@xxx "tail filePath"

   还是直接执行完毕退出。查tail有没有自动刷新的模式，有一个follow：

    ssh xx@xx "tail -f filePath"

   搞定。*配合[TMux]绝对好用*。
   
[1]: http://kumu-linux.github.io/blog/2013/08/06/tmux/   "Linux下终端利器tmux"
