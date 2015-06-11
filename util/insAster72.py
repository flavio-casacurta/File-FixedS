# -*- coding: utf-8 -*-

'''
   Created on 25/05/2015
   @author: C&C - HardSoft
'''

def insAster72(txt):
    ts=''
    tl=txt.split('\n')
    for l in tl:
         if l[6:7] == '*':
             if len(l) < 72:
                 l+=(' '*(71-len(l))+'*')
         ts+=l+'\n'
    return ts
