import sqlalchemy as sq
from sqlalchemy import select
from sqlalchemy.orm import sessionmaker, declarative_base, relationship
import json
import pprint

DB_tipe = "postgresql"
login = "postgres"
password = "______"
host = "localhost"
port = "5432"
DB_name = "BooksDB"

DSN = f'{DB_tipe}://{login}:{password}@{host}:{port}/{DB_name}'
engine = sq.create_engine(DSN)
conn = engine.connect()
Base = declarative_base()

class Publisher(Base):
    __tablename__ = "publisher"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return self.name
class Book(Base):
    __tablename__ = "book"

    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String(length=50), nullable=False)
    id_publisher = sq.Column(sq.Integer, sq.ForeignKey("publisher.id"), nullable=False)

    publisher = relationship(Publisher, backref="books")
    def __str__(self):
        return self.title

class Shop(Base):
    __tablename__ = "shop"

    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String(length=40), unique=True)

    def __str__(self):
        return self.name

class Stock(Base):
    __tablename__ = "stock"

    id =  sq.Column(sq.Integer, primary_key=True)
    id_book = sq.Column(sq.Integer, sq.ForeignKey("book.id"), nullable=False)
    id_shop = sq.Column(sq.Integer, sq.ForeignKey("shop.id"), nullable=False)
    count = sq.Column(sq.Integer)

    book = relationship(Book, backref="Stocks")
    shop = relationship(Shop, backref="Stocks")

class Sale(Base):
    __tablename__ = "sale"

    id = sq.Column(sq.Integer, primary_key=True)
    price = sq.Column(sq.Float, nullable=False)
    date_sale = sq.Column(sq.Date, nullable=False)
    id_stock = sq.Column(sq.Integer, sq.ForeignKey("stock.id"), nullable=False)
    count = sq.Column(sq.Integer)

    stock = relationship(Stock, backref="sales")
    def __str__(self):
        return self.price, self.date_sale

def create_tables(engine):
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

create_tables(engine)

with open("tests_data.json") as f:
    data = json.load(f)

def add_data(json_data):
    for i in json_data:
        if i["model"] == "publisher":
            publ = Publisher(id = i["pk"],
                             name = i["fields"]["name"]
                             )
            session.add(publ)
        elif i["model"] == "book":
            book = Book(id = i["pk"],
                        title = i["fields"]["title"],
                        id_publisher = i["fields"]["id_publisher"]
                        )
            session.add(book)
        elif i["model"] == "shop":
            shop = Shop(id = i["pk"],
                        name = i["fields"]["name"]
                        )
            session.add(shop)
        elif i["model"] == "stock":
            stock = Stock(id = i["pk"],
                          id_shop = i["fields"]["id_shop"],
                          id_book = i["fields"]["id_book"],
                          count = i["fields"]["count"]
                          )
            session.add(stock)
        elif i["model"] == "sale":
            sale = Sale(id = i["pk"],
                        price = i["fields"]["price"],
                        date_sale = i["fields"]["date_sale"],
                        count = i["fields"]["count"],
                        id_stock = i["fields"]["id_stock"]
                        )
            session.add(sale)

def get_info(publisher_name):
    info = session.query(Publisher.name, Book.title, Shop.name, Sale.price, Sale.date_sale
                         ).join(Book).join(Stock).join(Shop).join(Sale
                         ).filter(Publisher.name == publisher_name).all()
    return info



Session = sessionmaker(bind=engine)
session = Session()
#add_data(data)

pub_name = input("Введите имя издателя: ")

info = get_info(pub_name)
for i in info:
    print(f"{i[1]}".ljust(40)
          +f"| {i[2]}".ljust(10)
          +f" | {i[3]}".ljust(9)
          + f"| {i[4]}")
session.commit()
session.close()
