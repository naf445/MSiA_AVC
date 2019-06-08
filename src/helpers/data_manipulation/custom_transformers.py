# for all classes 
from sklearn.base import BaseEstimator, TransformerMixin

# for class Tokenizer
from nltk.tokenize import word_tokenize
from nltk import pos_tag, word_tokenize
import nltk.chunk

# for class Filter_sentence
import pandas as pd
import numpy as np
from nltk.corpus import stopwords 

# for class StemmingLemming
from nltk import pos_tag
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
import os
import re

import logging
import logging.config

directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

logging.config.fileConfig(directory_abs_path+"/../../../config/logging_local.conf")
logger = logging.getLogger(__name__)

#Custom Transformer that tokenizes
class Tokenizer( BaseEstimator, TransformerMixin ):
         
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    #Method that describes what we need this transformer to do
    def transform(self, DF, y = None):
        logger.info("Calling the Tokenizer transformer")
        DF_2 = DF.copy(deep=True)
        DF_2['plotSum'] = DF_2['plotSum'].apply(lambda row: word_tokenize(row))
        return DF_2
    
    
#Custom Transformer that filters a sentence
class Filter_sentence( BaseEstimator, TransformerMixin ):
        
    #Class Constructor 
    def __init__( self, filter_names=False ):
        self.filter_names = filter_names        
        
    def filter_sentence(self, tokenized_sentence):
        filtered_sentence = [] 
        stop_words = set(stopwords.words('english')) 
        punctuation= ["?",":","!",".",",",";","-","`","'", "'", "(", ")", "'s", "'", "`", '''"''']
        names = pd.read_csv(directory_abs_path+'/../../../data/names/names.csv', header=None)
        names = names.values.tolist()
        names = [i[0].lower() for i in names]

        for w in tokenized_sentence: 
            w = w.lower()
            w = re.sub(r'\d+', '', w)
            if w not in stop_words:
                if w not in punctuation: 
                    if self.filter_names:
                        if w not in names:
                            filtered_sentence.append(w.replace('-','').strip())
                    else:
                        filtered_sentence.append(w.replace('-','').strip())
        return filtered_sentence
        
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    #Method that describes what we need this transformer to do
    def transform( self, DF, y = None ):
        logger.info("Calling the filter sentence transformer")
        DF_2 = DF.copy(deep=True)
        DF_2['plotSum'] = DF_2['plotSum'].apply(lambda row: self.filter_sentence(row))
        return DF_2
 
# Custom Transformer that MeanEmbeddingVectorizes
class MeanEmbeddingVectorizer( BaseEstimator, TransformerMixin ):
         
    #Class Constructor 
    def __init__( self, word2vecModel ):
        self.word2vec = word2vecModel
        
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    #Method that describes what we need this transformer to do
    def transform(self, DF, y = None):
        
        def meanWord2Vec(tokenized_sentence, word2vecModel):
            sentence2vec = [] 
            for word in tokenized_sentence:
                try:
                    sentence2vec.append(word2vecModel.get_vector(word))
                except:
                    sentence2vec.append(np.zeros(50))
            sentence2vec = np.array(sentence2vec)
            return np.mean(sentence2vec, axis=0)

        DF_2 = DF.copy(deep=True)
        DF_2['plotSum2vec'] = DF_2['plotSum'].apply(lambda row: meanWord2Vec(row, self.word2vec))
        
        return DF_2
    
    
#Custom Transformer that stems or lemmatizes
class StemmingLemming(BaseEstimator, TransformerMixin):
        
    #Class Constructor 
    def __init__(self, prune_type="Porter"):
        self.prune_type = prune_type        
        
    def get_wordnet_pos(self, word):
        """Map POS tag to first character lemmatize() accepts"""
        tag = pos_tag([word])[0][1][0].upper()
        tag_dict = {"J": wordnet.ADJ,
                    "N": wordnet.NOUN,
                    "V": wordnet.VERB,
                    "R": wordnet.ADV}

        return tag_dict.get(tag, wordnet.NOUN) 
    
    def stemLem_sentence(self, sentence):
        stemLemmed_sentence = []
        for word in sentence:
            if word:
                if self.prune_type == "Porter":
                    stemLemmed_sentence.append(PorterStemmer().stem(word))
                elif self.prune_type == "Lancaster":
                    stemLemmed_sentence.append(LancasterStemmer().stem(word))
                elif self.prune_type == "Lemmatization":
                    stemLemmed_sentence.append(WordNetLemmatizer().lemmatize(word,\
                                                        self.get_wordnet_pos(word)))
        return stemLemmed_sentence
        
    #Return self nothing else to do here    
    def fit(self, X, y = None):
        return self 
    
    #Method that describes what we need this transformer to do
    def transform(self, DF, y = None):
        logger.info("Calling the StemmingLemming transformer")
        DF_2 = DF.copy(deep=True)
        DF_2['plotSum'] = DF_2['plotSum'].apply(lambda row: self.stemLem_sentence(row))
        return DF_2
    
    
#Custom Transformer that joins
class Joiner( BaseEstimator, TransformerMixin ):
         
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    #Method that describes what we need this transformer to do
    def transform(self, DF, y = None):
        logger.info("Calling the Joiner transformer")
        DF_2 = DF.copy(deep=True)
        DF_2['plotSum'] = DF_2['plotSum'].apply(lambda row: ' '.join(row))
        return DF_2