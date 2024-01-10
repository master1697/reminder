from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
import smtplib
import sys


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config["SECRET_KEY"] = "abc"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

CARRIERS = {
    "att": "@mms.att.net",
    "tmobile": "@tmomail.net",
    "verizon": "@vtext.com",
    "sprint": "@messaging.sprintpcs.com"
}

EMAIL = "remindmenotif@gmail.com"
PASSWORD = "xkzgnnyogyoakduo"

    
class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), unique=True,
                         nullable=False)
    password = db.Column(db.String(250),
                         nullable=False)
    
class Reminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    name = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    phone = db.Column(db.String(100))
    user_id = db.Column(db.Integer)

@login_manager.user_loader
def loader_user(user_id):
    return Users.query.get(user_id)

@app.route("/")
def home():
    # Render home.html on "/" route
    return render_template("home.html")


@app.route('/base')
def index():
    #to show all the todos
    all_reminders = Reminder.query.filter_by(user_id = current_user.get_id())
    print(all_reminders)
    return render_template('base.html', all_reminders = all_reminders)

@app.route('/register', methods=["GET", "POST"])
def register():
# If the user made a POST request, create a new user
    if request.method == "POST":
        user = Users(username=request.form.get("username"),
                    password=request.form.get("password"))
        # Add the user to the database
        db.session.add(user)
        # Commit the changes made
        db.session.commit()
        # Once user account created, redirect them
        # to login route (created later on)
        return redirect(url_for("login"))
    # Renders sign_up template if user made a GET request
    return render_template("sign_up.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    # If a post request was made, find the user by 
    # filtering for the username
    if request.method == "POST":
        user = Users.query.filter_by(
            username=request.form.get("username")).first()
        # Check if the password entered is the 
        # same as the user's password
        if user.password == request.form.get("password"):
            # Use the login_user method to log in the user
            login_user(user)
            print("login times", file=sys.stderr)
            print(current_user.get_id(), file=sys.stderr)
            return redirect(url_for("home"))
        # Redirect the user back to the home
        # (we'll create the home route in a moment)
        print(current_user.get_id(), file=sys.stderr)
    return render_template("login.html")

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))

@app.route("/add", methods=["POST"])
def add():
    #add a new item to the todo list
    print("it's below this")
    print(current_user.get_id(), file=sys.stderr)
    title = request.form.get("title")
    name = request.form.get("name")
    local_date = request.form.get("date")
    date = datetime.strptime(local_date, '%Y-%m-%dT%H:%M')
    phone = request.form.get("phone")
    carrier = request.form.get("phone")
    message = "hey"
    user_id = current_user.get_id()
    new_reminder = Reminder(title = title, name = name, date = date, phone = phone, user_id = user_id, complete = False)
    db.session.add(new_reminder)
    db.session.commit()
    # recipient = phone + CARRIERS[carrier]
    # auth = (EMAIL, PASSWORD)
 
    # server = smtplib.SMTP("smtp.gmail.com", 587)
    # server.starttls()
    # server.login(auth[0], auth[1])
 
    # server.sendmail(auth[0], recipient, message)
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
    # if len(sys.argv) < 4:
    #     print(f"Usage: python3 {sys.argv[0]} <PHONE_NUMBER> <CARRIER> <MESSAGE>")
    #     sys.exit(0)
    # phone_number = sys.argv[1]
    # carrier = sys.argv[2]
    # message = sys.argv[3]
    # print(phone_number, EMAIL, PASSWORD)
 


    app.run(debug=True)