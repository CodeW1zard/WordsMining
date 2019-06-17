import argparse
from os.path import join
from time import time
from Extractor import Extractor


RFDIR = "data/"
WFDIR = "out/"

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--fname", required=True, type=str, dest='fname')
parser.add_argument("-o", "--oname", required=False,
                    default=None, type=str, dest='oname')
parser.add_argument("--thresh", required=False,
                    default=4.0, type=float, dest='thresh')
parser.add_argument("--count", required=False,
                    default=20, type=int, dest='count')                    
parser.add_argument("-n", "--ngram", required=False,
                    default=8, type=int, dest='ngram')
parser.add_argument("--save", required=False,
                    default=False, type=bool, dest='save')
parser.add_argument("--preprocess", required=False,
                    default=False, type=bool, dest='preprocess')

if __name__ == '__main__':
    tic = time()
    args = parser.parse_args()
    rfpath = join(RFDIR, args.fname)
    if not args.preprocess:
        text = open(rfpath, "r").readlines()[:5000]
        extracter = Extractor(text=text, max_len=args.ngram)
    else:
        extracter = Extractor(rfpath=rfpath, max_len=args.ngram)
    words = extracter.extract_words(score_thresh=args.thresh, cnt_thresh=args.count)
    if args.save:
        if args.oname:
            opath = join(WFDIR, args.oname)
            words.to_csv(opath, encoding="utf_8_sig", index=False, sep='\t')
        else:
            opath = join(WFDIR, args.fname)
            words.to_csv(opath, encoding="utf_8_sig", index=False, sep='\t')
    print(words)
    toc = time()
    print("Total time: %.2fs" % (toc - tic))