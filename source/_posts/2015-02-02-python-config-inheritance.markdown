---
layout: post
title: "Python Configuration Inheritance"
date: 2015-02-02 11:54
comments: true
published: true
categories: "Python"
---

  While refactoring a project, I met with a situation that one configuration extends another configuration, like this:

	ConfigA = {"a":xx, "b":xx}
	ConfigB extends ConfigA + {"a":yy, c:"yy"}

  Code before refactor treats configA and configB separately. So after a few code iterations you will find configA has something same with configB. So I change it to this：

  	configA = {"a":xx, "b":xx}
  	configB = dict(configA.items() + {"a":yy, c:"yy"}}
  
  While this treats configA and configB evenly, meanwhile, it costs extra replication. A better way is like this:

  	configA = {"a":xx, "b":xx}
  	configB = dict(configA, **{"a":yy, c:"yy"}})

  The order of configA and configB's own elements is immutable, which means if configA and configB has a same element, use configB as result.
