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
    occurs = 0
    dicoccurs = {}
    level_redefines = 0

    for line in lines:
        match = CobolPatterns.row_pattern.match(line.strip())
        if not match:
            continue
        match = match.groupdict()
        if not match['level']:
            continue

        if 'REDEFINES' in line and not match['redefines']:
            match['redefines'] = CobolPatterns.row_pattern_redefines.search(line).groupdict().get('redefines')
        if 'OCCURS' in line and not match['occurs']:
            match['occurs'] = CobolPatterns.row_pattern_occurs.search(line).groupdict().get('occurs')

        level = int(match['level'])

        if redefines:
            if level > level_redefines:
                continue
        redefines = False
        level_redefines = 0

        if match['redefines']:
            level_redefines = level
            redefines = True
            continue

        if occurs:
            if level > dicoccurs[occurs]['level']:
                if match['occurs']:
                    occurs += 1
                    attrib = {}
                    attrib['occ'] = int(match['occurs'])
                    attrib['level'] = level
                    attrib['length'] = 0
                    dicoccurs[occurs] = attrib
                if match['pic']:
                    dicoccurs[occurs]['length'] += FieldLength(match['pic'], match['usage'])
                continue
            while True:
                if occurs == 1:
                    lrecl += dicoccurs[occurs]['length'] * dicoccurs[occurs]['occ']
                else:
                    dicoccurs[occurs-1]['length'] += dicoccurs[occurs]['length'] * dicoccurs[occurs]['occ']
                del dicoccurs[occurs]
                occurs -= 1
                if not occurs:
                    break
                if level > dicoccurs[occurs]['level']:
                    break

        if match['occurs']:
            occurs += 1
            attrib = {}
            attrib['occ'] = int(match['occurs'])
            attrib['level'] = level
            attrib['length'] = 0
            dicoccurs[occurs] = attrib

        if match['pic']:
            if occurs:
                dicoccurs[occurs]['length'] += FieldLength(match['pic'], match['usage'])
            else:
                lrecl += FieldLength(match['pic'], match['usage'])

    return {'retorno': True, 'msg': None, 'lrecl': lrecl}


def FieldLength(pic_str, usage):
    if pic_str[0] == 'S':
        pic_str = pic_str[1:]

    while True:
        match = CobolPatterns.pic_pattern_repeats.search(pic_str)

        if not match:
            break

        match = match.groupdict()
        expanded_str = match['constant'] * int(match['repeat'])
        pic_str = CobolPatterns.pic_pattern_repeats.sub(expanded_str, pic_str, 1)

    len_field = len(pic_str.replace('V', ''))

    if not usage:
        usage = 'DISPLAY'

    if 'COMP-3' in usage or 'COMPUTATIONAL-3' in usage:
        len_field = len_field / 2 + 1
    elif 'COMP' in usage or 'COMPUTATIONAL' in usage or 'BINARY' in usage:
        len_field = len_field / 2
    elif 'SIGN' in usage:
        len_field += 1

    return len_field

