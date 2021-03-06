import sys; sys.path.append('helpers')
import sys; sys.path.append('src/helpers')
import boto3
import argparse
from data_manipulation import data
from data_manipulation import custom_transformers as ct
import gensim.downloader as api
import logging
import logging.config
import numpy as np
import os
import pandas as pd
from sklearn.pipeline import Pipeline 
import yaml




directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    src_config = yaml.load(yml_file)
src_config = src_config['src']

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)
config = config['clean_summaries_gen_vecs']

logging.config.fileConfig(directory_abs_path+config["logger_config"], disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# load in data
logger.info("Load in raw data")
books = pd.read_csv(directory_abs_path+config['infile'])
logger.info("Loaded in raw data")

# load in word 2 vec model
logger.info("Load in word2vec_model")
word2vec_model = api.load("glove-wiki-gigaword-50")
logger.info("Loaded in word2vec_model")

if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('filter_names', help="When filtering words from sentences, designate whether to filter out names. 'True' will filter out names while 'False' will leave names in")
    parser.add_argument('stem_lem_type', help="Designate which type of word pruning to enforce. There are 3 options, 'Porter', 'Lancaster', and 'Lemmatization'.")
    args = parser.parse_args()    
    logger.info("Parsed Arguments")
    
    # create sklearn pipeline
    logger.info("Creating sklearn pipeline")
    steps = [('tokenizer', ct.Tokenizer()),
                ('filterer', ct.Filter_sentence(filter_names=args.filter_names)),
                ('mean_words2vec_er',ct.MeanEmbeddingVectorizer(word2vec_model)),
                ('pruner', ct.StemmingLemming(prune_type=args.stem_lem_type)),
                ('joiner_transformer', ct.Joiner())]
    pipeline = Pipeline(steps)
    logger.info("Created sklearn pipeline")
    
    # apply previously created sklearn pipeline
    logger.info("Applying sklearn pipeline to book data")
    cleaned_books = pipeline.transform(books)
    logger.info("Successfully applied pipeline to book data")

    # save data after pipeline has been applied
    logger.info("Saving cleaned books to data folder")
    outfile = directory_abs_path+config['outdirectory']+'/books_{}_{}.csv'\
                        .format(args.stem_lem_type, args.filter_names)
    cleaned_books.to_csv(outfile, index=False)
    logger.info("Saved cleaned books to data folder")

    # if specified, save data to S3
    if src_config['s3']['use']:
        logger.info("s3 option initiated")
        s3 = boto3.client('s3')
        logger.info("connect to S3 & upload file to bucket")
        s3.upload_file(Bucket=src_config['s3']['bucket_name'],
                       Filename=outfile, 
                       Key=src_config['s3']['booksummaries']+'books_summaries_cleaned.csv')