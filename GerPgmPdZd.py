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
from util.homogenize import Homogenize
from columns import Columns
from calc_length import calc_length

class GerPgmPdZd(object):

    def __init__(self, path, programId, book, signal):
        self.path = path
        self.programId = programId
        self.book = book
        self.signal=signal

    def gerpgm(self):
        try:
            bookin = file(self.book).readlines()
            lengthin = str(calc_length(bookin)['lrecl'])

            col = Columns()
            bkout = col.columns(self.book,fmt='cbl', signal=self.signal)
            bookout = ''
            for b in bkout:
                bookout += b

            lengthout = str(calc_length(bookout)['lrecl'])
            regout = 'WRK-ARQOUTZD-REGISTRO'
            bookin = Homogenize(bookin)

            if int(word(bookin[0],1)) == 1:
               regin = word(bookin[0],2).replace('.','')
               bookout = change({regin:regout}, bookout)
               lvl01bookin  = ''
               lvl01bookout = ''
            else:
               regin = 'WRK-ARQINPPD-REGISTRO'
               lvl01bookin  = '{:>9} {}.\n'.format('01',regin)
               lvl01bookout = '{:>9} {}.\n'.format('01',regout)
            formatout = ''
            for line in bookin:
                if 'PIC' in line:
                    if word(line , 2) == 'FILLER':
                        continue
                    fld = word(line,2)
                    formatout += '{:>15} {:31} OF {}\n'.format('MOVE', fld, regin)
                    formatout += '{:>15} {:31} OF {}\n'.format('TO', fld, regout)

            dicProg={'@PGMID'       :self.programId
                    ,'@DATE'        :date.today().strftime('%d %b %Y').upper()
                    ,'@BOOKIN'      :os.path.basename(self.book).split('.')[0].upper()
                    ,'@SINAL'       :'COM' if self.signal else 'SEM'
                    ,'@BOOKOUT\n'   :bookout
                    ,'@REGIN'       :regin
                    ,'@REGOUT'      :regout
                    ,'@LVL01BKIN\n' :lvl01bookin
                    ,'@LVL01BKOUT\n':lvl01bookout
                    ,'@LENGTHIN'    :lengthin
                    ,'@LENGTHOUT'   :lengthout
                    ,'@FORMATOUT\n' :formatout
                    }

            prog = insAster72(change(dicProg, file('legrpdzd.cbl').read()))
            progName = os.path.join(self.path, '{}.cbl'.format(self.programId))
            progWrite = open(progName, 'w')
            progWrite.write(prog)
            progWrite.close()
            return True, None
        except:
            return (False, traceback.format_exc(sys.exc_info))

