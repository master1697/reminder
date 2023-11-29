from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

    

class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    name = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    phone = db.Column(db.String(100))


@app.route('/')
def index():
    #to show all the todos
    all_reminders = Reminder.query.all()
    print(all_reminders)
    return render_template('base.html', all_reminders = all_reminders)

@app.route("/add", methods=["POST"])
def add():
    #add a new item to the todo list
    print("hello")
    title = request.form.get("title")
    name = request.form.get("name")
    local_date = request.form.get("date")
    date = datetime.strptime(local_date, '%Y-%m-%dT%H:%M')
    phone = request.form.get("phone")
    new_reminder = Reminder(title = title, name = name, date = date, phone = phone, complete = False)
    db.session.add(new_reminder)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:reminder_id>")
def update(reminder_id):
    #update status of an item in the todo list
    reminder = Reminder.query.filter_by(id=reminder_id).first()
    reminder.complete = not reminder.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:reminder_id>")
def delete(reminder_id):
    #delete an item in the todo list
    reminder = Reminder.query.filter_by(id=reminder_id).first()
    db.session.delete(reminder)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()


    app.run(debug=True)
