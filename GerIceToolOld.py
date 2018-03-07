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
            bookin = file(self.book).readlines()
            bookin = Homogenize(bookin, cbl=True)
            for line in bookin:
                if not isPic(line):
                    continue
                col = l672(line).split()[1].replace(self.prefix, '')
                splt_pic = line.split('PIC')[1].strip()
                pic = '9' if splt_pic[0] == 'S' else splt_pic[0]
                length  = calc_length(line)['lrecl']
                if col == 'FILLER':
                    start += length
                    continue
                hdr = ('ZD' + self.decimals(splt_pic) if 'COMP' not in splt_pic and pic == '9' else
                       'PD' + self.decimals(splt_pic) if 'COMP-3' in splt_pic else
                       'BI' if 'COMP' in splt_pic else
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

    def decimals(self, pic):
        pic = pic.split()[0]
        ret = ''
        if 'V' in pic:
            if pic[0] == 'S':
                pic = pic[1:]
            integer, decimal = pic.split('V')
            pap = decimal.find('(')
            if pap == -1:
                decimal = len(decimal)
            else:
                try:
                    decimal = int(decimal[pap + 1:decimal.find(')')])
                except ValueError:
                    decimal = 0
            if decimal == 0:
                return ret
            if decimal == 2:
                ret = ',F2'
            else:
                pap = integer.find('(')
                if pap == -1:
                    integer = len(integer)
                else:
                    integer = int(integer[pap + 1:integer.find(')')])
                ret = ",E'{},{}'".format('9'*integer, '9'*decimal)
        return ret
