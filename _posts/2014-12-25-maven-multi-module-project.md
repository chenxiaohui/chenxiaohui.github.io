---
layout: article
title: "Maven多模块"
key: maven-multi-module-project
date: 2014-12-25 20:24
comments: true
published: false
categories: "java"
---


	mvn exec:java -pl module2 -Dexec.mainClass=MyMain

	  	<build>
		<plugins>
			<plugin>
				<artifactId>maven-compiler-plugin</artifactId>
				<configuration>
					<source>1.7</source>
					<target>1.7</target>
				</configuration>
			</plugin>
		</plugins>
	</build>