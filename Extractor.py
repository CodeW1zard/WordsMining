import sys
import pandas as pd
import numpy as np
from time import time

from Trie import Trie
from Cleaner import Cleaner
from Entropy import calculate_entropy, cal_pmi


class Extractor(object):

    def __init__(self, rfpath=None, text=None, max_len=4):
        self.prefixTree = Trie()
        self.suffixTree = Trie(direction='suffix')

        self.vocabulary = []
        self.len_dict = dict()
        # 想要计n个字的词必须用n+1-gram
        self.max_len = max_len + 1

        if rfpath is not None:
            text = Cleaner.preprocess_text(rfpath)
        elif text is None:
            raise ValueError()

        self.buildTreesAndDics(text)
        self.prefixTree.set_entropy()
        self.suffixTree.set_entropy()

        self.words = dict()

    def buildTreesAndDics(self, text):
        tic = time()

        for i in range(self.max_len):
            n_gram_list = sum(
                map(lambda x: Cleaner.n_gram(x, i + 1), text), [])
            self.len_dict[i + 1] = len(n_gram_list)
            if i >= 1:
                self.vocabulary.extend(list(set(n_gram_list)))
            for word in n_gram_list:
                self.prefixTree.insert(word, i + 1)
                self.suffixTree.insert(word, i + 1)
            sys.stdout.write('build tree done %d/%d\r' % (i, self.max_len))

    def score(self, candidate, cnt_thresh):
        '''
        淘宝
        h_r_l:宝的左信息熵
        h_l_r:淘的右信息熵
        '''
        children = set()
        h_l, count = calculate_entropy(
            candidate, self.prefixTree, return_count=True)
        if count < cnt_thresh:
            return count, None, None

        h_r = calculate_entropy(candidate, self.suffixTree, return_count=False)
        min_score = -np.inf
        for seg_index in range(1, len(candidate)):
            left_candidate = candidate[:seg_index]
            right_candidate = candidate[seg_index:]

            if left_candidate in self.words:
                children.add(left_candidate)
            if right_candidate in self.words:
                children.add(right_candidate)

            h_r_l = calculate_entropy(
                right_candidate, self.prefixTree, return_count=False)
            h_l_r = calculate_entropy(
                left_candidate, self.suffixTree, return_count=False)
            pmi = cal_pmi(candidate, self.len_dict, seg_index, self.suffixTree)
            score = pmi - min(h_l_r, h_r_l)
            if score > min_score:
                min_score = score
                

        if h_l == 0 or h_r == 0:
            return count, 0, 0

        min_score += min(h_l, h_r)

        for child in children:
            # 出现次数大于等于子段，选长的
            if min_score > self.words[child]['score']:
                del self.words[child]
        return count, min_score, min_score * count

    def extract_words(self, score_thresh=4.0, cnt_thresh=20):
        # calculate PMI and freq remove dict words
        for i, word in enumerate(self.vocabulary):
            res = self.score(word, cnt_thresh)
            count, score, final = res
            if score is None or score < score_thresh:
                continue
            self.words[word] = {"candidate": word,
                                "count": count, "score": score, "final": final}
            sys.stdout.write('extract words done %d/%d\r' %(i, len(self.vocabulary)))
        words = pd.DataFrame.from_dict(list(self.words.values())).sort_values("final", ascending=False).reset_index(drop=True)
        return words
