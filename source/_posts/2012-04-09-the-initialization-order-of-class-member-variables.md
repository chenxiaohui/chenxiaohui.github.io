---
title: 关于类成员变量初始化顺序
author: Harry Chen
layout: post
----

  java和C#语言里类变量初始化的顺序是

>1. 类成员变量初始化先于类的构造函数

>2. 静态成员变量先于实例变量

>3. 父类成员变量先于子类成员变量 C#相反

>4. 父类构造函数先于子类构造函数

<!--more-->

  举一个java的例子:

    :::java
    class Base
    {
        public static Test a=new Test("a");
        public static Test b;
        public Test c=new Test("c");
        public Test d;
        static
        {
            b=new Test("b");
        }
        public Base()
        {
            d=new Test("d");
        }
        public static void main(String[] args) {
            new Derived();
        }
    }
    class Derived extends Base
    {
        public static Test da=new Test("da");
        public static Test db;
        public Test dc=new Test("dc");
        public Test dd;
        static
        {
            db=new Test("db");
        }
        public Derived()
        {
            dd=new Test("dd");
        }
    }

    class Test
    {
        public Test (String name) {
            System.out.println(name);
        }
    }

  运行结果是：

    a
    b
    da
    db
    c
    d
    dc
    dd

  C++中没有成员变量定义时初始化的方式，所以有如下几条：

1. 构造函数初始化列表的变量优先于构造函数（至少明显的写在前面）

2. 静态成员变量先于实例变量

3. 父类成员变量先于子类成员变量

4. 父类构造函数先于子类构造函数

  举一个例子：

    :::cpp
    #include <iostream>
    #include <string>
    using namespace std;
    class Test
    {
    public:
        Test(string n)
        {
            cout<<n<<endl;
        }
    };
    class Base
    {
    public:
        static Test* a;
        Test* b;
        Test* c;
        Base():b(new Test("b"))
        {
            c=new Test("c");
        }
        virtual ~Base()
        {
            if(a) delete a;//似乎是很欠妥的做法
            if(b) delete b;
            if(c) delete c;
        }
    };
    Test* Base::a=new Test("a");
    class Derived:Base
    {
    public:
        static Test* da;
        Test* db;
        Test* dc;
        Derived():db(new Test("db"))
        {
            dc=new Test("dc");
        }
        ~Derived()
        {
            if(da) delete da;//似乎是很欠妥的做法
            if(db) delete db;
            if(dc) delete dc;
        }
    };
    Test* Derived::da=new Test("da");

    void main()
    {
        Derived d;
    }

  结果是：

    a
    da
    b
    c
    db
    dc

  另外需要注意一点：析构函数是先子类再父类的，而且虚析构函数也是面试笔试经常考的问题。
