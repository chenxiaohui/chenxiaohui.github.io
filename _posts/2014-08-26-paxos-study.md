---
layout: article
title: "Paxos算法学习"
key: paxos-study
date: 2014-08-26 20:53
comments: true
categories: "Oceanbase"
---
  
  本来想写点东西，后来觉得都是一知半解。这里转载一点学习资料吧。

  一个是知行学社的分布式系统与Paxos算法视频课程，循序渐进，讲解地比较浅显易懂。

  <embed src="http://www.tudou.com/v/e8zM8dAL6hM/&bid=05&rpid=51943457&resourceId=51943457_05_05_99/v.swf" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" wmode="opaque" width="480" height="400"></embed>

  另一个是百度刘杰[《分布式系统原理介绍》][1]。当然Lamport的几篇论文是不能不看的，虽然都不太好懂。
  
  - [The Part-Time Parliament][3] 
  - [Paxos Made Simple][2]
  - [The Byzantine Generals Problem][4]

  相比较而言，[paxos的wiki][5]可能更好懂一些。有余力的同学可以做一下[MIT Distributed Systems Labs][6]。


[1]: http://www.valleytalk.org/2012/07/12/%E3%80%8A%E5%88%86%E5%B8%83%E5%BC%8F%E7%B3%BB%E7%BB%9F%E5%8E%9F%E7%90%86%E4%BB%8B%E7%BB%8D%E3%80%8B-%E3%80%82%E7%99%BE%E5%BA%A6-%E3%80%82%E5%88%98%E6%9D%B0/ "《分布式系统原理介绍》"
[2]: http://research.microsoft.com/en-us/um/people/lamport/pubs/paxos-simple.pdf "paxos made simple"
[3]: http://research.microsoft.com/en-us/um/people/lamport/pubs/lamport-paxos.pdf "The Part-Time Parliament"
[4]: https://www.andrew.cmu.edu/course/15-749/READINGS/required/resilience/lamport82.pdf "The Byzantine Generals Problem"
[5]: http://en.wikipedia.org/wiki/Paxos_(computer_science) "Paxos (computer science)"
[6]: http://css.csail.mit.edu/6.824/2014/ "MIT Distributed Systems Labs"