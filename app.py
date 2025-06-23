from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify, abort, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, Text, Date, Boolean, Time, DateTime
from sqlalchemy.orm import relationship, joinedload
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
import logging
from flask import send_file
from io import BytesIO
from PIL import Image
from sqlalchemy.exc import OperationalError, IntegrityError
from sqlalchemy import text, desc
from werkzeug.utils import secure_filename
import io
import os
from functools import wraps
from flask_migrate import Migrate

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://@DESKTOP-VF9RI0P\SQLEXPRESS/REDWOLFS?driver=ODBC+Driver+17+for+SQL+Server'
app.config['SECRET_KEY'] = 'your_secret_key_here'

UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)

# Инициализация Flask-Migrate
migrate = Migrate(app, db)

try:
    with app.app_context():
        db.session.execute(text("SELECT 1"))
    print("Подключение к базе данных успешно!")
except OperationalError as e:
    print(f"Ошибка подключения к базе данных: {e}")

logging.basicConfig(level=logging.DEBUG)
logging.debug(f"SECRET_KEY настроен: {app.config['SECRET_KEY']}")

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
    __tablename__ = 'Request'
    id = Column(Integer, primary_key=True)
    teamName = Column(String(50), nullable=False)
    eventID = Column(Integer, ForeignKey('Event.id'), nullable=False)
    sportTypeID = Column(Integer, ForeignKey('SportType.id'), nullable=False)
    genderID = Column(Integer, ForeignKey('Gender.id'), nullable=False)
    status = Column(String(20), default='pending')
    userID = Column(Integer, ForeignKey('User.id'), nullable=False)

    students = relationship("StudentInCommand", back_populates="request", cascade="all, delete-orphan")
    event = relationship("Event", back_populates="requests")
    sportType = relationship("SportType")
    user = relationship("User")

class Course(db.Model):
    __tablename__ = 'Course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Role(db.Model):
    __tablename__ = 'Role'
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    users = relationship('User', back_populates='role')

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

class EventType(db.Model):
    __tablename__ = 'EventType'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class Place(db.Model):
    __tablename__ = 'Place'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class Event(db.Model):
    __tablename__ = 'Event'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    date = Column(Date, nullable=False)
    description = Column(Text, nullable=True)
    sportTypeID = Column(Integer, ForeignKey('SportType.id'), nullable=True)
    time = Column(Time, nullable=True)
    eventTypeID = Column(Integer, ForeignKey('EventType.id'), nullable=True)
    placeID = Column(Integer, ForeignKey('Place.id'), nullable=True)
    imageURL = Column(String(255), nullable=True)

    place = relationship('Place', backref='events')
    requests = relationship("Request", back_populates="event")

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
    __tablename__ = 'StudentInCommand'
    id = Column(Integer, primary_key=True)
    surname = Column(String(50), nullable=False)
    name = Column(String(50), nullable=False)
    patronymic = Column(String(50), nullable=True)
    groupID = Column(Integer, ForeignKey('Group.id'), nullable=False)
    requestID = Column(Integer, ForeignKey('Request.id'), nullable=False)
    commandID = Column(Integer, ForeignKey('Command.id'), nullable=True)

    request = relationship("Request", back_populates="students")
    group = relationship("Group") 

class SportType(db.Model):
    __tablename__ = 'SportType'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

class TeamStatistics(db.Model):
    __tablename__ = 'TeamStatistics'
    id = Column(Integer, primary_key=True)
    commandID = Column(Integer, ForeignKey('Command.id'), nullable=False)
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    activities = Column(Integer, default=0)

def role_required(role_id):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                abort(401)
            user = User.query.get(session['user_id'])
            if not user or user.roleID != role_id:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def update_user_password(login, plain_password):
    with app.app_context():
        hashed_password = generate_password_hash(plain_password, method='pbkdf2:sha256')
        user = db.session.execute(db.select(User).filter_by(login=login)).scalar_one_or_none()
        if user:
            user.password = hashed_password
            db.session.commit()
            logging.debug(f"Пароль обновлен для пользователя {user.login}")
        else:
            logging.debug("Пользователь не найден")

