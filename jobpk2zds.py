import os, sys
from GerJobPdZds import GerJobPdZds

print '\nGera JOB para ler   arquivo compactado com varios Lay Outs\n'
print '              e grava arquivo zonado\n'

jobname = raw_input(u'Informe o nome do JOB: ').upper()
while True:
    if len(jobname) > 4 and len(jobname) < 9:
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

qtbks = raw_input(int(u'\nInforme a quantidade de Books: '))
while True:
    if qtbks > 0:
        break
    elif qtbks == 1:
        print 'Utilize o utilitario jobpk2zd'
        sys.exit(1)

lisbooks = []
qtbksinf = 1
while True:
    book = raw_input(u'Informe o Book de numero : {}'.format(qtbksinf)).upper()
    while True:
        if os.path.isfile(book):
            if book in lisbooks:
                print 'Book "' + book + '" - ja informado!\n'
                book = raw_input('Tente Novamente: ').upper()
            else:
                lisbooks.append(book)
                break
        else:
            print 'Book "' + book + '" - inexistente!\n'
            book = raw_input('Tente Novamente: ').upper()

    while True:
        start = raw_input(int(u'Qual a posicao inicial do arquivo que identifica o Book :'))
        if start:
            break
        else:
            print 'campo invalido!\n'
            start = raw_input(int('Tente Novamente: '))

    while True:
        length = raw_input(int(u'Qual o tamanho que identifica o Book :'))
        if length:
            break
        else:
            print 'campo invalido!\n'
            length = raw_input(int('Tente Novamente: '))

    list_cont = []
    while True:
        content = raw_input(u'Qual o conteudo eue identifica o Book de numero {} :'.format(qtbksinf))
        if content:
            list_cont.append(content)
            print 'Mais algum conteudo?\n'
            content = raw_input('Informe Novo conteudo : ')
            if not content:
                break
        else:
            print 'conteudo invalido!\n'
            content = raw_input('Tente Novamente: ')

    qtbksinf += 1
    if qtbksinf > qtbks:
        break
    dicbooks = {}
    for book in lisbooks:
        dicbooks[book] = list_cont

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

gerjcl = GerJobPdZds(jobname, path, dicbooks, start, length, sortin, sortout)
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
