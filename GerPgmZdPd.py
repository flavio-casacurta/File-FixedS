# -*- coding:utf-8
'''
   Created on 22/05/2015
   @author: C&C - HardSoft
'''
import os
import sys
import traceback
from datetime import date
from util.HOFs import *
from util.insAster72 import insAster72
from util.change import change
from util.homogenize import homogenize
from columns import Columns
from calc_length import calc_length

class GerPgmZdPd(object):

    def __init__(self, path, programId, book, signal):
        self.path = path
        self.programId = programId
        self.book = book
        self.signal=signal

    def gerpgm(self):
        try:
            bookout = file(self.book).readlines()
            lengthout = str(calc_length(bookout)['lrecl'])

            col = Columns()
            bkin = col.columns(self.book,fmt='cbl', signal=self.signal)
            bookin = ''
            for b in bkin:
                bookin += b

            lengthin = str(calc_length(bookin)['lrecl'])
            regin  = 'WRK-ARQINPZD-REGISTRO'
            bookout = homogenize(bookout)

            if int(word(bookout[0],1)) == 1:
               regout = word(bookout[0],2).replace('.','')
               bookin = change({regout:regin}, bookin)
               lvl01bookin  = ''
               lvl01bookout = ''
            else:
               regout = 'WRK-ARQOUTPD-REGISTRO'
               lvl01bookin  = '{:>9} {}.\n'.format('01',regin)
               lvl01bookout = '{:>9} {}.\n'.format('01',regout)
            formatout = ''
            for line in bookout:
                if 'PIC' in line:
                    if word(line , 2) == 'FILLER':
                        continue
                    fld = word(line,2)
                    formatout += '{:>15} {:31} OF {}\n'.format('MOVE', fld, regin)
                    formatout += '{:>15} {:31} OF {}\n'.format('TO', fld, regout)

            dicProg={'@PGMID'       :self.programId
                    ,'@DATE'        :date.today().strftime('%d %b %Y').upper()
                    ,'@BOOKOUT'     :os.path.basename(self.book).split('.')[0].upper()
                    ,'@SINAL'       :'COM' if self.signal else 'SEM'
                    ,'@BOOKIN\n'    :bookin
                    ,'@REGIN'       :regin
                    ,'@REGOUT'      :regout
                    ,'@LVL01BKIN\n' :lvl01bookin
                    ,'@LVL01BKOUT\n':lvl01bookout
                    ,'@LENGTHIN'    :lengthin
                    ,'@LENGTHOUT'   :lengthout
                    ,'@FORMATOUT\n' :formatout
                    }

            prog = insAster72(change(dicProg, file('legrzdpd.cbl').read()))
            progName = os.path.join(self.path, '{}.cbl'.format(self.programId))
            progWrite = open(progName, 'w')
            progWrite.write(prog)
            progWrite.close()
            return True, None
        except:
            return (False, traceback.format_exc(sys.exc_info))

