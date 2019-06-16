import re
from time import time
from Entropy import line_entropy

with open('data/stop_words.txt', 'r', encoding='utf-8') as rf:
    stop_words = set(rf.readlines())

class Cleaner(object):

    @classmethod
    def diversity(self, sent):
        counter = Counter(sent)
        
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
        EOS = '*'
        cnt = 0
        text = open(rfpath, 'r', encoding='UTF-8').readlines()
        text = sum(map(self.remove_punc, text), [])
        text = [line for line in text if line and line_entropy(line)>=1]
        text = [EOS + sent + EOS for sent in text]
        cnt = sum(map(len, text))
        return text

    @classmethod
    def preprocess_danmu(self, rfpath):
        EOS = '*'
        cnt = 0
        text = open(rfpath, 'r', encoding='UTF-8').readlines()
        num = len('2019-04-08 14:45:24,')
        text = [line[num:] for line in text]
        text = sum(map(self.remove_punc, text), [])
        # 弹幕里很多句子是由一两种字符组成，过滤掉
        text = [line for line in text if line and line_entropy(line)>=1]
        text = [EOS + sent + EOS for sent in text]
        cnt = sum(map(len, text))
        return text