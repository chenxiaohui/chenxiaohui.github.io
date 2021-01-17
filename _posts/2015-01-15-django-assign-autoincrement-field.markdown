---
layout: article
title: "处理Django的自增字段"
date: 2015-01-15 22:00
comments: true
published: true
categories: "Python"
---
  有时候需要手动构造一个Django model对象并保存，遇到如下的情况：

  	model定义如下：
  	class AuthHistory(models.Model):
    user_name = models.CharField(max_length=100, default=None)
    item_id = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    url = models.CharField(max_length=1000)
    title = models.CharField(max_length=1000)
    operation = models.CharField(max_length=100, default=None)

    构造对象如下：
    history = AuthHistory("cxh", tid, datetime.datetime.now(), item['url'], item['title'], operation)

  报错:`django title invalid literal for int() with base 10:cxh`，明显是把第一个字段赋给自增长id了，因为Django会给没有主键的表直接加上id字段作为主键。

  手动指定域当然是可以的：

  	history = AuthHistory( user_name="cxh", item_id=tid, datetime=datetime.datetime.now(), url=item['url'], title=item['title'], operation=operation)

  但是未免很麻烦。传值肯定不合理，毕竟id是数据库记录的。试了一下，给id域直接传NULL就行了。

  	history = AuthHistory(None, "cxh", tid, datetime.datetime.now(), item['url'], item['title'], operation)
