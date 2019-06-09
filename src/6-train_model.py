import sys; sys.path.append('helpers')
import pandas as pd
import logging
import logging.config
import os
import yaml
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import MultiLabelBinarizer as MLB
import ast
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score, f1_score, recall_score
import csv

directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)
config = config['train_model']

logging.config.fileConfig(directory_abs_path+config["logger_config"], disable_existing_loggers=False)
logger = logging.getLogger(__name__)

logger.info("Load in data")
books = pd.read_csv(directory_abs_path+config['infile_data'])
logger.info("Loaded in data")

genres = books['bookGenre'].to_list()
genres_list = [ast.literal_eval(x) for x in genres]

logger.info("Get Y's")
mlb = MLB()
mlb_Genres = mlb.fit_transform(y=genres_list)
Y = pd.DataFrame(mlb_Genres, columns=mlb.classes_)

logger.info("Get word2vec features")
plotSumVecs = books['plotSum2vec']
plotSumVecs_list = [ast.literal_eval(x) for x in plotSumVecs]
plotSumVecs_DF = pd.DataFrame(data=plotSumVecs_list)

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

logger.info("Concat word2vec and LDA features ")
X = pd.concat([plotSumLDA_DF,plotSumVecs_DF], axis=1)

logger.info("Concat word2vec and LDA features ")
rfc = OneVsRestClassifier(RandomForestClassifier(bootstrap=True, random_state=541, n_estimators=100, max_features='sqrt'))

logger.info("Fit rfc model")
rfc.fit(X, Y)


logger.info("save RFC model for deployment")
# save the model
with open(directory_abs_path+config['outfile_model'], 'wb') as file:  
    pickle.dump(rfc, file)
logger.info("saved RFC model")

logger.info("save Y column names")
category_names = list(Y.columns)
with open(directory_abs_path+config['outfile_genres'], 'w') as csvFile:
    writer = csv.writer(csvFile)
    writer.writerow(category_names)
logger.info("saved Y column names")