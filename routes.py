import os
from flask import Blueprint, jsonify, request, session, render_template
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Command, Event, ScheduleSections, News, Award, SportType, MeasureType, Place, Statistic, Notification, Registration, Feedback, Partners

api = Blueprint('api', __name__)

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_login = data.get('login')
    password = data.get('password')

    user = User.query.filter_by(login=user_login).first()
    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return jsonify({'success': True, 'message': 'Login successful'})
    else:
        return jsonify({'success': False, 'message': 'Invalid login or password'}), 401

@api.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)
    return jsonify({'success': True, 'message': 'Logout successful'})

@api.route('/update_profile', methods=['POST'])
def update_profile():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'success': False, 'message': 'User not authenticated'}), 401

    user = User.query.get(user_id)
    if user:
        user.full_name = request.form.get('full_name')
        user.date_of_birth = request.form.get('date_of_birth')
        user.profile_picture = request.form.get('profile_picture')
        db.session.commit()
        return jsonify({'success': True, 'message': 'Profile updated successfully'})
    else:
        return jsonify({'success': False, 'message': 'User not found'}), 404

@api.route('/upload', methods=['POST'])
def upload():
    files = request.files.getlist('media_files')
    upload_dir = 'static/uploads/'
    for file in files:
        file.save(os.path.join(upload_dir, file.filename))
    return jsonify({'success': True, 'message': 'Media uploaded successfully'})

@api.route('/add_command', methods=['POST'])
def add_team():
    data = request.form
    new_team = Command(
        name=data.get('team_name'),
        course=data.get('course'),
        sport_type=data.get('sport_type'),
        gender=data.get('gender'),
        team_members=data.get('team_members'),
        reserve_member=data.get('reserve_member')
    )
    db.session.add(new_team)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Team added successfully'})

@api.route('/add_physorg', methods=['POST'])
def add_physorg():
    data = request.form
    new_physorg = User(
        last_name=data.get('last_name'),
        first_name=data.get('first_name'),
        middle_name=data.get('middle_name'),
        gender=data.get('gender'),
        course=data.get('course'),
        group=data.get('group'),
        login=data.get('login'),
        password=generate_password_hash(data.get('password'), method='pbkdf2:sha256')
    )
    db.session.add(new_physorg)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Physorg added successfully'})

@api.route('/add_event', methods=['POST'])
def add_event():
    data = request.form
    new_event = Event(
        event_type=data.get('event_type'),
        sport_type=data.get('sport_type'),
        gender=data.get('gender'),
        event_name=data.get('event_name'),
        event_date=data.get('event_date'),
        event_time=data.get('event_time'),
        location=data.get('location')
    )
    db.session.add(new_event)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Event added successfully'})

@api.route('/edit_schedule', methods=['POST'])
def edit_schedule():
    data = request.form
    schedule = ScheduleSections.query.get(1)  # Предполагается, что у вас есть ID расписания
    if schedule:
        schedule.sport_type_schedule = data.get('sport_type_schedule')
        schedule.training_date = data.get('training_date')
        schedule.training_time = data.get('training_time')
        schedule.coach_name = data.get('coach_name')
        db.session.commit()
        return jsonify({'success': True, 'message': 'Schedule updated successfully'})
    else:
        return jsonify({'success': False, 'message': 'Schedule not found'}), 404

@api.route('/add_news', methods=['POST'])
def add_news():
    data = request.form
    files = request.files.getlist('news_image')
    new_news = News(
        title=data.get('news_title'),
        content=data.get('news_content'),
        image=files[0].filename if files else None  # Проверка на наличие файлов
    )
    db.session.add(new_news)
    db.session.commit()
    return jsonify({'success': True, 'message': 'News added successfully'})

@api.route('/add_award', methods=['POST'])
def add_award():
    data = request.form
    files = request.files.getlist('award_image')
    new_award = Award(
        name=data.get('award_name'),
        recipient=data.get('recipient'),
        image=files[0].filename if files else None  # Проверка на наличие файлов
    )
    db.session.add(new_award)
    db.session.commit()
    return jsonify({'success': True, 'message': 'Award added successfully'})

@api.route('/', methods=['GET'])
def home():
    return render_template('index.html')
