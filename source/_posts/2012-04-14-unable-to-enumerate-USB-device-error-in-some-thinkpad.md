---
title: 记ThinkPad某些型号下Linux报Unable to enumerate USB device错误的问题
author: Harry Chen
layout: post

mkd_text:
  - |
    这问题确实挺烦的，据说常见于某些ThinkPad系的笔记本，具体表现是不停的报
    
    	
    	Unable to enumerate USB device…..
    
    <!--more-->
    
    的错误，而在某些Linux版本（比如pinguy os）下会不停提示Device Recognized和Device Removed，有人提供了如[1]的解决方案，但是好像在pinguy os 下并无效果，而且这实际上就是禁用了usb2.0，还有人直接禁用了全部usb。
    
    这里面好像有硬件问题，但是如果是Thinkpad系普遍的问题的话，也就有点说不过去了，硬件不检测好就出场，这也不是Thinkpad的风格。后来想到会不会是指纹识别的问题，于是在BIOS里禁用指纹识别，一切OK。反正这是实验室的笔记本，也不能存我自己的指纹吧。
    
    后来证实其实是指纹识别坏了…还好在保修内…
    
    ###参考文献：
    
    >[1] Solved: unable to enumerate USB device on port 1,
    
    ><http://uucode.com/blog/2011/01/18/solved-unable-to-enumerate-usb-device-on-port-1/>
dsq_thread_id:
  - 1289308299
categories:
  - Others
  - 与技术相关
tags:
  - Linux
  - thinkpad
  - Unable to enumerate USB device
format: standard
---
# 

这问题确实挺烦的，据说常见于某些ThinkPad系的笔记本，具体表现是不停的报


    Unable to enumerate USB device…..


的错误，而在某些Linux版本（比如pinguy os）下会不停提示Device Recognized和Device Removed，有人提供了如[1]的解决方案，但是好像在pinguy os 下并无效果，而且这实际上就是禁用了usb2.0，还有人直接禁用了全部usb。

这里面好像有硬件问题，但是如果是Thinkpad系普遍的问题的话，也就有点说不过去了，硬件不检测好就出场，这也不是Thinkpad的风格。后来想到会不会是指纹识别的问题，于是在BIOS里禁用指纹识别，一切OK。反正这是实验室的笔记本，也不能存我自己的指纹吧。

后来证实其实是指纹识别坏了…还好在保修内…

### 参考文献：

> [1] Solved: unable to enumerate USB device on port 1,
>
> 
