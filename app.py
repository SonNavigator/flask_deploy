from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from covid import covid_obj
import random
from datetime import datetime

from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

login_manager = LoginManager() # Login manage for flask-login
login_manager.init_app(app)

# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = "swru9sor39isfsg"


# User.query.all()
# User.query.filter_by(username="James").first()
class User(UserMixin, db.Model):
    """Create columns to store our data"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), unique=True, nullable=False)
    password = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(60), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


class Course(db.Model):
    """Create this course table to store course details"""

    id = db.Column(db.Integer,
                    primary_key=True)
    title = db.Column(db.String(120),
                      nullable=False)
    description = db.Column(db.Text,
                            nullable=False)
    price = db.Column(db.Integer,
                      nullable=False)
    duration = db.Column(db.Integer,
                         nullable=False)
    instructor = db.Column(db.String(80),
                           nullable=False)
    date_created = db.Column(db.DateTime(),
                             default=datetime.utcnow)


# Only test
@app.route('/test')
def home_test():

    name = "Son"
    return render_template("home-test.html", name=name)  


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/script')
def test_script():
    return render_template("test-script.html")


@app.route('/covid-table')
def covid_table():
    """Return covid19 data to show in a table"""

    covid_data = covid_obj

    return render_template("covid-table.html", covid_data=covid_data)


@app.route('/covid-dashboard')
def covid_dashboard():
    """Return covid19 data to display in a dashboard"""

    data = covid_obj
    confirmed_case = data["Confirmed"]
    recovered_case = data["Recovered"]
    hospitalized_case = data["Hospitalized"]
    new_deaths_case = data["NewDeaths"]
    new_confirmed_case = data["NewConfirmed"]
    last_updated = data["UpdateDate"]

    return render_template("covid-dashboard.html", confirmed_case=confirmed_case,
                                                    recovered_case=recovered_case,
                                                    hospitalized_case=hospitalized_case,
                                                    new_deaths_case=new_deaths_case,
                                                    new_confirmed_case=new_confirmed_case,
                                                    last_updated=last_updated)



@app.route('/random-menu')
def random_menu():

    random_list = ["กะเพราหมู", "ไข่เจียวหมูสับ", "หมูทอดกระเทียม", "ก๋วยเตี๋ยว", "ผัดซีอิ๊ว"]
    menu_data = random.choice(random_list)

    return render_template("random-menu.html", menu_data=menu_data)


@app.route('/create', methods=["GET", "POST"])
def create():
    """Create a new course"""

    # Check if method that being sent is "POST"
    if request.method == "POST":

        # Create variables to get input attributes from form
        title = request.form["title"]
        instructor = request.form["instructor"]
        price = request.form["price"]
        duration = request.form["duration"]
        description = request.form["description"]

        # Create an object, then pass variables into the class(Course)
        obj = Course(title=title,
                     instructor=instructor,
                     price=price,
                     duration=duration,
                     description=description)

        # Add the object to SQlAlchemy session
        # then submit it into our database
        db.session.add(obj)
        db.session.commit()

        # Redirect to home page after submitting form
        return redirect(url_for('home'))
                
    return render_template("create-course.html")



@app.route('/')
@login_required
def home():
    """Retrieve all courses from the database"""

    all_courses = Course.query.all()

    return render_template("home.html", all_courses=all_courses) 

    

@app.route('/post-details/<int:id>')
def post_details(id):
    """Retrieve only one course(by id)"""

    single_course = Course.query.get(id)

    return render_template("post-details.html", single_course=single_course)


@app.route('/update/<int:id>', methods=["GET", "POST"])
def update(id):
    """Update an existing post"""

    data = Course.query.get(id)

    # Check if method that being sent is "POST"
    if request.method == "POST":

        # Create variables to get input attributes from form
        title = request.form["title"]
        instructor = request.form["instructor"]
        price = request.form["price"]
        duration = request.form["duration"]
        description = request.form["description"]

        data.title = title
        data.instructor = instructor
        data.price = price
        data.duration = duration
        data.description = description

        # Submit an updated post into the database
        db.session.commit()

        # Redirect to home page after finishing update
        return redirect(url_for('home'))

    return render_template('update.html', data=data)


@app.route('/delete/<int:id>', methods=["GET", "POST"])
def delete(id):
    """Delete a post"""

    data = Course.query.get(id)

    db.session.delete(data)
    db.session.commit()

    return redirect(url_for('home'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.
    form = LoginForm()
    if form.validate_on_submit():
        # Login and validate the user.
        # user should be an instance of your `User` class
        login_user(user)

        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)


@app.route("/settings")
@login_required
def settings():
    pass


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(somewhere)


if __name__ =="__main__":
    app.run(debug=True)
