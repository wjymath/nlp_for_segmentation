# coding:gbk
""" ����ƥ���㷨 """

from mm_function import MM

class RMM:
    def __init__(self):
        self.MATCHLEN = 4
    def cut(self, text):
        result = []
        dic = ['�ϵ�ʮ��', '10��', '�ٶȴ���', '������', '�Ͼ���', '��������', '�Ͼ��г�', '������']

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
    print(RMM().cut("�����к������ϵ�ʮ��10�Űٶȴ���"))
    print("����ƥ���㷨")
    print(MM().cut("�Ͼ��г�������"))
    print("����ƥ���㷨")
    print(RMM().cut("�Ͼ��г�������"))