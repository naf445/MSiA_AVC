import logging
import logging.config
import matplotlib.pyplot as plt
import os
import pandas as pd
import seaborn as sns
import yaml

directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/flask_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)
config = config['plot_results']

logging.config.fileConfig(directory_abs_path+config["logger_config"], disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def save_plot_results(results, path):
	'''Takes results from our RFC model and plots them

	 Args:
        results (tuple of length 2): First object in tuple is list of genres
        	which the model was using. Second object in tuple is a list of the
        	probabilities assigned by the model to each of these genres.

        path (string): path where to save images generated
	'''

	# get the two tuple objects
	genres = results[0]
	probabilities = results[1]

	# create a results dataframe for easier plotting
	results_df = pd.DataFrame(data={'genre':genres, 'probability':probabilities})
	results_df = results_df.sort_values('probability', ascending=False)

	logger.info('about to make your plot')
	# Initialize the matplotlib figure
	f, ax = plt.subplots(figsize=(6, 10))
	logger.info('setting sns stuff')
	sns.set_color_codes("pastel")
	sns.barplot(x="probability", y="genre", data=results_df, color="b", tick_label=True)
	logger.info('setting axes stuff')
	ax.set_xlim(0.0, 1)
	logger.info('saving plot')
	plt.savefig(path, bbox_inches='tight')
	plt.close()