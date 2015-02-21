#! /bin/python
# encoding=utf-8
# NickGu <https://github.com/nickgu>
# 
# A simple nlp tool.
# This program stat the cooc-term-distiance (mean and var)
# Usage:
#   python coocterm.py 
# 

import sys
import logging
import jieba
import math

def addoffset(ta, tb, offset, dct):
    key = (ta, tb)
    if key not in dct:
        dct[key] = []
    dct[key].append(offset)

if __name__=='__main__':
    dct = {}
    term_tf = {}
    logging.basicConfig(level=logging.INFO)
    window_size = 5
    cutoff = 2
    for line in sys.stdin.readlines():
        window = []
        for term in jieba.cut(line):
            term_tf[term] = term_tf.get(term, 0) + 1
            for idx, preterm in enumerate(window):
                offset = len(window) - idx
                addoffset(preterm, term, offset, dct)
            window.append(term)
            if len(window)>window_size:
                window.pop(0)
    logging.info('Load data over')
    # load data over.
    for coocterm, posset in sorted(dct.iteritems(), key=lambda x:-len(x[1])):
        if len(posset) <= cutoff:
            continue
        avg = 1.0 * sum(posset) / len(posset)
        var = 1.0 * sum(map(lambda x:(x-avg)*(x-avg), posset)) / len(posset)
        stdvar = math.sqrt(var)
        print '%s\t%s\t%d\t%.4f\t%.4f\t%d\t%d' % (
                coocterm[0].encode('utf-8'), 
                coocterm[1].encode('utf-8'), 
                len(posset), avg, stdvar, 
                term_tf.get(coocterm[0]),
                term_tf.get(coocterm[1]))

