# -*- coding: utf-8 -*-

import json
from collections import namedtuple


__author__ = 'flavio@casacurta.com'


class Fixed_files(object):

    def __init__(self, filejson, obj=False, dic=False):

        self.dic = dic

        try:
            if obj:
                lattrs = filejson
            else:
                filejson = filejson if filejson.endswith('.json') else '{}.json'.format(filejson)
                attrs = open(filejson).readlines()
                lattrs = [json.loads(line.decode('utf-8')) for line in attrs]
        except:
            lattrs = []

        self.attr = [att['field'] for att in lattrs]

        start = 0
        for att in lattrs:
            if att['sign']:
                att['length'] = att['length'] + 1
            exec ("self.{} = slice({}, {})".format(att['field'], start, (start + att['length'])))
            start += att['length']

        self.slices = ''
        for att in lattrs:
            if att['type'] == 'str':
                self.slices += 'record[self.{}], '.format(att['field'])
                fc = ''
            elif att['type'] == 'int':
                fc = ']'
                self.slices += '['
                if att['decimals']:
                    self.slices += 'round('
                if att['sign']:
                    self.slices += "int(record[self.{0}][:-1])*int(record[self.{0}][-1]+{1})".format(
                         att['field'], "'1'")
                else:
                    self.slices += 'int(record[self.{}])'.format(att['field'])
                if att['decimals']:
                    self.slices += ' * .{0:>0{1}}, {1})'.format('1', att['decimals'])
                self.slices += '{}, '.format(fc)

        self.Record = namedtuple('Record', self.attr)

    def parse(self, record):

        nt = eval("self.Record({})".format(self.slices))

        if self.dic:
            return {k:nt[n] for n, k in enumerate(self.attr)}

        return nt
