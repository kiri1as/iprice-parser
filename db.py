from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from constants import DB_URL

engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
