import re
from time import time
from Entropy import line_entropy

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
    def z_alg(self, s):
        n = len(s)
        z = [0] * n
        L = 0
        R = 0
        for i in range(n):
            if i > R:
                L = R = i
                while R < n and s[R-L] == s[R]:
                    R += 1
                z[i] = R-L
                R -= 1
            else:
                k = i-L
                if z[k] < R-i+1:
                    z[i] = z[k]
                else:
                    L = i
                    while R < n and s[R-L] == s[R]:
                        R += 1
                    z[i] = R-L
                    R -= 1  
            if z[i] + i == n:
                return s[:i]
        return ''

    @classmethod
    def preprocess_text(self, rfpath):
        EOS = '*'
        cnt = 0
        text = open(rfpath, 'r', encoding='UTF-8').readlines()
        text = sum(map(self.remove_punc, text), [])
        text = [line for line in text if line and line_entropy(line)>=1]
        text = [EOS + sent + EOS for sent in text]
        return text

    @classmethod
    def preprocess_danmu(self, rfpath):
        EOS = '*'
        cnt = 0
        text = open(rfpath, 'r', encoding='utf-8').readlines()
        num = len('2019-04-08 14:45:24,')
        res = []
        prev_line = ''
        rule = re.compile(r"[^a-zA-Z0-9\u4e00-\u9fa5]")
        for i, line in enumerate(text):
            line = rule.sub(' ', line[num:]).lower()
            if prev_line == line:
                continue
            prev_line = line
            line = [word for word in line.split() if word and line_entropy(word)>=1]
            res.extend(line)

        for i, word in enumerate(res):
            word_ = self.z_alg(word)
            if word_:
                res[i] = EOS + word_ + EOS
            else:
                res[i] = EOS + word + EOS
        return res

if __name__ =='__main__':
    text = Cleaner.preprocess_danmu("data/bilibili_txt/20181222_5_67235555.txt")
    print(text)