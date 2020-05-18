import json
import numpy as np
sin_count = {}  #单个字出现次数{str:int}
dou_count = {}  #二元组出现次数{str:{str:int}}
fir_fre = {}  #出现在句首的字频率对数{str:float} viterbi算法中概率乘转换为对数加
new_pinyin = {}  #拼音表
sin_total = 1509420

def load():
    global new_pinyin
    global sin_count
    global dou_count
    global fir_fre
    with open('./data/new_pinyin.txt', encoding="utf-8") as f:
        new_pinyin = eval(f.read())
    with open('./data/dou_count.json', encoding="utf-8") as f:
        dou_count = json.load(fp=f)
    with open('./data/sin_count.txt', encoding="utf-8") as f:
        sin_count = eval(f.read())
    with open('./data/fir_fre.txt', encoding="utf-8") as f:
        fir_fre = eval(f.read())

"""
二元节点
ch_code:汉字
pr:概率
prev：前驱
"""
class node():
    def __init__(self, ch_code, pr, prev):
        self.ch_code = ch_code
        self.pr = pr
        self.prev = prev

"""
返回二元概率，利用lam做平滑处理
"""
def getpr(ch1, ch2, lam):
    temp = {}
    double_count = dou_count.get(ch1, temp).get(ch2, 0)
    single_one = sin_count.get(ch1, 0)
    if single_one > 0:
        single_two = sin_count.get(ch2, 0)
        res = np.log(lam * double_count / single_one +
                     (1 - lam) * single_two / sin_total)
    else:
        res = -50
    return res


def viterbi(pinyin_list, lam=0.8):
    for py in pinyin_list:
        if py not in new_pinyin:
            return ['error']
    nodes = []
    #第一个节点
    nodes.append([node(ch_code, fir_fre.get(ch_code, -25.0), None) for ch_code in new_pinyin[pinyin_list[0]]])
    for i in range(len(pinyin_list)):
        #从第二个开始
        if i == 0:
            continue
        nodes.append([node(ch_code, 0, None)for ch_code in new_pinyin[pinyin_list[i]]])
        for n in nodes[i]:
            n.pr = nodes[i - 1][0].pr + getpr(nodes[i - 1][0].ch_code,
                                              n.ch_code, lam)
            n.prev = nodes[i - 1][0]
            for pren in nodes[i - 1]:
                #用最大的概率更新
                if pren.pr + getpr(pren.ch_code, n.ch_code, lam) > n.pr:
                    n.pr = pren.pr + getpr(pren.ch_code, n.ch_code, lam)
                    n.prev = pren

    #回溯路径
    ans=nodes[-1]
    ans.sort(key=lambda x: x.pr,reverse=True)
    sentense = []
    for biggest_node in ans:
        temp=''
        while biggest_node is not None:
            temp+=biggest_node.ch_code
            biggest_node=biggest_node.prev
        sentense.append(temp[::-1])
    return sentense

"""
返回输入str的可能输出列表
"""
def pinyin2hanzi(str,lam):
    return viterbi(str.lower().split(),lam)
#
# load()
# pinyin_list="ai"
# ans=pinyin2hanzi(pinyin_list,0.9)
# print(ans)


