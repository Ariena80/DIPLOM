from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, Text, Date, Time, DateTime
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True, autoincrement=True)
    roleID = Column(Integer, ForeignKey('Role.id'), nullable=False)
    surname = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)
    login = Column(String(50), nullable=False, unique=True)
    password = Column(Text, nullable=False)
    image = Column(LargeBinary, nullable=True)
    genderID = Column(Integer, ForeignKey('Gender.id'), nullable=False)
    groupID = Column(Integer, ForeignKey('Group.id'), nullable=True)
    position = Column(String(50), nullable=True)

    role = relationship('Role', back_populates='users')
    gender = relationship('Gender', back_populates='users')
    group = relationship('Group', back_populates='users')

class Request(db.Model):
    __tablename__ = 'requests'
    id = Column(Integer, primary_key=True)
    team_name = Column(String(50), nullable=False)
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    sport_type_id = Column(Integer, ForeignKey('sport_type.id'), nullable=False)
    gender_id = Column(Integer, ForeignKey('gender.id'), nullable=False)
    status = Column(String(20), default='pending')
    created_at = Column(DateTime, default=datetime.utcnow)

    # Связь с таблицей StudentInCommand
    students = relationship("StudentInCommand", back_populates="request", cascade="all, delete-orphan")


class Course(db.Model):
    __tablename__ = 'Course'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class Gender(db.Model):
    __tablename__ = 'Gender'
    id = Column(Integer, primary_key=True)
    name = Column(String(7), nullable=False)
    users = relationship('User', back_populates='gender')

class Group(db.Model):
    __tablename__ = 'Group'
    id = Column(Integer, primary_key=True)
    name = Column(String(10), nullable=False)
    users = relationship('User', back_populates='group')

class Award(db.Model):
    __tablename__ = 'Award'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    recipient = Column(String(100), nullable=True)
    imageURL = Column(String(255), nullable=True)

class Role(db.Model):
    __tablename__ = 'Role'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    users = relationship('User', back_populates='role')

class News(db.Model):
    __tablename__ = 'News'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    date = Column(Date, nullable=False)
    imageURL = Column(String(255), nullable=True)

class Command(db.Model):
    __tablename__ = 'Command'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    courseID = Column(Integer, ForeignKey('Course.id'), nullable=False)
    genderID = Column(Integer, ForeignKey('Gender.id'), nullable=False)
    groupID = Column(Integer, ForeignKey('Group.id'), nullable=False)
    sportTypeID = Column(Integer, ForeignKey('SportType.id'), nullable=False)

class Event(db.Model):
    __tablename__ = 'Event'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)
    sportTypeID = Column(Integer, ForeignKey('SportType.id'), nullable=False)
    time = Column(Time, nullable=True)
    eventTypeID = Column(Integer, ForeignKey('EventType.id'), nullable=False)
    placeID = Column(Integer, ForeignKey('Place.id'), nullable=False)
    imageURL = Column(String(255), nullable=True)

    place = relationship('Place', backref='events')

class Media(db.Model):
    __tablename__ = 'Media'
    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    mediaUrl = Column(String(255), nullable=False)
    sportTypeID = Column(Integer, ForeignKey('SportType.id'), nullable=False)

class ScheduleSections(db.Model):
    __tablename__ = 'ScheduleSections'
    id = Column(Integer, primary_key=True)
    sportTypeID = Column(Integer, ForeignKey('SportType.id'), nullable=False)
    time = Column(String(11), nullable=False)
    date = Column(Date, nullable=False)
    coachName = Column(String(100), nullable=True)

class StudentInCommand(db.Model):
    __tablename__ = 'student_in_command'
    id = Column(Integer, primary_key=True)
    surname = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)
    group_id = Column(Integer, ForeignKey('group.id'), nullable=False)

    # Внешний ключ для связи с таблицей Request
    request_id = Column(Integer, ForeignKey('requests.id'), nullable=False)

    # Связь с таблицей Request
    request = relationship("Request", back_populates="students")

class SportType(db.Model):
    __tablename__ = 'SportType'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class EventType(db.Model):
    __tablename__ = 'EventType'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class Place(db.Model):
    __tablename__ = 'Place'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class TeamStatistics(db.Model):
    __tablename__ = 'TeamStatistics'
    id = Column(Integer, primary_key=True)
    commandID = Column(Integer, ForeignKey('Command.id'), nullable=False)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    activities = Column(Integer, default=0)
