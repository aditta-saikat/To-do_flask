from flask import Flask, Blueprint, render_template, flash, url_for,redirect, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_paginate import Pagination, get_page_parameter



app = Flask(__name__)
app.config['SECRET_KEY'] = 'abc'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(150))

    def __init__(self, task):
        self.task = task



@app.route('/')
@app.route('/index' , methods=['POST' , 'GET'])
def index():
    if request.method == "POST":
        task = request.form["task"]
        data = User(task)
        db.session.add(data)
        db.session.commit()
        flash('Task added successfully', 'success')
        return redirect(url_for('index', values=User.query.all()))
     
    else:
       return render_template('index.html' , values=User.query.all())



@app.route('/delete/<int:todo_id>', methods=['GET'])
def delete(todo_id):
    task = User.query.get(todo_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        flash('Task deleted successfully', 'success')
    else:
        flash('Task not found', 'error')
    return redirect(url_for('index'))



@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == "POST":
        data = User.query.get(request.form['id'])
        if data:
            data.task = request.form['task']
            db.session.commit()
            flash('Task updated successfully', 'success')
        else:
            flash('Task not found', 'error')
        
        return redirect(url_for('index'))
   




if __name__ == "__main__":
    app.run(debug=True)