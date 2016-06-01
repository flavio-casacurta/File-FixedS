import os
import re
from util.HOFs import *
from util.homogenize import homogenize
from util.CobolPatterns import *
from attribute import Attribute

class Columns(object):

    def __init__(self):
        self.attr = Attribute(lenVar=4)

    def columns(self, file, fmt='json', signal=True):
        self.fmt = fmt
        basename = os.path.basename(file).split('.')[0]
        file = open(file).readlines()
        lines = homogenize(file)

        addColumns = []
        filler = 0
        redefines = False
        lvlAnt = 0

        for line in lines:

            match = CobolPatterns.row_pattern.match(line.strip())

            if not match:
                continue

            match = match.groupdict()

            if not match['level']:
                continue

            line = line[:-1]
            if self.fmt != 'json':
                line = ' ' * 6 + line

            level = int(match['level'])

            if redefines:
                if level > lvlAnt:
                    continue
            redefines = False

            if match['redefines']:
                lvlAnt = level
                redefines = True
                continue

            if not match['pic']:
                if self.fmt != 'json':
                    addColumns.append(line + '.\n')
                continue

            dataname = match['name'].replace('-','_').lower()
            if dataname == 'filler':
               filler+=1
               dataname = '{}_{}_{:02}'.format(basename.lower(), dataname, filler)

            if self.fmt == 'json':
                type, length, decimals, sign = self.attr.attribute_json(match['pic']
                                                                       ,match['usage']
                                                                       ,match['occurs']
                                                                       ,signal)

                jCol = ('{}"field": "{}", "type": "{}", "length": "{}", "decimals": "{}", "sign": '
                        '"{}"{}\n').format('{', dataname, type, length, decimals, sign, '}')
                addColumns.append(jCol)
            else:
                lCol = line.replace(line.split('PIC')[1].strip(), match['pic'])
                sign = '.\n'
                if match['pic'][0] == 'S':
                    if signal:
                        sign = ' SIGN TRAILING SEPARATE.\n'
                    else:
                        lCol = re.sub('PIC\s+S', 'PIC  ',lCol)
                    if len(lCol) > 73 - len(sign):
                        addColumns.append(lCol + '\n')
                        addColumns.append('{:>72}'.format(sign))
                    else:
                        addColumns.append(lCol + sign)
                else:
                    addColumns.append(lCol + sign)
        return addColumns
