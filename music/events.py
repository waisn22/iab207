import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Event, Comment, Ticket
from .forms import EventForm, CommentForm, TicketForm
from . import db
import os
from werkzeug.utils import secure_filename
#additional import:
from flask_login import login_required, current_user

eventbp = Blueprint('event', __name__, url_prefix='/events')

@eventbp.route('/<id>', methods=['GET','POST'])
def show(id):
  print('Method type: ', request.method)
  event = db.session.scalar(db.select(Event).where(Event.id==id))
  totaltickets = event.ticketquantity - event.boughttickets
  if (totaltickets == 0):
    event.status = "Sold Out"
  ticket_form = TicketForm()
  comment_form = CommentForm()


  if (ticket_form.validate_on_submit()==True):
    if (totaltickets >= ticket_form.quant_tickets.data):
      event.boughttickets += ticket_form.quant_tickets.data
      for i in range(ticket_form.quant_tickets.data):
        order_number = str(uuid.uuid4())
        ticket = Ticket(order_number = order_number, price = event.price, event_id=event.id, event_name = event.name, 
                        user=current_user)
        db.session.add(ticket)
        flash(f'Successfully Booked Ticket {i+1}: Order No {order_number}', "success")
      
    
      db.session.commit()
      return redirect(url_for('event.show', id=id))
    else:
      flash(f'Requested number of tickets unavailable please try again')
    


  return render_template('event/show.html', event = event, ticket_form = ticket_form, comment_form = comment_form, totaltickets = totaltickets)

@eventbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    #Add Creator ID
    event_date = form.date.data
    start_datetime = datetime.combine(event_date, form.start_time.data)
    end_datetime = datetime.combine(event_date, form.end_time.data)
    event = Event(creatorid= current_user.id,name=form.name.data,description=form.description.data,venue=form.location.data,date=form.date.data,
                  starttime=start_datetime,endtime=end_datetime, 
                  image=db_file_path,price=form.price.data,category=form.category.data,status=form.status.data,
                  ticketquantity=form.ticketquantity.data, boughttickets = 0)
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.commit()
    flash('Successfully created new event', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('event.create'))
  return render_template('event/create.html', form=form)

def check_upload_file(form):
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/img
  upload_path = os.path.join(BASE_PATH, 'static/img', secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/img/' + secure_filename(filename)
  #save the file and return the db upload path
  fp.save(upload_path)
  return db_upload_path

@eventbp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    #get the event object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data, event_id=event.id,
                        user=current_user) 
      #here the back-referencing works - comment.event is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      #flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')  
      # print('Your comment has been added', 'success') 
    # using redirect sends a GET request to event.show
    return redirect(url_for('event.show', id=id))