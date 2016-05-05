import os
from DirFileList import *
from GerJobPdZd import GerJobPdZd

print '\nGera JOBs para ler arquivo compactado'
print '          e gravar arquivo zonado\n'

path_in = raw_input(u'\nInforme o Caminho dos Books: ').upper()
while True:
    if os.path.isdir(path_in):
        break
    else:
        print '\nDiretorio "' + path_in + '" - invalido!\n'
        path_in = raw_input('Tente Novamente: ').upper()

isbook = lambda book: book[-3:].upper() == 'CPY'
dirfilelist = DirFileList()
dirfilelist.setDirFileList(path_in)
booklist = dirfilelist.getDirFileList()
books = filter(isbook, booklist)

if len(books) > 0:
    path = raw_input(u'\nInforme o Caminho para gravacao dos Jobs: ').upper()
    while True:
        if os.path.isdir(path):
            break
        else:
            print '\nDiretorio "' + path + '" - invalido!\n'
            path = raw_input('Tente Novamente: ').upper()
    for book in books:
        jobname = os.path.basename(book).split('.')[0].upper()
        gerjcl = GerJobPdZd(jobname, path, book, 'ENTRADA', 'SAIDA')
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
else:
    print 'Ops!!! Nenhum Book Encontrado em ', path_in
