# -*- coding: utf-8 -*-

from util.CobolPatterns import *

dicAttrSql = {'COMP2'    : 'SMALLINT'
             ,'COMP4'    : 'INTEGER'
             ,'COMP8'    : 'DOUBLE'
             ,'COMP-3'   : 'DECIMAL('
             ,'DISPLAYX' : 'CHAR('
             ,'OUTROS'   : 'CHAR('
             ,'DISPLAY9' : 'DECIMAL('}

dicAttrJson = {'COMP2'    : ['int', '4', '0', True]
              ,'COMP4'    : ['int', '9', '0', True]
              ,'COMP8'    : ['int', '18', '0', True]
              ,'COMP-3'   : ['int', '0', '0', None]
              ,'DISPLAYX' : ['str', '0', '0', None]
              ,'OUTROS'   : ['str', '0', '0', None]
              ,'DISPLAY9' : ['int', '0', '0', None]}

class Attribute(object):

    def __init__(self, lenVar=20):
        self.lenVar = lenVar

### Atributos SQL

    def attributeSql(self, pic_str, usage=None, occurs=None):

        usage = 'DISPLAY' if not usage else usage

        if  pic_str[0] == 'S':
            pic_str = pic_str[1:]

        pic_str0 = pic_str[0] if not occurs else 'X'

        while True:
            match = CobolPatterns.pic_pattern_repeats.search(pic_str)

            if  not match:
                break

            match = match.groupdict()
            expanded_str = match['constant'] * int(match['repeat'])
            pic_str = CobolPatterns.pic_pattern_repeats.sub(expanded_str, pic_str, 1)

        length = len(pic_str.replace('V', ''))

        if  usage == 'COMP':
            return dicAttrSql[usage + str(length / 2 )]

        if  occurs:
            occ = int(occurs)
            usage = 'DISPLAY'
            length = length * occ

        comma = ''
        decimals = ''
        if CobolPatterns.pic_pattern_float.match(pic_str):
            comma    = ','
            decimals = len(pic_str.split('V')[1])

        var = ''
        if  length  > self.lenVar and usage == 'DISPLAY' and pic_str0 == 'X':
            var = 'VAR'
            comma = ''
            decimals = ''

        length = str(length)
        decimals = str(decimals)

        if  usage in dicAttrSql:
            return dicAttrSql[usage] + length + comma + decimals +')'
        if  usage + pic_str0 in dicAttrSql:
            return var + dicAttrSql[usage + pic_str0] + length + comma + decimals + ')'
        return dicAttrSql['OUTROS'] + length + comma + decimals + ')'

### Atributos COBOL

    def attributeCob(self, col):

        pic = 'S9' if col.datatypes.picture_cobol == '9' else ' X'

        lenCol = str(col.colunas.lengthColuna - col.colunas.decimals)

        comma = ('' if col.datatypes.picture_cobol == 'X' else
                 'V' if not col.colunas.decimals else
                 'V9({})'.format(col.colunas.decimals))

        usage = ('.' if col.datatypes.usage_cobol == 'DISPLAY'
                     else ' USAGE {}.'.format(col.datatypes.usage_cobol))

        return '{}({}){}{}'.format(pic, lenCol, comma, usage)


### Atributos JSON

    def attribute_json(self, pic_str, usage=None, occurs=None, signal=True):

        usage = 'DISPLAY' if not usage else usage
        decimals = 0

        sign = False

        if  pic_str[0] == 'S':
            pic_str = pic_str[1:]
            if signal == True:
                sign = True

        pic_str0 = pic_str[0] if not occurs else 'X'

        while True:
            match = CobolPatterns.pic_pattern_repeats.search(pic_str)

            if  not match:
                break

            match = match.groupdict()
            expanded_str = match['constant'] * int(match['repeat'])
            pic_str = CobolPatterns.pic_pattern_repeats.sub(expanded_str, pic_str, 1)

        length = len(pic_str.replace('V', ''))

        if CobolPatterns.pic_pattern_float.match(pic_str):
            decimals = len(pic_str.split('V')[1])

        if  occurs:
            occ = int(occurs)
            usage = 'DISPLAY'
            length = length * occ
            decimals = 0

        if usage == 'COMP':
            usage = usage + str(length / 2 )

        if usage == 'COMP-3':
            dicAttrJson[usage][1] = str(length)
            dicAttrJson[usage][2] = str(decimals)
            dicAttrJson[usage][3] = sign

        if usage in dicAttrJson:
            return dicAttrJson[usage]

        if usage + pic_str0 in dicAttrJson:
            return [dicAttrJson[usage + pic_str0][0], str(length), str(decimals), sign]
        return [dicAttrJson['OUTROS'][0], str(length), str(decimals), sign]