def update_team_statistics(team_id, points):
    if team_id is None:
        return {'success': False, 'message': 'Некорректный ID команды'}

    team = db.session.get(Command, team_id)
    if not team:
        return {'success': False, 'message': 'Команда не найдена'}

    stats = TeamStatistics.query.filter_by(commandID=team_id).first()
    if not stats:
        stats = TeamStatistics(commandID=team_id, wins=0, losses=0, activities=0)
        db.session.add(stats)
        db.session.flush()

    if points == 3:
        stats.wins += 3
    elif points == 2:
        stats.wins += 2
    elif points == 1:
        stats.wins += 1

    stats.activities += 1
    db.session.commit()
    return {'success': True, 'message': 'Статистика успешно обновлена'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/media')
def media():
    return render_template('media.html')

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/measure')
def measure():
    return render_template('measure.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/user_panel')
@role_required(1)
def admin_panel():
    return render_template('user_panel.html')

@app.route('/physorg_panel')
@role_required(2)
def physorg_panel():
    return render_template('physorg_panel.html')

@app.route('/api/user_data', methods=['GET'])
def get_user_data_route():
    user_id = session.get('user_id')
    if user_id:
        user = db.session.get(User, user_id)
        if user:
            user_data = {
                'surname': user.surname,
                'name': user.name,
                'patronymic': user.patronymic,
                'login': user.login,
                'gender': user.genderID,
                'group': user.groupID,
                'role': user.roleID
            }
            return jsonify(user_data)
    return jsonify({'error': 'Пользователь не найден'}), 404

@app.route('/login.html', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_login = request.form['login']
        user_password = request.form['password']
        user = db.session.execute(db.select(User).filter_by(login=user_login)).scalar_one_or_none()
        if user and check_password_hash(user.password, user_password):
            session['user_id'] = user.id
            if user.roleID == 1:
                return redirect(url_for('admin_panel'))
            elif user.roleID == 2:
                return redirect(url_for('physorg_panel'))
            else:
                flash('Неверная роль пользователя', 'error')
                return redirect(url_for('login'))
        else:
            flash('Неверный логин или пароль', 'error')
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    user_login = data.get('login')
    user_password = data.get('password')
    user = db.session.execute(db.select(User).filter_by(login=user_login)).scalar_one_or_none()
    if user:
        if check_password_hash(user.password, user_password):
            session['user_id'] = user.id
            role = 'admin' if user.roleID == 1 else 'physorg'
            return jsonify({
                "success": True,
                "redirect": url_for('admin_panel') if user.roleID == 1 else url_for('physorg_panel'),
                "role": role
            }), 200
        else:
            return jsonify({"success": False, "message": "Неверный логин или пароль"}), 401
    else:
        return jsonify({"success": False, "message": "Неверный логин или пароль"}), 401

@app.route('/api/logout', methods=['POST'])
def api_logout():
    session.pop('user_id', None)
    return jsonify({"success": True, "message": "Выход выполнен успешно"}), 200

@app.route('/api/add_news', methods=['POST'])
def add_news():
    title = request.form.get('title')
    content = request.form.get('content')
    image = request.files.get('image')

    existing_news = News.query.filter_by(title=title).first()
    if existing_news:
        return jsonify({"success": False, "message": "Новость с таким заголовком уже существует."}), 400

    image_path = None
    if image and image.filename != '':
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        unique_filename = f"photo_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        image.save(save_path)
        image_path = f"static/uploads/{unique_filename}"

    new_news = News(
        title=title,
        description=content,
        date=datetime.now().date(),
        imageURL=image_path
    )

    try:
        db.session.add(new_news)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"success": False, "message": "Новость с таким заголовком уже существует."}), 400

    return jsonify({"success": True, "message": "Новость добавлена успешно", "imageURL": image_path}), 200

@app.route('/api/get_news', methods=['GET'])
def get_news():
    news = News.query.order_by(News.date.desc()).limit(4).all()
    news_list = [{
        'id': n.id,
        'title': n.title,
        'description': n.description,
        'date': n.date.isoformat(),
        'imageURL': n.imageURL
    } for n in news]
    return jsonify({'news': news_list})

