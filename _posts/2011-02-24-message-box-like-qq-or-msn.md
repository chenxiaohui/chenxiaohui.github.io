---
title: '仿QQ、MSN消息提示窗口的实现（C#）'
author: Harry Chen
key: message-box-like-qq-or-msn
layout: article

dsq_thread_id:
  - 1255708991
categories:
  - .Net
  - 与技术相关
tags:
  - MSN
  - QQ
  - 多窗口
  - 多线程
  - 消息提示
---

  前言：我们在QQ、MSN、飞信等即时通信软件中经常看到消息弹出提示，即屏幕右下角弹出一个消息提示框，然后过一段时间隐去（有时候也不隐去，比如一个艰难的决定）。这种提示方式在消息通信中比弹MessageBox更符合用户习惯，前者往往阻碍用户正常操作。我们尝试在.Net下模拟这种方式。

  坦白的说核心代码是某位大牛（John O’Byrne）写的，另一位大牛Patrick Vanden Driessche 修改了部分代码，我在此基础上增加了对多弹框的支持，文后附了原代码和我修改之后的代码。

  多弹框的实现部分主要写了一个PlaceManager类每次从0下标开始检测哪个位置可用，然后在这个位置弹出消息提示框，消息提示框隐掉之后再回收这个位置。

  考虑到同时弹出两个及两个以上框的几率非常小，同时建立TaskbarNotifier窗口的过程资源消耗较多，程序里默认建立了一个TaskbarNotifier的对象，每次检测如果这个对象没有被使用则直接填入标题和内容并弹出，否则新建一个TaskbarNotifier对象再弹出。没有做使用概率的分析，大家如果觉得一个不够用可以默认多建立几个。

  Demo里弹出消息提示框是在界面线程里，如果不是界面线程则会有问题，即使取消了CheckForIllegalCrossThreadCalls依然不行，这时需要在界面类里添加代理方法，使用代理方法弹出消息，具体代码如下所示，这问题也困扰了我好久：


    delegate void PromptMessage(string message);
    public void Msg(string message)
    {
    	PromptMessage call = new PromptMessage(PromptMsg);
    	this.Invoke(call, new object[] { message });
    }

  程序界面如图1所示：

![未命名][1] 图2 程序界面

  点击[这里][2]下载源程序代码，[这里][3]下载我添加了多窗口提示后的代码。

参考文献：

 [1]: TaskbarNotifier代码，Created by John O’Byrne，2002-12-2，Modified by Patrick Vanden Driessche ，2003-1-11

