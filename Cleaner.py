import re
from time import time


class Cleaner(object):

    @classmethod
    def n_gram(self, line, n):
        return [line[i:i + n] for i in range(len(line) - n + 1)] if len(line) >= n else []

    @classmethod
    def remove_punc(self, line):
        rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
        line = rule.sub(' ', line).strip().split(' ')
        return line

    @classmethod
    def preprocess_text(self, rfpath):
        tic = time()
        EOS = '*'
        cnt = 0
        text = open(rfpath, 'r', encoding='UTF-8').readlines()
        text = sum(map(self.remove_punc, text), [])
        text = [EOS + sent + EOS for sent in text]
        cnt = sum(map(len, text))
        print("peprocess done! %.2fs    %d words in total" % (time() - tic, cnt))
        return text
