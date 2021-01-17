---
layout: article
title: "post-review插件"
key: ppost-review-plugin
date: 2014-06-21 20:57
comments: true
categories: "vim"
---

###post-review.vim

A plugin to generate post-review script

### Usage

####install:

    git clone https://github.com/chenxiaohui/post-review.vim 

put post-review.vim to your $VIM/plugin 

add this to your vimrc

    nmap <leader>pr :call PostReview()<cr>

####process:

svndiff use vimdiff: see [link](http://www.ccvita.com/445.html "svndiff use vimdiff")

gitdiff use vimdiff: see [link](http://cxh.me/2013/09/14/show-gitdiff-using-vimdiff/ "svn diff use vimdiff")

![](/assets/images/2013/git-vimdiff.png)

<!--more-->

first use svn diff/git diff and open vimdiff to see the difference

secondly when you consider the changed file needs to be posted , use <leader>pr to add it to post-review.sh

if you has no post-review.sh on your base_dir( specified by the g:base_dir_mark), you need to input the review id or just enter for a new review.

after you added all files you need to review, chmod +x post-review.sh and execute it.

(if you set g:chmod_after_create to 1 you will not need to chmod +x)


----------------------------------------

  请无视楼主以上装逼的英文:

### post-review.vim


  就是一个用来从vimdiff记录需要Post-review的文件的插件

  不知道Post-review的同学请google之, 用百度搜索的同学自觉面壁去

### 用法


####安装

  统共分三步:

1.下载解压(或者git clone) url:<https://github.com/chenxiaohui/post-review.vim>
2.放到$VIM/plugin目录下(原谅我不写doc的习惯)
3.在vimrc中添加 

    nmap <leader>pr :call PostReview()<cr>

####使用

  比如说Jack正欢快的写着代码呢，然后Jack要提交, 猛然发现好多修改啊

![](/assets/images/common/ask.jpg)

> 难道不应该写一部分就post-review的嘛

  好了不要care这种细节, 然后Jack需要一个一个查看修改的文件, 确定是放到哪个Post-review中提交

![](/assets/images/common/ask.jpg)

    What a fucking job!!!

  这时候你需要的就是这一款全自动, 人性化, 帮你生成post-review命令的插件, 只要998, 打进电话你就能拥有它...
    
![](/assets/images/common/ask.jpg)

> 跑题了...

  好了, 我们先svn diff或者git diff一下, 为了保证你看到的是如下界面请参考[这里](http://www.ccvita.com/445.html "svndiff use vimdiff")或者[这里](http://cxh.me/2013/09/14/show-gitdiff-using-vimdiff/ "svn diff use vimdiff").

![](http://www.ccvita.com/usr/uploads/2011/svn_diff.png "svndiff")

  好了, 在你需要提交文件的那个窗口用快捷键<leader>pr, 标记完了所有的文件之后进入你的根目录(根目录是什么, 这个待会再说, 不要care这种细节), 下面是不是有一个post-review.sh了? 没有? 卧槽...男子汉大丈夫, 我写的插件, 有问题....我也不承认...

  最后, 两个配置项:

    let g:base_dir_mark = 'cscope.out'

  制定了一个根目录标志, 也就是说你需要在你的项目根目录找一个(或者建一个)独一无二的文件(比如.git, cscope.out, tags)之类, 让插件去寻找这个文件, 找到之后就标识这个目录为根目录. 跟ctrlp学的.

    let g:chmod_after_create = 0

  无聊的选项, 建立完post-review之后是不是chmod +x, 无视它.

  发起新的post-review的时候建议把post-review.sh清空或者删除, 重复添加同一个文件的时候会判断.

  好了, 也就想到这么多了, 有其他的再补充, 钦此.

注：其实最后我发现还是这样更容易：

    alias st='svn st'
    alias sta='st|grep ^A '
    alias stm='st|grep ^M '
    alias po="echo 'post-review -d' >post-review.sh  && sta >> post-review.sh ; stm >> post-review.sh ; chmod +x post-review.sh ;sed -i 's/^[MA]\s\+//g' post-review.sh;sed -i 's/$/ \\\\/g' post-review.sh;vi post-review.sh"
