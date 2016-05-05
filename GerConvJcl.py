# -*- coding:utf-8
'''
   Created on 05/05/2016
   @author: C&C - HardSoft
'''
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

class GerConvJcl(object):

    def __init__(self, jclinf, path, temprefix, sepjcl, jclcnv, ambiente, ambdest):
        self.jclinf = jclinf
        self.path = path
        self.temprefix = temprefix
        self.sepjcl = sepjcl
        self.jclcnv = jclcnv
        self.ambiente = ambiente
        self.ambdest = ambdest

    def gerconvjcl(self):
        try:
            self.de = ['AV', 'MX', 'MP'].index(self.ambiente)
            para = ['AV', 'MX', 'MP'].index(self.ambdest)

            self.dicAmb = {v[self.de] : v[para] for v in lisAmbiente}
            self.dicJob = {v[self.de] : v[para] for v in lisPrejob}
            self.dicExec = {v[self.de] : v[para] for v in lisExecs}
            self.dicDsn = {v[self.de] : v[para] for v in lisDsns}
            st = 19 if self.temprefix else 11
            isjob = lambda line: line[st:st+5] == "JOB '"
            isdsn = lambda line: 'DSN=' in line
            isexec = lambda line: 'EXEC ' in line
            start = 8 if self.temprefix else 0
            isrem = lambda line: line[start:start+3] == '//*'
            isdcb = lambda line: 'DCB=(' in line

            jclconv =[]

            for line in self.jclcnv:
                if isrem(line):
                    jclconv.append(line)
                elif isjob(line):
                    jclconv.append(line.replace(lisPrejob[0][self.de], self.dicJob[lisPrejob[0][self.de]]))
                elif isdsn(line):
                    jclconv.append(self.linDsn(line))
                elif isexec(line):
                    jclconv.append(self.linExec(line))
                elif isexec(line):
                    jclconv.append(self.linExec(line))
                elif isdcb(line):
                    jclconv.append(self.linDcb(line))
                else:
                    jclconv.append(line)

            self.writejoin(jclconv)

            return True, None
        except:
            return (False, traceback.format_exc(sys.exc_info))


    def linDsn(self,line):
        dsn = line.split('=')[1].split(',')[0]
        if dsn[:2] == 'MJ':
            dsnn = dsn.replace('MJ', 'MX')
        else:
            dsnn = dsn
        if dsnn in self.dicDsn.keys():
            return line.replace(dsn, self.dicDsn[dsnn])
        elif dsn[:2] == lisAmbiente[0][self.de] and dsn[3:7] == lisPrejob[0][self.de]:
            rpi = '{}.{}'.format(lisAmbiente[0][self.de], lisPrejob[0][self.de])
            rpo = '{}.{}'.format(self.dicAmb[lisAmbiente[0][self.de]], self.dicJob[lisPrejob[0][self.de]])
            return line.replace(rpi,rpo)
        else:
            return line.replace(lisAmbiente[0][self.de], self.dicAmb[lisAmbiente[0][self.de]])


    def linExec(self,line):
        exc = nextWord('EXEC', line).rsplit(',')[0]
        if exc in self.dicExec.keys():
            return line.replace(exc, self.dicExec[exc])
        else:
            return line


    def linDcb(self,line):
        dcb = line.split('DCB=(')[1][:2]
        if dcb in self.dicAmb.keys():
            return line.replace(dcb, self.dicAmb[dcb])
        else:
            return line


    def writeseparate(self,jclconv):
        pass


    def writejoin(self,jclconv):
        name = os.path.join(self.path
                           , os.path.basename(self.jclinf).split('.')[0]
                           + '_' + self.dicAmb[lisAmbiente[0][self.de]] + '.txt' )
        with open(name, 'w') as arq:
            arq.writelines(jclconv)

