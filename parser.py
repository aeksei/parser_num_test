import nltk
import ssl
import pymorphy2
from pymystem3 import Mystem

from num_dict import nums


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download("stopwords")


# Create lemmatizer and stopwords list



class NumParser:
    def __init__(self):
        self.mystem = Mystem()
        self.morph = pymorphy2.MorphAnalyzer()

    def get_lemma(self, text):
        return self.mystem.lemmatize(text)


if __name__ == "__main__":
    file = 'text.txt'
    with open(file, 'r') as f:
        for line in f:
            # TODO clear punct and stop words and space
            sentence = mystem.lemmatize(line)[:-1]
            for token in sentence:
                for p in morph.parse(token):
                    if 'NUMR' in p.tag:
                        print('norm_form: {}'.format(p.normal_form))
                    break

    print(len(nums))
