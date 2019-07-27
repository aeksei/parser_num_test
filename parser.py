import ssl
import re
import pymorphy2
from pymystem3 import Mystem
from word2num import get_num

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context


class NumParser:
    def __init__(self):
        self.mystem = Mystem()
        self.morph = pymorphy2.MorphAnalyzer()

    def get_lemma(self, text):
        return self.mystem.lemmatize(text)

    def get_morph(self, lemma):
        return [self.morph.parse(token) for token in lemma if token != ' ']

    def get_pos_tags(self, morph):
        pos_list = []
        for morph_token in morph:
            pos = morph_token[0].tag.POS
            if pos is None:
                pos = str(morph_token[0].tag)[:4]
            pos_list.append(pos)
        return pos_list[:-1]

    def chunking_num(self, lemma):
        lemma = [l for l in lemma if l != ' ']
        pattern = r'((NUMR)?(NUMR)?(NOUN)?(NUMR)?(NUMR)?(NUMR)|(ADJF))+'
        pos_tag = self.get_pos_tags(self.get_morph(lemma))
        match = re.search(pattern, "".join(pos_tag))
        if match is not None:
            return lemma[match.start(0) // 4: match.end(0) // 4]
        else:
            return []

    def find_num(self, text):
        lemma = parser.get_lemma(text)
        num = None
        word_num = parser.chunking_num(lemma)
        num = get_num(word_num)
        return word_num, num


if __name__ == "__main__":
    parser = NumParser()

    file = 'text.txt'
    with open(file, 'r') as f:
        for line in f:
            # TODO clear punct and stop words and space
            print(line[:-1])
            print(parser.find_num(line))
            """
                for p in morph_token:
                    if 'NUMR' in p.tag:
                        print('norm_form: {}'.format(p.normal_form))
                    break
                """
            """
            sentence = mystem.lemmatize(line)[:-1]
            for token in sentence:
                for p in morph.parse(token):
                    if 'NUMR' in p.tag:
                        print('norm_form: {}'.format(p.normal_form))
                    break
            """


