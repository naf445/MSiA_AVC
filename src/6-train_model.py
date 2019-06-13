import sys; sys.path.append('helpers')
import sys; sys.path.append('src/helpers')
import ast
import boto3
import csv
import logging
import logging.config
import os
import pandas as pd
import pickle
import numpy as np
from sklearn.preprocessing import MultiLabelBinarizer as MLB
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score, f1_score, recall_score
import yaml


directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    src_config = yaml.load(yml_file)
src_config = src_config['src']

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)
config = config['train_model']

logging.config.fileConfig(directory_abs_path+config["logger_config"], disable_existing_loggers=False)
logger = logging.getLogger(__name__)

logger.info("Load in data")
books = pd.read_csv(directory_abs_path+config['infile_data'])
logger.info("Loaded in data")

# get just book genres as a list
genres = books['bookGenre'].to_list()
genres_list = [ast.literal_eval(x) for x in genres]

# get a dataframe in MultiLabelBinarizer form for multi-label training
logger.info("Get Y's")
mlb = MLB()
mlb_Genres = mlb.fit_transform(y=genres_list)
Y = pd.DataFrame(mlb_Genres, columns=mlb.classes_)

# turn our word2vec sentence array/matrices into separate features
logger.info("Get word2vec features")
plotSumVecs = books['plotSum2vec']
plotSumVecs_list = [ast.literal_eval(x) for x in plotSumVecs]
plotSumVecs_DF = pd.DataFrame(data=plotSumVecs_list)

# turn our LDA array/matrices into separate features
logger.info("Get LDA features")
plotSumLDA_vecs = books['plotSumLDA']
plotSumLDA_list = [ast.literal_eval(x) for x in plotSumLDA_vecs]
plotSumLDA_list = [innerList[0] for innerList in plotSumLDA_list]
plotSumLDA_DF = pd.DataFrame(data=plotSumLDA_list)

newColsWord2vec = []
for columnIndex in range(len(plotSumVecs_DF.columns)):
    newColsWord2vec.append('word2vec_'+str(columnIndex+1))
plotSumVecs_DF.columns = newColsWord2vec

newColsLDA = []
for columnIndex in range(len(plotSumLDA_DF.columns)):
    newColsLDA.append('LDA_'+str(columnIndex+1))
plotSumLDA_DF.columns = newColsLDA

# concatenate dataframes for one big feature matrix
logger.info("Concat word2vec and LDA features ")
X = pd.concat([plotSumLDA_DF,plotSumVecs_DF], axis=1)

# create model object
logger.info("Concat word2vec and LDA features ")
rfc = OneVsRestClassifier(RandomForestClassifier(bootstrap=config['rfc']['bootstrap'], random_state=config['rfc']['random_state'], n_estimators=config['rfc']['n_estimators'], max_features=config['rfc']['max_features']))

# fit model object to our data set and MLB style response variable
logger.info("Fit rfc model")
rfc.fit(X, Y)


logger.info("save RFC model for deployment")
# save the model
with open(directory_abs_path+config['outfile_model'], 'wb') as file:  
    pickle.dump(rfc, file)
logger.info("saved RFC model")

# save category names for later interpretation
logger.info("save Y column names")
category_names = list(Y.columns)
with open(directory_abs_path+config['outfile_genres'], 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(category_names)
logger.info("saved Y column names")

if src_config['s3']['use']:
	logger.info("s3 option initiated")
	s3 = boto3.client('s3')
    
	logger.info("connect to S3 & upload data with LDA features to s3")
	s3.upload_file(Bucket=src_config['s3']['bucket_name'],
    	Filename=directory_abs_path+config['outfile_model'], 
    	Key=src_config['s3']['booksummaries']+'RFC_deployment_model.pkl')
