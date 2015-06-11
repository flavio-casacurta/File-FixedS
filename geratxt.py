import os
import sys
import traceback
import json
from calc_length import *
from columns import Columns
from fixed_files import Fixed_files


def geratxt(book, lines, csv):
    try:
        col = Columns()
        js = col.columns(book)
        ff = Fixed_files(js, obj=True)
        lenbook = calc_length(file(book).readlines())['lrecl']
        record = ff.parse('0' * lenbook)
        fj = [json.loads(line.decode('utf-8')) for line in js]
        fldtype = [(str(att['field']), str(att['type'])) for att in fj]

        txt = ''
        for line in lines:
            r = line.split(';')
            recordreplace = ''
            for n, f in enumerate(fldtype):
                recordreplace += "{} = {},".format(fldtype[n][0]
                                                  ,r[n] if fldtype[n][1] == 'int'
                                                        else "'"+r[n]+"'")

            record = eval('record._replace({})'.format(recordreplace))
            txt += ff.unparse(record)

        outtxt = csv.split('.')[0]
        nt = 0
        while True:
            filetxt = '{}{}.txt'.format(outtxt, '' if not nt else '({})'.format(nt))
            if os.path.exists(filetxt):
                nt += 1
            else:
                break

        out = open(filetxt, 'w')
        out.write(txt)
        out.close()
        return (True, filetxt)
    except:
        return (False, traceback.format_exc(sys.exc_info))
