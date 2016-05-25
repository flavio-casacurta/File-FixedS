import os
import re
from util.HOFs import *
from util.homogenize import homogenize
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

        for lin in lines:

            line = lin[:-1]
            if self.fmt != 'json':
                line = ' ' * 6 + line

            wrd, wrds = words(line)

            if not wrds[0].isdigit():
                continue

            level = int(wrds[0])

            if redefines:
                if level > lvlAnt:
                    continue
            redefines = False

            if 'REDEFINES' in wrds:
                lvlAnt = level
                redefines = True
                continue

            if 'PIC' not in wrds:
                if self.fmt != 'json':
                    addColumns.append(line + '.\n')
                continue

            dataname = wrds[1].lower().replace('-','_')
            if dataname == 'filler':
               filler+=1
               dataname = '{}_{}_{:02}'.format(basename.lower(), dataname, filler)

            picture = line.split('PIC')[1].split()
            pic = picture[0]
            usage = picture[1] if len(picture) > 1 and picture[1] != 'VALUE' else None
            occurs = picture[2:] if len(picture) > 2 and picture[2] == 'OCCURS' else None
            if self.fmt == 'json':
                type, length, decimals, sign = self.attr.attribute_json(pic, usage, occurs, signal)

                jCol = ('{}"field": "{}", "type": "{}", "length": "{}", "decimals": "{}", "sign": '
                        '"{}"{}\n').format('{', dataname, type, length, decimals, sign, '}')
                addColumns.append(jCol)
            else:
                splt_pic = line.split('PIC')[1]
                repl_pic = splt_pic.replace(' USAGE ', '').replace('COMP-3', '').replace('COMP', '').rstrip()
                lCol = line.replace(splt_pic, repl_pic)
                sign = '.\n'
                if pic[0] == 'S':
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
