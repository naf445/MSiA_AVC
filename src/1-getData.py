import urllib.request 
import tarfile
import os
import boto3
import sys; sys.path.append('helpers')
import logging
import logging.config
import yaml
import shutil

directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    src_config = yaml.load(yml_file)
src_config = src_config['src']

# import config yaml file
with open(directory_abs_path+"/../config/src_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)
config = config['get_data']

logging.config.fileConfig(directory_abs_path+config["logger_config"], disable_existing_loggers=False)
logger = logging.getLogger(__name__)

logger.info("download zipped data to local file system")
urllib.request.urlretrieve(config['download_url'],\
	directory_abs_path + config['tar_file'])

logger.info("extract contents from zipped data and delete zipped version")
tf = tarfile.open(directory_abs_path + config['tar_file'])
logger.info("save to {}".format(directory_abs_path + config['extraction_point']))
tf.extractall(path=directory_abs_path + config['extraction_point'])
tf.close()
os.remove(directory_abs_path + config['tar_file'])


if src_config['s3']['use']:
	logger.info("s3 option initiated")
	s3 = boto3.client('s3')
	logger.info("connect to S3 & upload file to bucket")
	s3.upload_file(Bucket=src_config['s3']['bucket_name'],
	               Filename=directory_abs_path + config['outfile'], 
	               Key=src_config['s3']['booksummaries.txt'])






