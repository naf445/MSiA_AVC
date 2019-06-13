# for all classes 
import logging
import logging.config
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from nltk.corpus import stopwords 
from nltk import pos_tag
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk.tokenize import word_tokenize
from nltk import pos_tag, word_tokenize
import nltk.chunk
import numpy as np
import os
import pandas as pd
import re
from sklearn.base import BaseEstimator, TransformerMixin



directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

logging.config.fileConfig(directory_abs_path+"/../../../config/logging_local.conf", disable_existing_loggers=False)
logger = logging.getLogger(__name__)


#Custom Transformer that tokenizes
class Tokenizer( BaseEstimator, TransformerMixin ):
    '''One of many transformers used to clean the plot summaries or generate features.

        This transformer simply tokenizes all of the plot summaries.

        Args:
            DF (pd.DataFrame): The booksummaries dataframe

        Returns: 
            pd.DataFrame: DF with tokenized plot summaries
    '''
         
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
    '''One of many transformers used to clean the plot summaries or generate features.

        This transformer filters all of the plot summaries to not include
        extraneous information like names, punctuation, etc...

        Args:
            DF (pd.DataFrame): The booksummaries dataframe
            filter_names (bool): Whether or not to filter out names from plot summaries

        Returns: 
            pd.DataFrame: DF with cleaned plot summaries
    '''
        
    #Class Constructor 
    def __init__( self, filter_names=True ):
        self.filter_names = filter_names        
        
    def filter_sentence(self, tokenized_sentence):
        filtered_sentence = [] 
        stop_words = set(stopwords.words('english')) 
        punctuation = ["?",":","!",".",",",";","-","`","'", "'", "(", ")", "'s", "'", "`", '''"''']
        names = pd.read_csv(directory_abs_path+'/../../../data/names/names.csv', header=None)
        names = names.values.tolist()
        names = [i[0].lower() for i in names]

        # filter out stop words, punctuation, common names, etc...
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
    '''One of many transformers used to clean the plot summaries or generate features.

        This transformer creates a word2vec vector which is the average of all
        the word2vec values for all of the words in the plot summary.

        Args:
            DF (pd.DataFrame): The booksummaries dataframe

        Returns: 
            pd.DataFrame: DF with word2vec features generated for each summary
    '''
         
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
            return list(np.mean(sentence2vec, axis=0))

        DF_2 = DF.copy(deep=True)
        DF_2['plotSum2vec'] = DF_2['plotSum'].apply(lambda row: meanWord2Vec(row, self.word2vec))
        
        return DF_2
    
    
#Custom Transformer that stems or lemmatizes
class StemmingLemming(BaseEstimator, TransformerMixin):
    '''One of many transformers used to clean the plot summaries or generate features.

        This transformer cleans the summaries by either stemming or lemmatization, depending
        on user input choice.

        Args:
            DF (pd.DataFrame): The booksummaries dataframe
            prune_type (string): Options are 'Porter', 'Lancaster', & 'Lemmatization'

        Returns: 
            pd.DataFrame: DF with plot summaries stemmed or lemmatized
    '''
        
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
    '''Simple transformer which joins tokenized plot summaries and returns data frame'''

    # Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    # Method that describes what we need this transformer to do
    def transform(self, DF, y = None):
        logger.info("Calling the Joiner transformer")
        DF_2 = DF.copy(deep=True)
        DF_2['plotSum'] = DF_2['plotSum'].apply(lambda row: ' '.join(row))
        return DF_2
    
# Custom Transformer that gets LDA scores
class LDA_Vectorizer( BaseEstimator, TransformerMixin ):
    '''One of many transformers used to clean the plot summaries or generate features.

        This transformer creates LDA features to be used by our RFC model from the summaries.

        Args:
            DF (pd.DataFrame): The booksummaries dataframe
            lda_model (sklearn lda object): Model used to generate LDA features
            tf_vect (sklearn count vectorizer object): Model used to get data in form for LDA

        Returns: 
            pd.DataFrame: DF with LDA features generated
    '''
         
    #Class Constructor 
    def __init__( self, lda_model, tf_vectorizer ):
        self.lda = lda_model
        self.tf_vectorizer = tf_vectorizer
        
    #Return self nothing else to do here    
    def fit( self, X, y = None ):
        return self 
    
    #Method that describes what we need this transformer to do
    def transform(self, DF, y = None):
        logger.info("Calling the LDA transformer")
        
        def getLDAScores(document, lda_model, tf_vect):
            document=[document]
            vectorized_doc = tf_vect.transform(document)
            return lda_model.transform(vectorized_doc).tolist()

        DF_2 = DF.copy(deep=True)
        DF_2['plotSumLDA'] = DF_2['plotSum'].apply(\
                    lambda row: getLDAScores(row, self.lda, self.tf_vectorizer) )
        
        return DF_2