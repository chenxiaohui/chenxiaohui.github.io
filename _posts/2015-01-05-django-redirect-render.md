---
layout: article
title: "django重定向的参数传递"
key: django-redirect-render
date: 2015-01-05 15:55
comments: true
published: true
categories: "Python"
---
  
  其实就是想实现如下一个功能，重定向到一个网页，但是这个网页根据传参的不同显示不同的内容。基于Django各种render的shortcut理所当然的想有没有render_redirect，但是想想网络请求的流程，redirect只是返回了一个302，让浏览器直接去请求新的网页了，首先这个response很简单没有携带其他信息，此外，浏览器也不会把302code和url之外的内容作为下一次请求的参数。

  可行的办法还是用get参数。针对遇到的需求：传入不同的参数的时候在不同的div上显示class=active，我们可以简化的实现如下：

    模板：
      <div role="tabpanel" class="tab-pane {{A}}" id="a">
      <div role="tabpanel" class="tab-pane {{B}}" id="b">
      <div role="tabpanel" class="tab-pane {{C}}" id="c">
    后台：
   	  init = request.GET.get('init', 'a')#a是默认active的tab
      return render(request, 'xx.html', {init:'active'})
    跳转：
      return HttpResponseRedirect("/?init=b")

  直接用传入参数当了render参数的名字。`request.GET.get('init', 'a')`保证了无参数的时候active a作为默认值。django容错保证了没有的变量置空。基本够用了。


