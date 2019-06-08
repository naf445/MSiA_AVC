import sys; sys.path.append('helpers')
import pandas as pd
import logging
import logging.config
import os
import yaml
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)
config = config['gen_LDA_model']

logging.config.fileConfig(directory_abs_path+config["logger_config"])
logger = logging.getLogger(__name__)

logger.info("Load in data")
books = pd.read_csv(directory_abs_path+config['infile'])
logger.info("Loaded in raw data")

corpus = books['plotSum']
               
# get our corpus docs into BOW style.
logger.info("get data in BOW style")
tf_vectorizer = CountVectorizer(max_df=0.90, max_features=7000)
tf = tf_vectorizer.fit_transform(corpus)
tf_feature_names = tf_vectorizer.get_feature_names()

               
# Run LDA
logger.info("run LDA")
lda = LatentDirichletAllocation(n_topics=20, max_iter=5, learning_method='online', \
                                learning_offset=50.,random_state=123)
lda.fit(tf)

logger.info("save LDA model")
# save the model
with open(directory_abs_path+config['outfile'], 'wb') as file:  
    pickle.dump(lda, file)
               