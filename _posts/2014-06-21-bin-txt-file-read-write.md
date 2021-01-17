---
layout: article
title: "文本文件和二进制文件读写"
key: bin-txt-file-read-write
date: 2014-06-21 12:28
comments: true
categories: "C++"
---

  探究这个的起因是我在序列化一个数据结构，用二进制写到文件之后用vim打开发现后面居然多了一个值。

![](/assets/images/2014/binfile.png "用vim显示二进制文件" "用vim显示二进制文件")

  所以总结一下文件的两种不同写入方式。(当然上面是vim里面xxd显示的问题)

  我们用如下代码测试:	

	int main(int argc, const char *argv[])
	{
	  FILE * fp  = fopen("output.txt", "w");
	  fputc(10, fp);
	  fputc(13, fp);
	  fputc('\n', fp);
	  fclose(fp);

	  fp  = fopen("output.bin", "wb");
	  int32_t length[] ={0x0a, 0x12345678};
	  fwrite(&length, sizeof(int32_t), 2, fp);
	  fclose(fp);
	  return 0;
	}
	
<!--more-->

**windows下**

文本文件写入：
	
	0000000: 0d0a 0d0d 0a                             .....

二进制写入

	0000000: 0a00 0000 7856 3412                      ....xV4.

**linux下：**

  文本方式写入

	0000000: 0a0d 0a                                  ...

  二进制写入：

	0000000: 0a00 0000 7856 3412                      ....xV4.

**mac下**

  文本方式写入：

	0000000: 0a0d 0a                                  ...

  二进制写入

	0000000: 0a00 0000 7856 3412                      ....xV4.

  解释几个问题：

### 回车符的转义

  windows下写文本文件的时候换行符会被替换成回车换行(0d0a), 直接写0a(10)也是一样的. Linux和mac下不会,二进制文件不care这些.

### 文件结尾判断

  详见这里：<http://blog.csdn.net/bingqing07/article/details/5785080>

### UTF-8 BOＭ

  转载：

> UTF-8 不需要 BOM，尽管 Unicode 标准允许在 UTF-8 中使用 BOM。
所以不含 BOM 的 UTF-8 才是标准形式，在 UTF-8 文件中放置 BOM 主要是微软的习惯（顺便提一下：把带有 BOM 的小端序 UTF-16 称作「Unicode」而又不详细说明，这也是微软的习惯）。
BOM（byte order mark）是为 UTF-16 和 UTF-32 准备的，用于标记字节序（byte order）。微软在 UTF-8 中使用 BOM 是因为这样可以把 UTF-8 和 ASCII 等编码明确区分开，但这样的文件在 Windows 之外的操作系统里会带来问题。
「UTF-8」和「带 BOM 的 UTF-8」的区别就是有没有 BOM。即文件开头有没有 U+FEFF。


