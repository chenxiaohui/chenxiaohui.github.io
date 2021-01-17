---
layout: article
title: "c/c++ 文件/流读取函数总结"
key: c-cpp-file-stream-operation-function
date: 2014-06-16 20:00
comments: true
categories: "C++"
---


### 针对文本文件的，  c++主要有如下几种吧

1. getline： 实现上，输入istream流，需要支持特定traits的迭代器。从流里面每次一行读入string，遇到delim结束。

		  template<typename _CharT, typename _Traits, typename _Alloc>
		    basic_istream<_CharT,_Traits>&
		    getline(basic_istream<_CharT, _Traits>& __is,
			    basic_string<_CharT, _Traits, _Alloc>& __str, _CharT __delim);

		  template<typename _CharT, typename _Traits, typename _Alloc>
		    inline basic_istream<_CharT,_Traits>&
		    getline(basic_istream<_CharT, _Traits>& __is,
			    basic_string<_CharT, _Traits, _Alloc>& __str);

<!--more-->

2. stream.get/put：分为如下几种类型。
	
	1. 不接收参数的直接返回结果
	2. 接收一个char类型的参数
	3. 接收一个缓冲区和缓冲区大小，读取结果直到遇到delim，默认回车符
	4. put直接输入一个字符
	5. get 系的函数都不会ignore delim分隔符的，读到行尾需要手动ignore回车

		      int_type 
		      get(void);

		      __istream_type& 
		      get(char_type& __c);

		      __istream_type& 
		      get(char_type* __s, streamsize __n, char_type __delim);

		      inline __istream_type& 
		      get(char_type* __s, streamsize __n)

		      __istream_type&
		      get(__streambuf_type& __sb, char_type __delim);

		      inline __istream_type&
		      get(__streambuf_type& __sb)

		      // Unformatted output:
		      __ostream_type& 
		      put(char_type __c);

3. stream.getline()：接收一个缓冲区和缓冲区大小，读取结果直到遇到delim，默认回车符

	      __istream_type& 
	      getline(char_type* __s, streamsize __n, char_type __delim);

	      inline __istream_type& 
	      getline(char_type* __s, streamsize __n)

4. stream.read/stream.write()： 二进制操作，读写一段数据。

	      __istream_type& 
	      read(char_type* __s, streamsize __n);

	      streamsize 
	      readsome(char_type* __s, streamsize __n);

	      __ostream_type& 
	      write(const char_type* __s, streamsize __n);

4. 输入输出运算

	
### c大概有如下几个：
 
  1. fgetc/fputc
  2. fgets/fputs
  2. fscanf/fprintf
  3. fread/fwrite

		__STDIO_INLINE _IO_ssize_t
		getline (char **__lineptr, size_t *__n, FILE *__stream)

  另外，stdio.h里也有getline的实现，传入一个FILE指针。需要注意的是传入的char **指针是会被申请内存并赋值的。所以需要自己释放。
 
  这里就不详述了，详见：
  <http://zhaoyuqiang.blog.51cto.com/6328846/1296902>