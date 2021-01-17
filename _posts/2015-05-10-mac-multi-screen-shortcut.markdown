---
layout: article
title: "mac下多屏幕移动窗口的快捷键"
date: 2015-05-10 15:50
comments: true
published: true
categories: "mac"
---
  
  mac下使用多屏幕的话，经常需要把一个窗口移动到另一个窗口，windows下有快捷键win+shift+左右，linux下貌似可以通过xdotool实现，绑定一个快捷键，xdotool帮助你移动窗口到一个绝对位置。如下：

  	xdotool getactivewindow windowmove 0 y windowactivate windowfocus
	xdotool getactivewindow windowmove 1280 y windowactivate windowfocus

  mac下没有找到对应的系统快捷键，虽然可以设定一个zoom键来完成窗口最适化，但是没有快捷键来完成窗口的移动。这里我们通过[Moom][1]实现。

  Moom是一个窗口管理工具，安装之后只有一个配置页面，但是你会发现鼠标移动到左上角窗口最适化的按钮上的时候会弹出一个窗口管理的提示框。如下：

![](/images/2015/moom_tooltip.png)

  然后我们配置窗口移动的功能，首先需要一个全局快捷键：

![](/images/2015/moom_shortcut.png)

  之后可以设置按下全局快捷键之后上下左右键的功能。有移动窗口，半最大化窗口，缩小放大和移动窗口到一个屏幕。

![](/images/2015/moom_config.png)

  这样就可以先按下全局快捷键，如下：

![](/images/2015/moom_press_shortcut.png)

  再通过你定义的快捷键来移动窗口了。



[1]: http://manytricks.com/moom/   "Moom"
