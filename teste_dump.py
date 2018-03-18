import json
from collections import namedtuple
filejson = r'record_dump'
filejson = filejson if filejson.endswith('.json') else '{}.json'.format(filejson)
attrs = open(filejson).readlines()
lattrs = [json.loads(line.decode('utf-8')) for line in attrs]
attr = [att['field'][1] for att in lattrs]

def mult_per(att, mp):
    start = 0
    length = att['length']
    if att['sign']:
        length += 1
    stop = length
    slices = ''
    for n in range(mp):
        if att['type'] == 'str':
            slices += """record[{}][{}:{}], """.format(
                att['field'][1], start, stop)
        elif att['type'] == 'int':
            if att['decimals']:
                slices += 'round('
            if att['sign']:
                slices += "int(record[{0}][{1}:{2}][:-1])*int(record[{0}][{1}:{2}][-1]+{3})".format(
                    att['field'][1], start, stop, "'1'")
            else:
                slices += 'int(record[{0}][{1}:{2}])'.format(att['field'][1], start, stop)
            if att['decimals']:
                slices += ' * .{0:>0{1}}, {1})'.format('1', att['decimals'])
            slices += ','
        start += length
        stop += length
    return '[{}],'.format(slices)

if __name__ == '__main__':
    with open(r'D:\Python\MyTools\File-FixedS\record_dump.txt') as fi:
        for record in fi:
            print record
            mpn = {}
            start = 0
            for att in lattrs:
                mp = 1
                length = att['length']
                if att['sign']:
                    length += 1
                if att['field'][0] != 'N':
                    mp = ord(record[start:start + 1])
                    mpn[att['field'][1]]=mp
                    start += 1
                length *= mp
                exec ("{} = slice({}, {})".format(att['field'][1], start, (start + length)))
                print att['field'][1], '=', eval("{}".format(att['field'][1]))
                start += length

            slices = ''
            for att in lattrs:
                mp = mpn.get(att['field'][1], None)
                if mp:
                    slices += mult_per(att, mp)
                else:
                    if att['type'] == 'str':
                        slices += """record[{}], """.format(att['field'][1])
                    elif att['type'] == 'int':
                        if att['decimals']:
                            slices += 'round('
                        if att['sign']:
                            slices += "int(record[{0}][:-1])*int(record[{0}][-1]+{1})".format(
                                 att['field'][1], "'1'")
                        else:
                            slices += 'int(record[{}])'.format(att['field'][1])
                        if att['decimals']:
                            slices += ' * .{0:>0{1}}, {1})'.format('1', att['decimals'])
                        slices += ','

            Record = namedtuple('Record', attr)

            record = (eval("Record({})".format(slices)))
            print record.nome, record.valor