import spacy
from spacy.lang.en import English
import nltk
import ssl
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
import random
import pandas as pd
from gensim import corpora
import pickle
import gensim
from tqdm import tqdm
import os
from gensim import models

DOWNLOAD_WORDLISTS = False


def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            #lda_tokens.append('SCREEN_NAME')
            pass
        else:
            lda_tokens.append(token.lower_)

    return lda_tokens

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

def prepare_text_for_lda(text):
    text = str(text)
    tokens = tokenize(text)
    tokens = [token for token in tokens if len(token) > 4]
    tokens = [token for token in tokens if token not in en_stop]
    tokens = [get_lemma(token) for token in tokens]
    return tokens



if __name__=='__main__':

    if DOWNLOAD_WORDLISTS:
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        nltk.download()
        nltk.download('wordnet')
        nltk.download('stopwords')

    en_stop = set(nltk.corpus.stopwords.words('english'))
    spacy.load('en')
    parser = English()

    #here the magic begins
    dictionary = gensim.corpora.dictionary.Dictionary.load('dictionary.gensim')


    ldamodel = models.LdaModel.load('model5.gensim')
    topics = ldamodel.print_topics(num_words=1)
    for topic in topics:
        print(topic)

    dataset = 'data/twitter_dataset.csv'
    df_dataset = pd.read_csv(dataset, nrows = 15)

    tweets = df_dataset['text'].tolist()

    columns = list(df_dataset).append('topic')
    final_df = pd.DataFrame(columns=columns)

    from operator import itemgetter # serve per prendere il topic con il valore più alto

    for new_doc in tweets:
        print(f'TWEET: {new_doc}')
        new_doc = prepare_text_for_lda(new_doc)
        new_doc_bow = dictionary.doc2bow(new_doc)
        l = ldamodel.get_document_topics(new_doc_bow)
        print(l)
        topic = topics[max(l,key=itemgetter(1))[0]][1]
        print(topics[max(l,key=itemgetter(1))[0]][1])
