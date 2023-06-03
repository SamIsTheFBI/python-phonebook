import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'your secret key'
db.init_app(app)

class Contact(db.Model):
    name = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, unique=True, primary_key=True)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    contacts = db.session.execute(db.select(Contact).order_by(Contact.name)).scalars()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=('GET', 'POST'))
def add_contact():
    if request.method == 'POST':
        name = request.form['name']
        number = request.form['number']
        exists = db.session.query(Contact.number).filter_by(number=number).first() is not None

        if not name:
            flash('Name is required!')
        elif not number:
            flash('Phone number is required!')
        elif exists:
            flash('Phone number already exists!')
        else:
            contact = Contact(
                name = request.form['name'],
                number = request.form['number'],
            )
            db.session.add(contact)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/<int:id>')
def contact_details(number):
    contact = db.get_or_404(Contact, number)
    return render_template('contact_details.html', contact=contact)
