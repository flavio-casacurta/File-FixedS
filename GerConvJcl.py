# -*- coding:utf-8
'''
   Created on 05/05/2016
   @author: C&C - HardSoft
'''
import re
import os
import sys
import traceback
from util.HOFsGenericas import *

lisAmbiente = [['AV', 'MX', 'MP']]

lisPrejob = [['GFCT', 'GFCT', 'T7GF']]

lisExecs = [['DB2A2HPU', 'DB2M1HPU', 'DB2CMHPU']
           ,['DB2A2UTL', 'DB2M1UTL', 'DB2CMUTL']
           ,['DB2A2UTB', 'DB2M1UTB', 'DB2CMUTB']]

lisDsns = [ ['AV.BIBGERAL'     , 'MX.BIBGERAL'     , 'MP.BIBGERAL']
          , ['AV.BIBGERTT'     , 'MX.BIBGERTT'     , 'MP.BIBGERTT']
          , ['DB2A2.R2.DSNLOAD', 'DB2M1.R2.DSNLOAD', 'DB2CM.R2.DSNLOAD']
          , ['DB2A2.R2.SYSIN'  , 'DB2M1.R2.SYSIN'  , 'DB2CM.R2.SYSIN']
          , ['AD.DBII.DEFUTIL' , 'MX.DBII.DEFUTIL' , 'MP.DBII.DEFUTIL']
          , ['SA.RDG1.ARC.AL2.ARCLIB'
            ,'SA.RDG1.ARC.MZ1.ARCLIB'
            ,'SA.RDG1.ARC.CM1.ARCLIB']
          , ['SA.RDG2.SREST.AL2C.DCALOAD.D051115'
            ,'SA.RDG2.SREST.MZ1.DCALOAD'
            ,'SA.RDG2.SREST.CM1A.DCALOAD']]

subForm = lambda line: re.sub('%%FORM#....', '%%FORM#!!!!', line)

