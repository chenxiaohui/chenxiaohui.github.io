---
layout: article
title: "cgo实践"
key: cgo-practice
date: 2016-04-02 16:56
comments: true
published: true
categories: "其他"
---

  工作里遇到一个问题，想把mysql的crc直接封装一下让go来调用，因为查表的crc计算性能实在是不快，对我们这种文件系统的大报文计算来看，crc容易变成瓶颈。大概性能对比如下：

	两线程crc32查表 O2优化
	time_elapsed:471.474976s
	total_size_m : 200000.000000M
	crc rate : 424.200684m/s


	两线程crc64指令 O2优化
	time_elapsed:24.877853s
	total_size_m : 200000.000000M
	crc rate : 8039.278809m/s

  c这一端的计算比较容易，go的crc默认是查表， 所以存在不兼容的问题。出于兼容和性能考虑，用cgo封装一下。

  首先在c语言下把crc打包成lib库，考虑go的移植，直接用静态库比较好。go这边调用如下：

	package s3crc

	import "unsafe"

	// #include <stdlib.h>
	// #cgo CFLAGS: -I../../../../src/lib
	// #cgo LDFLAGS: -L../../../../src/lib -lcrc
	// #include "s3_crc64.h"
	import "C"

	func s3_crc64(buf string, len int64) uint64 {
	    cbuf := C.CString(buf)
	    defer C.free(unsafe.Pointer(cbuf))
	    return uint64(C.s3_crc64(unsafe.Pointer(cbuf), C.int64_t(len)))
	}

  遇到的坑主要有：

  1. cgo不支持ccache，所以这个比较扯。习惯使用ccache的同学（好样的）建议export CC=gcc
  2. 所有类型都需要做转换。go的类型对应到c的类型之后，都在C命名空间下。
  3. 静态库路径需要指明，go的buffer映射到c下面之后，需要考虑释放的问题。参见[文献][1]


[1]: https://golang.org/cmd/cgo/ "Command cgo"