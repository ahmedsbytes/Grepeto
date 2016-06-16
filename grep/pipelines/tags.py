from tagger


class TagsMakerPipeline(object):
    def process_item(item, spider):
        weights = pickle.load(open('data/dict.pkl', 'rb'))  # or your own dictionary
        myreader = tagger.Reader()  # or your own reader class
        mystemmer = tagger.Stemmer()  # or your own stemmer class
        myrater = tagger.Rater(weights)  # or your own... (you got the idea)
        mytagger = Tagger(myreader, mystemmer, myrater)
        best_3_tags = mytagger(text_string, 3)
        return item