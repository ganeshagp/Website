from flask import Flask,render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
import openpyxl

app = Flask(__name__)
app.config['SECRET_KEY']='secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app) 


class Developer(db.Model):
    name=db.Column(db.Integer,nullable=False)
    email=db.Column(db.String(100),nullable=False)
    phone_number=db.Column(db.Integer,nullable=False,primary_key=True)
    domain=db.Column(db.String(100),nullable=False)
    github_link=db.Column(db.String(200),nullable=False)
    linkedin_link=db.Column(db.String(200),nullable=False)
    experience=db.Column(db.Integer)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Developer %r>' % self.name

class Client(db.Model):
    name=db.Column(db.Integer,nullable=False)
    email=db.Column(db.String(100),nullable=False)
    phone_number=db.Column(db.Integer,nullable=False,primary_key=True)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return '<Client %r>' % self.name

@app.route('/', methods=['GET', 'POST'])
def gfg():
    return render_template('index.html',template_folder='templates')

@app.route('/developer', methods=['GET', 'POST'])
def developer(): 
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('number')
        domain = request.form.get('domain')
        github_link = request.form.get('glink')
        linkedin_link = request.form.get('llink')
        experience = request.form.get('experience')

        dev=Developer.query.filter_by(phone_number=phone_number).first()
        if dev:
            return redirect(url_for("developer"))

        with app.app_context():
            new_dev = Developer(name=name, email=email, phone_number=phone_number, domain=domain, github_link=github_link, linkedin_link=linkedin_link, experience=experience)
            db.session.add(new_dev)
            db.session.commit()
        
        wb = openpyxl.load_workbook('Developers.xlsx')
        sheet = wb.active
        sheet.append([name, email, phone_number, domain, github_link, linkedin_link, experience])
        wb.save('Developers.xlsx')

    return render_template('index1.html',template_folder='templates')

@app.route('/client', methods=['GET', 'POST'])
def client():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone_number = request.form.get('number')

        client=Client.query.filter_by(phone_number=phone_number).first()
        if client:
            flash('Phone number already exists')
            return redirect(url_for("client"))
        

        with app.app_context():
            new_client = Client(name=name, email=email, phone_number=phone_number)
            db.session.add(new_client)
            db.session.commit()

        wb = openpyxl.load_workbook('Clients.xlsx')
        sheet = wb.active
        sheet.append([name, email, phone_number])
        wb.save('Clients.xlsx')
    
    return render_template('index2.html',template_folder='templates')


if __name__ == '__main__':
    app.run()
    
