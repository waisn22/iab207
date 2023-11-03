from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from .forms import RegisterForm, LoginForm
from . import db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    
    registerform = RegisterForm
    loginform = LoginForm

    event = db.session.scalars(db.select(Event)).all()
    return render_template('index.html', event=event, register_form = registerform, login_form = loginform)
@bp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        event = db.session.scalars(db.select(Event).where(Event.name.like(query)))
        return render_template('index.html', event=event)
    else:
        return redirect(url_for('main.index'))
@bp.route('/category') 
def category():
    category = request.args.get('category')

    if category:
        query = "%" + category + "%"
        event = db.session.scalars(db.select(Event).where(Event.category.like(query)))
        return render_template('index.html', event=event)
    else:
        return redirect(url_for('main.index'))
@bp.route('/price') 
def price():
    # Get the 'price' parameter from the request
    price_range = request.args.get('price')

    if price_range:
        # Split the 'price_range' into two values: min_price and max_price
        min_price, max_price = map(int, price_range.split('-'))

        # Perform a search for all figures between min_price and max_price (inclusive)
        event = db.session.scalars(db.select(Event).where(Event.price >= min_price, Event.price <= max_price))
        return render_template('index.html', event=event)
    else:
        return redirect(url_for('main.index'))
@bp.route('/ticketquantity') 
def ticketquantity():
    # Get the 'price' parameter from the request
    ticketrange = request.args.get('ticketquantity')

    if ticketrange:
        # Split the 'price_range' into two values: min_price and max_price
        min_ticket, max_ticket = map(int, ticketrange.split('-'))

        # Perform a search for all figures between min_price and max_price (inclusive)
        event = db.session.scalars(db.select(Event).where(Event.ticketquantity >= min_ticket, Event.ticketquantity <= max_ticket))
        return render_template('index.html', event=event)
    else:
        return redirect(url_for('main.index'))
    




