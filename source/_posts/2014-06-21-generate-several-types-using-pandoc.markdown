---
layout: post
title: "直接从markdown生成各种电子书"
date: 2014-06-21 21:23
comments: true
categories: "Latex"
---


  有时候我们需要把编辑的markdown转成各种格式，这不失为一种写书的方式。借助pandoc这把瑞士军刀，我们可以实现一个脚本编译各种格式的功能，代码如下：

	#!/usr/bin/python
	#coding=utf-8
	#Filename:build.py
	import glob,os,sys,shutil

	cmd_template={'html':"pandoc %s -o output/html/%s.html --template=default.html",
	              'pdf':'pandoc -N --toc --template=default.latex --latex-engine=xelatex %s -o output/pdf/%s.pdf',
	              'beamer': 'pandoc -N -t beamer --toc --template=default.beamer --latex-engine=xelatex %s -o output/beamer/%s.pdf',
	              'epub': 'pandoc %s -o output/epub/%s.epub'
	             }

	if __name__ == '__main__':
	    if len(sys.argv) > 2:
	        print 'Usage: build.py [pdf|html|epub|beamer]'
	    else:
	        out_type = 'html' if len(sys.argv) == 1 else sys.argv[1]
	        assert(out_type in cmd_template)

	    os.system('cat *.md > swift_book.mkd')
	    cmd = [os.system(cmd_template[out_type] %(path, os.path.splitext(path)[0])) for path in glob.glob("*.md")]
	    cmd += [os.system(cmd_template[out_type] %('swift_book.mkd', 'swift_book'))]
	    print cmd

	    if out_type == 'html':
	        try:
	            shutil.rmtree('output/html/pic')
	        except Exception , e:
	            pass
	        shutil.copytree("pic",'output/html/pic')

<!--more-->


  为此你需要[安装一下pandoc][3]，需要pdf支持的话还需要[装一下texlive][4]，用法如下：

  	build.py [pdf|html|epub|beamer]

	需要如下的目录结构：
	
	    output  - beamer
	            - pdf
	            - epub
	            - html
	                - pic

   另外，脚本会拼一份合集在目录下，所以需要markdown文件有序，比如9.md会拼在10.md后面，所以需要9.md改名为09.md。

  一个使用的例子可以看[这里][1]。那些template都是模板文件，可以参考上面例子里的。


[1]: https://github.com/letsswift/The-Swift-Programming-Language-in-Chinese "The-Swift-Programming-Language-in-Chinese"
[2]:http://johnmacfarlane.net/pandoc/ "pandoc"
[3]:http://johnmacfarlane.net/pandoc/installing.html "pandoc"
[4]:https://www.tug.org/texlive/ "texlive"

###参考文献:

  \[1] The-Swift-Programming-Language-in-Chinese, <https://github.com/letsswift/The-Swift-Programming-Language-in-Chinese>

  \[2] pandoc, <http://johnmacfarlane.net/pandoc/>

  \[3] pandoc, <http://johnmacfarlane.net/pandoc/installing.html>

  \[4] texlive, <https://www.tug.org/texlive/>
