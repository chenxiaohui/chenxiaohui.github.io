---
title: 一个比较有意思的输入库
layout: article
key: readline_lib
date: 2021-03-07 14:59
published: true
comments: true
categories: "技术"
---

其实很多项目里面最后都依赖了readline，但是之前没注意过。readline主要提供了命令行输入的快捷键，历史查询什么的。一个例子：

```cpp
#include <stdio.h>
#include <readline/readline.h>
#include <readline/history.h>
#include <iostream>
/* A static variable for holding the line. */
static char *line_read = (char *)NULL;

/* Read a string, and return a pointer to it.  Returns NULL on EOF. */
char *
rl_gets ()
{
  /* If the buffer has already been allocated, return the memory
     to the free pool. */
  if (line_read)
    {
      free (line_read);
      line_read = (char *)NULL;
    }

  /* Get a line from the user. */
  line_read = readline ("");

  /* If the line has any text in it, save it on the history. */
  if (line_read && *line_read)
    add_history (line_read);

  return (line_read);
}
int main(int argc, const char *argv[]) {
  const char* out = rl_gets();
  printf("%s\n", out);
  return 0;
}
```

需要安装readline的依赖。

sudo apt-get install libreadline-dev

编译的时候加上-lreadline就行。