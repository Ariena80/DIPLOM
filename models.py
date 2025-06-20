from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, Text, Date, Boolean
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    roleID = Column(Integer, ForeignKey('Role.id'), nullable=False)
    surname = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)
    login = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    genderID = Column(Integer, ForeignKey('Gender.id'), nullable=True)
    groupID = Column(Integer, ForeignKey('Group.id'), nullable=True)
    image = Column(LargeBinary, nullable=True)

    role = relationship('Role', back_populates='users')
    gender = relationship('Gender', back_populates='users')
    group = relationship('Group', back_populates='users')

class Gender(db.Model):
    __tablename__ = 'Gender'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    users = relationship('User', back_populates='gender')

class Group(db.Model):
    __tablename__ = 'Group'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    users = relationship('User', back_populates='group')

class Role(db.Model):
    __tablename__ = 'Role'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    users = relationship('User', back_populates='role')

class News(db.Model):
    __tablename__ = 'News'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    imageURL = Column(String(255), nullable=True)
    date = Column(Date, nullable=False)

class Command(db.Model):
    __tablename__ = 'Command'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

class Event(db.Model):
    __tablename__ = 'Event'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    sportTypeID = Column(Integer, ForeignKey('SportType.id'), nullable=False)

class MediaCards(db.Model):
    __tablename__ = 'MediaCards'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    mediaType = Column(String(50), nullable=False)
    mediaUrl = Column(String(255), nullable=False)

class ScheduleSections(db.Model):
    __tablename__ = 'ScheduleSections'
    id = Column(Integer, primary_key=True)
    sportTypeID = Column(Integer, ForeignKey('SportType.id'), nullable=False)
    time = Column(String(11), nullable=False)
    date = Column(Date, nullable=False)

class StudentInCommand(db.Model):
    __tablename__ = 'StudentInCommand'
    id = Column(Integer, primary_key=True)
    studID = Column(Integer, ForeignKey('User.id'), nullable=False)
    groupID = Column(Integer, ForeignKey('Group.id'), nullable=False)
    commandID = Column(Integer, ForeignKey('Command.id'), nullable=False)
    date = Column(Date, nullable=False)

class Award(db.Model):
    __tablename__ = 'Award'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    recipient = Column(String(255), nullable=False)
    image = Column(String(255), nullable=True)

class SportType(db.Model):
    __tablename__ = 'SportType'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    events = relationship('Event', backref='sport_type')
    schedules = relationship('ScheduleSections', backref='sport_type')
    measures = relationship('Measure', backref='sport_type')
    statistics = relationship('Statistic', backref='sport_type')

class Measure(db.Model):
    __tablename__ = 'Measure'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    sportTypeID = Column(Integer, ForeignKey('SportType.id'), nullable=False)
    date = Column(Date, nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    placeID = Column(Integer, ForeignKey('Place.id'), nullable=False)
    result = Column(String(255), nullable=True)
    commandID = Column(Integer, ForeignKey('Command.id'), nullable=False)
    awardID = Column(Integer, ForeignKey('Award.id'), nullable=False)
    measureTypeID = Column(Integer, ForeignKey('MeasureType.id'), nullable=False)

class MeasureType(db.Model):
    __tablename__ = 'MeasureType'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    measures = relationship('Measure', backref='measure_type')

class Place(db.Model):
    __tablename__ = 'Place'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    measures = relationship('Measure', backref='place')

class Statistic(db.Model):
    __tablename__ = 'Statistic'
    id = Column(Integer, primary_key=True)
    studID = Column(Integer, ForeignKey('User.id'), nullable=False)
    reward = Column(String(10), nullable=False)
    sportTypeID = Column(Integer, ForeignKey('SportType.id'), nullable=False)

class Notification(db.Model):
    __tablename__ = 'Notification'
    id = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('User.id'), nullable=False)
    message = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    isRead = Column(Boolean, nullable=False, default=False)

class Registration(db.Model):
    __tablename__ = 'Registration'
    id = Column(Integer, primary_key=True)
    eventID = Column(Integer, ForeignKey('Event.id'), nullable=False)
    userID = Column(Integer, ForeignKey('User.id'), nullable=False)
    registrationDate = Column(Date, nullable=False)

class Feedback(db.Model):
    __tablename__ = 'Feedback'
    id = Column(Integer, primary_key=True)
    userID = Column(Integer, ForeignKey('User.id'), nullable=False)
    eventID = Column(Integer, ForeignKey('Event.id'), nullable=True)
    feedbackText = Column(Text, nullable=False)
    rating = Column(Integer, nullable=True)
    date = Column(Date, nullable=False)

class Partners(db.Model):
    __tablename__ = 'Partners'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    image = Column(LargeBinary, nullable=False)
