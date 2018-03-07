#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Raises the .json file with the image of COBOL copybook
for all copybooks of config.txt file in the directory ['DIRSOUVAL'] with the extension ['EXTCPY']
'pathProp.txt' is the default of config

Gera o arquivo .json com a imagem do copybook COBOL
para todos os books do diretório no config ['DIRSOUVAL'] com a extenção ['EXTCPY']
'pathProp.txt' � o default do config
'''

import os
from columns import Columns
from DirFileList import *

class Montajson(object):

    def __init__(self, config = 'pathProp.txt'):
        self.config = config
        self.col = Columns()

    def montajson(self):
        path = ''.join(open(self.config).readline().replace("'", "").split())
        config = open(os.path.join(path,'config.properties')).readlines()
        diccnfg = {line.split()[0]:line.split()[1] for line in config}
        isbook = lambda book: book[-3:].upper() == diccnfg['EXTCPY']

        dirfilelist = DirFileList()
        dirfilelist.setDirFileList(diccnfg['DIRSOULIB'])
        booklist = dirfilelist.getDirFileList()

        for book in filter(isbook, booklist):
            basename = os.path.basename(book).split('.')[0]
            print book
            bookwrite = open('{}{}'.format(diccnfg['DIRCNVJSON'], basename + '.json'), 'w')
            bookwrite.writelines(self.col.columns(book))
            bookwrite.close()
