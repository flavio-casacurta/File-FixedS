# -*- coding: utf-8 -*-

'''
   Created on 25/05/2015
   @author: C&C - HardSoft
'''

from HOFs import *
def Homogenize(book, cbl=False):
    inlin = '      ' if cbl else ''
    clearLines = map(l672, filter(all3(isNotRem, isNotBlank, isNotEjectOrSkip), book))
    joinLines = []
    holder = []
    for line in clearLines:
        holder.append(inlin + line if not holder else line.strip())
        if line.endswith('.'):
            joinLines.append(" ".join(holder))
            holder = []
    return joinLines
