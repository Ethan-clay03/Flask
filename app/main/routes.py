from flask import render_template
from app.main import bp
import datetime

@bp.route('/')
def index():
    date=datetime.datetime.now()
    tomorrow_object = date + datetime.timedelta(days=1)
    return render_template('index.html', today = date.strftime('%Y-%m-%d'), tomorrow = tomorrow_object.strftime('%Y-%m-%d'))