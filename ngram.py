#! /bin/python
# encoding=utf-8
# NickGu
# http://nickgu.github.io

import cPickle
import logging

class NGramTraining:
    '''
        HOW TO USE:
            lm = NGramTraining(gram=2) # bigram.
            for term in text:
                lm.add(term)
            lm.save(output_model)
    '''
    def __init__(self, gram=2, cutoff=0):
        self.__gram = gram
        self.__cutoff = cutoff
        self.__dct = {}
        self.__total_count = 0
        self.__window = []

    def clear(self):
        ''' clear window '''
        self.__window = []

    def save(self, file_name):
        processed_dict = {}
        logging.info('compact dict.')
        for item, cnt in self.__dct.iteritems():
            if cnt <= self.__cutoff:
                continue
            if len(item) == self.__gram:
                key = tuple(item[:-1])
                if key not in processed_dict:
                    processed_dict[key] = [0, {}]
                processed_dict[key][1][item[-1]] = cnt
            else:
                if item in processed_dict:
                    processed_dict[item][0] = cnt
                else:
                    processed_dict[item] = [0, {}]

        logging.info('sort by prefix.')
        for prefix, info in processed_dict.iteritems():
            sl = sorted(info[1].iteritems(), key=lambda x:-x[1])
            processed_dict[prefix][1] = sl

        logging.info('write to file [%s] prefix_lemma:%d' % (file_name, len(processed_dict)))
        fd = file(file_name, 'wb')
        cPickle.dump(self.__gram, fd)
        cPickle.dump(self.__cutoff, fd)
        cPickle.dump(self.__total_count, fd)
        cPickle.dump(processed_dict, fd, protocol=2)
        fd.close()

    def add(self, word):
        self.__window.append(word)
        if len(self.__window) > self.__gram:
            self.__window.pop(0)
        if len(self.__window) == self.__gram:
            self.__total_count += 1
            key = tuple(self.__window)
            prefix_key = tuple(self.__window[:-1]) 
            self.__dct[key] = self.__dct.get(key, 0) + 1
            # update prefix counter.
            self.__dct[prefix_key] = self.__dct.get(prefix_key, 0) + 1

class NGramModel:
    '''
        How to use:
            mod = NGramModel()
            mod.load(filename)
            print mod.predict(prefix)
    '''
    def __init__(self):
        self.__dct = {}
        self.__gram = -1
        self.__cutoff = 0
        self.__total_count = 0

    def load(self, filename):
        fd = file(filename, 'rb')
        self.__gram = cPickle.load(fd)
        logging.info('gram:%d' % self.__gram)
        self.__cutoff = cPickle.load(fd)
        logging.info('cutoff:%d' % self.__cutoff)
        self.__total_count = cPickle.load(fd)
        logging.info('totalcount:%d' % self.__total_count)
        self.__dct = cPickle.load(fd)
        logging.info('item_loads:%d' % len(self.__dct))
        fd.close()

    def predict(self, prefix, output_num=5):
        if len(prefix) != self.__gram-1:
            logging.warning('input_prefix_length=%d, but model_prefix_length=%d' % (len(prefix), self.__gram-1))
        out = self.__dct.get(prefix, [-1, []])
        out[1] = out[1][:output_num]
        return out

if __name__ == '__main__':
    '''
    tester code:
        use jieba word-segment libary to genearte/predict chinese document.
    usage:
        ngram.py [--train|-t] <output>
            read document from stdin and train the data.
        ngram.py [--predict|-p] <model>
            read prefix from stdin, then return the best term list.
    '''
    import jieba
    import sys
    logging.basicConfig(level=logging.INFO)

    if sys.argv[1] == '--train' or sys.argv[1]=='-t':
        mod = NGramTraining()
        output_file = sys.argv[2]
        for line in sys.stdin.readlines():
            mod.clear()
            for term in jieba.cut(line):
                mod.add(term)
        mod.save(output_file)

    elif sys.argv[1] == '--predict' or sys.argv[1]=='-p':
        mod = NGramModel()
        mod.load(sys.argv[2])
        while 1:
            sys.stdout.write('> ')
            prefix = sys.stdin.readline()
            prefix = prefix.strip('\n').strip(' ')
            
            prefix_key = tuple(jieba.cut(prefix))
            out = mod.predict(prefix_key)
            print out[0]
            for item, cnt in out[1]:
                print item, cnt




