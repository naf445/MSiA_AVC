import sys; sys.path.append('helpers')
import sys; sys.path.append('src/helpers')
from data_manipulation import custom_transformers as ct
import boto3
import logging
import logging.config
import numpy as np
import os
import pandas as pd
import pickle
import yaml




directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    src_config = yaml.load(yml_file)
src_config = src_config['src']

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)
config = config['gen_LDA_vecs']

logging.config.fileConfig(directory_abs_path+config["logger_config"], disable_existing_loggers=False)
logger = logging.getLogger(__name__)

logger.info("Load in data")
books = pd.read_csv(directory_abs_path+config['infile_data'])
logger.info("Loaded in data")

# Load LDA from file
logger.info("Load in lda_model")
with open(directory_abs_path+config['infile_lda'], 'rb') as file:  
    lda_model = pickle.load(file)
logger.info("Loaded in lda_model")

# Load tf_vectorizer from file
logger.info("Load in tf_vect")
with open(directory_abs_path+config['infile_tf_vect'], 'rb') as file:  
    tf_vect = pickle.load(file)
logger.info("Loaded in tf_vect")

# Call and transform our data with the LDA model to get features
logger.info("call LDA vectorizer and transform")
LDAvecGenerator = ct.LDA_Vectorizer(lda_model, tf_vect)
books_with_LDA_vecs = LDAvecGenerator.transform(books)

logger.info("save data with LDA features")
books_with_LDA_vecs.to_csv(directory_abs_path+config['outfile'], index=False)
logger.info("saved data with LDA features")

if src_config['s3']['use']:
	logger.info("s3 option initiated")
	s3 = boto3.client('s3')
    
	logger.info("connect to S3 & upload data with LDA features to s3")
	s3.upload_file(Bucket=src_config['s3']['bucket_name'],
    	Filename=directory_abs_path+config['outfile'], 
    	Key=src_config['s3']['booksummaries']+'booksummaries_ready2train.csv')




