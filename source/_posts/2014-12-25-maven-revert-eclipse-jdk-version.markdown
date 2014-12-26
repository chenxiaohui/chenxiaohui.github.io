---
layout: post
title: "关于Maven回滚了eclipse中项目的JRE版本"
date: 2014-12-25 14:49
comments: true
published: true
categories: "其他"
---

  发现在命令行对一个项目执行`mvn install`的时候，回eclipse看就会有些错误，原因如[这里][1]所说，JRE版本和compliance level被回滚到1.5了。查看配置发现，eclipse导入配置并没有设置这里。如下：

	<?xml version="1.0" encoding="UTF-8"?>
	<projectDescription>
		<name>realtime_ua</name>
		<comment></comment>
		<projects>
		</projects>
		<buildSpec>
			<buildCommand>
				<name>org.eclipse.m2e.core.maven2Builder</name>
				<arguments>
				</arguments>
			</buildCommand>
		</buildSpec>
		<natures>
			<nature>org.eclipse.m2e.core.maven2Nature</nature>
		</natures>
	</projectDescription>

  实际导入的JRE版本是m2eclipse插件决定的。参考[这里][2]加入对maven-compiler-plugin的默认配置即可：

	<build>
	    <plugins>
	        <plugin>
	          <artifactId>maven-compiler-plugin</artifactId>
	            <configuration>
	              <source>1.6</source>
	              <target>1.6</target>
	            </configuration>
	        </plugin>
	  </plugins>
	</build>

  多module项目请把配置直接加在root-project的pom.xml下。

<!--more-->

[1]: http://cxh.me/2014/12/08/eclipse-java-override-warning/   "关于eclipse里面override上的warning"
[2]: http://stackoverflow.com/questions/3539139/what-causes-a-new-maven-project-in-eclipse-to-use-java-1-5-instead-of-java-1-6-b "What causes a new Maven project in Eclipse to use Java 1.5 instead of Java 1.6 by default and how can I ensure it doesn't?"
[3]: http://howtodoinjava.com/2013/06/04/solved-java-compiler-level-does-not-match-the-version-of-the-installed-java-project-facet/ "Solved: Java compiler level does not match the version of the installed Java project facet"
###参考文献:

>\[1] 关于eclipse里面override上的warning, <http://cxh.me/2014/12/08/eclipse-java-override-warning/>

>\[2] What causes a new Maven project in Eclipse to use Java 1.5 instead of Java 1.6 by default and how can I ensure it doesn't?, <http://stackoverflow.com/questions/3539139/what-causes-a-new-maven-project-in-eclipse-to-use-java-1-5-instead-of-java-1-6-b>

>\[3] Solved: Java compiler level does not match the version of the installed Java project facet, <http://howtodoinjava.com/2013/06/04/solved-java-compiler-level-does-not-match-the-version-of-the-installed-java-project-facet/>
