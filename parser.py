import nltk
import ssl
from pymystem3 import Mystem


try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('punkt')
nltk.download("stopwords")

# Create lemmatizer and stopwords list
mystem = Mystem()

if __name__ == "__main__":
    file = 'text.txt'
    with open(file, 'r') as f:
        for line in f:
            # TODO clear punct and stop words and space
            sentence = mystem.lemmatize(line)[:-1]
            for token in sentence:
                analysis = mystem.analyze(token)[0].get('analysis')
                if analysis and analysis is not None:
                    if 'NUM' in analysis[0].get('gr'):
                        print(token)