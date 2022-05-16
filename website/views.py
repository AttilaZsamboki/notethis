from hashlib import new
from sre_constants import SUCCESS
from flask import Blueprint, flash, jsonify, render_template, request, jsonify, session, redirect, url_for
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms.fields import DateField
from wtforms.validators import DataRequired
from wtforms import SubmitField

views = Blueprint('views', __name__)

# route to the home page
@views.route('/', methods=['GET'])
@login_required
def home():
    return render_template("home.html", user=current_user, current_page='home')


class InfoForm(FlaskForm):
    date = DateField('Date', format='%Y/%m/%d')

# route to notes
@views.route('/notes', methods=['GET', 'POST'])
@login_required
def notes():
    form = InfoForm()
    if form.validate_on_submit():
        session['date'] = form.date.data.strftime('%Y/%m/%d')

    if request.method == 'POST':
        note = request.form.get('note')
        date = request.form.get('date')

        if len(note) < 1:
            flash('Note is too short!', category='error')
        elif len(date) < 1:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('views.notes'))
        else:
            new_note = Note(data=note, date=datetime.strptime(date, "%Y-%m-%d"), user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            return redirect(url_for('views.notes'))
        
    return render_template("notes.html", form=form, user=current_user, current_page='notes')

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return redirect(url_for('views.notes'))
    return jsonify({})