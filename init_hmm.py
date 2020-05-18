import re
import json
import numpy as np

# encoding=utf-8
sin_count = {}  #单个字出现次数{str:int}
dou_count = {}  #二元组出现次数{str:{str:int}}
fir_fre = {}  #出现在句首的字频率对数{str:float} viterbi算法中概率乘转换为对数加
sin_total = 1509420


def preload_sentences():
    path = './data/pinyin_train.txt'
    out = open('./data/temp.txt', 'w', encoding="utf-8")
    with open(path, encoding="utf-8") as f:
        for line in f.readlines():
            pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|' \
                      r'\(|\)|-|=|\_|\+|，|。|、|；|‘|’|' \
                      r'【|】|·|！| |…|（|）|：|？|!|“|”|【|】|『|』|{|}|《|》|「|」'
            segs = [x for x in re.split(pattern, line) if len(x) > 1]
            for s in segs:
                out.write(s + '\n')


"""处理上个函数的语料，消除空行"""
def deal_space():
    path = './data/temp.txt'
    out = open('./data/sentence.txt', 'w', encoding="utf-8")
    with open(path, encoding="utf-8") as f:
        for line in f.readlines():
            if line.split():
                out.write(line)



"""处理单个字、二元组、拼音并保存"""
def pre_load():
    def addone(dict, key):
        if key in dict:
            dict[key] += 1
        else:
            dict[key] = 1

    def addtwo(dict, ch1, ch2):
        if ch1 in dict:
            d = dict[ch1]
            if ch2 in d:
                d[ch2] += 1
            else:
                d[ch2] = 1
        else:
            dict[ch1] = {ch2: 1}

    fir_count = {}  #句首字
    fir_total = 0
    with open('./data/sentence.txt', 'r', encoding="utf-8") as f:
        for line in f.readlines():
            addone(fir_count, line[0])
            fir_total += 1
            for hanzi in line:
                if hanzi != '\n':
                    addone(sin_count, hanzi)
            for i in range(len(line) - 2):
                addtwo(dou_count, line[i], line[i + 1])
    for hanzi in fir_count:
        fir_fre[hanzi] = np.log(1.0 * fir_count[hanzi] / fir_total)
    pinyin = {}
    with open('./data/pinyin.txt', 'r', encoding="utf-8") as f:
        out = open('./data/new_pinyin.txt', 'w', encoding="utf-8")
        for line in f.readlines():
            x = line.split(':')
            t = []
            for word in x[1]:
                if word != '\n':
                    t.append(word)
            pinyin[str(x[0])] = t
        out.write(str(pinyin))
    with open('./data/fir_fre.txt', 'w', encoding="utf-8") as f:
        f.write(str(fir_fre))
    with open('./data/sin_count.txt', 'w', encoding="utf-8") as f:
        f.write(str(sin_count))
    with open('./data/dou_count.pkl', 'w', encoding="utf-8") as f:
        json.dump(dou_count, f)

if __name__=='__main__':
    preload_sentences()
    deal_space()
    pre_load()
