import argparse
from datetime import datetime
import logging
import logging.config
import os
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData, DateTime
import sqlalchemy as sql
import yaml
from datetime import datetime

directory_abs_path = str(os.path.dirname(os.path.abspath(__file__)))

# import config yaml file
with open(directory_abs_path+"/../config/mysql_config.yml", "r") as yml_file:
    config = yaml.load(yml_file)

logging.config.fileConfig(directory_abs_path+config["logger_config"], disable_existing_loggers=False)
logger = logging.getLogger(__name__)

Base = declarative_base()

logger.info('defining user_interaction class')
class user_interaction(Base):
	"""Create a data model for the database to be set up for capturing user input and model predictions"""
	__tablename__ = 'user_interaction'
	#interaction_id = Column(Integer, primary_key=True)
	date = Column(DateTime, primary_key=True, unique=False, nullable=False) 
	plot_summary = Column(String(1000), unique=False, nullable=False)
	model_results = Column(String(300), unique=False, nullable=False)
	user_satisfaction = Column(String(50), unique=False, nullable=False)


def create_db(user='', password='', host='', port='', USE_RDS=False, RDS_db_name=''):
	logger.info('creating a database')
	if USE_RDS:
		logger.info('using RDS to store database')
		conn_type = "mysql+pymysql"
		user = user
		password = password
		host = host
		port = port
		database_name = RDS_db_name
		engine_string = "{}://{}:{}@{}:{}/{}".format(conn_type, user, password, host, port, database_name)
		logger.info('creating engine with engine string')
		engine = sql.create_engine(engine_string)
		Base.metadata.create_all(engine)

		logger.info('creating db session')
		# create a db session
		Session = sessionmaker(bind=engine)  
		session = Session()
		logger.info('committing table to session')
		session.commit()
		session.close()
		logger.info('returning engine string')
		return engine_string

	else:
		logger.info('storing database locally')
		# set up sqlite connection
		database_name = 'genre_app'
		engine_string = 'sqlite:///'+directory_abs_path+'/../data/'+database_name+'.db'
		logger.info('setup db engine with engine string')
		engine = sql.create_engine(engine_string)
		Base.metadata.create_all(engine)

		# create a db session
		logger.info('creating db session')
		Session = sessionmaker(bind=engine)  
		session = Session()
		logger.info('committing db session')
		session.commit()
		session.close()
		logger.info('returning engine_string')
		return engine_string

def add_interaction(engine_string, date, plot_summary, model_results, user_satisfaction="n/a"):
	
	logger.info('adding interaction to db')
	logger.info('creating session')
	engine = sql.create_engine(engine_string)
	Session = sessionmaker(bind=engine)
	session = Session()

	logger.info('creating interaction row object')
	user_interaction_1 = user_interaction(date=date, plot_summary=plot_summary, model_results=model_results, user_satisfaction=user_satisfaction)

	logger.info('adding row to session')
	session.add(user_interaction_1)
	logger.info('committing row from session')
	session.commit()
	logger.info('closing session')
	session.close()
	logger.info("User interaction information added to database")