@app.route('/static/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/get_courses', methods=['GET'])
def get_courses():
    courses = Course.query.all()
    courses_list = [{'id': course.id, 'name': course.name} for course in courses]
    return jsonify({'courses': courses_list})

@app.route('/api/get_genders', methods=['GET'])
def get_genders():
    genders = Gender.query.all()
    genders_list = [{'id': gender.id, 'name': gender.name} for gender in genders]
    return jsonify({'genders': genders_list})

@app.route('/api/get_sport_types', methods=['GET'])
def get_sport_types():
    sport_types = SportType.query.all()
    sport_types_list = [{'id': st.id, 'name': st.name} for st in sport_types]
    return jsonify({'sport_types': sport_types_list})

@app.route('/api/get_event_types', methods=['GET'])
def get_event_types():
    event_types = EventType.query.all()
    event_types_list = [{'id': et.id, 'name': et.name} for et in event_types]
    return jsonify({'event_types': event_types_list})

@app.route('/api/get_locations', methods=['GET'])
def get_locations():
    locations = Place.query.all()
    locations_list = [{'id': loc.id, 'name': loc.name} for loc in locations]
    return jsonify({'locations': locations_list})

@app.route('/api/add_team_request', methods=['POST'])
def add_team_request():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Пользователь не авторизован'}), 401

    data = request.get_json()
    logging.debug(f"Received data: {data}")

    if not all(key in data for key in ['team_name', 'event_id', 'sport_type', 'gender']):
        return jsonify({"success": False, "message": "Отсутствуют обязательные поля"}), 400

    teamName = data.get('team_name')
    eventID = data.get('event_id')
    sportTypeID = data.get('sport_type')
    genderID = data.get('gender')
    team_members = data.get('team_members', [])
    reserve_member = data.get('reserve_member')

    new_request = Request(
        teamName=teamName,
        eventID=eventID,
        sportTypeID=sportTypeID,
        genderID=genderID,
        status='pending',
        userID=user_id
    )

    db.session.add(new_request)
    db.session.commit()

    def parse_member(member):
        if isinstance(member, dict):
            return member
        elif isinstance(member, str):
            parts = member.split()
            return {
                'surname': parts[0] if len(parts) > 0 else '',
                'name': parts[1] if len(parts) > 1 else '',
                'patronymic': parts[2] if len(parts) > 2 else '',
                'group_id': 1
            }
        else:
            raise ValueError("Member data should be either a dictionary or a string")

    for member in team_members:
        member_data = parse_member(member)
        new_member = StudentInCommand(
            surname=member_data['surname'],
            name=member_data['name'],
            patronymic=member_data['patronymic'],
            groupID=member_data['group_id'],
            requestID=new_request.id,
            commandID=1
        )
        db.session.add(new_member)

    if reserve_member:
        reserve_member_data = parse_member(reserve_member)
        new_reserve_member = StudentInCommand(
            surname=reserve_member_data['surname'],
            name=reserve_member_data['name'],
            patronymic=reserve_member_data['patronymic'],
            groupID=reserve_member_data['group_id'],
            requestID=new_request.id,
            commandID=1
        )
        db.session.add(new_reserve_member)

    db.session.commit()

    return jsonify({"success": True, "message": "Заявка на команду добавлена успешно"}), 200

import logging

@app.route('/api/get_requests', methods=['GET'])
def get_requests():
    user_id = session.get('user_id')
    if not user_id:
        logging.warning('Пользователь не авторизован')
        return jsonify({'error': 'Пользователь не авторизован'}), 401

    try:
        user = User.query.get(user_id)
        if not user:
            logging.warning(f'Пользователь с id {user_id} не найден')
            return jsonify({'error': 'Пользователь не найден'}), 404

        if user.roleID == 1:
            requests = Request.query.options(joinedload(Request.event), joinedload(Request.sportType), joinedload(Request.students)).all()
            logging.info(f'Администратор {user_id} запросил все заявки. Найдено {len(requests)} заявок.')
        else:
            requests = Request.query.filter_by(userID=user_id).options(joinedload(Request.event), joinedload(Request.sportType), joinedload(Request.students)).all()
            logging.info(f'Пользователь {user_id} запросил свои заявки. Найдено {len(requests)} заявок.')

        requests_list = [{
            'id': req.id,
            'team_name': req.teamName,
            'event_name': req.event.name if req.event else 'Не указано',
            'sport_type_name': req.sportType.name if req.sportType else 'Не указан',
            'gender': req.genderID,
            'status': req.status,
            'team_members': [{
                'surname': student.surname,
                'name': student.name,
                'patronymic': student.patronymic,
                'group': student.group.name if student.group else 'Не указана'
            } for student in req.students]
        } for req in requests]

        return jsonify({'requests': requests_list})
    except Exception as e:
        logging.error(f"Ошибка в get_requests: {e}")
        return jsonify({"success": False, "message": str(e)}), 500

    
