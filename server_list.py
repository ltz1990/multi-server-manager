#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import re
import sys
import codecs

LANGUAGE_RETURN = '\033[1;30;40m[R. 返回]\033[0m'
LANGUAGE_EXIT = '\033[1;30;40m[E. 退出]\033[0m'
LANGUAGE_ERROR = '错误 :'
LANGUAGE_INPUT = '请选择 : '
LANGUAGE_INPUT_ERROR = '请输入正确的选项!'

f = codecs.open(sys.argv[1],"r","utf-8")
jsonStr = f.read()
root = json.loads(jsonStr)

stack = []
nav = []

def select(item, msg) :
    os.system('clear')
    if isinstance(item, dict):
        print LANGUAGE_EXIT,LANGUAGE_RETURN
        printNav()
        menuList = [name for name in item]
        for i in range(len(menuList)) :
            print str(i+1)+'.', menuList[i]

        if msg :
            print LANGUAGE_ERROR,msg
        no = raw_input(LANGUAGE_INPUT)

        if re.match(r'^[0-9]+$',no) :
            print "loading..."
            index = int(no)-1
            if index<0 or index>=len(menuList) :
                select(item,LANGUAGE_INPUT_ERROR)
            else :
                selected = item[menuList[index]]
                push(menuList[index], selected)
                select(selected,'')

        elif re.match(r'^[rR]$',no) :
            pop()
            if len(stack) == 0 :
                sys.exit()
            else:
                select(stack[len(stack)-1],None)

        elif re.match(r'^[eE]$',no) :
            sys.exit()

        else :
            select(item,LANGUAGE_INPUT_ERROR)
    elif isinstance(item, unicode) or isinstance(item, str):
        if re.match(r'^\[.*\]$',item):
            print item
        else :
            os.system(item)
        pop()
        select(stack[len(stack)-1],None)

def push(name, value) :
    stack.append(value)
    nav.append(name+'/')

def pop() :
    stack.pop()
    nav.pop()

def printNav() :
    sys.stdout.write('\033[1;32;40m')
    for m in nav :
        sys.stdout.write(m)
    print '\033[0m'

stack.append(root)
nav.append('root/')
select(root, None)
