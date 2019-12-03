# coding=gbk

""" hidden markov model """


class HMM:
    def __init__(self):
        import os
        self.model_file = './data/hmm_model.pkl'

        self.state_list = ['B', 'E', 'M', 'S']

        self.load_para = False

    def try_load_model(self, trained):
        if trained:
            import pickle
            with open(self.model_file, 'rb') as f:
                self.A_dic = pickle.load(f)
                self.B_dic = pickle.load(f)
                self.Pi_dic = pickle.load(f)
                self.load_para = True
        else:
            # ״̬ת�Ƹ���(״̬->״̬����������)
            self.A_dic = {}
            # �������(״̬->�������������)
            self.B_dic = {}
            # ״̬�ĳ�ʼ����
            self.Pi_dic = {}
            self.load_para = False

    def train(self, path):
        self.try_load_model(False)
        # ͳ��״̬���ִ���������P(o)
        count_dic = {}

        # ��ʼ������
        def init_para():
            for state in self.state_list:
                self.A_dic[state] = {s: 0.0 for s in self.state_list}
                self.Pi_dic[state] = 0.0
                self.B_dic[state] = {}
                count_dic[state] = 0
        def makeLabel(text):
            out_text = []
            if len(text) == 1:
                out_text.append('S')
            else:
                out_text += ['B'] + ['M'] * (len(text) - 2) + ['E']
            return out_text
        init_para()
        line_num = -1
        words = set()
        with open(path, encoding='utf8') as f:
            for line in f:
                line_num += 1

                line = line.strip("\n")
                if not line:
                    continue
                word_list = [i for i in line if i != '']
                words |= set(word_list)

                line_list = line.split()
                line_state = []

                for w in line_list:
                    line_state.extend(makeLabel(w)) # �����дʽ��������label

                for k, v in enumerate(line_state):
                    count_dic[v] += 1
                    if k == 0:
                        self.Pi_dic[v] += 1  # ÿ�����ӵĵ�һ���ֵ�״̬�����ڼ����ʼ״̬����
                    else:
                        self.A_dic[line_state[k - 1]][v] += 1
                        self.B_dic[line_state[k]][word_list[k]] = self.B_dic[line_state[k]].get(word_list[k], 0) + 1
        self.Pi_dic = {k: v * 1.0 / line_num for k, v in self.Pi_dic.items()}
        self.A_dic = {k: {k1: v1 / count_dic[k] for k1, v1 in v.items()} for k, v in self.A_dic.items()}  # ״̬ת�ƾ���˫�ֵ�
        self.B_dic = {k: {k1: (v1 + 1) / count_dic[k] for k1, v1 in v.items()} for k, v in self.B_dic.items()}

        import pickle
        with open(self.model_file, 'wb') as f:
            pickle.dump(self.A_dic, f)
            pickle.dump(self.B_dic, f)
            pickle.dump(self.Pi_dic, f)

        return self

    def viterbi(self, text, states, start_p, trans_p, emit_p):  # �ֲ����ſ����Ƴ�ȫ������
        V = [{}]
        path = {}
        for y in states:
            V[0][y] = start_p[y] * emit_p[y].get(text[0], 0)
            path[y] = [y]
        for t in range(1, len(text)):
            V.append({})
            newpath = {}

            # ����ѵ���ķ�����ʾ������Ƿ��и���
            neverSeen = text[t] not in emit_p['S'].keys() and text[t] not in emit_p['M'].keys() and text[t] not in emit_p['E'].keys() and text[t] not in emit_p['B'].keys()
            for y in states:
                emitP = emit_p[y].get(text[t], 0) if not neverSeen else 1.0
                (prob, state) = max([(V[t - 1][y0] * trans_p[y0].get(y, 0) * emitP, y0) for y0 in states if V[t - 1][y0] > 0])  # ά�ر��㷨����̬�滮������ת�Ƹ��ʡ��������
                V[t][y] = prob
                newpath[y] = path[state] + [y]
            path = newpath
        if emit_p['M'].get(text[-1], 0) > emit_p['S'].get(text[-1], 0):
            (prob, state) = max([(V[len(text) - 1][y], y) for y in ('E', 'M')])
        else:
            (prob, state) = max([(V[len(text) - 1][y], y) for y in states])
        return (prob, path[state])

    def cut(self, text):
        import os
        if not self.load_para:
            self.try_load_model(os.path.exists(self.model_file))
        prob, pos_list = self.viterbi(text, self.state_list, self.Pi_dic, self.A_dic, self.B_dic)
        begin, next = 0, 0
        for i, char in enumerate(text):
            pos = pos_list[i]
            if pos == 'B':
                begin = i
            elif pos == 'E':
                yield text[begin: i + 1]
                next = i + 1
            elif pos == 'S':
                yield char
                next = i + 1
        if next < len(text):
            yield text[next:]
if __name__ == '__main__':
    hmm = HMM()
    hmm.train('./data/trainCorpus.txt_utf8')

    text = '�дʵĳ�������'
    res = hmm.cut(text)
    print(text)
    print(str(list(res)))