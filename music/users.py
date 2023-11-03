from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Ticket
from . import db
from flask_login import login_required, current_user

userbp = Blueprint('user', __name__, url_prefix='/user')

@userbp.route('/bookinghistory')
@login_required
def bookinghistory():
  print('Method type: ', request.method)
  tickets = db.session.query(Ticket).filter(Ticket.user_id == current_user.id).all()
  return render_template('user/bookinghistory.html', tickets = tickets)

