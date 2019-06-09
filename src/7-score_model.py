import sys; sys.path.append('helpers')
from scoring import score_user_input
import gensim.downloader as api
import pickle
import logging
import logging.config
import os
import yaml

directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)
config = config['score_model']

logging.config.fileConfig(directory_abs_path+config["logger_config"], disable_existing_loggers=False)
logger = logging.getLogger(__name__)

logger.info("Loading in word2vec model")
word2vec_model = api.load("glove-wiki-gigaword-50")

logger.info("Loading in lda model")
with open(directory_abs_path+config['infile_lda'], 'rb') as file:  
    lda_model = pickle.load(file)
    
logger.info("Loading in tf_vect model")
with open(directory_abs_path+config['infile_tf_vect'], 'rb') as file:  
    tf_vect = pickle.load(file)

logger.info("Loading in RFC model")
with open(directory_abs_path+config['infile_model'], 'rb') as file:  
    rfc = pickle.load(file)

user_input_plot_summary = '''This story is about a boy named Jim. 
Jim decided he wanted to be a pirate, but not just any pirate. No Jim
 wanted to be aQWDWQND space pirate. someone who had laser guns and could take his family across the universe
 and fight aliens 238 and protect his homeland from the evil aliens who were invading
 the solar XNIAMne system that he lived in. But d18x1m ncziomz nnwiMQ the year 19272672 far in the future nothin could have prepared jim for the fights and battles
 and stars and explosions and bombs and explodings that were coming his way.
 You will have to read more to find out what happened to Jim!'''
    
logger.info("initiating model scoring")
print(score_user_input.score_model(user_input_plot_summary, word2vec_model, tf_vect, lda_model, rfc))
