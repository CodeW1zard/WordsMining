import numpy as np
from collections import Counter

def line_entropy(line):
    counter = Counter(line)
    nums = np.array(list(counter.values()))
    return entropy(nums)

def entropy(x):
    N = np.sum(x)
    return np.log2(N) - np.sum(x * np.log2(x)) / N


def cal_pmi(candidate, len_dict, seg_index, triTree):
    left_, right_ = candidate[:seg_index], candidate[seg_index:]
    total_num, left_num, right_num = len_dict[len(candidate)], len_dict[len(left_)], len_dict[len(right_)]
    freq_total = triTree.search(candidate).count
    freq_word1 = triTree.search(left_).count
    freq_word2 = triTree.search(right_).count

    return np.log2((freq_total / total_num) / (freq_word1 / left_num * freq_word2 / right_num))


def calculate_entropy(candidate, TriTree, return_count=True):
    '''
    对于candidate
    计算左右两侧的信息熵
    例如 “单词”左边可能出现了['背':3， '读':1, '记':10],以此计算熵h_l，熵越小，越有可能与左侧成词
    '''
    node = TriTree.search(candidate)
    entropy = node.entropy
    if return_count:
        return entropy, node.count
    else:
        return entropy
