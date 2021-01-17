---
layout: article
title: "Python编码"
date: 2015-01-19 14:34
comments: true
published: true
categories: "python"
---
  众所周知Python的内码编码是Unicode，所有输入的编码都需要转换成unicode然后转出成为其他编码。Python2中存在unicode对象和str对象两种，在中文处理的时候很容易出问题，而Python3直接全部统一了编码到unicode。

  举一个例子说明编码的转换，首先我们的环境是utf-8

	LANG=zh_CN.UTF-8
	LANGUAGE=zh_CN:zh
	LC_CTYPE="zh_CN.UTF-8"
	LC_NUMERIC="zh_CN.UTF-8"
	LC_TIME="zh_CN.UTF-8"
	LC_COLLATE="zh_CN.UTF-8"
	LC_MONETARY="zh_CN.UTF-8"
	LC_MESSAGES="zh_CN.UTF-8"
	LC_PAPER="zh_CN.UTF-8"
	LC_NAME="zh_CN.UTF-8"
	LC_ADDRESS="zh_CN.UTF-8"
	LC_TELEPHONE="zh_CN.UTF-8"
	LC_MEASUREMENT="zh_CN.UTF-8"
	LC_IDENTIFICATION="zh_CN.UTF-8"
	LC_ALL=zh_CN.UTF-8
  
  然后测试一个从环境的输入和写回到环境。

    文件编码gbk:
    print '中文'
    print u'中文'
    输出
    	����
		中文

    文件编码utf-8
    print '中文'
    print u'中文'

    输出
    	中文
    	中文

  说明print输出的时候按照default encoding进行了编码。所以只有gbk的编码乱码了。同样对输入的判断，环境如果是utf8，输出不变的话，不会有乱码。但是如果从文件里读取了字符串或者代码里有硬编码字符，就需要考虑编码了。另外，unicode和str相加会有编码问题。比如：

 	文件编码gbk: 	
  	value = raw_input()
	print value + "中文"
	输入
		中文
	输出
		中文����
	
	value = raw_input()
	print value + u"中文"
	输入
		en
	输出
		en中文
	输入
		中文
	输出
		UnicodeDecodeError: 'ascii' codec can't decode byte 0xe4 in position 0: ordinal not in range(128)


  str+str输出肯定是str，所以需要适配环境的编码，第一个乱码可以理解。而str+unicode的时候，str会被按default encoding解码。utf8无法按照python default encoding ascii解码。utf8文件编码下的情况类似。
    