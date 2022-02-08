from flask import Blueprint, render_template

bp = Blueprint('homepage', __name__, url_prefix='/')


@bp.route('/')
def introduction():
    return render_template('home/homepage.html', show_header=True)
