---
layout: article
title: "关于Django下获取checkbox的返回值"
date: 2015-01-19 16:46
comments: true
published: true
categories: "Python"
---
  
  HTML中我们可以在form中这样写复选框：
  
	<form action="demo_form.asp">
	  <input type="checkbox" name="vehicle" value="Bike"> I have a bike<br>
	  <input type="checkbox" name="vehicle" value="Car" checked> I have a car<br>
	  <input type="submit" value="Submit">
	</form>

  但是作为服务端处理起来未免不变，尤其是checkbox list是自动生成的时候。此时可以用group方式把form value组合起来。如下：

    {\% for item in items \%}
		<td><input type="checkbox" name="selected_push[]" value="{{item.id}}"></td>
    {\% endfor \%}

  服务端从命令行可以看到收到的post里面是有'selected_push[]'变量的。但是直接get的结果只有一个。查阅stackoverflow发现RequestContext有单独的getlist函数来处理。果然还是跟PHP不一样啊。