# -*- coding:utf-8
'''
   Created on 22/05/2015
   @author: C&C - HardSoft
'''
import os
import sys
import traceback
from util.change import change
from util.homogenize import Homogenize
from columns import Columns
from calc_length import calc_length

class GerJobPdZds(object):

    def __init__(self, jobname, path, dicbooks, sortin, sortout):
        self.jobname = jobname
        self.path = path
        self.dicbooks = dicbooks
        self.sortin = sortin
        self.sortout = sortout

    def gerjob(self):
        try:
            inrec = " INREC "
            for book in self.dicbooks:
                basename = os.path.basename(self.book).split('.')[0].upper()

                col = Columns()
                bookout = col.columns(self.book,fmt='cbl', signal=False)
                book_zonado = os.path.join(self.path, '{}_ZD.cpy'.format(basename))
                with open(book_zonado, 'w') as bkzd:
                    bkzd.writelines(bookout)
                lengthout = str(calc_length(bookout)['lrecl'])
                start = 1
                strt = self.dicbooks['start']
                length = self.dicbooks['length']
                content = self.dicbooks['content']
                formatout = "{}IFTHEN=(WHEN=({},{},CH,EQ,C'{}'),\n".format(inrec, strt, length, content)
                inrec = "       "
                build = '         BUILD('
                bookin = file(self.book).readlines()
                bookin = Homogenize(bookin, cbl=True)
                for line in bookin:
                    if 'PIC' not in line:
                        continue
                    splt_pic = line.split('PIC')[1]
                    repl_pic = splt_pic.replace(' USAGE ', '').replace('COMP-3', '').replace('COMP', '').rstrip()

                    length = int(str(calc_length(line.replace(splt_pic, repl_pic))['lrecl']))
                    lenpd  = calc_length(line)['lrecl']
                    pd2zd = ('PD,TO=ZD,LENGTH={:03},'.format(length)
                                                     if 'COMP-3' in splt_pic else
                             'BI,TO=ZD,LENGTH={:03},'.format(length)
                                                     if 'COMP' in splt_pic else '')
                    formatout += '{}{:03},{:03},{}\n'.format(build, start, lenpd, pd2zd)
                    build = '               '
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

