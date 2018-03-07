import json
from collections import namedtuple
filejson = r'record_dump'
filejson = filejson if filejson.endswith('.json') else '{}.json'.format(filejson)
attrs = open(filejson).readlines()
lattrs = [json.loads(line.decode('utf-8')) for line in attrs]

with open(r'C:\Python\MyTools\File-FixedS\record_dump.txt') as fi:
    for row in fi:
        print row
        start = 0
        for att in lattrs:
            mp = 1
            length = att['length']
            if att['sign']:
                length += 1
            if att['field'][0] != 'N':
                mp = ord(row[start:start+1])
                start += 1
            length *= mp
            exec ("{} = slice({}, {})".format(att['field'][1], start, (start + length)))
            print att['field'][1], '=', eval("{}".format(att['field'][1]))
            start += length