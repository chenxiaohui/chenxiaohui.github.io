---
layout: article
title: "ps grep不显示grep自己本身的方法"
date: 2015-03-31 15:45
comments: true
published: true
categories: "Linux"
---

  主要两种方式：

1. 不grep自己。
		
	    -v, --invert-match
            Invert the sense of matching, to select non-matching lines.
        所以：
			ps xuf|grep python|grep -v grep

2. awk 略去最后一行。

		ps xuf|grep python|awk 'NR>1{print p}{p=$2}'

	解释下：第一行的时候，NR=1不打印，但是把pid存在p中，下一行打印，最后一行的时候，打印的是上一行的pid。

	awk博大精深...