# -*- coding: utf-8 -*-

"""
   Created on 27/04/2015
   @author: C&C - HardSoft
"""

from util.HOFs import *


def calc_length(copy):
    if isinstance(copy, list):
        book = copy
    else:
        if isinstance(copy, str):
            book = copy.splitlines()
        else:
            book = []

    clearlines = map(l672, filter(all3(isNotRem, isNotBlank, isNotEjectOrSkip), book))

    havecopy = filter(isCopy, clearlines)
    if havecopy:
        bkm = ''.join(havecopy[0].split('COPY')[1].replace('.', '').split())
        msg = 'COPY {} deve ser expandido.'.format(bkm)
        return {'retorno': False, 'msg': msg, 'lrecl': 0}

    lines = []
    holder = []
    for l in clearlines:
        holder.append(l if not holder else l.strip())
        if l.endswith('.'):
            lines.append(" ".join(holder))
            holder = []

    lrecl = 0
    redefines = False
    occurs = False
    locc = 0
    lvlred = 0
    lvlocc = 0

    for line in lines:
        line = line[:-1]

        wrd, wrds = words(line)

        if not wrds[0].isdigit():
            continue

        level = int(wrds[0])

        if redefines:
            if level > lvlred:
                continue
        redefines = False
        lvlred = 0

        if 'REDEFINES' in wrds:
            lvlred = level
            redefines = True
            continue

        if occurs:
            if level > lvlocc:
                if 'PIC' in wrds:
                    locc += lenfield(wrds[wrds.index('PIC') + 1:])
                continue
            lrecl += locc * occurs
        occurs = False
        lvlocc = 0

        if 'OCCURS' in wrds:
            lvlocc = level
            occurs = (int(nextWord('OCCURS', line)) if 'TO' not in wrds else
                      int(nextWord('TO', line)))

        if 'PIC' in wrds:
            if occurs:
                locc += lenfield(wrds[wrds.index('PIC') + 1:])
            else:
                lrecl += lenfield(wrds[wrds.index('PIC') + 1:])

    return {'retorno': True, 'msg': None, 'lrecl': lrecl}


def lenfield(attrs):
    pic = attrs[0]
    if pic[0] == 'S':
        pic = pic[1:]
    pap = pic.find('(')
    decimais = 0
    if pap == -1:
        if 'V' in pic:
            inteiros = pic.index('V')
            decimais = len(pic) - (inteiros + 1)
        else:
            inteiros = len(pic)
    else:
        if 'V' in pic:
            inttmp = pic[:pic.index('V')]
            dectmp = pic[pic.index('V') + 1:]
            if '(' in inttmp:
                inteiros = int(inttmp[inttmp.index('(') + 1:inttmp.index(')')])
            else:
                inteiros = len(inttmp)
            if '(' in dectmp:
                decimais = int(dectmp[dectmp.index('(') + 1:dectmp.index(')')])
            else:
                decimais = len(dectmp)
        else:
            inteiros = int(pic[pap + 1:pic.index(')')])

    lentmp = inteiros + decimais

    if 'COMP-3' in attrs or 'COMPUTATIONAL-3' in attrs:
        lrecl = lentmp / 2 + 1
    elif 'COMP' in attrs or 'COMPUTATIONAL' in attrs or 'BINARY' in attrs:
        lrecl = lentmp / 2
    elif 'SIGN' in attrs:
        lrecl = lentmp + 1
    else:
        lrecl = lentmp

    return lrecl

