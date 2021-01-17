---
title: Life is like a function
author: Harry Chen
key: life-is-like-a-function
layout: article

categories:
  - 挨踢人生
---


    void Life()
    {
         while (1)
        {
              Work();
              if(!bJobCompleted)
                 ExtraWork();
              Sleep();
         }
    }

  上班下班加班，每天往返，日子过得无比简单。这让我觉得能换种生活状态是最大的幸福。Life is like a box of chocolate, you never know what you are going to get。如此最好。


    Plus:my beloved VB Version
    Sub Life()
    While True
        Call Work
        If (bJobCompleted = False) Then
            Call ExtraWork
        End If
        Call Sleep
    Wend
    End Sub
