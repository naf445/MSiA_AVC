import sys; sys.path.append('../src/helpers')
import database_interaction
from database_interaction import create_db
from database_interaction import add_interaction
from datetime import datetime
import flask
from flask import url_for
import gensim.downloader as api
import logging
import logging.config
import os
import pandas as pd
import pickle
import plot_results
from random import randint
from scoring import score_user_input
import yaml


directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/flask_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)

# import config yaml file
with open(directory_abs_path+"/../config/mysql_config.yml", "r") as yml_file:
    mysql_config = yaml.load(yml_file)

logging.config.fileConfig(directory_abs_path+config['app']["logger_config"], disable_existing_loggers=False)
logger = logging.getLogger(__name__)

# get word2vec model
logger.info("Loading in word2vec model")
word2vec_model = api.load("glove-wiki-gigaword-50")

# get lda model
logger.info("Loading in lda model")
with open(directory_abs_path+config['app']['infile_lda'], 'rb') as file:  
    lda_model = pickle.load(file)
    
# get tf_vect model
logger.info("Loading in tf_vect model")
with open(directory_abs_path+config['app']['infile_tf_vect'], 'rb') as file:  
    tf_vect = pickle.load(file)

# get RFC model
logger.info("Loading in RFC model")
with open(directory_abs_path+config['app']['infile_model'], 'rb') as file:  
    rfc = pickle.load(file)

# create db instance and engine to store the user interactions
logger.info("creating db instance and getting engine string")
eng_string = create_db(user=mysql_config['MYSQL_USER'], password=os.environ.get('MYSQL_PASSWORD'),\
    host=mysql_config['MYSQL_HOST'],\
    port=mysql_config['MYSQL_PORT'],\
    RDS_db_name=mysql_config['DB_NAME'],\
    USE_RDS=mysql_config['USE_RDS'])

# create flask object
logger.info("Instantiate flask app object")
app = flask.Flask(__name__, template_folder='templates')

# create main route
logger.info("create main route")
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def main():

    # return the main.html file
    if flask.request.method == 'GET':
    	logger.info("GET request received by host server")
    	return(flask.render_template('main.html'))


# once user has clicked submit, taken to this page
@app.route("/results", methods=['GET', 'POST'])
def results():

    if flask.request.method == 'POST':
        
        # collect user data, 
        logger.info("POST request received by host server")
        author = flask.request.form['author']
        plot_summary = flask.request.form['plot_summary']
        # run user collected data through scoring function
        model_results = score_user_input.score_model(plot_summary, word2vec_model, tf_vect, lda_model, rfc)
        
        # commit results to database
        logger.info("add to database info about user interaction")
        add_interaction(engine_string=eng_string, date=datetime.now(), plot_summary=plot_summary, model_results=str(model_results))

        # create visualization from model results
        model_png_path = 'static/images/current_model_results_{}.png'.format(str(datetime.now()))
        plot_results.save_plot_results(model_results, model_png_path)

        return flask.render_template('results.html',\
                        original_input = {'author': author,'plot_summary': plot_summary},
                        url = model_png_path)

logger.info("Perform __name__ == __main__ check")
if __name__ == '__main__':
	
    logger.info("Run App")
    app.run(debug=False, host='0.0.0.0', port=3000)











