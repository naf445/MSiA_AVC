import sys; sys.path.append('helpers')
import pandas as pd
import logging
import logging.config
import data_manipulation.data as data
import os
import yaml
import re

directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)
config = config['clean_book_genres']

logging.config.fileConfig(directory_abs_path+config["logger_config"])
logger = logging.getLogger(__name__)

logger.info("Load in raw data")
books = data.loadAndClean(directory_abs_path+config['infile'])
books = books[['bookGenre', 'plotSum', 'bookTitle']]
logger.info("Loaded in raw data")

def ruleSwapper(tokenized_genres, rules_dict):
    for key in rules_dict:
        newGenre = key
        for value in rules_dict[key]:
            originalGenre = value
            tokenized_genres = [newGenre if re.search(originalGenre+'$', word)\
                    else word for word in tokenized_genres]
    return tokenized_genres

#consolidate genres
books['bookGenre'] = books['bookGenre'].apply(lambda row: ruleSwapper(row, config['rules']))

def removeDuplicates(tokenized_genres):
    return list(dict.fromkeys(tokenized_genres))

#remove duplicates
books['bookGenre'] = books['bookGenre'].apply(lambda row: removeDuplicates(row))

#remove books that have only bogus genres remaining
N_total = books.shape[0]
books['Drop'] = books.bookGenre.apply(lambda row: True if row==['bogus'] else False)
books = books[books.Drop==False]
N_after_dropping = books.shape[0]
logger.info("Dropped {} books because they did not have usable genre(s)".format(N_total-N_after_dropping))

# remove any 'bogus' genres left
books['bookGenre'] = books['bookGenre'].apply(lambda row: [word for word in row if word!='bogus'])

books = books[['bookGenre', 'plotSum', 'bookTitle']]

logger.info("Saving cleaned books with clean genres to data folder")
books.to_csv(directory_abs_path+config['outfile'], index=False)
logger.info("Saved cleaned books with clean genres to data folder")






    