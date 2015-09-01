---
layout: post
title: "RBTools兼容的问题"
date: 2015-08-31 15:26
comments: true
published: true
categories: "Python"
---
  
  某天ReviewBoard客户端突然用不了，使用	`rbt post`的时候报错:

  	from six.moves.urllib.parse import quote
	ImportError: No module named urllib.parse

  乍一看以为什么包被卸载了。于是pip install six --upgrade，无果。pip uninstall RBTools再重新安装RBTools，也无效。

  查了一下six是python2、python3的兼容包，直接修改源码，不要兼容了，发现用到的地方好多，改不过来（ps，兼容python2、python3真不容啊）。

  查看six的版本，发现跟本地一样的，本地没什么问题。说明不是six的问题。直接在命令行from six.moves.urllib.parse import quote，发现本地ok，服务器上不行。

  这就比较扯了，同样的版本，本地可以服务器不行。直接卸了重装：

    pip uninstall six #注，这里卸载了1.9的six
    pip uninstall six #日，还有一个1.2的six，不知道pip list为啥显示不出来。
    pip install six
    easy_install RBTools

  然后就ok了。所以还是要习惯在virtualenv下搞啊...
