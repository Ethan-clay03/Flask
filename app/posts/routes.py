from flask import render_template
from app.posts import bp

@bp.route('/')
def index():
    return render_template('posts/index.html')
