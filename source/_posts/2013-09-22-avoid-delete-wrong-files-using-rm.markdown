---
layout: post
title: "防止通过rm误删文件"
date: 2013-09-22 20:46
comments: true
categories: Linux
---

  相信大家都有通过rm误删文件的经历, 而且Linux下又貌似没有Final Data之类的工具. 相对于Windows或者Nautilus里的删除机制, rm虽然高效, 但是很危险.

  为了防止误删文件, 我们可以把删除的文件先转移到/tmp下, /tmp下的文件会被系统定时清除, 也就起到了回收站的作用.

  这里我们首先建立如下脚本:

    #!/bin/sh 
    dirpath=/tmp/recycle_$USER # find a place for recycle
    now=`date +%Y%m%d_%H_%M_%S_`  
    arg=$1
    if [ "$arg" = "-rf" ] || [ "$arg" = "-fr" ] || [ "$arg" = "-r" ]; then # compatible with /bin/rm
        shift
        arg=$1
    elif [ -d $arg ]; then # is a directory
        echo "rm: cannot remove '$arg': Is a directory"
        exit
    fi
    filename=${now}$arg # add a timestamp for files deleted
    if [ ! -d ${dirpath} ];then  
        /bin/mkdir -p ${dirpath} 
        chmod 777 ${dirpath} 
    fi 
    /bin/mv $arg ${dirpath}/${filename} # move to trash
 
  然后把脚本命名为rm放到/bin目录下, 最好放到home/bin目录下然后指定一下Path, 这样不影响其他人.

    export PATH=$HOME/bin:$PATH

  最后记得给rm加权限就行

  需要说明的一点是, 服务器端有时候为了限制rm会给rm做alias(别名), 所以以上rm脚本需要根据实际情况判断传入参数的序号, 比如如果有别名设置如下:

    alias rm='rm -i --preserve-root' 

  就需要把上面的$1都改成$3, 钦此.
