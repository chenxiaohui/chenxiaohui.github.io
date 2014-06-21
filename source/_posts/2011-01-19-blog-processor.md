---
title: 日志格式处理BlogProcessor
author: Harry Chen
layout: post

categories:
  - .Net
  - 与技术相关
---

  从之前的博客转文章的时候发现存在格式问题，之前格式贴到LiveWriter里总是一堆混乱。LiveWriter也是微软一大神器，格式莫名奇妙，如果直接拷贝一篇文章进去，那么段前的空格缩进都会消失，又没有什么好的缩进方式。不知道有没有牛人给解释一下？

  无奈做了一个格式处理的工具，先处理掉所有的空行，空格和tab，然后在每行前加四个空格的缩进。为了显得好看，每行之间再加一个空行，最后拷贝到剪贴板。也是没办法的办法，不知道各位有什么高招？

  程序很简单，在界面拖一个TextBox，一个Button，如下所示：

![][1]

  代码如下所示：


        using System;
        using System.Collections.Generic;
        using System.ComponentModel;
        using System.Data;
        using System.Drawing;
        using System.Text;
        using System.Windows.Forms;

        namespace BlogProcessor
        {
            public partial class BlogPorcess : Form
            {
                public BlogPorcess()
                {
                    InitializeComponent();
                }

                private void btnProcess_Click(object sender, EventArgs e)
                {
                    string str = txtInput.Text;
                    str = "    "   str.Replace(" ", "").Replace("	", "");
                    while (str.IndexOf(" ") != -1)
                        str=str.Replace(" ", " ");
                    int idx = str.IndexOf(" ");
                    while (idx != -1)
                    {
                        str = str.Substring(0, idx   2)   "    "
                            str.Substring(idx   2);
                        idx = str.IndexOf(" ", idx   2);
                    }
                    str=str.Replace(" ", " ");
                    txtInput.Text = str;
                    Clipboard.SetDataObject(str);
                }
            }
        }

  程序文件就不放了，没啥含量，而且也没有完美的解决问题，期待牛人。

   [1]: http://www.roybit.com/wp-content/uploads/2011/01/sds_thumb1.jpg
