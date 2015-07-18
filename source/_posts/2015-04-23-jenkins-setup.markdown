---
layout: post
title: "Jenkins 安装配置"
date: 2015-04-23 13:57
comments: true
published: true
categories: "其他"
---
  
  首先介绍一下Jenkins，如果你熟悉自动化构建的话，那么肯定听说过hudson。Jenkins是hudson的开发者跟Oracle撕bi之后，另立门户的一个hudson分支。当然这么说似乎不太靠谱，目前hudson已经不维护了毕竟，而Jenkins的开发社区还是很活跃的，各种插件层出不穷。总的来说，如果你不是已经习惯了hudson并且有一个能用的副本，都应该迁移到Jenkins。

  下面说一下如何配置。

  Jenkins的安装非常简单，只需要从Jenkins的[主页][2]上下载最新的jenkins.war文件然后运行 java -jar jenkins.war。如果需要配置运行参数可以如下设置一些环境变量。

 	JENKINS_ROOT=/home/harrychen/share/jenkins
 	export JENKINS_HOME=$JENKINS_ROOT/jenkins_home
 	java -jar $JENKINS_ROOT/jenkins.war --httpPort=8080 >>output.log 2>&1 &
  	
  打开对应url可以看到如下界面

<!--more-->

  {% img img-polaroid center /images/2015/jenkins.png %}

  系统管理里面有一些需要配置的项，比如JDK：

  {% img img-polaroid center /images/2015/jenkins_jdk.png %}

  GIT

  {% img img-polaroid center /images/2015/jenkins_git.png %}

  MAVEN

  {% img img-polaroid center /images/2015/jenkins_maven.png %}

  ssh-key

  {% img img-polaroid center /images/2015/jenkins_sshkey.png %}

  ssh-server

  {% img img-polaroid center /images/2015/jenkins_sshserver.png %}

  装一下slack的插件可以配置slack

  {% img img-polaroid center /images/2015/jenkins_slack.png %}

  然后是建立项目的配置，Jenkins把每个自动发布的项目作为一个单独的配置，主要是如下几个：

  指定代码路径：

  {% img img-polaroid center /images/2015/jenkins_gitclone.png %}

  部署前事件：

  {% img img-polaroid center /images/2015/jenkins_deploy_pre.png %}

  部署后事件:

  {% img img-polaroid center /images/2015/jenkins_after_deploy.png %}

  最后保证这些事件是在之前配置的ssh-server上执行的。

  {% img img-polaroid center /images/2015/jenkins_enent_server.png %}


  细节请看[这里][1]
  
[1]: http://files.cnblogs.com/files/itech/Jenkins%E5%85%A5%E9%97%A8.pdf "Jenkins 入门"
[2]: https://jenkins-ci.org/ "Jenkins"