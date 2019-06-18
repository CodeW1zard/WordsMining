import os
import sys
import multiprocessing
import pandas as pd

from time import time
from Extractor import Extractor
from Cleaner import Cleaner

RFDIR = 'data/bilibili_txt/'
WFDIR = 'data/bilibili_daily_txt/'
OFDIR = 'out/bilibili_daily_words/'
if not os.path.isdir(WFDIR):
    os.makedirs(WFDIR)
if not os.path.isdir(OFDIR):
    os.makedirs(OFDIR)

max_len = 10
thresh = 5.0


def info(fname):
    date, rank, cid = fname.split('.')[0].split('_')
    rank = int(rank)
    return date, rank, cid, fname

def extract(item):
    date, text = item
    extractor = Extractor(text=text, max_len=max_len)
    words = extractor.extract_words(thresh=thresh)
    words['date'] = date
    return words, date

def write(wfpath, text):
    with open(wfpath, 'w') as wf:
        for line in text:
            wf.write(line + '\n')

def read(rfpath):
    with open(rfpath, 'r') as rf:
        text = rf.readlines()
    return text

if __name__ == "__main__":
    '''
    预处理 并保存
    '''
    files = os.listdir(RFDIR)
    fdf = list(map(info, files))
    fdf = pd.DataFrame(data=fdf, columns=['date', 'rank', 'cid', 'fname']).sort_values(['date', 'rank'])
    fdf = fdf[fdf['rank'] <= 15]
    fdf['fpath'] = fdf.apply(lambda x:os.path.join(RFDIR, x['fname']), axis=1)
    texts = dict()
    for i, (date, frame) in enumerate(fdf.groupby('date')['fpath']):
        text = []
        for fpath in frame:
            text.extend(Cleaner.preprocess_danmu(fpath))
        write(os.path.join(WFDIR, date+'_danmu.txt'), text)
        texts[date] = text
        sys.stdout.write('preprocess done %d/%d\r' %(i, len(fdf.date.unique().size)))

    # '''
    # 预处理后，可直接读取
    # '''
    # texts = dict()
    # files = os.listdir(WFDIR)
    # for f in tqdm(files):
    #     fpath = os.path.join(WFDIR, f)
    #     date = f.split('_')[0]
    #     text = read(fpath)
    #     texts[date] = text

    ####################################################
    # cores = multiprocessing.cpu_count() # 4 danger!!!
    # pool = multiprocessing.Pool(processes=cores)
    ####################################################

    # tic = time()
    # cnt = 1
    # for result in pool.imap_unordered(extract, texts.items()):
    #     words, date = result
    #     sys.stdout.write('done %d/%d\r' % (cnt, len(texts)))
    #     words.to_csv(os.path.join(OFDIR, date+".xlsx"), index=False, encoding="utf_8_sig")
    #     cnt += 1
    # print("extract done %.2f"%(time() - tic))