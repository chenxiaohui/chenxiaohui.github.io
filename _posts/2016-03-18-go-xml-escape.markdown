---
layout: article
title: "go生成xml的时候特殊字符转义的问题"
date: 2016-03-18 17:43
comments: true
published: true
categories: "其他"
---


  最近在做http返回的时候发现go的xml生成（marshal）会把引号转义，如下：

		<?xml version="1.0" encoding="UTF-8"?>

		<Part>
		  <PartNumber>1</PartNumber>
		  <LastModified>2016-03-18T08:24:25.000Z</LastModified>
		  <ETag>&#34;0c78aef83f66abc1fa1e8477f296d394&#34;</ETag>
		  <Size>12121</Size>
		</Part>  	

  看了下源码，marshal函数的实现就会默认转义。这样就只能加一个Type，不直接用string，然后定义这个Type的marshl函数。上网搜了一下发现可以找个方法绕过去：struct的修饰可以指明当前的struct field不做转义，直接输出。


		type Part struct {
		     XMLName      xml.Name `xml:"Part"`
		     PartNumber   int
		     LastModified string
		     ETag         string `xml:",innerxml"`
		     Size         int64
		}

  这样可以直接在序列化的时候传自己拼成的ETag值。比如：

	     Part{PartNumber: 1,
	         LastModified: S3TimeFormat(GetCurrentTime()),
	         ETag:         `<ETag>"acbd18db4cc2f85cedef654fccc4a4d8"</ETag>`,
	         Size:         12121}
   
  输出结果满足要求：

		<?xml version="1.0" encoding="UTF-8"?>

		<Part>
		  <PartNumber>1</PartNumber>
		  <LastModified>2016-03-18T08:32:39.000Z</LastModified><ETag>"acbd18db4cc2f85cedef654fccc4a4d8"</ETag>
		  <Size>12121</Size>
		</Part>
