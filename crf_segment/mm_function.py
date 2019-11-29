# coding:gbk
""" ����ƥ���㷨 """

class MM:
    def __init__(self):
        self.MATCHLEN = 4
    def cut(self, text):
        result = []
        dic = ['�ϵ�ʮ��', '10��', '�ٶȴ���', '������', '�Ͼ���', '��������', '�Ͼ��г�', '������']

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
    print(MM().cut("�����к������ϵ�ʮ��10�Űٶȴ���"))
    print(MM().cut("�Ͼ��г�������"))