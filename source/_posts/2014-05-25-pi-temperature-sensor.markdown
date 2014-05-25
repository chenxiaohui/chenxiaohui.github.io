---
layout: post
title: "用树莓派和DS18B20监控温度变化"
date: 2014-05-25 14:16
comments: true
categories: "其他"
---

  基本的教程在这里: 

  1. [引脚定义][1]

  2. [传感器教程1][2]

  3. [传感器教程2][3]

  鉴于我的硬件水平只限于插板子焊板子和对针脚，其他的都还给数电模电老师了，我还是老老实实买了模块，省的自己焊电阻。
芯片，模块都是淘宝买的，随便搜一家就行，几块钱的东西一般不会有假的。

<!--more-->

  整个过程可以按照教程1，2 对应针脚完成，如果顺利基本一次成功。别人的知识产权我就不好摘录了。但是代码我优化了一下，硬件工程师的代码果然是写的异常粗犷。修改后的代码如下：

	#!/usr/bin/python
	#coding=utf-8
	#Filename:temperature.py
	import os,datetime,time

	def calc_temperature(filename):
	    res = 0
	    valid_count = 0
	    for i in range(0,5):
	        with open(filename) as tfile:
	            text = tfile.read()
	        lines = text.split("\n")
	        firstline, secondline = lines[0], lines[1]
	        crc = firstline.split(" ")[11]
	        if crc == 'YES':
	            temperaturedata = secondline.split(" ")[9]
	            temperature = float(temperaturedata[2:])
	            temperature = temperature / 1000
	            valid_count += 1
	            res += temperature
	            print temperature
	        else:
	            with open(os.path.expanduser("~/sys.log"), "a") as err:
	                err.write("CRC Error: %s\n%s\n" % (datetime.datetime.now().strftime("%Y/%M/%d-%H:%M:%S"), text))
	        time.sleep(0.2)
	    return res/valid_count if valid_count > 0 else -1

	#temperature = calc_temperature("input.txt")
	temperature = calc_temperature("/sys/bus/w1/devices/28-000005e31fe6/w1_slave")
	if temperature > 0:
	    res = '{"value":%f}' %temperature
	    with open(os.path.expanduser('~/datafile.txt'), 'w') as output:
	        output.write(res)

  上传的脚本依然可以用教程里面的。Yeelink居然是一家青岛的公司，感慨省里总算有点互联网的公司了，当然网站做的是挺粗糙的。Yeelink的android手机端一直提示我登录密码出错。重置了也不行。后来发现登陆的时候不是邮箱...那你网站干嘛又能用邮箱登陆我擦....

  温度曲线的图片如下： 
  
  {% img img-polaroid center /images/2014-5/before.png "温度曲线" "温度曲线" %}

  开始的程序没有考虑求平均，不知道会不会有临时跳变的瞬间值。后来加了平均值之后发现多次取的结果是不一样，但是不清楚这个芯片采集的周期是多少。多次平均的结果如下所示：

  {% img img-polaroid center /images/2014-5/data.png "多次平均的结果" "多次平均的结果" %}

  ps: 公司周末真热....

[1]: http://wemaker.cc/60   "树莓派GPIO引脚详解"
[2]: http://s.mile77.com/?p=2039  "树莓派+多个DS18B20+Yeelink，全天候监测多个点的温度“
[3]: http://blog.sina.com.cn/s/blog_3cb6a78c0101a46w.html  "Raspberry Pi 使用DS18B20温度传感器"


###参考文献:

>\[1] 树莓派GPIO引脚详解, <http://wemaker.cc/60>

>\[2] 树莓派+多个DS18B20+Yeelink，全天候监测多个点的温度“, <http://s.mile77.com/?p=2039>

>\[3] Raspberry Pi 使用DS18B20温度传感器, <http://blog.sina.com.cn/s/blog_3cb6a78c0101a46w.html>