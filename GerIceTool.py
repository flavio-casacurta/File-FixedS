# -*- coding:utf-8
'''
   Created on 29/01/2016
   @author: C&C - HardSoft
'''
import os
import sys
import traceback
from util.HOFs import *
from util.change import change
from util.CobolPatterns import *
from util.homogenize import Homogenize
from calc_length import calc_length

class GerIceTool(object):

    def __init__(self, progname, path, book, entrada, titulo, prefix):
        self.progname = progname
        self.path = path
        self.book = book
        self.entrada = entrada
        self.titulo = titulo
        self.prefix = prefix

    def gericetool(self):
        try:
            header = ''
            start = 1
            bookin = Homogenize(file(self.book).readlines(), cbl=True)
            for line in bookin:
                match = CobolPatterns.row_pattern.match(line.strip())
                if not match:
                    continue
                match = match.groupdict()
                if not match['pic']:
                    continue
                col = match['name'].replace(self.prefix, '')
                pic_str = match['pic']
                if pic_str[0] == 'S':
                    pic_str = pic_str[1:]
                pic = pic_str[0]
                length  = calc_length(line)['lrecl']
                if col == 'FILLER':
                    start += length
                    continue
                usage = match['usage'] if match['usage'] else ''
                hdr = ('ZD' + self.decimals(pic_str) if 'COMP' not in usage and pic == '9' else
                       'PD' + self.decimals(pic_str) if 'COMP-3' in usage else
                       'BI' if 'COMP' in usage else
                       'CH')
                header += """ HEADER('{:30} ON({},{},{}) -\n""".format(col + "')"
                                                                     , start, length, hdr)
                start += length

            dicjob={'@TITULO'   :self.titulo
                   ,'@ENTRADA'  :self.entrada
                   ,'@PROGRAM'  :'{:8}'.format(self.progname)
                   ,'@HEADER\n' :header
                   }

            job = change(dicjob, file('icetool.template').read())
            jobName = os.path.join(self.path, '{}.jcl'.format(self.progname))
            with open(jobName, 'w') as jobWrite:
                jobWrite.write(job)
            return True, None
        except:
            return (False, traceback.format_exc(sys.exc_info))

    def decimals(self, pic_str):
        ret = ''
        if 'V' in pic_str:

            while True:
                match = CobolPatterns.pic_pattern_repeats.search(pic_str)

                if  not match:
                    break

                match = match.groupdict()
                expanded_str = match['constant'] * int(match['repeat'])
                pic_str = CobolPatterns.pic_pattern_repeats.sub(expanded_str, pic_str, 1)

            integer, decimal = pic_str.split('V')

            if decimal:
                if len(decimal) == 2:
                    ret = ',F2'
                else:
                    ret = ",E'{},{}'".format(integer, decimal)
        return ret
