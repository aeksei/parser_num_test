import ssl
import re
import pymorphy2
from pymystem3 import Mystem
from word2num import get_numr, get_numb
from num_dict import rank

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
        return [l for l in self.mystem.lemmatize(text) if l != ' ']

    def get_morph(self, lemma):
        return [self.morph.parse(token) for token in lemma]

    def get_pos_tags(self, morph):
        pos_list = []
        for morph_token in morph:
            pos = morph_token[0].tag.POS
            if pos is None:
                pos = str(morph_token[0].tag)[:4]
            pos_list.append(str(pos))
        return pos_list[:-1]

    def chunking_numr(self, lemma):
        pattern = r'((NUMR)?(NUMR)?(NOUN)?(NUMR)?(NUMR)?(NUMR)|(ADJF))+(NOUN)?'
        pos_tag = self.get_pos_tags(self.get_morph(lemma))
        match = re.search(pattern, "".join(pos_tag))
        if match is not None:
            return lemma[match.start(0) // 4: match.end(0) // 4]
        else:
            return []

    def find_num(self, text):
        num = None
        lemma = self.get_lemma(text)
        pos_list = self.get_pos_tags(self.get_morph(lemma))
        if 'NUMR' in pos_list:
            # word_num = parser.chunking_numr()
            num = get_numr(lemma)
        elif 'NUMB' in pos_list:
            lemma[pos_list.index('NUMB')] = float(lemma[pos_list.index('NUMB')].replace(',', '.'))
            num = get_numb(lemma[pos_list.index('NUMB'):])
        else:
            replace = False
            for i, l in enumerate(lemma):
                if lemma[i] in rank:
                    replace = True
                    lemma[i] = rank[lemma[i]][0]
                    pos_list[i] = 'NUMB'
                    break
            if replace:
                num = get_numb(lemma[pos_list.index('NUMB'):])

        return num


if __name__ == "__main__":
    parser = NumParser()
    parser.find_num('первый')

    file = 'text.txt'
    with open(file, 'r') as f:
        for line in f:
            print(line[:-1])
            print(parser.find_num(line))



