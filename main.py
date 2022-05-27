from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
from smtplib import SMTP_SSL
import os
from forms import UpdateForm

EMAIL = os.environ.get('EMAIL')
PASSWORD = os.environ.get('PASSWORD')


# initialize flask app and configure secret key
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')


# Initialize flask bootstrap
Bootstrap(app)

# Initialize and configure sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL'), 'sqlite:///projects.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Create Database model/table
class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.String(250), unique=False, nullable=False)
    img_url = db.Column(db.String(300), unique=False, nullable=False)
    git_url = db.Column(db.String(300), unique=False, nullable=False)
    identifiers = db.Column(db.String(300), unique=False, nullable=False)




def send_message(name, email, subject : str, message):
    msg = f"Subject: New Contact Mail - {subject.upper()} \n\n Name: {name} \n EMAIL: {email}\n{message}"
    with SMTP_SSL('smtp.gmail.com', port=465) as connection:
        connection.login(user=EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=EMAIL, to_addrs=EMAIL, msg=msg)
        connection.close()
    return True

@app.route('/')
def home_page():
    return render_template('index.html')


@app.route('/about')
def about_page():
    return render_template('about-us.html', title='About')


@app.route('/services')
def service_page():
    return render_template('services.html', title='Services')


@app.route('/portfolio')
def portfolio_page():
    projects = Projects.query.all()
    return render_template('portfolio.html', projects=projects) 

@app.route('/cv')
def cv_page():
    return send_from_directory(directory='static', path='cv/resume.pdf')
    # return redirect(request.referrer)  


@app.route('/contacts', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        if send_message(name=name, email=email, subject=subject, message=message):
            flash('successfully sent')
        else:
            flash('something went wrong')
        return redirect(url_for('contact_page'))
    return render_template('contact.html', title='Contact')


@app.route('/update', methods=['GET', 'POST'])
def update_page():
    form = UpdateForm()
    if form.validate_on_submit():
        new_project = Projects(
            name=form.name.data,
            description=form.description.data,
            img_url=form.img_url.data,
            git_url=form.git_url.data,
            identifiers=form.identifiers.data
        )
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('home_page'))
    return render_template('update.html', form=form)

db.create_all()

# if __name__ == '__main__':
#     # db.create_all()
#     app.run()
    