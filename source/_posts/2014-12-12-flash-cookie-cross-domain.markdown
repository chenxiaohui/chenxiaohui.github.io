---
layout: post
title: "Flash Cookie的跨域读取"
date: 2014-12-12 12:35
comments: true
publised: true
categories: "Flex"
---

  关于Flash Cookie相关的问题见[参考文献1][1]。这里主要说如何实现跨域的Flash Cookie读取。

  首先，我们要实现Js调用Flash插件。比较简单的实现是用[swfobject][2]。简单的示例代码如下：

	<object id="myCom" name="myCom" classid="clsid:D27CDB6E-AE6D-11cf-96B8-444553540000" width="0" height="0">
	    <param name="movie" value="http://xxx/xxx.swf" />
	    <param name="allowScriptAccess" value="always" />
	    <!--[if !IE]>-->
	    <object name="myCom" type="application/x-shockwave-flash" data="http://xxx/xxx.swf" width="0" height="0">
	    <!--<![endif]-->
	        <div>
	            <h1>SWF Cannot be loaded!</h1>
	        </div>
	    <!--[if !IE]>-->
	    </object>
	    <!--<![endif]-->
	</object>

<!--more-->

  js部分代码如下：

	    function callbackfn() {
			var obj = swfobject.getObjectById("myCom");
			if (obj && typeof obj.getXXX != "undefined") {
				alert(obj.getXXX('xxx'));
			}
		};
		swfobject.registerObject("myCom", "9.0.0", "expressInstall.swf");

  具体含义参见如下swfobject的document：

  * classid (outer object element only, value is always clsid:D27CDB6E-AE6D-11cf-96B8-444553540000)
  * type (inner object element only, value is always application/x-shockwave-flash)
  * data (inner object element only, defines the URL of a SWF)
  * width (both object elements, defines the width of a SWF)
  * height (both object elements, defines the height of a SWF)
  
  跨域的问题上，需要注意如下几个：

  1. 调用object的组件的跨域声明是必须的。

		<param name="allowScriptAccess" value="always" />

  2. swf_url使用被访问域的swf链接。
  3. 被访问的域根目录需要开放访问。crossdomain.xml需要开放跨域限制。当然像如下这种粗放的是不好的。（虽然很方便）

		<cross-domain-policy>
			<allow-access-from domain="*" />
		</cross-domain-policy>

  4. swf源码需要开放权限：

		System.security.allowDomain("yourhtmldomain.com");
  
  OK.

[1]: http://cxh.me/2014/11/25/flash-shared-cookie/   "跨浏览器cookie"
[2]: https://code.google.com/p/swfobject/ "swfobject"
[3]: http://stackoverflow.com/questions/1038668/cross-domain-externalinterface-error-calling-method-on-npobject "Cross Domain ExternalInterface “Error calling method on NPObject”"