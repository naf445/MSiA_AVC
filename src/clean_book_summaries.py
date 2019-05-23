import sys; sys.path.append('helpers')
from data_manipulation import data
from data_manipulation import custom_transformers as ct
import pandas as pd
import argparse
import logging
import logging.config
from sklearn.pipeline import Pipeline 
import os

directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

logging.config.fileConfig(directory_abs_path+"/../config/logging.conf")
logger = logging.getLogger(__name__)
logger.info("Testing... Delete this message in the clean_book_summaries_file")

books = data.loadAndClean('../data/booksummaries/booksummaries.txt')
books = books[['bookGenre', 'plotSum', 'bookTitle']]

if __name__=='__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('filter_names', help="When filtering words from sentences, designate whether to filter out names. 'True' will filter out names while 'False' will leave names in")
    parser.add_argument('stem_lem_type', help="Designate which type of word pruning to enforce. There are 3 options, 'Porter', 'Lancaster', and 'Lemmatization'.")
    args = parser.parse_args()    
    
    steps = [('tokenizer', ct.Tokenizer()),
                ('filterer', ct.Filter_sentence(filter_names=args.filter_names)),
                ('pruner', ct.StemmingLemming(prune_type=args.stem_lem_type)),
                ('joiner_transformer', ct.Joiner())]
    pipeline = Pipeline(steps)
    
    cleaned_books = pipeline.transform(books)
    
    cleaned_books.to_csv(directory_abs_path+'/../data/booksummaries/books_{}_{}.csv'\
                        .format(args.stem_lem_type, args.filter_names), index=False)
    