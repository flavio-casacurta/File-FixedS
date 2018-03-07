# -*- coding: utf-8 -*-
'''
   Created on 29/01/2016
   @author: C&C - HardSoft

   To use:
  >>> from print_dict import Print_Dict
  >>> # in screen
  >>>Print_Dict()(my_dict)
  >>> # in file
  >>>Print_Dict(r'my_dict.txt')(my_dict)

'''

class Print_Dict(object):
    def __init__(self, archive=None):
        self.archive = archive


    def __call__(self, obj):
        self.bn = ''
        if self.archive:
            self.fprint = open(self.archive, 'w')
            self.bn = '\n'
        self.print_dict(obj)
        if self.archive:
            self.fprint.close()


    def print_dict(self, obj, space=0, occo_list=''):
        if isinstance(obj, dict):
            for k, v in sorted(obj.items()):
                if isinstance(v, dict):
                    str_print = '{}{}{} {}{}'.format(' '*(space-len(occo_list)), occo_list, k, '{', self.bn)
                    if self.archive:
                        self.fprint.write(str_print)
                    else:
                        print str_print
                    space+=4
                    self.print_dict(v, space)
                    str_print = '{}{}{}'.format(' '*space, '}', self.bn)
                    if self.archive:
                        self.fprint.write(str_print)
                    else:
                        print str_print
                    space-=4
                elif isinstance(v, list):
                    str_print = '{}{} {}{}'.format(' '*space, k, '[', self.bn)
                    if self.archive:
                        self.fprint.write(str_print)
                    else:
                        print str_print
                    space+=4
                    for n, l in enumerate(v):
                        occo_list='[{}]'.format(n)
                        self.print_dict(l, space, occo_list)
                    space-=4
                    str_print = '{}{}{}'.format(' '*space, ']', self.bn)
                    if self.archive:
                        self.fprint.write(str_print)
                    else:
                        print str_print
                    occo_list=''
                else:
                    str_print = '{}{}{} = {}{}'.format(' '*(space-len(occo_list)), occo_list, k, v, self.bn)
                    if self.archive:
                        self.fprint.write(str_print)
                    else:
                        print str_print
        elif isinstance(obj, list):
            for l in obj:
                self.print_dict(l, space)

