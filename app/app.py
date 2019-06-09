import flask
import pickle
import os
import yaml
import pandas as pd
import logging
import logging.config
import gensim.downloader as api
import sys; sys.path.append('../src/helpers')
from scoring import score_user_input
from flask import url_for

directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/flask_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)

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




logger.info("Instantiate flask app object")
app = flask.Flask(__name__, template_folder='templates')

logger.info("create main route")
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def main():

    if flask.request.method == 'GET':
    	logger.info("GET request received by host server")
    	return(flask.render_template('main.html'))

    if flask.request.method == 'POST':
        
        logger.info("POST request received by host server")
        author = flask.request.form['author']
        plot_summary = flask.request.form['plot summary']
        model_results = score_user_input.score_model(plot_summary, word2vec_model, tf_vect, lda_model, rfc)

        return flask.render_template('main.html')


@app.route("/results", methods=['GET', 'POST'])
def results():

    if flask.request.method == 'POST':
        
        logger.info("POST request received by host server")
        author = flask.request.form['author']
        plot_summary = flask.request.form['plot_summary']
        model_results = score_user_input.score_model(plot_summary, word2vec_model, tf_vect, lda_model, rfc)

        return flask.render_template('results.html',\
                        original_input = {'author': author,'plot_summary': plot_summary}, \
                        model_results = model_results)

logger.info("Perform __name__ == __main__ check")
if __name__ == '__main__':
	
    logger.info("Run App")
    app.run(debug=False)











