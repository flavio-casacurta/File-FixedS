#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

'''

import os
from operator  import truth
from Diretorio import *
from time      import gmtime, time, sleep
from tqdm      import tqdm

ERRO = 'DESCRICAO DO ERRO'

IDCLI = 'IDENTIFICACAO DO ARQUIVO:'
IDCON = 'IDENTIFICACAO DO ARQUIVO:'
IDPRO = 'RELATORIO INCONSISTENCIA ARQUIVO:'

descErro = lambda line:truth(ERRO in line)

idCli = lambda line:truth(IDCLI in line)
idCon = lambda line:truth(IDCON in line)
idPro = lambda line:truth(IDPRO in line)

diretorio = Diretorio()
directory = diretorio.selectDirectory(txtDisplay = 'Selecione a pasta onde estao os relatorios desejados')

data_hora = gmtime(time() - 10800)

dt_hora   = '{0:2}/{1:2}/{2:4}'.format(str(data_hora.tm_mday).zfill(2),
                                       str(data_hora.tm_mon).zfill(2) ,
                                       str(data_hora.tm_year).zfill(4))

listdir = os.listdir(directory)

if not len(listdir):
    print ' '
    print 'Nenhum relatorio processado'
else:
    csv = open(os.path.join(directory, 'Inconsistencias consolidadas - Migracao_{0:4}{1:2}{2:2}.csv'.format(str(data_hora.tm_year).zfill(4),
                                                                                                            str(data_hora.tm_mon).zfill(2) ,
                                                                                                            str(data_hora.tm_mday).zfill(2))), 'w')
    csvs = ['Modulo;Tabela;Erro;Qtd;V.;Resp;Data Geracao;Analista;Observacao;\n']
    print ' '
    print 'Processando...'
    for modulo in listdir:
        if not os.path.isdir(os.path.join(directory, modulo)):
            continue
        try:
            pb.close()
        except:
            pass
        pb = tqdm(total=len(diretorio.listArqs(os.path.join(directory, modulo))))
        pb.write(modulo)
        errorList = {}
        for rel in os.listdir(os.path.join(directory, modulo)):
            pb.update(1)
            if 'contrato' in modulo.lower() and '162' not in rel:
                continue
            if 'proposta' in modulo.lower() and '408' in rel:
                continue
            arq = open('{}/{}'.format(os.path.join(directory, modulo), rel)).readlines()
            if not filter(descErro, arq):
                continue
            tb = filter(idCli, arq)
            if tb:
                tabela = tb[0].split(IDCLI)[1].strip()
                if len(tabela.split(' ')) > 1:
                    tabela = tabela.split(' ')[0]
                if not tabela:
                    tabela = rel.split('.txt')[0]
            else:
                tb = filter(idCon, arq)
                if tb:
                    tabela = tb[0].split(IDCON)[1].strip()
                    if len(tabela.split(' ')) > 1:
                        tabela = tabela.split(' ')[0]
                    if not tabela:
                        tabela = rel.split('.txt')[0]
                else:
                    tb = filter(idPro, arq)
                    if tb:
                        tabela = tb[0].split(IDPRO)[1].strip()
                        if len(tabela.split(' ')) > 1:
                            tabela = tabela.split(' ')[0]
                        if not tabela:
                            tabela = rel.split('.txt')[0]
                    else:
                        tabela = rel.split('.txt')[0]
            stop = False
            ilines = iter(arq)
            while True:
                try:
                    iline = ilines.next()
                except StopIteration:
                    stop = True
                    break
                while not descErro(iline):
                    try:
                        iline = ilines.next()
                    except StopIteration:
                        stop = True
                        break
                if stop:
                    break
                st = iline.index(ERRO)
                try:
                    iline = ilines.next()
                except StopIteration:
                    stop = True
                    break
                length = len(iline[st:].split()[0])
                try:
                    iline = ilines.next()
                except StopIteration:
                    stop = True
                    break
                while iline[st:st+length].strip():
                    if not iline[st:st+length].strip() in errorList:
                        errorList[iline[st:st+length].strip()] = 1
                    else:
                        errorList[iline[st:st+length].strip()] += 1
                    try:
                        iline = ilines.next()
                    except StopIteration:
                        stop = True
                        break
            for el in errorList:
                csvs.append('{};{};{};{};;;{};;;\n'.format(modulo, tabela, el, errorList[el], dt_hora))
            errorList = {}
    pb.close()
    csv.write(''.join(csvs))
    csv.close()
    print ' '
    print '*** Arquivo: CSV Gerado com Sucesso ***'
