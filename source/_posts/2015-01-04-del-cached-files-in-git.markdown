---
layout: post
title: "git中删除已经缓存的文件"
date: 2015-01-04 16:49
comments: true
published: true
categories: "其他"
---

  经常遇到一种情况，开始项目的时候没加.gitignore文件，提交之后发现有大量的pyc文件残留，这样两地共同修改的时候pyc文件会造成大量的冲突。针对这种情况，可以如下解决：

  1. 建立.gitignore文件并写入：

  		.pyc
  		.swp

  2. 删除所有缓存中的数据：

  		find . -name '*.pyc' -o -name '*.swp' > /tmp/files
  		while read line; do
  			git rm --cached $line
  		done < /tmp/files

  3. 在冲突的一端回滚所有pyc冲突：

		find . -name '*.pyc' -o -name '*.swp' > /tmp/files
  		while read line; do
  			git checkout -f  $line
  		done < /tmp/files

  4. 冲突的一端更新修改：

  		git pull origin

  补充：

  蛋疼了...直接这样就行了 

    rm `  find . -name '*.pyc' -o -name '*.swp'`

  忘了这些命令都接受多个参数....