from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData, DateTime
import sqlalchemy as sql
import argparse
import logging
import pandas as pd
import os

Base = declarative_base()

class Interactions(Base):
	"""Create a data model for the database to be set up for capturing songs """
	__tablename__ = 'interactions'
	interactionId = Column(Integer, primary_key=True)
	date = Column(DateTime, unique=False, nullable=False) 
	userId = Column(Integer, unique=False, nullable=False)
	userInput = Column(String(1000), unique=False, nullable=False)
	modelOutput = Column(String(50), unique=False, nullable=False)
	userSatisfaction = Column(String(50), unique=False, nullable=False)
  	  
	def __repr__(self):
		return '<Track %r>' % self.title

if __name__=='__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('db_location', help="designate 'sqlite' for local db creation or 'RDS' for AWS RDS db creation")
	args = parser.parse_args()

	if args.db_location == 'sqlite':

		# set up sqlite connection
		engine_string = 'sqlite:///'+os.getcwd()+'/data/avc423.db'
		engine = sql.create_engine(engine_string)
		# create the tracks table
		
		Base.metadata.create_all(engine)
		# set up looging config
		#logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
		#logger = logging.getLogger(__file__)
		# create a db session
		Session = sessionmaker(bind=engine)  
		session = Session()
		# add a record/track
		# add a record/track
		#track1 = Users(title="NathansSong")  
		#session.add(track1)
		session.commit()
		# To add multiple rows
		# session.add_all([track1, track2])
		#logger.info("Database created with song added: Red by Tayler Swift from the album, Red")
		session.close()

	elif args.db_location == 'RDS':

		# the engine_string format
		#engine_string = "{conn_type}://{user}:{password}@{host}:{port}/DATABASE_NAME"
		conn_type = "mysql+pymysql"
		user = os.environ.get("MYSQL_USER")
		password = os.environ.get("MYSQL_PASSWORD")
		host = os.environ.get("MYSQL_HOST")
		port = os.environ.get("MYSQL_PORT")
		DATABASE_NAME = 'msia423'
		engine_string = "{}://{}:{}@{}:{}/{}".\
		format(conn_type, user, password, host, port, DATABASE_NAME)
		engine = sql.create_engine(engine_string)
		Base.metadata.create_all(engine)

		# create a db session
		Session = sessionmaker(bind=engine)  
		session = Session()
		session.commit()
		session.close()

	else:
		raise ValueError("Must designate 'sqlite' for local db creation or 'RDS' for AWS RDS db creation")
