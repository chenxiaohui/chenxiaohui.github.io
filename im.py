#!/usr/bin/env python
#coding=utf-8
#Filename:im.py
import os
import sys
import re

if __name__ == '__main__':
    if len(sys.argv) > 0:
        del sys.argv[0]
        pat = re.compile('{% img.*?(/\S*)')
        for doc in sys.argv:
            try:
                content = open(doc).read()
                filelist = ' '.join(pat.findall(content))
                os.system('python ~/repo/scripts/img.py ' + filelist)
            except Exception:
                raise
