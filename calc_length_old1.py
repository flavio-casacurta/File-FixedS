# -*- coding: utf-8 -*-

"""
   Created on 27/04/2015
   @author: C&C - HardSoft
"""

from util.HOFs import *
from util.CobolPatterns import *
from util.homogenize import Homogenize

def calc_length(copy):
    if isinstance(copy, list):
        book = copy
    else:
        if isinstance(copy, str):
            book = copy.splitlines()
        else:
            book = []

    lines = Homogenize(book)

    havecopy = filter(isCopy, lines)
    if havecopy:
        bkm = ''.join(havecopy[0].split('COPY')[1].replace('.', '').split())
        msg = 'COPY {} deve ser expandido.'.format(bkm)
        return {'retorno': False, 'msg': msg, 'lrecl': 0}

    lrecl = 0
    redefines = False
    occurs = False
    locc = 0
    lvlred = 0
    lvlocc = 0

    for line in lines:
        match = CobolPatterns.row_pattern.match(line.strip())
        if not match:
            continue
        match = match.groupdict()

        if not match['level']:
            continue

        level = int(match['level'])

        if redefines:
            if level > lvlred:
                continue
        redefines = False
        lvlred = 0

        if match['redefines']:
            lvlred = level
            redefines = True
            continue

        if occurs:
            if level > lvlocc:
                if match['pic']:
                    locc += lenfield(match['pic'], match['usage'])
                continue
            lrecl += locc * occurs
        occurs = False
        lvlocc = 0

        if match['occurs']:
            lvlocc = level
            occurs = (int(nextWord('OCCURS', line)) if 'TO' not in wrds else
                      int(nextWord('TO', line)))

        if match['pic']:
            if occurs:
                locc += lenfield(match['pic'], match['usage'])
            else:
                lrecl += lenfield(match['pic'], match['usage'])

    return {'retorno': True, 'msg': None, 'lrecl': lrecl}


def lenfield(pic, usage):
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

    if not usage:
        usage = 'DISPLAY'

    if 'COMP-3' in usage or 'COMPUTATIONAL-3' in usage:
        lrecl = lentmp / 2 + 1
    elif 'COMP' in usage or 'COMPUTATIONAL' in usage or 'BINARY' in usage:
        lrecl = lentmp / 2
    elif 'SIGN' in usage:
        lrecl = lentmp + 1
    else:
        lrecl = lentmp

    return lrecl

