from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy import Column, Integer, String, MetaData
import sqlalchemy as sql
import logging
import pandas as pd
import os

Base = declarative_base()

class FakeTable(Base):
	"""Create a data model for the database to be set up for capturing songs """
	__tablename__ = 'fakeTableName'
	id = Column(Integer, primary_key=True)
	title = Column(String(100), unique=False, nullable=False)
	artist = Column(String(100), unique=False, nullable=False)
	album = Column(String(100), unique=False, nullable=True)
  	  
	def __repr__(self):
		return '<Track %r>' % self.title

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
#print(engine_string)
engine = sql.create_engine(engine_string)
Base.metadata.create_all(engine)

# set up looging config
logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__file__)
# create a db session
Session = sessionmaker(bind=engine)  
session = Session()
# add a record/track
track1 = Track(artist="Britney Spears", album="Circus", title="Radar")  
session.add(track1)
session.commit()
logger.info("Database created with song added: Radar by Britney spears from the album, Circus")  
track_record = session.query(Track.title, Track.album).filter_by(artist="Britney Spears").first()
print(track_record)
query = "SELECT * FROM tracks WHERE artist LIKE '%%Britney%%'"
df = pd.read_sql(query, con=engine)
print(df)
session.close()
