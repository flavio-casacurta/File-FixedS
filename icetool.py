import os
from GerIceTool import GerIceTool

print '\nGera STEP para relatório com ICETOOL\n'

progname = raw_input(u'Informe o nome do Programa: ').upper()
if not progname:
    print 'Nome do Programa assumido como "PROG0000"\n'
    progname = "PROG0000"

titulo = raw_input(u'Informe o Titulo do Relatorio: ').upper()
if not titulo:
    print 'Titulo do Relatorio assumido como "RELATORIO 0000"\n'
    titulo = "RELATORIO 0000"

path = raw_input(u'\nInforme o Caminho para gravar o JOB gerado: ').upper()
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

book = raw_input(u'Informe o Book: ').upper()
while True:
    if os.path.isfile(book):
        break
    else:
        print 'Book "' + book + '" - inexistente!\n'
        book = raw_input('Tente Novamente: ').upper()

entrada = raw_input(u'Informe o nome do arquivo de Entrada: ').upper()
if not entrada:
    print '"ARQUIVO.ENTRADA" Assumido\n'
    entrada = 'ARQUIVO.ENTRADA'

prefix = ''
retpre = raw_input(u"Retirar Prefixo 'S' ou 'N': ").upper()
if retpre == 'S':
    prefix = raw_input(u"Iforme o Prefixo a Retirar : ").upper()
    while True:
        if prefix:
            break
        else:
            print 'Ops\n'
            prefix = raw_input(u"Iforme o Prefixo a Retirar : ").upper()

gericet = GerIceTool(progname, path, book, entrada, titulo, prefix)
gerstep = gericet.gericetool()

if gerstep[0]:
    command = 'notepad.exe {}'.format(os.path.join(path, progname + '.jcl'))
    os.system(command)
    disp = '*** ICETOOL Gerado com Sucesso ***'
    print '{}'.format('*' * len(disp))
    print disp
    print '{}'.format('*' * len(disp))
else:
    disp = '*** ICETOOL Nao foi Gerado ***'
    print '{}'.format('*' * len(disp))
    print disp
    print '{}'.format('*' * len(disp))
    print ''
    print gerstep[1]

