from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.kl import KLSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"
SENTENCES_COUNT = 7


class GrepSummarizer(object):
    def __init__(self):
        pass

    def process_item(self, item, spider):
        # pickle_path = os.path.dirname(os.path.realpath(__file__))+'/../../nltk_data/tokenizers/punkt/english.pickle'
        # tokenizer = nltk.data.load(pickle_path)

        parser = PlaintextParser.from_string(item['content'], Tokenizer(LANGUAGE))
        stemmer = Stemmer(LANGUAGE)
        summarizer = Summarizer(stemmer)
        summarizer.stop_words = get_stop_words(LANGUAGE)

        item['summary'] = ''
        for sentence in summarizer(parser.document, SENTENCES_COUNT):
            item['summary'] += ' ' + sentence._text
        return item