class GerConvJcl(object):

    def __init__(self, jclinf, path, temprefix, sepjcl, jclcnv, ambiente, ambdest, jobs):
        self.jclinf = jclinf
        self.path = path
        self.temprefix = temprefix
        self.sepjcl = sepjcl
        self.jclcnv = jclcnv
        self.ambiente = ambiente
        self.ambdest = ambdest
        self.jobs = jobs

    def gerconvjcl(self):
        try:
            self.de = ['AV', 'MX', 'MP'].index(self.ambiente)
            para = ['AV', 'MX', 'MP'].index(self.ambdest)

            self.dicAmb = {v[self.de] : v[para] for v in lisAmbiente}
            self.dicJob = {v[self.de] : v[para] for v in lisPrejob}
            self.dicExec = {v[self.de] : v[para] for v in lisExecs}
            self.dicDsn = {v[self.de] : v[para] for v in lisDsns}
            start = 8 if self.temprefix else 0
            st = 18 if self.temprefix else 10
            self.isjob = lambda line: line[start:start+3] != '//*' and line[st:st+5] == " JOB "
            isdsn = lambda line: 'DSN=' in line
            isexec = lambda line: 'EXEC ' in line
            isrem = lambda line: line[start:start+3] == '//*'
            isdcb = lambda line: 'DCB=(' in line
            isform = lambda line: '%%FORM#' in line

            jclconv =[]

            for line in self.jclcnv:
                if isrem(line):
                    jclconv.append(self.linPrefix(line))
                elif self.isjob(line):
                    jclconv.append(line.replace(lisPrejob[0][self.de], self.dicJob[lisPrejob[0][self.de]]))
                elif isdsn(line):
                    jclconv.append(self.linDsn(line))
                elif isexec(line):
                    jclconv.append(self.linExec(line))
                elif isdcb(line):
                    jclconv.append(self.linDcb(line))
                elif isform(line):
                    jclconv.append(self.linPrefix(subForm(line)))
                else:
                    jclconv.append(self.linMisc(line))

            if (self.sepjcl or len(self.jobs) == 1) and not self.temprefix:
                self.writeseparate(jclconv)
            else:
                self.writejoin(jclconv)

            return True, None
        except:
            return (False, traceback.format_exc(sys.exc_info))


    def linDsn(self,line):
        rpo = '{}.{}'.format(self.dicAmb[lisAmbiente[0][self.de]], self.dicJob[lisPrejob[0][self.de]])
        dsn = line.split('=')[1].split(',')[0]
        if '(' in dsn:
            dsn = dsn.split('(')[0]
        if self.de == 1 and dsn[:2] == 'MJ':
            dsnn = dsn.replace('MJ', 'MX')
            if dsnn in self.dicDsn.keys():
                ret = line.replace(dsn, self.dicDsn[dsnn])
            elif dsn[3:7] == lisPrejob[0][self.de]:
                rpi = 'MJ.{}'.format(lisPrejob[0][self.de])
                ret = line.replace(rpi,rpo)
            else:
                ret = line.replace('MJ', self.dicAmb[lisAmbiente[0][self.de]])
        else:
            if dsn in self.dicDsn.keys():
                ret = line.replace(dsn, self.dicDsn[dsn])
            elif dsn[:2] == lisAmbiente[0][self.de] and dsn[3:7] == lisPrejob[0][self.de]:
                rpi = '{}.{}'.format(lisAmbiente[0][self.de], lisPrejob[0][self.de])
                ret = line.replace(rpi,rpo)
            else:
                ret = line.replace(lisAmbiente[0][self.de], self.dicAmb[lisAmbiente[0][self.de]])
        if re.findall(r'(2\s*DSN='+rpo+'\.[A-Z]\d{6})', ret):
            ret = re.sub('(\d{6})', '!!!!!!', ret, 1)

        return self.linPrefix(ret)

    def linExec(self,line):
        exc = nextWord('EXEC', line).rsplit(',')[0]
        if exc.startswith('PGM='):
            exc = exc.split('=')[1]
        if exc in self.dicExec.keys():
            line = line.replace(exc, self.dicExec[exc])
        return self.linPrefix(line)


    def linDcb(self,line):
        dcb = line.split('DCB=(')[1][:2]
        if dcb in self.dicAmb.keys():
            return self.linPrefix(line.replace(dcb, self.dicAmb[dcb]))
        else:
            return self.linPrefix(line)


    def linMisc(self,line):
        for k in self.dicDsn.keys():
            if k in line:
                line = line.replace(k, self.dicDsn[k])
                if 'ZAN01FGDEANYLOCAL' in line or 'ZAN01' in line:
                    line = re.sub('(\d{6})', '!!!!!!', line, 1)
                return self.linPrefix(line)

        if re.match(r'(^'+lisAmbiente[0][self.de]+'\.)', line):
            return self.linPrefix(line.replace(lisAmbiente[0][self.de], self.dicAmb[lisAmbiente[0][self.de]], 1))

        rpi = '{}.{}'.format(lisAmbiente[0][self.de], lisPrejob[0][self.de])
        if re.findall(rpi, line):
            rpo = '{}.{}'.format(self.dicAmb[lisAmbiente[0][self.de]], self.dicJob[lisPrejob[0][self.de]])
            return self.linPrefix(line.replace(rpi, rpo))

        return self.linPrefix(line)


    def linPrefix(self,line):
        if self.temprefix:
            return line[:8].replace(lisPrejob[0][self.de], self.dicJob[lisPrejob[0][self.de]])+line[8:]
        return line


    def writeseparate(self,jclconv):
        stop = False
        ijclconv = iter(jclconv)
        jclconv_next = ijclconv.next()

        while True:
            tmp = []
            jobname = jclconv_next[2:10]
            tmp.append(jclconv_next)
            jclconv_next = ijclconv.next()
            while not self.isjob(jclconv_next):
                tmp.append(jclconv_next)
                try:
                    jclconv_next = ijclconv.next()
                except StopIteration:
                    stop = True
                    break
            name = os.path.join(self.path, jobname  + '.jcl' )
            with open(name, 'w') as arq:
                arq.writelines(tmp)
            if stop:
                break


    def writejoin(self,jclconv):
        name = os.path.join(self.path
                           , os.path.basename(self.jclinf).split('.')[0]
                           + '_' + self.dicAmb[lisAmbiente[0][self.de]] + '.txt' )
        with open(name, 'w') as arq:
            arq.writelines(jclconv)

