---
layout: article
title: "关于java编码规范"
date: 2015-01-08 14:34
comments: true
published: true
categories: "java"
---
  
  首先推荐[google的编码规范][1]，其次，关于class member ordering的问题，google的解释是：

  	The ordering of the members of a class can have a great effect on learnability, but there is no single correct recipe for how to do it. Different classes may order their members differently.

	What is important is that each class order its members in some logical order, which its maintainer could explain if asked. For example, new methods are not just habitually added to the end of the class, as that would yield "chronological by date added" ordering, which is not a logical ordering.

  道理是对的，但是不好执行啊。看了看JDK的顺序，觉得[这里][2]说的还是能达成共识的。

  >1. Class (static) variables: First the public class variables, then the protected, and then the private.
  > 2. Instance variables: First public, then protected, and then private.
  > 3. Constructors
  >4. Methods: These methods should be grouped by functionality rather than by scope or accessibility. For example, a private class method can be in between two public instance methods. The goal is to make reading and understanding the code easier.

[1]: https://google-styleguide.googlecode.com/svn/trunk/javaguide.html   "Google Java Style"
[2]: http://stackoverflow.com/questions/4668218/are-there-any-java-method-ordering-conventions "Are there any Java method ordering conventions?"
#### 参考文献:

  \[1] Google Java Style, <https://google-styleguide.googlecode.com/svn/trunk/javaguide.html>
  
  \[2] Are there any Java method ordering conventions?, <http://stackoverflow.com/questions/4668218/are-there-any-java-method-ordering-conventions>
