# __author__ = "Dan-Gabriel Pintoiu"
# __copyright__ = "Copyright (C) 2020 Dan-Gabriel Pintoiu"
# __license__ = "Public Domain"

from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, current_user, LoginManager, login_user, logout_user
from sqlalchemy import func
from datetime import datetime

# create a date entry variable to be used as default value in the db table 'employee'
# in case the user doesn't add it when submitting the form
today = datetime.today()
month = today.strftime("%B")
day = today.strftime("%d")
defaultDate = month + "-" + day

app = Flask(__name__)
app.config['SECRET_KEY'] = "bF-xcay-xffp-x0bc--xb53xeaxfc8-xc8y-xcb-xe4"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///posts.db"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# table models
class employee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    dept = db.Column(db.String(50), nullable = False)
    date = db.Column(db.String(50), nullable = False, default = defaultDate)
    created_date = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return 'Employee ' + str(self.id)

class empCount(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    max = db.Column(db.Integer, nullable = False, default = 0)

    def __repr__(self):
        return 'Employee ' + str(self.id)

class admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

# create an empty database at runtime based on the above models, if it's not already created
db.create_all()
db.session.commit()

# create helping lists to iterate over 
all_employees = []
monthList = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# function that returns the max employee counter; the function will be called by multiple flask routes
# if there isn't a max value set up, returns '0' as the default value
def maxEmp():
    employeeCounter = ""
    maxEmpCount = empCount.query.with_entities(empCount.max).all()
    for character in str(maxEmpCount):
        if character.isdigit():
            employeeCounter += character
    try:
        employeeCounter = int(employeeCounter)
    except:
        employeeCounter = 0

    return employeeCounter

# function that returns a dict with the retrieved values
# iterates through the dict to remove the square brackets retreived by the SQLAlchemy query
def empDict():
    group = employee.query.with_entities(employee.date, func.count(employee.date)).group_by(employee.date).all()
    dict = {}
    for i in range(len(group)):
        dict[group[i][0]] = []
        dict[group[i][0]].append(group[i][1])
    for key, value in dict.items():
        newValue = str(dict[key])
        newValue = newValue.replace("[", "")
        newValue = newValue.replace("]", "")
        dict[key] = newValue
    return dict

@login_manager.user_loader
def load_user(admin_id):
    # query by primary key of the admin table
    return admin.query.get(int(admin_id))

@app.route("/login/login", methods=["GET", "POST"])
def login():
# the authentication was implemented folowing the tutorial wote by Anthony Herbert: https://www.digitalocean.com/community/tutorials/how-to-add-authentication-to-your-app-with-flask-login
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = admin.query.filter_by(username=username).first()
        password = admin.query.filter_by(password=password).first()

        if not user or not password:
            flash("Invalid Credentials. Please try again!", "warning")
            return redirect("/login")
        else:
            login_user(user)
            return redirect("/adminManagement")
    else:
        return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("index.html")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/login")
def loginPage():
    return render_template("login.html")

@app.route("/userManagement")
def userManagement():
    employeeCounter = maxEmp()
    return render_template("userManagement.html", months = monthList, maxEmpCount = employeeCounter)

@app.route("/adminManagement")
@login_required
def adminManagement():
    employeeCounter = maxEmp()
    return render_template("adminManagement.html", months = monthList, maxEmpCount = employeeCounter, name=current_user.username)

@app.route("/employeeList")
def empList():
    all_employees = employee.query.order_by(employee.created_date).all()
    emp_count = employee.query.count()
    dict = empDict()
    employeeCounter = maxEmp()

    return render_template("employeeList.html", employees=all_employees, emp_count=emp_count, dict=dict, maxEmpCount = employeeCounter)

@app.route("/employeeListUser")
def empListUser():
    all_employees = employee.query.order_by(employee.created_date).all()
    emp_count = employee.query.count()
    dict = empDict()
    employeeCounter = maxEmp()
    
    return render_template("employeeListUser.html", employees=all_employees, emp_count=emp_count, dict=dict, maxEmpCount = employeeCounter)

@app.route("/employeeListRemove")
@login_required
def empListRemoveList():
    all_employees = employee.query.order_by(employee.created_date).all()
    emp_count = employee.query.count()
    dict = empDict()
    employeeCounter = maxEmp()

    return render_template("employeeListRemove.html", employees=all_employees, emp_count=emp_count, dict=dict, maxEmpCount = employeeCounter)

@app.route("/employeeListRemove/delete/<int:id>")
def empListRemove(id):
    # delete the selected employee from the db
    emp = employee.query.get_or_404(id)
    db.session.delete(emp)
    db.session.commit()

    return redirect("/employeeListRemove")

@app.route("/employeeListRemove/delete/all")
def empListRemoveAll():
    # delete all the employees from the db
    db.session.query(employee).delete()
    db.session.commit()

    return redirect("/employeeListRemove")

@app.route("/userManagement", methods=["GET", "POST"])
@app.route("/adminManagement", methods=["GET", "POST"])
def employees():
    # add a new employee to the db
    if request.method == "POST":
        empName = request.form["name"]
        department = request.form["dept"]
        date = request.form["dateElement"]
        if date == " " or date == "":
            date = defaultDate
        newEmployee = employee(name=empName, dept=department, date=date)
        db.session.add(newEmployee)
        db.session.commit()
        print(str(empName) + ", dept: " + str(department) + " has been added to the db")
        return redirect("/")
    else:
        all_employees = employee.query.order_by(employee.created_date).all()
        return render_template("index.html", employees=all_employees)

@app.route("/employeeCount", methods = ["GET", "POST"])
def employeeCount():
    # read the retreived jquery ajax post request
    # add the maximum employees threshold to the db
    if request.method == "POST":
        db.session.query(empCount).delete()
        db.session.commit()
        employeeCount = request.form["data"]
        print(employeeCount + " received")
        newCounter = empCount(max = employeeCount)
        db.session.add(newCounter)
        db.session.commit()
        return redirect("/adminManagement")
    else:
        return render_template("adminManagement.html")

if __name__ == "__main__":
    # generate a default admin/admin profile in case the profile is not already created in the db
    admin_count = admin.query.count()
    if admin_count == 0:
        default_admin = admin(username="admin", password="admin")
        db.session.add(default_admin)
        db.session.commit()
    app.run(debug=True)
