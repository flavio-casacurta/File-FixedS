import os
from GerJobPdZd import GerJobPdZd

print '\nGera JOB para ler   arquivo compactado'
print '              e grava arquivo zonado\n'

jobname = raw_input(u'Informe o nome do JOB: ').upper()
while True:
    if jobname:
        break
    else:
        print 'Nome do JOB invalido!\n'
        jobname = raw_input('Tente Novamente: ').upper()

path = raw_input(u'\nInforme o Caminho para gravar o JOB gerado: ').upper()
while True:
    if os.path.isdir(path):
        break
    else:
        print '\nDiretorio "' + path + '" - invalido!\n'
        path = raw_input('Tente Novamente: ').upper()

book = raw_input(u'Informe o Book: ').upper()
while True:
    if os.path.isfile(book):
        break
    else:
        print 'Book "' + book + '" - inexistente!\n'
        book = raw_input('Tente Novamente: ').upper()

sortin = raw_input(u'Informe o nome do arquivo de Entrada: ').upper()
while True:
    if sortin:
        break
    else:
        print 'arquivo de Entrada invalido!\n'
        sortin = raw_input('Tente Novamente: ').upper()

sortout = raw_input(u'Informe o nome do arquivo de Saida: ').upper()
while True:
    if sortout:
        break
    else:
        print 'arquivo de Entrada invalido!\n'
        sortot = raw_input('Tente Novamente: ').upper()

gerjcl = GerJobPdZd(jobname, path, book, sortin, sortout)
gerjob = gerjcl.gerjob()

if gerjob[0]:
    disp = '*** JOB: {} Gerado com Sucesso ***'.format(jobname)
    print '{}'.format('*' * len(disp))
    print disp
    print '{}'.format('*' * len(disp))
else:
    disp = '*** JOB: {} Nao foi Gerado ***'.format(jobname)
    print '{}'.format('*' * len(disp))
    print disp
    print '{}'.format('*' * len(disp))
    print ''
    print gerjob[1]
