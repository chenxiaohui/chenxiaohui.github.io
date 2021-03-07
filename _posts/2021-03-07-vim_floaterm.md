---
title: vim-floaterm配置
layout: article
key: vim_floaterm
date: 2021-03-07 15:02
---

这个插件主要是提供vim内部调用shell环境的，安装是比较容易，但是发现会有很多不兼容的地方。

https://github.com/voldikss/vim-floaterm

安装可以用vundle、bundle或者手动等。我这边一直是bundle

git submodule add https://github.com/voldikss/vim-floaterm


首先这个插件默认配置直接跟tabnine冲突，大概是window的问题，仔细看了下代码，注释掉tabnine里面的vimsupport的window切换部分可以，但是看着不优雅啊。

![](https://cxhblog.s3.amazonaws.com/2021-03-07-070937.png)

后来发现其实可以控制floaterm不使用默认的float方式，也就是改split或者vsplit，顺便重定义快捷键。

```vimscript
    let g:floaterm_wintype = "vsplit"
    let g:floaterm_keymap_toggle = '<leader>s'
    let g:floaterm_keymap_new = '<leader>sn'
    let g:floaterm_keymap_prev = '<leader>sl'
    let g:floaterm_keymap_next = '<leader>sh'
```

但是发现vim8.0的版本下，这个快捷键定义直接会报错，查了一下function load，发现FloatermNew什么的在这个版本直接不支持。看来只能手动编译8.2了。

```shell
 ./configure --prefix=$HOME \
 --enable-multibyte \
 --enable-pythoninterp \
 --enable-python3interp \
 --enable-cscope \
 --enable-fontset \
 --enable-largefile \
 --enable-luainterp \
 --enable-tclinterp \
 --enable-perlinterp \
 --with-python3-command=python3.5 \
 --with-python-config-dir=/usr/lib/python2.7/config-x86_64-linux-gnu \
 --with-python3-config-dir=/usr/lib/python3.5/config-3.5m-x86_64-linux-gnu \
 --with-lua-prefix=/usr/local/bin/lua
```

上面编译完之后会发现vim的python和python3 support要么都没识别，要么都识别之后，进去就崩溃。看了下vim论坛的反馈，好像python和python3同时支持会有冲突。改成只用python的话，很多插件又有问题，改成只用python3好了。

```shell
 ./configure --prefix=$HOME \
 --enable-multibyte \
 --enable-python3interp \
 --enable-cscope \
 --enable-fontset \
 --enable-largefile \
 --enable-luainterp \
 --enable-tclinterp \
 --enable-perlinterp \
 --enable-rubyinterp  \
 --with-python3-command=python3.4 \
 --with-python3-config-dir=/usr/lib/python3.4/config-3.4m-x86_64-linux-gnu 
```

另外有的机器上是python3.4-dev有的是python3.5。编译完之后至少正常使用不会报错了，但是发现vimsupport切换window的时候有新问题，表现为q:的时候会直接报错。

![](https://cxhblog.s3.amazonaws.com/2021-03-07-141000.png)

开始我考虑直接改tabnine或者youcompleteme算了。。翻了下代码，windows switch的逻辑只有在youcompleteme的g:ycm_enable_diagnostic_highlighting打开的时候才会调用，看了下一些issue，这个特性打开也会带来性能的下降，而只有在编译错误提示的时候会用到，而我的vim的编译插件是我自己写的，所以算了。关掉。

```vimscript
    let g:ycm_enable_diagnostic_signs = 0
    let g:ycm_enable_diagnostic_highlighting = 0
    let g:ycm_min_num_of_chars_for_completion = 1
```

世界终于清净了。效果类似于

![](https://harrychen.oss-cn-beijing.aliyuncs.com/2021-03-07-071627.png)

然鹅折腾这些也花了一个晚上。。
