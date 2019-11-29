# coding:gbk
""" 逆向匹配算法 """

from mm_function import MM

class RMM:
    def __init__(self):
        self.MATCHLEN = 4
    def cut(self, text):
        result = []
        dic = ['上地十街', '10号', '百度大厦', '海淀区', '南京市', '长江大桥', '南京市长', '江大桥']

        len_text = len(text)
        index = len_text - 1

        while index > 0:
            for i in range(index - self.MATCHLEN + 1, index + 1, 1):
                local_text = text[i:index + 1]
                if local_text in dic:
                    index = i
                    break
            index -= 1
            result.append(local_text + "---")
        return result


if __name__ == "__main__":
    print(RMM().cut("北京市海淀区上地十街10号百度大厦"))
    print("正向匹配算法")
    print(MM().cut("南京市长江大桥"))
    print("逆向匹配算法")
    print(RMM().cut("南京市长江大桥"))