import os
from geratxt import geratxt

print '\nRotina para formatar arquivos .csv em .txt\n'

book = raw_input(u'Informe o Book: ')
while True:
    if os.path.exists(book):
        break
    else:
        print 'Book "' + book + '" - inexistente!\n'
        book = raw_input('Tente Novamente: ')

csv = raw_input(u'\nInforme o Caminho e nome do arquivo .csv: ')
while True:
    if csv.split('.')[1].lower() == 'csv':
        try:
            lines = open(csv).read().splitlines()[1:]
            break
        except IOError:
            print '\nArquivo "' + csv + '" - inexistente!\n'
            csv = raw_input('Tente Novamente: ')
    else:
        print '\nArquivo "' + csv + '" - nao eh ".csv"\n'
        csv = raw_input('Tente Novamente: ')

gertxt = geratxt(book, lines, csv)

if gertxt[0]:
    filetxt = gertxt[1]
    disp = '*** Arquivo: ' + csv + '" Processado com Sucesso ***'
    print '\n\n{}'.format('*' * len(disp))
    print disp
    print '***{}***'.format('-' * (len(disp)-6))
    print '*** Arquivo: ' + filetxt + '" Gerado com Sucesso     ***'
    print '{}'.format('*' * len(disp))
else:
    disp = '*** Arquivo: ' + csv + '" Processado com Erro ***'
    print '{}'.format('*' * len(disp))
    print disp
    print '{}'.format('*' * len(disp))
    print gertxt[1]
