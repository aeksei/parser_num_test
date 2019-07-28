import re
import pymorphy2
from pymystem3 import Mystem
from word2num import get_numr, get_numb


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
        try:
            if 'NUMB' in pos_list:
                lemma[pos_list.index('NUMB')] = lemma[pos_list.index('NUMB')].replace(',', '.')
                num = get_numb(lemma[pos_list.index('NUMB'):])
            else:
                num = get_numr(lemma)
        except ValueError as e:
            print(e)

        return num


if __name__ == "__main__":
    parser = NumParser()
    print(parser.find_num('двадцать три хвоинки'))



