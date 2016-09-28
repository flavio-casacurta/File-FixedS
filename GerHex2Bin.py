# -*- coding:utf-8
'''
   Created on 09/01/2016
   @author: C&C - HardSoft
'''
import os
import sys
import traceback
import codecs

isLrecl = lambda line: 'LRECL' in line
isZone = lambda line: line.startswith('ZONE')
isNumr = lambda line: line.startswith('NUMR')

class GerHex2Bin(object):

    def __init__(self, arq):
        self.arq = arq

    def gerbin(self):
        try:
            lines = file(self.arq).readlines()
            try:
                lrecl = int(filter(isLrecl, lines)[0].split()[2])
            except:
                return (False, 'Faltou LRECL')

            zone = filter(isZone, lines)
            numr = filter(isNumr, lines)

            lzone = []
            stop = 0
            izone = iter(zone)
            zone_next = izone.next()
            while True:
                tmp = ''
                while len(tmp) < lrecl:
                    tmp += zone_next.split()[1]
                    try:
                        zone_next = izone.next()
                    except StopIteration:
                        stop = 1
                        break
                lzone.append(tmp)
                if stop:
                    break

            lnumr = []
            stop = 0
            inumr = iter(numr)
            numr_next = inumr.next()
            while True:
                tmp = ''
                while len(tmp) < lrecl:
                    tmp += numr_next.split()[1]
                    try:
                        numr_next = inumr.next()
                    except StopIteration:
                        stop = 1
                        break
                lnumr.append(tmp)
                if stop:
                    break

            basename = self.arq.split('.')[0]
            arqbin = basename + '.bin'
            arqasc = basename + '_ascii.txt'
            with open(arqbin, 'wb') as bin, open(arqasc, 'wb') as asc:
                for r in xrange(len(lzone)):
                    zn = zip(lzone[r], lnumr[r])
                    ebc = ''
                    for z, n in zn:
                        ebc += chr(int(z+n, 16))

                    bin.write(ebc)

                    asc.write(codecs.decode(ebc, "cp500").encode('ASCII', 'replace') + '\n')

            return True, None
        except:
            return (False, traceback.format_exc(sys.exc_info))
