# -*- coding: utf-8 -*-
'''
   Created on 25/05/2015
   @author: C&C - HardSoft
'''

def change(dic, obj):
    if isinstance(obj, list):
        for n, i in enumerate(obj):
            for k, v in dic.items():
                obj[n] = i.replace(k, v)
                i = obj[n]
    else:
        if isinstance(obj, (str, unicode)):
            for k, v in dic.items():
                obj = obj.replace(k, v)
    return obj

