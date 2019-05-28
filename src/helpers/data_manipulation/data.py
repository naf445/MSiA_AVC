import pandas as pd
import ast
import yaml
import os
import logging
import logging.config

directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../../../config/src_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)
config = config["data"]

logging.config.fileConfig(directory_abs_path+config["logger_config"])
logger = logging.getLogger(__name__)

def loadAndClean(path=True):
    """ 
    Loads and cleans the booksummaries.txt data file for more
    exploratory analysis and machine learning training. 
  
    Parameters: 
    path (str): Relative path to the booksummaries.txt data file
  
    Returns: 
    pandas.DataFrame: Cleaned version of the booksummaries.txt file in DataFrame form 
    """
    
    logger.info("Called loadAndClean function")

    # cleaned column names
    column_names = ['wikiArticleID','freebaseID','bookTitle','author','pubDate','bookGenre', 'plotSum']
    
    logger.info("Read in booksummary data")

    booksummaries = pd.read_csv(path, sep='\t', header=None, names=column_names)
    
    logger.info("Drop any NA's present in dataset under book genre or plot summary")
    # drop values which are NA for bookGenre or plotSum which would not be trainable
    booksummaries.dropna(subset = ['bookGenre','plotSum'] , inplace=True)
    
    booksummaries['bookGenre'] = booksummaries.apply(lambda row:\
                                    list(ast.literal_eval(row.bookGenre).values()), axis=1)
    
    
    booksummaries['bookGenre'] = booksummaries['bookGenre'].apply(lambda row:\
                                    [v.strip().lower().replace("'",'').replace(' ','_') for v in row])
    
    logger.info("returning booksummary data set")

    return booksummaries