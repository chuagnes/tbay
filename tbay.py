from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, ForeignKey, desc
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

engine = create_engine('postgresql://ubuntu:thinkful@localhost:5432/tbay')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Item(Base):
    __tablename__="items"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    bids = relationship("Bid", backref="item")
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

class User(Base):
    __tablename__="users"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    bids = relationship("Bid", backref="bidder")
    items = relationship("Item", backref="owner")

class Bid(Base):
    __tablename__="bid"
    
    id = Column(Integer, primary_key=True)
    price = Column(Float, nullable=False)
    item_id = Column(Integer, ForeignKey('items.id'), nullable=False)
    bidder_id = Column(Integer, ForeignKey('users.id'), nullable=False)

Base.metadata.create_all(engine)

#Add 3 users to db
jake = User(username="Jake", password="secret")
magnolia = User(username="Magnolia", password="flower")
victoria = User(username="Victoria", password="queen")

session.add_all([jake, magnolia, victoria])
session.commit()

#One user actions a baseball
baseball = Item(name="baseball", description="Mark McGuire's final homerun baseball", owner=jake)
session.add(baseball)
session.commit()
print("{} is auctioning a {}".format(baseball.owner.username, baseball.name))

#Each user places two bids on the baseball
bid1 = Bid(price=100, bidder=jake, item=baseball)
bid2 = Bid(price=150, bidder=jake,item=baseball)
bid3 = Bid(price=120, bidder=magnolia, item=baseball)
bid4 = Bid(price=160, bidder=magnolia, item=baseball)
bid5 = Bid(price=130, bidder=victoria, item=baseball)
bid6 = Bid(price=170, bidder=victoria, item=baseball)
bid_list = [bid1, bid2, bid3, bid4, bid5, bid6]
session.add_all([bid1, bid2, bid3, bid4, bid5, bid6])
session.commit()

for bid in bid_list:
    print("{} bid on {} for ${}".format(bid.bidder.username, baseball.name, bid.price))

#Find the highest bid 
highest_bid = session.query(Bid).order_by(desc(Bid.price)).first()
print("The highest bid on {} is {} by {}".format(baseball.name, highest_bid.price, highest_bid.bidder.username))