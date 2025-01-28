# utils.py

import os
from flask import current_app
from werkzeug.utils import secure_filename


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_booking_image(file):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(os.path.join(current_app.config['BOOKING_IMAGE_UPLOADS'], filename))

        # Ensure the directory exists before saving images
        os.makedirs(os.path.join(current_app.config['BOOKING_IMAGE_UPLOADS']), exist_ok=True)
        
        print(f"File Path: {file_path}")


        file.save(file_path)
        return filename
    else:
        return None
