#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import re
import sys
import codecs

LANGUAGE_RETURN = '[R. Return]'
LANGUAGE_EXIT = '[E. Exit]'
LANGUAGE_ERROR = 'ERROR :'
LANGUAGE_INPUT = 'Input : '
LANGUAGE_INPUT_ERROR = 'Input Error!'

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
        # 这里绝对不会为空
        select(stack[len(stack)-1],None)

def push(name, value) :
    stack.append(value)
    nav.append(name+'/')

def pop() :
    stack.pop()
    nav.pop()

def printNav() :
    for m in nav :
        sys.stdout.write(m)
    print ''

stack.append(root)
nav.append('/')
select(root, None)
