---
title: weka命令行脚本
author: Harry Chen
layout: post
permalink: /weka-command-line-script/
dsq_thread_id:
  - 1257097178
categories:
  - Others
---
# 

例如获取Bagging方法numExecutionSlots=1,2,3,4,5时，训练集image_train.arff上的正确率和测试集image_test.arff上的正确率，可以使用如下批处理：


    @echo off

    for /l %%i in (1,1,5) do (
    echo numExecutionSlots=%%i

    java weka.classifiers.meta.Bagging -t image_train.arff -d train.model
    -v -P 100 -S 1 -num-slots %%i -I 10 -W weka.classifiers.trees.REPTree
     -- -M 2 -V 0.0010 -N 3 -S 1 -L -1|findstr "Correctly"

    java weka.classifiers.meta.Bagging -l train.model -T image_test.arff|
    findstr "Correctly")

-v(不输出静态信息)之后到|findstr之前的部分可以在界面上配好然后右键拷贝到剪贴板

结果第一行为训练集正确率，第二行为测试集正确率

![][1]

weka3.7.2下测试通过

   [1]: http://fmn.rrimg.com/fmn049/20101120/2005/b_large_e8kG_3ec00001ddd55c15.jpg
