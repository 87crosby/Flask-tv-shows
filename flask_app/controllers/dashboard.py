import re

from flask.helpers import flash
from flask_app import app
from flask import render_template, redirect, session, request
from flask_bcrypt import Bcrypt
from flask_app.models.users import User
from flask_app.models.shows import Show

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')

    shows = Show.get_all_shows()

    return render_template('dashboard.html', shows = shows)

@app.route('/shows/new')
def new_show():
    if 'user_id' not in session:
        return redirect('/')

    return render_template('new_show.html')

@app.route('/shows/create', methods = ['POST'])
def add_show():
    info = {
            'name' : request.form['name'],
            'network' : request.form['network'],
            'release_date' : request.form['release_date'],
            'description' : request.form['description'],
            'users_id' : session['user_id']
        }
    if Show.validate_show(request.form):
        Show.create_show(info)
        return redirect('/dashboard')
    return redirect('/shows/new')

@app.route('/shows/<int:show_id>')
def view_show(show_id):
    data = {'id': show_id}
    show_info = Show.get_shows_by_id(data)
    
    return render_template('show_info.html', show_info = show_info)

@app.route('/shows/edit/<int:show_id>')
def edit_show(show_id):
    data = {'id': show_id}
    show_info = Show.get_shows_by_id(data)
    if session['user_id'] != show_info['users_id']:
        return redirect('/dashboard')
    
    return render_template('show_edit.html', show_info = show_info)

@app.route('/shows/update/<int:show_id>', methods = ['POST'])
def update_show_info(show_id):
    if Show.validate_show(request.form):
        data = {
            'id' : show_id,
            'name' : request.form['name'],
            'description' : request.form['description'],
            'network' : request.form['network'],
            'release_date' : request.form['release_date'],
            'users_id' : session['user_id']
        }
        Show.update_show(data)
        return redirect('/dashboard')
    return redirect(f'/shows/edit/{show_id}')

@app.route('/shows/delete/<int:show_id>')
def delete_tv_show(show_id):
    data = {'id': show_id}
    show_info = Show.get_shows_by_id(data)
    if session['user_id'] != show_info['users_id']:
        return redirect('/dashboard')
    Show.delete_show(data)
    return redirect('/dashboard')
