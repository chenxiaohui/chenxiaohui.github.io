---
layout: post
title: "用vimdiff来显示gitdiff"
date: 2013-09-14 11:40
comments: true
categories: vim
---

git diff默认是调用linux的diff工具的, 一眼看上去毕竟还是不知所云, 不像其他两栏的diff工具那么直观. 我们可以考虑用vimdiff来显示gitdiff的结果.

具体说来有两种办法:

在~/.gitconfig中我们可以通过如下语句添加一个配置项, 指明使用的diff工具.

git config --global diff.tool vimdiff  
git config --global difftool.prompt No  

这里需要注意的是我们需要通过git difftool来调用vimdiff, 默认的gitdiff依然是调用Linux diff工具的.

第二行[difftool].prompt 的作用是免除gitdiff时的提示, 否则会有如下的结果:

![](/images/2013-9/difftool-prompt.png "git diff prompt")

当然我们也可以替换掉默认的diff工具, 可以指定

    git config --global diff.external git_diff_wrapper

然后在PATH的某个目录下建立git_diff_wrapper, 比如/usr/bin/git_diff_wrapper, 内容如下:
 
    #!/bin/sh
    vimdiff "$2" "$5"

最后加执行权限

    chmod +x git_diff_wrapper

执行git diff的时候就可以看到效果

![](/images/2013-9/git-vimdiff.png "vim diff 效果")

可以看出git其实就是调用了一个外部命令然后把参数传入(分别是当前修改的文件和从版本库获取的文件, 这个文件会在tmp下生成).


