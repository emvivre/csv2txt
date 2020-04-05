#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

'''
  Copyright: (c) 2020 François Lozes <emvivre@urdn.com.ua>
  This program is free software; you can redistribute it and/or
  modify it under the terms of the Do What The Fuck You Want To
  Public License, Version 2, as published by Sam Hocevar. See
  http://www.wtfpl.net/ for more details.
'''

import sys
import getopt
import csv

if len(sys.argv) < 3:
    print('Usage: %s [-d <DELIMITER>] [-s <SEPARATOR>] [-p <PADDING>] [-f <FIELD_0>,<FIELD_1>,...] <INPUT_CSV> <OUTPUT_CSV>' % sys.argv[0])
    quit(1)

padding = 1
delimiter = ','
fields_range = []
separator = '|'

(opt, args) = getopt.getopt(sys.argv[1:], 'd:p:f:s:')
for (k,v) in opt:
    if k == '-d':
        delimiter = v
    elif k == '-p':
        padding = int(v)
    elif k == '-f':
        fields_range = [ int(vv) for vv in v.split(',') ]
    elif k == '-s':
        separator = v

# read data
(input_csv, output_csv) = args
with open(input_csv) as fd:
    reader = csv.reader(fd)
    data = [ l for l in reader ]
nb_col = max([len(l) for l in data])
fields_range = fields_range if len(fields_range) > 0 else range(nb_col)

# normalize number of column for each line
for li in range(len(data)):
    data[li] += ['']*(nb_col-len(data[li]))

# compute maximum length for each column
max_length_per_col = [0]*nb_col
for line in data:
    for i in range(len(line)):
        l = len(line[i])
        if l > max_length_per_col[ i ]:
            max_length_per_col[ i ] = l

# check field range
for f in fields_range:
    if f >= len(max_length_per_col):
        print('ERROR: invalid field number given !')
        quit(1)

# apply padding to fields except the last one
for i in fields_range[:-1]:
    max_length_per_col[ i ] += 2 + padding

# generate output
s = ''
for line in data:
    for i in fields_range[:-1]:
        c = line[ i ]
        pad_len = max_length_per_col[i]-len(c)
        s += c + ' '*max(0,pad_len-2) + separator + ' '
    s += line[fields_range[-1]]
    s += '\n'

# save output
if output_csv != '-':
    with open(output_csv, 'w+t') as fd:
        fd.write(s)
else:
    print(s)
