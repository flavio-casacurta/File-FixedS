# -*- coding:utf-8
'''
   Created on 22/05/2015
   @author: C&C - HardSoft
'''
import os
import sys
import traceback
from util.change import change
from columns import Columns
from calc_length import calc_length

class GerJobPdZd(object):

    def __init__(self, jobname, path, book, sortin, sortout):
        self.jobname = jobname
        self.path = path
        self.book = book
        self.sortin = sortin
        self.sortout = sortout

    def gerjob(self):
        try:
            basename = os.path.basename(self.book).split('.')[0].upper()
            col = Columns()
            bookout = col.columns(self.book,fmt='cbl', signal=False)
            book_zonado = os.path.join(self.path, '{}_ZD.cpy'.format(basename))
            with open(book_zonado, 'w') as bkzd:
                bkzd.writelines(bookout)
            lengthout = str(calc_length(bookout)['lrecl'])

            formatout = ''
            start = 1
            bookin = file(self.book).readlines()
            for line in bookin:
                if 'PIC' not in line:
                    continue
                ap = ' OUTREC FIELDS=(' if start == 1 else '                 '
                length = int(str(calc_length(line.replace('COMP-3', ''))['lrecl']))
                lenpd  = calc_length(line)['lrecl']
                pd2zd = 'PD,TO=ZD,LENGTH={:03},'.format(length) if 'COMP-3' in line else ''
                formatout += '{}{:03},{:03},{}\n'.format(ap, start, lenpd, pd2zd)
                start += lenpd

            formatout = formatout[:-2] + ')\n'

            dicjob={'@JOBNAME'  :'{:8}'.format(self.jobname)
                   ,'@BOOK'     :basename
                   ,'@SORTIN'   :self.sortin
                   ,'@SORTOUT'  :self.sortout
                   ,'@LRECL'    :lengthout
                   ,'@OUTREC\n' :formatout
                   }

            job = change(dicjob, file('jobpk2zd.template').read())
            jobName = os.path.join(self.path, '{}.jcl'.format(self.jobname))
            with open(jobName, 'w') as jobWrite:
                jobWrite.write(job)
            return True, None
        except:
            return (False, traceback.format_exc(sys.exc_info))

