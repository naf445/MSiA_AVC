import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import logging
import logging.config
import os
import yaml

directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/flask_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)
config = config['plot_results']

logging.config.fileConfig(directory_abs_path+config["logger_config"], disable_existing_loggers=False)
logger = logging.getLogger(__name__)

def save_plot_results(results, path):
	genres = results[0]
	probabilities = results[1]

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

#results = (['absurdist_fiction', 'adventure', 'anthol_biog_autobiog', 'anthropology', 'anti-nuclear', 'anti-war', 'chick_lit', 'children', 'comedy', 'conspiracy', 'conspiracy_fiction', 'cookbook', 'creative_nonfiction', 'crime_fiction', 'drama', 'existential_philosophy', 'fantasy', 'fiction', 'gay_themed', 'historical_fiction', 'horror', 'indian_chick_lit', 'informational', 'lgbt', 'non_fiction_lit', 'popular_culture', 'pornography', 'realistic_fiction', 'religious', 'romance', 'science_fiction', 'speculative_fiction', 'sports', 'steampunk', 'suspense/thriller/spy', 'tragicomedy', 'true_crime', 'war', 'western', 'young_adult'], [0.01, 0.26, 0.19, 0.05, 0.0, 0.0, 0.01, 0.39375, 0.25, 0.0, 0.0, 0.03, 0.03, 0.5176147186147185, 0.01, 0.12, 0.4591507936507936, 0.5699054834054834, 0.0, 0.18512709512709513, 0.32785714285714285, 0.0, 0.38, 0.0, 0.34, 0.0, 0.02, 0.06, 0.1, 0.07, 0.5475, 0.4385164835164835, 0.07, 0.02, 0.32059829059829054, 0.0, 0.13, 0.0, 0.11, 0.3996190476190476])
#save_plot_results(results, directory_abs_path+config['outfile'])