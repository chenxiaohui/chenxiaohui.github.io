---
title: '关于C#序列化结果的长度获取'
author: Harry Chen
layout: post

dsq_thread_id:
  - 1380774281
categories:
  - .Net
  - 与技术相关
---

  关于C#序列化的文章真的是好多，但是内容大致一样，主要分四类：

  1. BinarySerialize
  2. SoapSerialize
  3. XmlSerialize
  4. JSON.Net和DataContractJsonSerializer

  最近的一个项目需要使用Socket进行通信，所以必然涉及序列化的问题。使用BinarySerialize序列化之后发现无论如何获取不了序列化后的实际长度，代码如下


    using System;
    using System.Collections.Generic;
    using System.Text;
    using System.IO;
    using System.Runtime.Serialization.Formatters.Binary;

    namespace Serialize
    {
        public class BinarySerialize
        {
            byte[] buffer=new byte[1024];

            public void Serialize(Book book)
            {
                using (MemoryStream fs = new MemoryStream(buffer, 0,1024))
                {
                    BinaryFormatter formatter = new BinaryFormatter();
                    formatter.Serialize(fs, book);
                }
            }

            public Book DeSerialize()
            {
                Book book;
                using (MemoryStream fs = new MemoryStream(buffer,0,1024))
                {
                    BinaryFormatter formatter = new BinaryFormatter();
                    book = (Book)formatter.Deserialize(fs);
                }
                return book;
            }
        }
    }

  通过MemoryStream获取长度，永远是1024。后来试了好久发现其实只需要改一点点地方就可以了，也就是建立MemoryStream的时候不指定缓冲区，让BinaryFormatter自己去建立缓冲区，同时通过Position获取当前的位置，把缓冲区重新调整。改正后的代码如下，顺便做了点通用性扩展：


    using System;
    using System.Collections.Generic;
    using System.Text;
    using System.IO;
    using System.Runtime.Serialization.Formatters.Binary;


    namespace Serialize
    {
        public class MemoryBinarySerialize
        {

            public static byte[] Serialize(object obj)
            {
                MemoryStream fs = new MemoryStream();
                BinaryFormatter formatter = new BinaryFormatter();
                formatter.Serialize(fs, obj);
                int length = (int)fs.Position;
                byte[] buffer = fs.GetBuffer();
                Array.Resize(ref buffer, length);
                return buffer;
            }

            public static object DeSerialize(byte[] data)
            {
                MemoryStream fs = new MemoryStream(data);
                BinaryFormatter formatter = new BinaryFormatter();
                object obj= formatter.Deserialize(fs);
                return obj;
            }
        }
    }

