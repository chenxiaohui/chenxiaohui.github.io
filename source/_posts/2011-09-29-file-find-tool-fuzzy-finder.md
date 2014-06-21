---
title: '文件查找利器&mdash;&mdash;FuzzyFinder'
author: Harry Chen
layout: post

dsq_thread_id:
  - 1254513643
categories:
  - vim
  - 与技术相关
tags:
  - fuzzyfinder
  - 查找利器
---
# 

  这个东东太华丽了……相当VisualAssist的查找符号和查找文件，不过功能更强大，支持正则表达式，支持全文检索。




> 下载地址：
>
> 需要的支持库：
>
> L9Library 

  另外，由于命令较多，可以配置一下命令提示，如下所示：


    "fuzzyfinder
    "
    " F4和shift F4调用FuzzyFinder命令行菜单"
    "
    function! GetAllCommands()
      redir => commands
      silent command
      redir END
      return map((split(commands, "
    ")[3:]),
          \      '":" . matchstr(v:val, ''^....\zs\S*'')')
    endfunction

    " 自定义命令行
    let g:fuf_com_list=[':FufBuffer',':FufFile',':FufCoverageFile',':FufDir',
                \':FufMruFile',':FufMruCmd',':FufBookmarkFile',
                \':FufBookmarkDir',':FufTag',':FufBufferTag',
                \':FufTaggedFile',':FufJumpList',':FufChangeList',
                \':FufQuickfix',':FufLine',':FufHelp',
                \":FufFile \=expand('%:~:.')[:-1-len(expand('%:~:.:t'))]\",
                \":FufDir \=expand('%:p:~')[:-1-len(expand('%:p:~:t'))]\",
                \]
    nnoremap   :call fuf#givencmd#launch('', 0, '选择命令>', GetAllCommands())
    nnoremap   :call fuf#givencmd#launch('', 0, '选择命令>', g:fuf_com_list)
