import sys; sys.path.append('helpers')
import sys; sys.path.append('src/helpers')
import pandas as pd
import logging
import logging.config
import data_manipulation.data as data
import os
import yaml
import re
import boto3

directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    src_config = yaml.load(yml_file)
src_config = src_config['src']

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)
config = config['clean_book_genres']

logging.config.fileConfig(directory_abs_path+config["logger_config"], disable_existing_loggers=False)
logger = logging.getLogger(__name__)

logger.info("Load in raw data")
books = data.loadAndClean(directory_abs_path+config['infile'])
logger.info("Loaded in raw data")

def ruleSwapper(tokenized_genres, rules_dict):
    for key in rules_dict:
        newGenre = key
        for value in rules_dict[key]:
            originalGenre = value
            tokenized_genres = [newGenre if re.search(originalGenre+'$', word)\
                    else word for word in tokenized_genres]
    return tokenized_genres

logger.info("applying rule swapping rules to data set")
#consolidate genres
books['bookGenre'] = books['bookGenre'].apply(lambda row: ruleSwapper(row, config['rules']))

def removeDuplicates(tokenized_genres):
    return list(dict.fromkeys(tokenized_genres))

logger.info("removing duplicates")
#remove duplicates
books['bookGenre'] = books['bookGenre'].apply(lambda row: removeDuplicates(row))

logger.info("removing books with only bogus genres remaining")
#remove books that have only bogus genres remaining
N_total = books.shape[0]
books['Drop'] = books.bookGenre.apply(lambda row: True if row==['bogus'] else False)
books = books[books.Drop==False]
N_after_dropping = books.shape[0]
logger.info("Dropped {} books because they did not have usable genre(s)".format(N_total-N_after_dropping))

logger.info("removing any bogus genres")
# remove any 'bogus' genres left
books['bookGenre'] = books['bookGenre'].apply(lambda row: [word for word in row if word!='bogus'])

logger.info("Saving cleaned books with clean genres to data folder on local")
books.to_csv(directory_abs_path+config['outfile'], index=False)
logger.info("Saved cleaned books with clean genres to data folder on local")

if src_config['s3']['use']:
	logger.info("s3 option initiated")
	s3 = boto3.client('s3')
	logger.info("connect to S3 & upload file to bucket")
	s3.upload_file(Bucket=src_config['s3']['bucket_name'],
	               Filename=directory_abs_path + config['outfile'], 
	               Key=src_config['s3']['clean_book_genres'])






    