---
title: '由&#8221;喵&#8221;代码想到的'
author: Harry Chen
layout: post
permalink: /from-the-miao-code/
mkd_text:
  - |
    网上看到这样一段代码
    
    <a href="http://www.roybit.com/wp-content/uploads/2013/05/miao.jpg"><img title="miao.jpg" alt="miao.jpg" src="http://www.roybit.com/wp-content/uploads/2013/05/miao.jpg"class="aligncenter" /></a>
    
    还是挺无聊的，于是想到一个问题，宏替换的时候假如有多个匹配，应该匹配哪一个的问题，于是实验如下：
    
    <!--more-->
    
    	:::cpp
    	#include <stdio.h> 
    
    	#define aaa "3a"
    	#define a "1a"
    	#define aa "2a"
    
    	int main(int argc, const char *argv[])
    	{
    		printf("%s\n",aaa);
    	}
    
    这里最终输入结果是3a，也符合我们的思维方式，最长匹配嘛，值得一提的是这种情况
    
    	:::cpp
    	printf("%s\n",aa a);
    
    替换结果是"2a" "a"，通过空格间隔。C++ Primer中提到过这种书写方式，这也是字符串跨行的一种有效的写法，但是毕竟很少在实际情况中看到。
    另外一种字符串跨行的方式是：
    
    	:::cpp
    		char chstr2[] = "abcabc\
    	abcabc";
    
    这里需要注意，第二行前面不能有空格或者tab。
dsq_thread_id:
  - 1334900498
categories:
  - 随笔
tags:
  - 字符串多行
  - 宏替换
format: standard
---
# 

网上看到这样一段代码

![miao.jpg][1]

还是挺无聊的，于是想到一个问题，宏替换的时候假如有多个匹配，应该匹配哪一个的问题，于是实验如下：


    #include 

    #define aaa "3a"
    #define a "1a"
    #define aa "2a"

    int main(int argc, const char *argv[])
    {
        printf("%s
    ",aaa);
    }


这里最终输入结果是3a，也符合我们的思维方式，最长匹配嘛，值得一提的是这种情况


    printf("%s
    ",aa a);


替换结果是”2a” “a”，通过空格间隔。C Primer中提到过这种书写方式，这也是字符串跨行的一种有效的写法，但是毕竟很少在实际情况中看到。
另外一种字符串跨行的方式是：


        char chstr2[] = "abcabc\
    abcabc";


这里需要注意，第二行前面不能有空格或者tab。

   [1]: http://www.roybit.com/wp-content/uploads/2013/05/miao.jpg (miao.jpg)
