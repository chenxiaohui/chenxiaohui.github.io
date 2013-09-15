---
layout: post
title: "Octopress的一些技巧"
date: 2013-09-14 15:03
comments: true
categories: vim
---

自从把wordpress换成Octopress, 腰不酸了背不疼了, 写博客也有劲了~

以上只是吐个槽而已, Octopress是基于Jekyll的博客系统, Jekyll是从markdown生成静态网页的网页生成器. 这是背景. 详细的不表.

主要说下面几个小技巧:

###1\. alias(别名)

话说每次写博客的时候要敲rake new_post/ rake generate/ rake preview/ rake deploy...等等, 中间再出一点什么git同步的错误, 严重影响写博客的心情.可以通过alias简化命令:
  
    alias rg='rake generate && rake preview'
    alias rd='rake deploy && git add . && git commit "`date`" && git push origin source'
    alias rn='rake new_post'

###2\. 插入图片

octopress的一大优点是插图片方便, 拷贝到source/images目录下, 然后在markdown里插入就行了, 但是不是很智能啊...其实如果大家在vim里装了nerdtree的话, 完全可以通过nerdtree找到图片, 然后拷贝图片链接. 问题是nerd_tree不支持这个操作...

![](/images/2013-9/are-you-fucking-kidding-me.jpg  "你特么在逗我?")

不过我们可以 [扩展一下nerd_tree][1]. 在$VIM/nerdtree_plugin下建立yank_mapping.vim, 内容如下

    call NERDTreeAddKeyMap({
            \ 'key': 'yy',
            \ 'callback': 'NERDTreeYankCurrentNode',
            \ 'quickhelpText': 'put full path of current node into the default register' })
    function! NERDTreeYankCurrentNode()
        let n = g:NERDTreeFileNode.GetSelected()
        if n != {}
            call setreg('"', n.path.str())
        endif
    endfunction

这样找到文件之后就可以yy了~~~    yy...yy...

###3\. 生成文件直接打开

我们执行rake new_post之后, 填好title之后会在_post下生成一个markdown文件(先不讨论title翻译slug的蛋疼之处), 每次那么长的文件命不能让我每次都敲进去或者复制进去吧. 我们可以修改Rakefile在task:new_post最后加一句自动打开生成的文件:

    system "vi #{filename}"

###4\. 加快生成速度

Jekyll每次都会生成所有的_posts, 这会导致生成速度的极度下降, 而且官方也没有给出什么解决方案啊. Octopress实现一个比较笨的办法, Rake Isolate和 Rake Integrate, 从名字就可以看出, 是把需要生成的文件保留, 其他的都移出去, 生成完毕之后再移动回来. 不管怎么说吧, 至少是个方案. 写了一段简单的vimscript实现这个功能跟vim的集成.


    "plugin -ocotpress  写octopress博客的插件
    function! RakePreview()
      silent! execute "!rake isolate['".expand("%<")."']"
      silent! execute "!rake generate"
      silent! execute "!rake integrate"
      silent! execute "!google-chrome http://localhost:4000"
      silent! execute "!rake preview"
    endf

    nmap <leader>rp :call RakePreview()<cr>

chrome打开的时候还没有执行preview, 所以需要再刷新一下...preview有些输出, 觉得不想看的可以重定向.

[1]: http://stackoverflow.com/questions/16368771/copy-path-file-with-nerdtree-vim-plugin  "Copy path file with NERDtree Vim plugin"


