# -*- coding:utf-8
'''
   Created on 21/04/2016
   @author: C&C - HardSoft
'''
import os
import sys
import traceback

print '\nRotina para formatar Hexprint do IDCAMS em .ZIP\n'

name = raw_input(u'Informe o Arquivo de Entrada: ')
while True:
    if os.path.isfile(name):
        break
    else:
        print 'Arquivo de Entrada "' + name + '" - inexistente!\n'
        name = raw_input('Tente Novamente: ')

hex = lambda line: line[1:3] == '00'
l982 = lambda line: line[9:82].rstrip()
try:
    aux = file(name).readlines()
    lexs = map(l982, filter(hex, aux))
    if lexs[0][:8] == '504B0304':
        ascii=''
        for lex in lexs:
            lx = ''.join(lex.split())
            for n in xrange(0,len(lx),2):
                ascii += chr(int(lx[n:n+2], 16))

        auxzip = os.path.join(os.path.dirname(name), os.path.basename(name).split('.')[0] + '.zip')
        with open(auxzip, 'wb') as zip:
            zip.write(ascii)
        print '\n', auxzip ,' Gerado com Sucesso!'
    else:
        print '\nArquivo "' + name + '" Invalido!!!'
except:
    print traceback.format_exc(sys.exc_info)

