import re

def write(wfpath, text):
    with open(wfpath, 'w') as wf:
        for line in text:
            wf.write(line + '\n')

def read(rfpath):
    with open(rfpath, 'r') as rf:
        text = rf.readlines()
    return text

if __name__ =="__main__":
    book = read("data/xiyouji_wuchengen.txt")
    sections = re.split("*字卷之[一二三四五六七八九十]+")