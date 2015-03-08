---
layout: post
title: "编译hadoop native lib"
date: 2015-03-08 14:59
comments: true
published: true
categories: "分布式系统"
---
  跑hadoop的时候总遇到这个问题，不影响但是比较烦：

	WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform… using builtin-java classes where applicable	

  大概原因是说为hadoop native library是32位系统编译的，在64位系统上会有这个提示，需要下载hadoop的源码重新编译。如下：

1. 安装maven.
2. 配置好MAVEN_HOME/PATH
3. 下载 hadoop-2.4.0-src.tar.gz。
4. 安装protobuf2.5.9。
4. 安装cmake.
5. 安装openssl-devel
4. 安装ant
3. 安装zlib-devel
5. mvn package -Pdist,native -DskipTests -Dtar
6. 配置hadoop 环境变量
	
		export HADOOP_COMMON_LIB_NATIVE_DIR="~/hadoop/lib/"
		export HADOOP_OPTS="$HADOOP_OPTS -Djava.library.path=~/hadoop/lib/"

  遇到一个问题，openjdk好像没有tools.jar，所以需要安装sun的jdk，重新设置JAVA_HOME