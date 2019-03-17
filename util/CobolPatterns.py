
import re

class CobolPatterns:
    opt_pattern_format = "({})?"

    row_pattern_base = r'^(?P<level>\d{1,3})\s+(?P<name>\S+)'
    row_pattern_occur = r'\s+OCCURS\s+(\d+\s+TO\s+)?(?P<occurs>\d+)(\s+TIMES)?'
    row_pattern_indexed_by = r"\s+INDEXED BY\s(?P<indexed_by>\S+)"
    row_pattern_redefine = r"\s+REDEFINES\s+(?P<redefines>\S+)"
    row_pattern_pic = r'\s+PIC\s+(?P<pic>\S+)'
    row_pattern_usage = r'\s+(USAGE\s+)?(IS\s+)?(?P<usage>\S+)'
    row_pattern_remainder = r'(?P<remainder>.*)'
    row_pattern_end = r'\.$'

    row_pattern = re.compile(row_pattern_base +
                             opt_pattern_format.format(row_pattern_redefine) +
                             opt_pattern_format.format(row_pattern_occur) +
                             opt_pattern_format.format(row_pattern_indexed_by) +
                             opt_pattern_format.format(row_pattern_pic) +
                             opt_pattern_format.format(row_pattern_usage) +
                             row_pattern_remainder +
                             row_pattern_end)

    row_pattern_redefines = re.compile(row_pattern_redefine)
    row_pattern_occurs = re.compile(row_pattern_occur)

    pic_pattern_repeats = re.compile(r'(?P<constant>.)\((?P<repeat>\d+)\)')
    pic_pattern_float = re.compile(r'S?9*V9+')
    pic_pattern_float_edit = re.compile(r'S?[9Z]*[,][9Z]+')
    pic_pattern_integer = re.compile(r'S?9+(?!V)9+$')

    row_pattern_value = re.compile(r'\s+VALUE(S)?\s+(IS\s+)?(ARE\s+)?(?P<value>\S+)')
