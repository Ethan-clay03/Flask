# utils.py

import os
from flask import current_app
from datetime import time

def allowed_image_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def generate_time_options():
    time_options = []
    for hour in range(24):
        for minute in range(0, 60, 5):
            formatted_time = time(hour, minute).strftime('%H:%M')
            time_options.append(formatted_time)
    return time_options