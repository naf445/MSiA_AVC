import flask
import pickle
import os
import yaml
import pandas as pd
import logging
import logging.config

directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/flask_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)

logging.config.fileConfig(directory_abs_path+config["logger_config"], disable_existing_loggers=False)
logger = logging.getLogger(__name__)

logger.info("Load in RFC .pkl")
# Use pickle to load in the pre-trained model.
with open(directory_abs_path+'/../models/RFC_deployment_model.pkl', 'rb') as f:
    rfc = pickle.load(f)

logger.info("Instantiate flask app object")
app = flask.Flask(__name__, template_folder='templates')

logger.info("create main route")
@app.route('/', methods=['GET', 'POST'])
def main():

    if flask.request.method == 'GET':
    	logger.info("GET request received by host server")
    	return(flask.render_template('main.html'))

    if flask.request.method == 'POST':
    	logger.info("POST request received by host server")
    	author = flask.request.form['author']
    	plot_summary = flask.request.form['plot summary']

    	return flask.render_template('main.html',
    						original_input={'author':author,
    										'plot summary':plot_summary})



logger.info("Perform __name__==__main__ check")
if __name__ == '__main__':
	
	logger.info("Run App")
	app.run(debug=True)











