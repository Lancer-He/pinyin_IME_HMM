import viterbi

class Solver():
    def __init__(self):
        viterbi.load()
        self.sin_count = viterbi.sin_count #单个字出现次数{str:int}
        self.dou_count = viterbi.dou_count  #二元组出现次数{str:{str:int}}
        self.fir_fre = viterbi.fir_fre  #出现在句首的字频率对数{str:float} viterbi算法中概率乘转换为对数加
        self.new_pinyin = viterbi.new_pinyin #拼音表
        self.sin_total=1509420

    def solve(self,str):
        singal=str.split()
        ans=[]
        if len(singal)>1:
            temp=viterbi.pinyin2hanzi(str,0.9)
            if temp is not None:
                ans+=temp[:10]
            for word in singal:
                temp=viterbi.pinyin2hanzi(word,0.9)
                if temp is not None:
                    ans += temp
        elif len(singal)==1:
            temp = viterbi.pinyin2hanzi(str,0.9)
            if temp is not None:
                ans += temp

        return ans

# a=Solver()
# ans=a.solve("xiang dui lun")
# print(ans)