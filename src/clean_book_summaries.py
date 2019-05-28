import sys; sys.path.append('helpers')
from data_manipulation import data
from data_manipulation import custom_transformers as ct
import pandas as pd
import argparse
import logging
import logging.config
from sklearn.pipeline import Pipeline 
import os
import yaml

directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)
config = config['clean_book_summaries']

logging.config.fileConfig(directory_abs_path+config["logger_config"])
logger = logging.getLogger(__name__)

logger.info("Load in raw data")
books = data.loadAndClean(directory_abs_path+config['infile'])
books = books[['bookGenre', 'plotSum', 'bookTitle']]
logger.info("Loaded in raw data")

if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('filter_names', help="When filtering words from sentences, designate whether to filter out names. 'True' will filter out names while 'False' will leave names in")
    parser.add_argument('stem_lem_type', help="Designate which type of word pruning to enforce. There are 3 options, 'Porter', 'Lancaster', and 'Lemmatization'.")
    args = parser.parse_args()    
    logger.info("Parsed Arguments")
    
    logger.info("Creating sklearn pipeline")
    steps = [('tokenizer', ct.Tokenizer()),
                ('filterer', ct.Filter_sentence(filter_names=args.filter_names)),
                ('pruner', ct.StemmingLemming(prune_type=args.stem_lem_type)),
                ('joiner_transformer', ct.Joiner())]
    pipeline = Pipeline(steps)
    logger.info("Created sklearn pipeline")
    
    logger.info("Applying sklearn pipeline to book data")
    cleaned_books = pipeline.transform(books)
    logger.info("Successfully applied pipeline to book data")

    logger.info("Saving cleaned books to data folder")
    cleaned_books.to_csv(directory_abs_path+config['outdirectory']+'/books_{}_{}.csv'\
                        .format(args.stem_lem_type, args.filter_names), index=False)
    logger.info("Saved cleaned books to data folder")






    