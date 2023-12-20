import nltk
import pandas as pd
import ast
import re
import numpy as np

import string 
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import nltk
#nltk.download('wordnet')

import unidecode
import nltk.corpus
from gensim.models import Word2Vec

from gensim.models import Word2Vec
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from collections import defaultdict
import config

def ingredient_parser(ingredients):
    # measures and common words (already lemmatized)   
    measures = ['teaspoon', 't', 'tsp.', 'tablespoon', 'T', ...]
    words_to_remove = ['fresh', 'a', 'red', 'bunch', ...]
    # Turn ingredient list from string into a list 
    if isinstance(ingredients, list):
       pass
    else:
       ingredients = ast.literal_eval(ingredients)
    # We first get rid of all the punctuation
    remove_punctuations = str.maketrans('', '', string.punctuation)
    # initialize nltk's lemmatizer    
    lemmatizer = WordNetLemmatizer()
    ingred_list = []
    for each_item in ingredients:
        each_item.translate(remove_punctuations)
        # We split up with hyphens as well as spaces
        items = re.split(' |-', each_item)
        # Get rid of words containing non alphabet letters
        items = [word for word in items if word.isalpha()]
        # Turn everything to lowercase
        items = [word.lower() for word in items]
        # remove accents
        items = [unidecode.unidecode(word) for word in items]
        # Lemmatize words so we can compare words to measuring words
        items = [lemmatizer.lemmatize(word) for word in items]
        # get rid of stop words
        stop_words = set(nltk.corpus.stopwords.words('english'))
        items = [word for word in items if word not in stop_words]
        # Gets rid of measuring words/phrases, e.g. heaped teaspoon
        items = [word for word in items if word not in measures]
        # Get rid of common easy words
        items = [word for word in items if word not in words_to_remove]
        if items:
           ingred_list.append(' '.join(items))
    return ingred_list
