#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import json
import re
import sys
import codecs
import shlex

LANGUAGE_RETURN = '\033[1;30;40m[r. 返回]\033[0m'
LANGUAGE_EXIT = '\033[1;30;40m[e. 退出]\033[0m'
LANGUAGE_ADD = '\033[1;30;40m[A. 添加]\033[0m'
LANGUAGE_REMOVE = '\033[1;30;40m[R. 删除]\033[0m'
LANGUAGE_ERROR = '注意 :'
LANGUAGE_INPUT = '命令 : '
LANGUAGE_INPUT_ERROR = '请输入正确的命令!'
LANGUAGE_INPUT_DICT_EXIST = '路径已存在 : '
LANGUAGE_INPUT_ADD_SUCCESS = '添加成功! 新路径 : '
LANGUAGE_INPUT_REMOVE_SUCCESS = '删除成功! 被删除索引 : '
LANGUAGE_INPUT_A_HELP = '添加节点命令正确格式 : A [目录名] [命令<省略即为创建目录>]'
LANGUAGE_INPUT_R_HELP = '删除结果正确格式 : R [索引]'

f = codecs.open(sys.argv[1],"r+","utf-8")
jsonStr = f.read()
root = json.loads(jsonStr)

stack = []
nav = []

def select(item, msg) :
    os.system('clear')
    if isinstance(item, dict):
        print LANGUAGE_EXIT,LANGUAGE_RETURN,LANGUAGE_ADD,LANGUAGE_REMOVE
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

        elif re.match(r'^[r]$',no) :
            pop()
            if len(stack) == 0 :
                sys.exit()
            else:
                select(stack[len(stack)-1],None)

        elif re.match(r'^[e]$',no) :
            sys.exit()

        elif re.match(r'^[A].*$',no) :
            cmd = shlex.split(no)
            print cmd
            if len(cmd) == 2 :
                ## 创建菜单
                tagName = cmd[1].decode(sys.getfilesystemencoding())
                if tagName in item:
                    select(item, LANGUAGE_INPUT_DICT_EXIST + cmd[1])
                else :
                    ## 添加成功
                    item[tagName] = {}
                    dump()
                    select(item, LANGUAGE_INPUT_ADD_SUCCESS + cmd[1])
            elif len(cmd) == 3 :
                tagName = cmd[1].decode(sys.getfilesystemencoding())
                tagValue = str(cmd[2])
                if tagName in item :
                    select(item, LANGUAGE_INPUT_DICT_EXIST + cmd[1])
                else :
                    item[tagName] = tagValue
                    dump()
                    select(item, LANGUAGE_INPUT_ADD_SUCCESS + cmd[1])
            else :
                select(item, LANGUAGE_INPUT_A_HELP)

        elif re.match(r'^[R].*$', no) :
            cmd = shlex.split(no)
            print cmd
            if len(cmd) == 2 and re.match(r'[0-9]+',cmd[1]) :
                index = int(cmd[1])-1
                if index<0 or index>=len(menuList) :
                    select(item,LANGUAGE_INPUT_ERROR)
                else :
                    del(item[menuList[index]])
                    dump()
                    select(item,LANGUAGE_INPUT_REMOVE_SUCCESS + cmd[1])
            else :
                select(item, LANGUAGE_INPUT_R_HELP)

        else :
            select(item,LANGUAGE_INPUT_ERROR)
    elif isinstance(item, unicode) or isinstance(item, str):
        if re.match(r'^\[.*\]$',item):
            print item
        else :
            os.system(item)
        pop()
        select(stack[len(stack)-1],None)

def dump() :
    f.seek(0)
    f.truncate()
    json.dump(root,f,ensure_ascii=False)

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
