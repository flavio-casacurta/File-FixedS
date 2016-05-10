import re
import os
import sys
import traceback
from GerConvJcl import GerConvJcl

print '\nConverte JCL\n'

jclinf = raw_input(u'Informe o Caminho e nome do JCL: ').upper()
while True:
    if jclinf:
        if os.path.isfile(jclinf):
            break
        else:
            print 'JCL "' + jclinf + '" - inexistente!\n'
            jclinf = raw_input('Tente Novamente: ').upper()
    else:
        print u'Informe o Caminho e nome do JCL\n'
        jclinf = raw_input('Tente Novamente: ').upper()

print u'\nInforme o Caminho para gravar o(s) JOB(s) convertido(s)'
path = raw_input(u'\nOu deixe em branco para assumir o default: ').upper()

if not path:
    if os.path.isdir(r'C:\TEMP'):
        path = 'C:\TEMP'
    else:
        path = os.getenv('TEMP')
    print 'Caminho "{}" assumido\n'.format(path)
else:
    while True:
        if os.path.isdir(path):
            break
        else:
            print '\nDiretorio "' + path + '" - invalido!\n'
            path = raw_input('Tente Novamente: ').upper()

try:
    jcl = open(jclinf).readlines()
    isvalid = lambda line: r'// REP' not in line and r'// ADD' not in line and r'// DEL' not in line
    jcl = filter(isvalid, jcl)
    manterPrefix = False
    if jcl[0].startswith('//'):
        temprefix = False
    else:
        temprefix = True

    if temprefix:
        manterPrefix = raw_input(u'Manter Prefixo? "S/N": ').upper()
        while True:
            if manterPrefix in ('S', 'N'):
                manterPrefix = True if manterPrefix == 'S' else False
                break
            else:
                print 'Ops! Informe "S" ou "N"\n'
                manterPrefix = raw_input('Tente Novamente: ').upper()

    sepjcl = False
    st = 19 if temprefix else 11
    isjob = lambda line: line[st:st+5] == "JOB '"
    jobs = filter(isjob, jcl)

    if len(jobs) == 0:
        print 'Faltou Cartao JOB'
    if not re.findall(r'//.{8} JOB ', jcl[0]):
        print 'Primeiro cartao tem que ser Cartao JOB'
    else:
        if len(jobs) > 1:
            if not manterPrefix:
                sepjcl = raw_input(u'Separar JCL? "S/N": ').upper()
                while True:
                    if sepjcl in ('S', 'N'):
                        sepjcl = True if sepjcl == 'S' else False
                        break
                    else:
                        print 'Ops! Informe "S" ou "N"\n'
                        sepjcl = raw_input('Tente Novamente: ').upper()

        if temprefix:
            if manterPrefix:
                start = 0
            else:
                start = 8
                temprefix = False
            stop = 80
        else:
            start = 0
            stop = 72
        lclear = lambda line: line[start:stop].rstrip() + '\n'
        jclcnv = map(lclear, jcl)

        bibgeral = filter(lambda line: 'BIBGERAL' in line, jclcnv)
        ib = bibgeral[0].index('BIBGERAL')
        ambiente = bibgeral[0][ib-3:ib-1]
        ambiente = 'MX' if ambiente == 'MJ' else ambiente
        dest = set('AV MX MP'.split()) - set(ambiente.split())
        sdest = str(sorted(list(dest)))
        ambdest = raw_input(u'Informe o Ambiente de destino ' + sdest + ': ').upper()
        while True:
            if ambdest:
                if ambdest in dest:
                    break
                else:
                    print u'Informe ' + sdest + '\n'
                    ambdest = raw_input('Tente Novamente: ').upper()
            else:
                print u'Informe o Ambiente de destino ' + sdest + ':\n'
                ambdest = raw_input('Tente Novamente: ').upper()

        gercjcl = GerConvJcl(jclinf, path, temprefix, sepjcl, jclcnv, ambiente, ambdest, jobs)
        gercjob = gercjcl.gerconvjcl()

        if gercjob[0]:
            disp = '*** JCL(s) convertido(s) com Sucesso ***'
            print '{}'.format('*' * len(disp))
            print disp
            print '{}'.format('*' * len(disp))
        else:
            disp = '*** JCL(s) Nao foram Convertido(s) ***'
            print '{}'.format('*' * len(disp))
            print disp
            print '{}'.format('*' * len(disp))
            print ''
            print gercjob[1]
except:
    print traceback.format_exc(sys.exc_info)
