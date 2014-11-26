---
layout: post
title: "跨浏览器cookie"
date: 2014-11-25 16:57
comments: true
categories: "web相关"
---

  有时候为了标识一个用户，我们需要跨浏览器的cookie，这样用户在一个浏览器的行为可以被另一个浏览器读取。当然这种行为也备受争议，对于保护用户隐私来讲，这简直是后门。所以cookie里面一定不要存任何重要数据。

  不过这么做也不完全是为了用户数据跟踪。从用户体验的角度看，可以这么实现跨浏览器甚至跨域的session。具体实现上有如下几种方法：

  1. Local Shared Objects (Flash Cookies)

  2. Silverlight Isolated Storage

  3. 使用HTML5客户端储存数据方法。

  4. evercookie
  
  关于第二种有一个解释：一般装了silverlight的人都装了flash，想想真是呵呵了。第三种参见[参考文献][4]。

  [evercookie][5]原则上讲不能算一种方法，而是一种实现。每次写入的时候都会把cookie写到多个地方，下次读取的时候如果发现cookie有丢失，就通过还存在cookie副本来恢复cookie。乍一看原理跟3721那个进程交叉保护差不多，也算是流氓软件了。

  这里我们重点讲第一种。

<!--more-->

  flash cookie使用的是flash自己的本地存储，所以决定于flash实例。大部分浏览器使用的是系统的flash实例，所以flash cookie能跨浏览器存在。但是有几个例外。

  目前实测IE/Maxthon/Firefox/Safari/360浏览器都是采用系统的Flash实例，所以能够共享flash cookie，目前测到的几个特例是chrome/搜狗/百度浏览器，分别采用了自己浏览器内部打包的flash实例。另外不同系统用户的cookie不共享。从下面一张图可以清晰看出：

  {% img img-polaroid center /images/2014/flash_cookie.png %}  

  flash cookie的写入可以参考如下项目``，作者在[主页][1]详细说明了使用方法。需要注意的是swf_url控制的写入路径会包含在cookie的namespace里面，也就是说会有如下的目录结构：

  {% img img-polaroid center /images/2014/tree.png %}

  另外关于跨域，作者说不同域的js需要使用同一个swf，猜测是js请求swf的时候浏览器不判断在哪个域。swf内部是有跨域安全机制的，如果关闭掉的话，是可以实现请求跨域的。但是js请求其他域的数据会被浏览器拒绝。

  测试如下：

  在两台机器上部署相同的Flash Cookie测试项目，其中61域和74域的js都请求74域的swf：

  {% img img-polaroid center /images/2014/cross.png %}

  在74的机器上写入flash cookie: "74 write"

  {% img img-polaroid center /images/2014/74write.png %}

  在61的机器上load:

  {% img img-polaroid center /images/2014/61load.png %}

  证明可以跨域读取cookie。



[1]: http://nfriedly.com/techblog/2010/07/swf-for-javascript-cross-domain-flash-cookies/   "JavaScript library and .swf for cross-domain flash cookies"
[2]: https://github.com/nfriedly/Javascript-Flash-Cookies "Javascript-Flash-Cookies"
[3]: http://nfriedly.com/techblog/2010/08/how-facebook-sets-and-uses-cross-domain-cookies/ " How Facebook Sets and uses cross-Domain cookies"
[4]: http://www.zhangxinxu.com/wordpress/2011/09/html5-localstorage%E6%9C%AC%E5%9C%B0%E5%AD%98%E5%82%A8%E5%AE%9E%E9%99%85%E5%BA%94%E7%94%A8%E4%B8%BE%E4%BE%8B/ "HTML5 localStorage本地存储实际应用举例"
[5]: https://github.com/samyk/evercookie "EverCookie"