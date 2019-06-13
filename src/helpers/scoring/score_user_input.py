import pandas as pd
import numpy as np
import os
import logging
import logging.config
import sys; sys.path.append('../')
from data_manipulation import custom_transformers as ct
import yaml
from sklearn.pipeline import Pipeline 
import ast
import csv

directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../../../config/src_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)
config = config['helpers']['scoring']['score_user_input']

logging.config.fileConfig(directory_abs_path+config['logger_config'], disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def score_model(user_input, word2vec_model, tf_vect, lda_model, RFC_model):
    '''Returns predictions using my RFC deployed model given a user input plot summery.

        This function is used in our web app to give back model results for our user input
        plot summary. It gives the list of possible genres as well as an associated
        probability for each of those genres based on the RFC model. It first takes the user 
        input and transforms it to have the correct form, and then applies our models.

        Args:
            user_input (string): User input plot summary to be transformed & scored
            word2vec_model (model object from gensim): used to generate word2vec vector for every word
                and then averaged to get a sentence score in word2vec form used as an input feature to model
            tf_vect (sklearn count vectorizer object): used to get data into form for LDA scoring
            lda_model (sklearn lda model object): used to generate features in LDA form for use in the RFC model
            RFC_model (sklearn multilabel-binarized random forest model object): Model object trained on our data used to predict
                probabilities for every label for a new entry

        Returns:
            tuple: tuple of length 2 in which the first object is the list of genres which the model
                was predicting probabilities for and the second object is the list of associated
                probabilites for each of the genres based on the user input plot summary. 
    '''
    
    # get user input to dataframe form to do some work on it
    logger.info("initiating model scoring protocol")
    new_entry_df = pd.DataFrame(data=[user_input], columns=['plotSum'])
    
    # apply our old trusty transformer friends as we have to our training set
    steps = [('tokenizer', ct.Tokenizer()),
                ('filterer', ct.Filter_sentence(filter_names=config['filter_names'])),
                ('mean_words2vec_er',ct.MeanEmbeddingVectorizer(word2vec_model)),
                ('pruner', ct.StemmingLemming(prune_type=config['prune_type'])),
                ('joiner_transformer', ct.Joiner())]
         
    pipeline = Pipeline(steps)
    logger.info("Calling filter->word2vec->prune->join pipelin on input")
    # apply this pipeline to new data to get word2vec features
    cleaned_summary_w_w2vec = pipeline.transform(new_entry_df)
    
    # apply lda transformer to get LDA features
    lda_transformer = ct.LDA_Vectorizer(lda_model, tf_vect)
    logger.info("getting LDA vectors")
    prediction_DF = lda_transformer.transform(cleaned_summary_w_w2vec)
    
    # turning our arrays into dataframes like training data was in
    logger.info("getting user_data into correct form")
    plotSumLDA_list = prediction_DF['plotSumLDA'].values[0][0]
    plotSumLDA_DF = pd.DataFrame([plotSumLDA_list])
    
    plotSumVecList = prediction_DF['plotSum2vec'].values[0]
    plotSumVecs_DF = pd.DataFrame([plotSumVecList])
    
    newColsWord2vec = []
    for columnIndex in range(len(plotSumVecs_DF.columns)):
        newColsWord2vec.append('word2vec_'+str(columnIndex+1))
    plotSumVecs_DF.columns = newColsWord2vec

    newColsLDA = []
    for columnIndex in range(len(plotSumLDA_DF.columns)):
        newColsLDA.append('LDA_'+str(columnIndex+1))
    plotSumLDA_DF.columns = newColsLDA
    
    # concatenate feature DF's together to get it into form to make model predictions on it
    logger.info("concatenate to make new data input DF")
    X = pd.concat([plotSumLDA_DF,plotSumVecs_DF], axis=1)
    logger.info("finished creating new data input DF")
    
    # make model prediction
    logger.info("make prediction")
    predicted_probs = RFC_model.predict_proba(X)
    
    # bring in genres
    with open(directory_abs_path+config['infile_genres'], 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)[0]
    
    # return genres and the associated probabilities for each one
    logger.info("return prediction")
    return (your_list, list(predicted_probs[0]))