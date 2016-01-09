import os
from GerHex2Bin import GerHex2Bin

print '\nApp para formatar arquivos HEXPrint em Binario\n'

arq = raw_input(u'Informe o Arquivo HEXPrint: ')
while True:
    if os.path.exists(arq):
        break
    else:
        print 'Arquivo HexPrint "' + arq + '" - inexistente!\n'
        arq = raw_input('Tente Novamente: ')

basename = os.path.basename(arq)
arqbin = '{}.bin'.format(basename.split('.')[0].upper())
gerabin = GerHex2Bin(arq)
gerbin = gerabin.gerbin()

if gerbin[0]:
    disp = '*** Arquivo: {} Processado com Sucesso ***'.format(basename)
    print '\n\n{}'.format('*' * len(disp))
    print disp
    print '***{}***'.format('-' * (len(disp)-6))
    print '*** Arquivo: {} Gerado com Sucesso     ***'.format(arqbin)
    print '{}'.format('*' * len(disp))
else:
    disp = '*** Arquivo: {} Processado com Erro ***'.format(basename)
    print '{}'.format('*' * len(disp))
    print disp
    print '{}'.format('*' * len(disp))
    print gerbin[1]
