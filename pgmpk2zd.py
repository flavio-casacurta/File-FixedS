import os
from GerPgmPdZd import GerPgmPdZd

print '\nGera programa para ler   arquivo compactado'
print '                   e grava arquivo zonado\n'

programId = raw_input(u'Informe o nome do programa: ').upper()
while True:
    if programId:
        break
    else:
        print 'Nome do programa invalido!\n'
        programId = raw_input('Tente Novamente: ').upper()

path = raw_input(u'\nInforme o Caminho para gravar o programa gerado: ')
while True:
    if os.path.isdir(path):
        break
    else:
        print '\nDiretorio "' + path + '" - invalido!\n'
        path = raw_input('Tente Novamente: ')

book = raw_input(u'Informe o Book: ')
while True:
    if os.path.isfile(book):
        break
    else:
        print 'Book "' + book + '" - inexistente!\n'
        book = raw_input('Tente Novamente: ')

signal = raw_input(u'Com sinal? (S - Sim ou N - Nao): ')
while True:
    if  signal and signal[0].upper() in ('S', 'N'):
        break
    else:
        print '\nOpss... informe S - Sim ou N - Nao!\n'
        signal = raw_input('Tente Novamente: ')

signal = True if signal[0].upper() == 'S' else False

gerprog = GerPgmPdZd(path, programId, book, signal)
gerpgm = gerprog.gerpgm()

if gerpgm[0]:
    disp = '*** Programa: ' + programId + ' Gerado com Sucesso ***'
    print '{}'.format('*' * len(disp))
    print disp
    print '{}'.format('*' * len(disp))
else:
    disp = '*** Programa: ' + programId + ' Nao foi Gerado ***'
    print '{}'.format('*' * len(disp))
    print disp
    print '{}'.format('*' * len(disp))
    print ''
    print gerpgm[1]
