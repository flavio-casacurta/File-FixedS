import os
import sys
import traceback
import re
import json
from columns import Columns
from fixed_files import Fixed_files

def geracsv(book, records, arq):
    try:
        basename = os.path.basename(book).split('.')[0]
        col = Columns()
        js = col.columns(book)
        ff = Fixed_files(js, obj=True)
        rec_in = []
        for record in records:
            rec_in.append(ff.parse(record))
        fj = [json.loads(line.decode('utf-8')) for line in js]
        flds = [str(att['field']) for att in fj]
        csvs = ';'.join(str(flds)[1:-1].upper().replace(basename + '_','').replace("'","").split(',')) + '\n'
        csvs = re.sub('FILLER_..', 'FILLER', csvs)
        for r in rec_in:
            for f in flds:
                csvs += str(eval('r.{}'.format(f)))+';'
            csvs += '\n'
        outcsv = arq.split('.')[0] + '.csv'
        out = open(outcsv, 'w')
        out.write(csvs)
        out.close()
        return (True, outcsv)
    except:
        return (False, traceback.format_exc(sys.exc_info))
