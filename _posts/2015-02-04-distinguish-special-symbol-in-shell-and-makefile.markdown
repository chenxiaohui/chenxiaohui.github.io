---
layout: article
title: "区分下shell和makefile中的特殊字符"
date: 2015-02-04 14:51
comments: true
published: true
categories: "Linux"
---
  主要是在Makefile中看到了这种字符($@)，不理解含义，查阅了一下，跟shell中意义不一样：

  	$@     -is the name of the target currently being processed.
	$<     -is the name of the first dependency.

  顺便提下shell下的

  	$#    Stores the number of command-line arguments that were passed to the shell program.
	$?    Stores the exit value of the last command that was executed.
	$0    Stores the first word of the entered command (the name of the shell program).
	$*    Stores all the arguments that were entered on thecommand line ($1 $2 ...).
	"$@"  Stores all the arguments that were entered on the command line, individually quoted ("$1" "$2" ...).