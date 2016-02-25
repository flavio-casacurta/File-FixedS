from HOFs import *
from columns import Columns
book = r'H:\Publico\Flavio\CMTF\CPY\CMTFW22A.cpy'
col = Columns()
bkout = col.columns(book,fmt='cbl')
bkout
from calc_length import *
calc_length(bkout)
bkin = file(book).readlines()
calc_length(bkin)
bkin = map(l672, filter(all3(isNotRem, isNotBlank, isNotEjectOrSkip), bkin))
word(bkin[0],1)
#teste do commit via pycharm
#teste do commit via pycharm 5.0.4
