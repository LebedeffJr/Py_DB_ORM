import sqlalchemy
from sqlalchemy.orm import sessionmaker
from models import create_tables

DB_tipe = "postgresql"
login = "postgres"
password = "____"
host = "localhost"
port = "5432"
DB_name = "BooksDB"

DSN = f'{DB_tipe}://{login}:{password}@{host}:{port}/{DB_name}'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()


session.close()
