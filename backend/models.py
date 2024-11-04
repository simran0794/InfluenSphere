from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, DateTime,ForeignKey,Enum,Boolean
import datetime

from sqlalchemy.orm import relationship
db=SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())
    type=Column(String(100), nullable=False)
    flag= Column(Boolean, default=False)

    __mapper_args__ = {
        'polymorphic_on': 'type',
        'polymorphic_identity': 'user'
    }

class Influencer(User):
    __tablename__ = 'influencers'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    bio = Column(String(200), nullable=True)

    category= Column(Enum('Food','Health & Fashion','Lifestyle','Memes','Pop Culture','Travel','Tech','Gaming','Parenting','Finance','Education','Environment','Pet','Art','Music', name='icategory'))

    facebook = db.Column(db.Boolean, default=False)
    instagram = db.Column(db.Boolean, default=False)
    twitter = db.Column(db.Boolean, default=False)
    linkedin = db.Column(db.Boolean, default=False)
    youtube = db.Column(db.Boolean, default=False)
    tiktok = db.Column(db.Boolean, default=False)
    pinterest = db.Column(db.Boolean, default=False)
    reddit = db.Column(db.Boolean, default=False)
    facebook_id = db.Column(db.String(120), nullable=True)
    instagram_id = db.Column(db.String(120), nullable=True)
    twitter_id = db.Column(db.String(120), nullable=True)
    linkedin_id = db.Column(db.String(120), nullable=True)
    youtube_id = db.Column(db.String(120), nullable=True)
    tiktok_id = db.Column(db.String(120), nullable=True)
    pinterest_id = db.Column(db.String(120), nullable=True)
    reddit_id = db.Column(db.String(120), nullable=True)

    reach= Column(Integer,nullable=True)



    __mapper_args__ = {
        'polymorphic_identity': 'influencer'
    }

class Sponsor(User):
    __tablename__ = 'sponsors'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    industry = Column(String(100), nullable=False)
    bio = Column(String(200), nullable=True)

    __mapper_args__ = {
        'polymorphic_identity': 'sponsor'
    }

class Admin(User):
    __tablename__ = 'admins'
    id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    admin_level = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
class AdRequest(db.Model):
    __tablename__ = 'ad_requests'
    id = Column(Integer, primary_key=True)
    campaign_id = Column(Integer, ForeignKey('campaigns.id'))
    campaign = relationship('Campaign', backref='ad_requests')
    influencer_id = Column(Integer, ForeignKey('users.id'))
    influencer = relationship('Influencer', backref='ad_requests')
    messages = Column(String)
    requirements = Column(String)
    payment_amount = Column(Integer)
    status = Column(Enum('Pending', 'Accepted', 'Rejected', name='ad_request_status'))

class Campaign(db.Model):

    __tablename__ = 'campaigns'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    budget = Column(Integer)
    visibility = Column(Enum('public', 'private', name='campaign_visibility'))
    sponsor_id=Column(Integer,ForeignKey('users.id'))
    sponsor = relationship('Sponsor', backref='campaigns')
    flag= Column(Boolean, default=False)
