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
    
    logger.info("initiating model scoring protocol")
    new_entry_df = pd.DataFrame(data=[user_input], columns=['plotSum'])
    
    steps = [('tokenizer', ct.Tokenizer()),
                ('filterer', ct.Filter_sentence(filter_names=True)),
                ('mean_words2vec_er',ct.MeanEmbeddingVectorizer(word2vec_model)),
                ('pruner', ct.StemmingLemming(prune_type='Porter')),
                ('joiner_transformer', ct.Joiner())]
         
    pipeline = Pipeline(steps)
    logger.info("Calling filter->word2vec->prune->join pipelin on input")
    cleaned_summary_w_w2vec = pipeline.transform(new_entry_df)
    
    lda_transformer = ct.LDA_Vectorizer(lda_model, tf_vect)
    
    logger.info("getting LDA vectors")
    prediction_DF = lda_transformer.transform(cleaned_summary_w_w2vec)
    
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
    
    logger.info("concatenate to make new data input DF")
    X = pd.concat([plotSumLDA_DF,plotSumVecs_DF], axis=1)
    logger.info("finished creating new data input DF")
    
    logger.info("make prediction")
    predicted_probs = RFC_model.predict_proba(X)
    
    with open(directory_abs_path+config['infile_genres'], 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)[0]
    
    logger.info("return prediction")
    return (your_list, list(predicted_probs[0]))