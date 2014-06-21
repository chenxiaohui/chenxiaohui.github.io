---
title: FTP命令
author: Harry Chen
layout: post

categories:
  - Others
---

  用命令如何把自己写好的网页上传到服务器或者从服务器上下载东西呢。方法有很多。用ftp是个不错的选择。方法如下



    echo open 你的ftpip >ftp.txt

    echo user >>ftp.txt

    echo password>>ftp.txt

    echo get test.exe >>ftp.txt

    echo bye >>ftp.txt

    ftp -s:ftp.txt

    del ftp.txt

  这样就可以把test.exe下载下来。也可以做个批处理


    @echo off

    echo open 你的ftpip >ftp.txt

    echo user >>ftp.txt

    echo password>>ftp.txt

    echo get test.exe >>ftp.txt

    echo bye >>ftp.txt

    ftp -s:ftp.txt

    delftp.txt

    @cls


  之前的部分是转载，其实就是利用了ftp命令可以读取指令的功能，实际ftp.txt文件内容如下（中文部分是需要替换的）：


    open 你的ftp地址

    你的用户名

    你的密码

    bin

    get 你的文件名

    bye
