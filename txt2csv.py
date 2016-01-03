import os
from geracsv import geracsv

print '\nRotina para formatar arquivos em .CSV\n'

book = raw_input(u'Informe o Book: ')
while True:
    if os.path.isfile(book):
        break
    else:
        print 'Book "' + book + '" - inexistente!\n'
        book = raw_input('Tente Novamente: ')

print '\nInforme o Caminho e nome do arquivo ou deixe '
arq = raw_input(u' o nome em branco para gerar o .csv vazio: ')
while True:
    if os.path.isdir(arq):
        records = []
        arq = arq + os.path.sep + os.path.basename(book)
        break
    elif os.path.isfile(arq):
        while True:
            try:
                records = open(arq).read().splitlines()
                break
            except IOError:
                print '\nArquivo "' + arq + '" - invalido!\n'
                arq = raw_input('Tente Novamente: ')
        break
    else:
        print '\nArquivo "' + arq + '" - invalido!\n'
        arq = raw_input('Tente Novamente: ')

signal = raw_input(u'Com sinal? (S - Sim ou N - Nao): ')
while True:
    if  signal and signal[0].upper() in ('S', 'N'):
        break
    else:
        print '\nOpss... informe S - Sim ou N - Nao!\n'
        signal = raw_input('Tente Novamente: ')

signal = True if signal[0].upper() == 'S' else False

gercsv = geracsv(book, records, arq, signal)
if gercsv[0]:
    disp = '*** Arquivo: ' + arq + '" Processado com Sucesso ***'
    print '\n\n{}'.format('*' * len(disp))
    print disp
    print '***{}***'.format('-' * (len(disp)-6))
    outcsv = gercsv[1]
    print '*** Arquivo: ' + outcsv + '" Gerado com Sucesso     ***'
    print '{}'.format('*' * len(disp))
else:
    disp = '*** Arquivo: ' + arq + '" Processado com Erro ***'
    print '{}'.format('*' * len(disp))
    print disp
    print '{}'.format('*' * len(disp))
    print ''
    print gercsv[1]
