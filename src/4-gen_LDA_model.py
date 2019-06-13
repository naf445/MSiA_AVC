import sys; sys.path.append('helpers')
import sys; sys.path.append('src/helpers')
import boto3
import logging
import logging.config
import os
import pandas as pd
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import yaml



directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    src_config = yaml.load(yml_file)
src_config = src_config['src']

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)
config = config['gen_LDA_model']

logging.config.fileConfig(directory_abs_path+config["logger_config"], disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# load in data
logger.info("Load in data")
books = pd.read_csv(directory_abs_path+config['infile'])
logger.info("Loaded in raw data")

# get only the plot summary column to train out LDA model on
corpus = books['plotSum']
               
# get our corpus docs into BOW style.
logger.info("get data in BOW style")
# apply count vectorizer
tf_vectorizer = CountVectorizer(max_df=config['tf_vect']['max_df'], max_features=config['tf_vect']['max_features'])
tf = tf_vectorizer.fit_transform(corpus)
tf_feature_names = tf_vectorizer.get_feature_names()

               
# Run LDA
logger.info("run LDA")
lda = LatentDirichletAllocation(n_topics=config['lda_model']['n_topics'], max_iter=config['lda_model']['max_iter'], learning_method=config['lda_model']['learning_method'], \
                                learning_offset=config['lda_model']['learning_offset'],random_state=config['lda_model']['random_state'])
lda.fit(tf)

logger.info("save LDA model")
# save the model
with open(directory_abs_path+config['outfile_lda'], 'wb') as file:  
    pickle.dump(lda, file)
logger.info("saved LDA model")
    
logger.info("save tf_vectorizer")
# save the model
with open(directory_abs_path+config['outfile_tf_vect'], 'wb') as file:  
    pickle.dump(tf_vectorizer, file)
logger.info("saved tf_vectorizer")

if src_config['s3']['use']:
	logger.info("s3 option initiated")
	s3 = boto3.client('s3')
        
	logger.info("connect to S3 & upload tf_vect to bucket")
	s3.upload_file(Bucket=src_config['s3']['bucket_name'],
    	Filename=directory_abs_path+config['outfile_tf_vect'], 
    	Key=src_config['s3']['booksummaries']+'tf_vect.pkl')
		
	logger.info("connect to S3 & upload LDA to bucket")
	s3.upload_file(Bucket=src_config['s3']['bucket_name'],
    	Filename=directory_abs_path+config['outfile_lda'], 
    	Key=src_config['s3']['booksummaries']+'LDA_model.pkl')




