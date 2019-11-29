# coding:gbk
""" 正向匹配算法 """

class MM:
    def __init__(self):
        self.MATCHLEN = 4
    def cut(self, text):
        result = []
        dic = ['上地十街', '10号', '百度大厦', '海淀区', '南京市', '长江大桥', '南京市长', '江大桥']

        index = 0
        len_text = len(text)

        while len_text > index:
            for i in range(self.MATCHLEN + index, index, -1):
                local_text = text[index:i]
                if local_text in dic:
                    index = i - 1
                    break
            index += 1
            result.append(local_text + "---")
        return result

if __name__ == "__main__":
    print(MM().cut("北京市海淀区上地十街10号百度大厦"))
    print(MM().cut("南京市长江大桥"))