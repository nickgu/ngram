#! /bin/env python
# encoding=utf-8
# gusimiu@baidu.com
# 

if __name__ == '__main__':
    '''
    tester code:
        use jieba word-segment libary to stat ngram count.
    usage:
        ngram.py <output> [max_n = 2]
            read document from stdin and train the data.
    '''
    import jieba
    import sys
    import logging
    logging.basicConfig(level=logging.INFO)

    output_file = file(sys.argv[1], 'w')
    max_n = 2

    stat_dict = []
    for n in range(max_n+2):
        stat_dict.append({})

    for line in sys.stdin.readlines():
        terms = []
        for term in jieba.cut(line):
            terms.append(term)


        for n in range(1, max_n+1):
            for idx in range(len(terms) - n):
                phrase = u''.join(terms[idx:idx+n])
                if len(phrase)<n*2:
                    continue
                phrase = phrase.encode('utf-8', 'ignore')

                stat_dict[n][phrase] = stat_dict[n].get( phrase, 0 ) + 1
            
    for n, d in enumerate(stat_dict):
        for item, count in sorted(d.iteritems(), key=lambda x:-x[1]):
            print >> output_file, '%d\t%s\t%d' % (n, item, count)
    

