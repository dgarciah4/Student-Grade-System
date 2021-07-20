from flask import Flask, render_template, request
import sqlite3
import random
import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

basedir = os.path.abspath(os.path.dirname(__file__))
## env = hw3flaskenv
app = Flask (__name__)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRAC_MODIFICATIONS']=False

db=SQLAlchemy(app)

## Model Structure to create the Table for each Student
class Student(db.Model):
    __tablename__="student"

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String(100))
    grade=db.Column(db.Integer)

    def __init__(self, id, name, grade):
        self.name=name
        self.grade=grade
        self.id=id

@app.route('/')
def home ():
    return render_template ('home.html')

## Redirection to Student Form Page
@app.route('/student_form', methods = ["POST", "GET" ])
def student_form ():

## Create Each User with a corresponding ID
    if request.method == 'POST':
        data = request.form
        idSuffix = random.randint(11111,99999)
        id = idSuffix
        name = data["name"]
        grade = data["grade"]


        new_data = Student(id, name, grade)
        db.session.add(new_data)
        db.session.commit()

        all_students = Student.query.all()
        return render_template('results.html',all_students = all_students)

    return render_template ('student_form.html')
## Lists all contents of the table and redirects to results page
@app.route('/list_all', methods = ['POST', 'GET'])
def list_all ():
    all_students = Student.query.all()
    return render_template ('results.html',all_students = all_students)

## Lists only passing students that meet a passing score criteria
@app.route('/list_pass', methods = ['POST', 'GET'])
def list_pass ():
    all_students = Student.query.filter(Student.grade>=85)
    return render_template('results.html',all_students = all_students)

## Deletes student depending on user ID specified
@app.route('/delete_student', methods = ['POST', 'GET'])
def delete_student ():
    if request.method == "POST":
        select_student = request.form.get("student.id")
        Student.query.filter(Student.id==select_student).delete()
        db.session.commit()

    return render_template('results.html',all_students= Student.query.all())


@app.route('/results', methods = ['POST', 'GET'])
def results ():

    return render_template('results.html')

@app.errorhandler(404)
def page_not_found (e):
    return render_template ('404.html'),404

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
