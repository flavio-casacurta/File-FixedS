# -*- coding: utf-8 -*-
import os

class Diretorio(object):
    def __init__(self):
        pass

    def selectDirectory(self, txtDisplay = '', onlyDir = True):
        '''
            M‚todo para selecionar um determindado diretorio, utilizando Tkinter
        '''

        import Tkinter
        import tkFileDialog

        Tkinter.Tk().withdraw()

        if  onlyDir:
## O comando abaixo mostra tela para selecionar o diretorio
            directory = tkFileDialog.askdirectory(initialdir = os.getcwd(), title = 'Selecione a pasta desejada' \
                                                                                    if not txtDisplay            \
                                                                                    else   txtDisplay)
            return directory
        else:
            myFormats = [('COBOL',                     '*.cbl *.cob *.txt'),
                         ('COPYBOOK',                  '*.cpy *.txt'),
                         ('JCL',                       '*.jcl *.txt'),
                         ('Python',                    '*.py'),
                         ('Windows Bitmap',            '*.bmp'),
                         ('Portable Network Graphics', '*.png'),
                         ('JPEG',                      '*.jpg *.jpeg'),
                         ('CompuServer GIF',           '*.gif'),
                         ('Text File',                 '*.txt'),
                         ('All files',                 '*.*'),
                        ]

## O comando abaixo mostra tela para selecionar o arquivo nos formatos "myFormats" acima
            in_path = tkFileDialog.askopenfilename(filetypes = myFormats, title = 'Selecione o arquivo desejado')
            return in_path

    def listArqs(self, dir, subDir = True):
        '''
            M‚todo para listar arquivos de um determinado diretorio e seus subdiretorios
        '''

        listdir = os.listdir(dir)
        arqs    = []

        for modulo in listdir:
            if  not os.path.isdir(os.path.join(dir, modulo)):
                arqs.append(os.path.join(dir, modulo))
            else:
                if  subDir:
                    for arq in self.listArqs(os.path.join(dir, modulo)):
                        if  not os.path.isdir(arq):
                            arqs.append(arq)

        return arqs
