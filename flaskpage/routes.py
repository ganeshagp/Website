from flask import render_template, request, flash, redirect, url_for    
from flask_login import login_user, current_user, logout_user, login_required, UserMixin
from PIL import Image
from flaskpage.forms import DeveloperForm, ClientForm, LoginForm, UpdateAccountForm
from flaskpage.models import Developer, Client
from flaskpage import app, db, bcrypt
import os
import secrets


@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():    
    return render_template('home.html',template_folder='templates')

@app.route('/developer', methods=['GET', 'POST'])
def developer():
    if current_user.is_authenticated:
        return redirect(url_for('home')) 
    form=DeveloperForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_developer = Developer(name=form.name.data, 
                                  email=form.email.data, 
                                  username=form.username.data,
                                  phone_number=form.phone_number.data,
                                  domain=form.domain.data,
                                  github_link=form.github_link.data,
                                  linkedin_link=form.linkedin_link.data,
                                  experience=form.experience.data,
                                  password=hashed_password)
        with app.app_context():
            db.session.add(new_developer)
            db.session.commit()
        
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('developer.html',template_folder='templates', form=form)

@app.route('/client', methods=['GET', 'POST'])
def client():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=ClientForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_client = Client(name=form.name.data, 
                            email=form.email.data,
                            username=form.username.data, 
                            phone_number=form.phone_number.data,
                            password=hashed_password)
        with app.app_context():
            db.session.add(new_client)
            db.session.commit()
        flash(f'Account created for {form.name.data}!', 'success')
        return redirect(url_for('home'))
    
    return render_template('client.html',template_folder='templates',form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print(current_user)
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form=LoginForm()
    if form.validate_on_submit():
        dev = Developer.query.filter_by(username=form.username.data).first()
        client = Client.query.filter_by(username=form.username.data).first()
        password_dev = None
        password_client = None
        if dev:
            print('dev found')
            password_dev = dev.password
        if client:
            print('client found')
            password_client = client.password
        if dev is None and client is None:
            flash('That username is not registered. Please register first.','danger')
            return redirect(url_for('home'))
        if dev:
            if bcrypt.check_password_hash(password_dev, form.password.data):
                login_user(dev, remember=form.remember.data)
                flash('You have been logged in!', 'success')
                return redirect(url_for('accountdetails'))
        elif client:
            if bcrypt.check_password_hash(password_client, form.password.data):
                login_user(client, remember=form.remember.data,force=True)
                print(login_user(client, remember=form.remember.data,force=True))
                print(current_user)
                flash('You have been logged in!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Login Unsuccessful. Please check username and password', 'danger')
                return redirect(url_for('login'))

        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')

    return render_template('login.html',template_folder='templates',form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('Logged out Successfully','success')
    return redirect(url_for('home'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn,".jpg")
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/accountdetails', methods=['GET', 'POST'])
def accountdetails():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('accountdetails'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('accountdetails.html',template_folder='templates', title='Account', image_file=image_file, form=form)