@app.route('/api/update_team_members', methods=['POST'])
def update_team_members():
    data = request.get_json()
    request_id = data.get('request_id')
    team_members = data.get('team_members', [])

    try:
        db_request = Request.query.get(request_id)
        if not db_request:
            return jsonify({"success": False, "message": "Заявка не найдена"}), 404

        # Clear existing students
        StudentInCommand.query.filter_by(requestID=request_id).delete()

        # Add new students
        for member in team_members:
            parts = member.split()
            new_member = StudentInCommand(
                surname=parts[0] if len(parts) > 0 else '',
                name=parts[1] if len(parts) > 1 else '',
                patronymic=parts[2] if len(parts) > 2 else '',
                groupID=1,  # Assuming groupID is 1 for simplicity
                requestID=request_id,
                commandID=1  # Assuming commandID is 1 for simplicity
            )
            db.session.add(new_member)

        db.session.commit()
        return jsonify({"success": True, "message": "Игроки успешно обновлены"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/approve_request', methods=['POST'])
def approve_request():
    data = request.get_json()
    request_id = data.get('id')

    db_request = Request.query.get(request_id)
    if db_request:
        db_request.status = 'approved'
        db.session.commit()
        return jsonify({"success": True, "message": "Заявка одобрена"})
    else:
        return jsonify({"success": False, "message": "Заявка не найдена"})

@app.route('/api/reject_request/<int:request_id>', methods=['POST'])
def reject_request(request_id):
    request_to_reject = Request.query.get(request_id)
    if request_to_reject:
        request_to_reject.status = 'rejected'
        db.session.commit()
        return jsonify({"success": True, "message": "Заявка отклонена"}), 200
    else:
        return jsonify({"success": False, "message": "Заявка не найдена"}), 404

@app.route('/api/add_event', methods=['POST'])
def add_event():
    data = request.form
    required_fields = ['event_type', 'event_name', 'sport_type', 'description', 'event_date', 'event_time', 'location']

    if all(field in data for field in required_fields):
        try:
            # Проверка на существование мероприятия с таким же названием и датой
            existing_event = Event.query.filter_by(
                name=data['event_name'],
                date=datetime.strptime(data['event_date'], '%Y-%m-%d').date()
            ).first()

            if existing_event:
                return jsonify({'success': False, 'message': 'Мероприятие с таким названием и датой уже существует.'}), 400

            new_event = Event(
                name=data['event_name'],
                date=datetime.strptime(data['event_date'], '%Y-%m-%d').date(),
                description=data['description'],
                sportTypeID=int(data['sport_type']),
                time=datetime.strptime(data['event_time'], '%H:%M').time(),
                eventTypeID=int(data['event_type']),
                placeID=int(data['location'])
            )

            db.session.add(new_event)
            db.session.commit()

            return jsonify({'success': True, 'message': 'Мероприятие успешно добавлено'})

        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500
    else:
        return jsonify({'success': False, 'message': 'Отсутствуют обязательные поля'}), 400

@app.route('/api/get_events', methods=['GET'])
def get_events():
    try:
        events = Event.query.options(joinedload(Event.place)).all()
        events_list = [{
            'id': event.id,
            'name': event.name,
            'date': event.date.isoformat() if event.date else None,
            'time': event.time.isoformat() if event.time else None,
            'description': event.description,
            'imageURL': event.imageURL,
            'sportTypeID': event.sportTypeID,
            'place': event.place.name if event.place else 'Не указано'
        } for event in events]

        return jsonify({'events': events_list})
    except Exception as e:
        return jsonify({'error': 'Ошибка при получении мероприятий'}), 500

@app.route('/api/add_media', methods=['POST'])
def add_media():
    title = request.form['title']
    mediaUrl = request.form['mediaUrl']
    sportTypeID = request.form['sportTypeID']
    new_media = Media(title=title, mediaUrl=mediaUrl, sportTypeID=sportTypeID)
    db.session.add(new_media)
    db.session.commit()
    return jsonify({"success": True, "message": "Медиа добавлено успешно"}), 200

@app.route('/api/get_media', methods=['GET'])
def get_media():
    media = Media.query.all()
    return jsonify({'media': [{'id': m.id, 'title': m.title, 'mediaUrl': m.mediaUrl, 'sportTypeID': m.sportTypeID} for m in media]})

@app.route('/api/add_physorg', methods=['POST'])
def add_physorg():
    try:
        surname = request.form['surname']
        name = request.form['name']
        patronymic = request.form['patronymic']
        gender_name = request.form['gender']
        course = request.form['course']
        group_name = request.form['group']
        login = request.form['login']
        password = request.form['password']

        existing_user = User.query.filter_by(login=login).first()
        if existing_user:
            return jsonify({"success": False, "message": "Пользователь с таким логином уже существует"}), 400

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        gender_id = 1 if gender_name == 'female' else 2

        group_record = Group.query.filter_by(name=group_name).first()
        if group_record is None:
            return jsonify({"success": False, "message": f"Указанная группа '{group_name}' не найдена в базе данных"}), 400

        group_id = group_record.id

        new_user = User(
            roleID=2,
            surname=surname,
            name=name,
            patronymic=patronymic,
            login=login,
            password=hashed_password,
            genderID=gender_id,
            groupID=group_id
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"success": True, "message": "Физорг успешно добавлен"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/api/get_groups', methods=['GET'])
def get_groups():
    groups = Group.query.all()
    groups_list = [{'id': group.id, 'name': group.name} for group in groups]
    return jsonify({'groups': groups_list})

@app.route('/api/profile_picture', methods=['POST'])
def upload_profile_picture():
    if 'user_id' not in session:
        return jsonify({'error': 'Пользователь не авторизован'}), 401

    user_id = session['user_id']
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'Пользователь не найден'}), 404

    if 'profile_picture' not in request.files:
        return jsonify({'error': 'Файл не найден в запросе'}), 400

    file = request.files['profile_picture']
    if file.filename == '':
        return jsonify({'error': 'Не выбран файл'}), 400

    if file:
        try:
            img = Image.open(file.stream)
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            user.image = img_byte_arr
            db.session.commit()

            return jsonify({'success': True, 'message': 'Фото профиля обновлено'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/get_profile_picture/<int:user_id>', methods=['GET'])
def get_profile_picture(user_id):
    user = User.query.get(user_id)
    if not user or not user.image:
        return jsonify({'error': 'Фото профиля не найдено'}), 404

    return send_file(io.BytesIO(user.image), mimetype='image/png')

@app.route('/api/delete_profile_picture', methods=['POST'])
def delete_profile_picture():
    user_id = session.get('user_id')
    if user_id:
        user = db.session.get(User, user_id)
        user.image = None
        db.session.commit()
        return jsonify({"success": True, "message": "Фото профиля удалено успешно"}), 200
    return jsonify({"error": "Пользователь не найден"}), 404

@app.route('/add_award.php', methods=['POST'])
def add_award_route():
    name = request.form.get('award_name')
    recipient = request.form.get('recipient')
    image_file = request.files.get('award_image')

    if not image_file or image_file.filename == '':
        return jsonify({'error': 'Фото не выбрано'}), 400

    try:
        # Сохраняем изображение и получаем его URL
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

        unique_filename = f"award_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        image_file.save(save_path)
        image_url = f"static/uploads/{unique_filename}"

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    new_award = Award(name=name, recipient=recipient, imageURL=image_url)
    db.session.add(new_award)
    db.session.commit()

    return jsonify({'success': True, 'message': 'Награда добавлена успешно'}), 200

@app.route('/api/delete_award', methods=['POST'])
def delete_award():
    data = request.get_json()
    award_id = data.get('id')
    award = Award.query.get(award_id)
    if award:
        db.session.delete(award)
        db.session.commit()
        return jsonify({"success": True, "message": "Награда успешно удалена"})
    else:
        return jsonify({"success": False, "message": "Награда не найдена"})

@app.route('/api/update_statistics', methods=['POST'])
def update_statistics():
    data = request.get_json()
    event_id = data.get('event_id')
    first_place_id = data.get('first_place')
    second_place_id = data.get('second_place')
    third_place_id = data.get('third_place')

    # Обновление статистики для команды, занявшей первое место
    update_team_statistics(first_place_id, 3)

    # Обновление статистики для команды, занявшей второе место
    update_team_statistics(second_place_id, 2)

    # Обновление статистики для команды, занявшей третье место
    update_team_statistics(third_place_id, 1)

    return jsonify({'success': True, 'message': 'Результаты успешно обновлены'})

@app.route('/api/get_statistics', methods=['GET'])
def get_statistics():
    statistics = db.session.query(Command.name, TeamStatistics.wins, TeamStatistics.losses, TeamStatistics.activities).join(TeamStatistics).all()
    stats_list = [{
        'name': stat.name,
        'wins': stat.wins,
        'losses': stat.losses,
        'activities': stat.activities
    } for stat in statistics]
    return jsonify({'statistics': stats_list})

@app.route('/api/get_commands', methods=['GET'])
def get_commands():
    commands = db.session.query(Command).join(TeamStatistics).order_by(
        desc(TeamStatistics.wins + TeamStatistics.activities)
    ).all()

    commands_data = [{'id': command.id, 'name': command.name} for command in commands]

    return jsonify({'commands': commands_data})

@app.route('/api/get_physorgs', methods=['GET'])
def get_physorgs():
    physorgs = User.query.filter_by(roleID=2).all()
    physorgs_list = [{
        'id': physorg.id,
        'surname': physorg.surname,
        'name': physorg.name,
        'patronymic': physorg.patronymic
    } for physorg in physorgs]
    return jsonify({'physorgs': physorgs_list})

@app.route('/api/get_awards', methods=['GET'])
def get_awards():
    awards = Award.query.all()
    awards_list = [{'id': award.id, 'name': award.name} for award in awards]
    return jsonify({'awards': awards_list})

@app.route('/upload.php', methods=['POST'])
def upload_media():
    title = request.form.get('title')
    course_id = request.form.get('course')
    sport_type_id = request.form.get('sport_type')

    files = request.files.getlist('media_files[]')

    if not files or files[0].filename == '':
        return jsonify({'error': 'Файлы не выбраны'}), 400

    file_paths = []
    for file in files:
        if file:
            filename = secure_filename(file.filename)
            unique_filename = f"media_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_{filename}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(save_path)
            file_paths.append(f"static/uploads/{unique_filename}")

    for file_path in file_paths:
        new_media = Media(title=title, mediaUrl=file_path, sportTypeID=sport_type_id)
        db.session.add(new_media)

    db.session.commit()

    return jsonify({'success': True, 'message': 'Фото добавлены успешно'}), 200

@app.route('/api/delete_physorg', methods=['POST'])
def delete_physorg():
    data = request.get_json()
    physorg_id = data.get('id')
    physorg = User.query.get(physorg_id)
    if physorg:
        db.session.delete(physorg)
        db.session.commit()
        return jsonify({"success": True, "message": "Физорг успешно удален"})
    else:
        return jsonify({"success": False, "message": "Физорг не найден"})

@app.route('/api/delete_team', methods=['POST'])
def delete_team():
    data = request.get_json()
    team_id = data.get('id')
    team = Command.query.get(team_id)
    if team:
        db.session.delete(team)
        db.session.commit()
        return jsonify({"success": True, "message": "Команда успешно удалена"})
    else:
        return jsonify({"success": False, "message": "Команда не найдена"})

if __name__ == '__main__':
    if os.getenv('FLASK_ENV') != 'testing':
        update_user_password('admin', 'admin')

    app.run(debug=True)
