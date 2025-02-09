# utils.py

from flask import current_app
from datetime import time, datetime
from datetime import datetime 

def allowed_image_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_time_options():
    time_options = []
    for hour in range(24):
        for minute in range(0, 60, 5):
            formatted_time = time(hour, minute).strftime('%H:%M')
            time_options.append(formatted_time)
    return time_options


def calculate_discount(date):
    depart_date = datetime.strptime(date, '%Y-%m-%d')
    today = datetime.now()
    days_away = (depart_date - today).days

    if 80 <= days_away <= 90:
        return 25, days_away
    elif 60 <= days_away <= 79:
        return 15, days_away
    elif 45 <= days_away <= 59:
        return 10, days_away
    else:
        return 0, days_away
    

def pretty_time(unformatted_time, to_12_hour=True):
    if not isinstance(unformatted_time, (datetime, time)):
        unformatted_time = datetime.strptime(unformatted_time, "%H:%M:%S")
    
    # Format the time
    if to_12_hour:
        formatted_time = unformatted_time.strftime("%I:%M %p")
    else:
        formatted_time = unformatted_time.strftime("%H:%M")
    
    return formatted_time
