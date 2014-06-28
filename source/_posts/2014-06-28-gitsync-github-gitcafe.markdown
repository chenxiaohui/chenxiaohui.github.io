---
layout: post
title: "同步github上的项目到gitcafe"
date: 2014-06-28 12:41
comments: true
categories: "其他"
---
	
  github固然好，只是国内访问有点慢。为了提高博客访问速度我决定把github上托管的博客同步到gitcafe上。最好能在DNS那里做CDN，但是貌似没有免费的服务。那直接指向gitcafe好了，反正没有什么国外访问的需求。简单记一下过程。
   
  gitcafe自己有导入的功能，但是貌似不是很好用。而且不够智能。所以我们先建立一个跟用户名一样的目录。gitcafe只允许这种方式的Html页面生成。并且只渲染gitcafe-pages分支。

  我们修改source分支.git/config加入

	[remote "cafe"]
	  url = git@gitcafe.com:xxx/xxx.git
	  fetch = +refs/heads/*:refs/remotes/cafe/*

  由于

	[branch "source"]
	  remote = origin
	  merge = refs/heads/source

  所以当前source分支（这下面我没有master）默认提交到origin（github)，所以我们通过

	git push cafe

  提交source，会被扩展成：

	git push cafe source:source "当前分支

  然后提交_deploy，这是渲染之后的html页面，前面那个是octopress的源码。修改_deploy/.git/config

  	[remote "cafe"]
	  url = git@gitcafe.com:chenxiaohui/chenxiaohui.git
	  fetch = +refs/heads/*:refs/remotes/cafe/*

  然后提交:

  	git push cafe master:gitcafe-pages

<!--more-->

  本地分支名字和远程分支不同的时候不能省略，否则会被自动扩展成相同的名字。这就是问题了，我们多了一个master分支....

  按照gitcafe的教程删除master未果，不过顺便把默认分支改成了gitcafe-pages。删除master分支的时候，里面有一段说明：

	为什么要删除 master 分支
	当你在创建一个新的仓库的时候没有指定分支的话，Git 会默认创建 master 分支并指定它为默认分支。

	一般情况下使用 master 分支作为整个项目的核心分支是很普遍的行为， 而 Pages 服务之所以使用 gitcafe-pages 分支的方式区别项目文件和 Pages 文件。 这样你就可以在一个仓库中保存他们而且彼此不会有任何影响。

	但是像是个人主页类的 Pages 服务或其他一些应用场合，可能并不需要 master 的存在， 甚至必须要删除它，或者只是你有洁癖┑(￣Д ￣)┍ 那么你就需要如下的方法来删除 master 分支。

  (#‵′)靠，就是这样。

  最后修改一下Rakefile

	...
	    system "git push origin #{deploy_branch}"
	    system "git push cafe #{deploy_branch}:gitcafe-pages"
	    puts "\n## Github Pages deploy complete"
	  end
	...

	  puts "\n## Pushing source"
	  system "git push origin "
	  system "git push cafe"
	  puts "\n## Github source pushed"

  当然问题是同一个本地分支track了两个远程分支，但是默认值只能配置一个：

	[branch "master"]
		remote = cafe
		merge = refs/heads/gitcafe-pages

  这说明master分支上更新gitcafe必须指明repository，好在我们直接用git push/pull不带任何参数的时候不多。同时如果git pull的话，默认的merge两个repository是不同的，好在我们也一般不用从两个repository上面pull。 

  顺便去挂一下域名就好了。

  矮马，快多了。

[1]: http://blog.gitcafe.com/116.html "GitCafe正式推出Pages服务"
[2]: https://gitcafe.com/GitCafe/Help/wiki/%E5%A6%82%E4%BD%95%E5%88%A0%E9%99%A4-Master-%E5%88%86%E6%94%AF "如何删除 Master 分支"