from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from . import db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    
    event = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', event=event)