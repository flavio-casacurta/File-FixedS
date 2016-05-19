# -*- coding:utf-8
'''
   Created on 21/04/2016
   @author: C&C - HardSoft
'''
import os
import sys
import traceback

def zipfile(auxfile, name, basename):
    try:
        lexs = map(l982, filter(hex, auxfile))
        if lexs[0][:8] == '504B0304':
            ascii=''
            for lex in lexs:
                lx = ''.join(lex.split())
                for n in xrange(0,len(lx),2):
                    ascii += chr(int(lx[n:n+2], 16))

            auxzip = os.path.join(os.path.dirname(name), basename + '.zip')
            with open(auxzip, 'wb') as zip:
                zip.write(ascii)
            print '\n', auxzip ,' Gerado com Sucesso!'
        else:
            print '\nArquivo "' + basename + '" Invalido!!!'
    except:
        print traceback.format_exc(sys.exc_info)

if __name__ == '__main__':
    print '\nRotina para formatar Hexprint do IDCAMS em .ZIP\n'

    name = raw_input(u'Informe o Arquivo de Entrada: ')
    while True:
        if os.path.isfile(name):
            break
        else:
            print 'Arquivo de Entrada "' + name + '" - inexistente!\n'
            name = raw_input('Tente Novamente: ')

    print_infile = lambda line: line.lstrip().startswith('PRINT INFILE')
    hex = lambda line: line[1:3] == '00'
    l982 = lambda line: line[9:82].rstrip()

    aux = file(name).readlines()
    prtinfile = filter(print_infile, aux)
    if len(prtinfile) == 1:
        basename = os.path.basename(name).split('.')[0]
        zipfile(aux, name, basename)
    else:
        stop = False
        ilines = iter(aux)
        iline = ilines.next()
        while not print_infile(iline):
            iline = ilines.next()
        while True:
            auxfile = []
            basename = iline.split('INFILE(')[1].split(')')[0]
            auxfile.append(iline)
            iline = ilines.next()
            while not print_infile(iline):
                auxfile.append(iline)
                try:
                    iline = ilines.next()
                except StopIteration:
                    stop = True
                    break
            zipfile(auxfile, name, basename)
            if stop:
                break
