---
title: 关于Python的类成员和Javascript的原型
author: Harry Chen
layout: post

categories:
  - 与技术相关
  - 基础理论
tags:
  - classmethod
  - javascript
  - prototype
  - Python
  - staticmethod
  - 原型
  - 阮一峰
---

  偶然发现两个的设计思路是一致的（个人理解，欢迎指正）。这里简要分析一下：

  Python的类成员，也就是直接定义在类里的变量（实例成员是用self.x直接声明的），而类方法就是用@classmethod说明的方法。

  > Python还有一种@staticmethod，静态方法，其实设立所有的静态方法和变量的目的主要是用类名限制访问范围，编译的时候就直接被改名然后变成了全局变量。

  Js的原型（prototype）是js里最复杂的一部分了，有的人可能Jquery什么的用的很熟，但是对原型一无所知。最初设计Js的时候设计师没有考虑把它设计成一门完整的语言，后来决定引入面向对象的时候，就采用了原型链这种诡异的设计模式。具体的使用大家应该都熟悉。类名（实际是函数名）.prototype.x=…，这样就在类的原型上加入了一方法或成员。

  > 实际Js也有静态方法和静态变量，就是通过类名.x=…定义的，跟一切静态方法一致，也只是限制了范围，最终会改名并变成全局变量。

  我们只讨论类成员类方法，静态的不在我们考虑范围之内，这种类即对象的设计理念，主流语言里貌似只有Js，Python和Perl采用了，跟静态方法是完全不同的理念。

  首先，我们要问为什么要引入类方法和类成员，它跟实例方法实际成员有什么不同呢?

  这里我们要建立一个概念，在Python和Js里，类也是一种对象（实例）（我的世界观颠覆了）。类其实相当于一个模板，只不过大多数语言里，我们通过类实例化出一个一个对象，抛去静态的，这些对象是各不相同的（先考虑成员对象，方法都是共享的）。而Python和Js里，这些对象共同引用类模板里的对象（及方法）。类模板好比一个公共的祖先，从这个祖先衍生的实例都有相同的血缘（共同的prototype），但是各自有自己不同的部分。

  不知道这么说是否清晰，我们举两个例子：

  Python的[1]:


    class Demo:
        i = 0
        def __init__(self):
            self.j = 0
    o1 = Demo()
    o2 = Demo()

    Demo.i = 10 #类成员的赋值
    print o1.i #结果为10,说明在没有显式定义实例成员的时候，就会取类成员的值
    print o2.i #结果为10,说明在没有显式定义实例成员的时候，就会取类成员的值

    o1.i = 1 #会为o1对象创建实例成员。
    o2.i = 2 #会为o2对象创建实例成员
    o1.j = 11
    o2.j = 12

    print o1.i # 结果为1
    print o2.i # 结果为2   这两个结果说明对i数据成员的赋值，每个对象都有自己的实例成员。
    print Demo.i #结果为10说明，前边的赋值，并没有覆盖该类成员。
    print o1.j # 结果为 11
    print o2.j # 结果为 12 正常的实例成员访问。

  结果很清晰，类成员大家共享，但是各自有各自不同的实例成员，类成员可以通过实例调用，这时候就存在了命名冲突了怎么办的问题，于是实例成员覆盖类成员，没有实例成员的时候才调用类成员，而通过类名调用类成员是最正统的方法了，毕竟Python里类也是对象，你把类名想象成一个直接被实例化了的原型对象，就好理解多了。

  然后举一个Js的例子[2]：


    var BaseClass = function() {
    this.method1 = function(){
           alert(' Defined by the "this" in the instance method');
     }
    };
    var instance1 = new BaseClass();
    instance1.method1 = function(){
        alert(' Defined directly in the instance method');
    }
    BaseClass.prototype.method1 = function(){
        alert(' Defined by the prototype instance method ');
    }
    instance1.method1();//Defined directly in the instance method

  > 通过运行结果跟踪测试可以看出直接定义在实例上的变量的优先级要高于定义在“this”上的，而定义在“this”上的又高于 prototype定义的变量。即直接定义在实例上的变量会覆盖定义在“this”上和prototype定义的变量，定义在“this”上的会覆盖prototype定义的变量。

  这与Python的例子思想一致。原型相当于类模板，实例共享原型，通过实例名调用一个方法时，如果出现命名混淆，实例的方法也会覆盖原型的方法。同样，实例同名成员的改动并不会影响原型成员，验证如下。而且原型最正统的调用方法也是通过类名，而不是实例名。


    function ec(str) {
    	document.write(str "");
    }
    var test= function(){
    }
    test.prototype.age = 11;
    var t=new test();
    var s=new test();

    ec(t.age);
    ec(s.age);

    t.age=12;
    s.age=13;

    ec(t.age);
    ec(s.age);
    ec(test.prototype.age);

  有了这种理解，阮一峰的三篇关于Js面向对象设计思想的文章也就不那么费解了。

  最后，吐个槽：Python真是纯面向对象啊，纯的……

> 参考文献：
>
> [1] python中类中的静态数据成员和实例数据成员
>
> 
>
> （注：实际上是类数据成员而不是静态）
>
> [2] javascript中静态方法、实例方法、内部方法和原型的一点见解
>
> 
>
> [3] 阮一峰，Javascript 面向对象编程（一）：封装
>
> 
>
> [4] 阮一峰，Javascript面向对象编程（二）：构造函数的继承
>
> 
>
> [5] 阮一峰，Javascript面向对象编程（三）：非构造函数的继承
>
> 
