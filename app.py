# __author__ = "Dan-Gabriel Pintoiu"
# __copyright__ = "Copyright (C) 2020 Dan-Gabriel Pintoiu"
# __license__ = "Public Domain"

from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, current_user, LoginManager, login_user, logout_user
from sqlalchemy import func
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = "bF-xcay-xffp-x0bc--xb53xeaxfc8-xc8y-xcb-xe4"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///employees.db"
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

#acest comentariu este adaugat de Teodor


# table models
class employee(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable = False)
    dept = db.Column(db.String(50), nullable = False)
    date = db.Column(db.String(50), nullable = False)
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

# create a helping list to iterate over later
all_employees = []

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

# function that returns a dict with all the db records, grouping by date and counting it
def empDict():
    group = employee.query.with_entities(employee.date, func.count(employee.date)).group_by(employee.date).all()
    dict = {}
    # iterates through the dict to remove the square brackets returned with the SQLAlchemy query
    for i in range(len(group)):
        dict[group[i][0]] = []
        dict[group[i][0]].append(group[i][1])
    for key, value in dict.items():
        newValue = str(dict[key])
        newValue = newValue.replace("[", "")
        newValue = newValue.replace("]", "")
        dict[key] = newValue
    return dict

# retrieve all records for a given employee
# case insensitive search
def currentEmpRecords(employeeName):
    currentEmployee = employee.query.filter(employee.name.ilike(employeeName)).all()
    employeeDict = {}
    employeeDict = currentEmployee
    return employeeDict

@login_manager.user_loader
def load_user(admin_id):
    # query by primary key of the admin table
    return admin.query.get(int(admin_id))

@app.route("/login/login", methods=["GET", "POST"])
def login():
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

@app.route("/individualRemove/<string:name>")
def indRem(name):
    currentEmployee = currentEmpRecords(name)
    emp_count = len(currentEmployee)
    employeeCounter = maxEmp()
    dict = empDict()
    return render_template("individualRemove.html", employees=currentEmployee, emp_count=emp_count, dict=dict, maxEmpCount = employeeCounter, name=name)

@app.route("/userManagement")
def userManagement():
    emp_count = employee.query.count()
    dict = empDict()
    employeeCounter = maxEmp()

    return render_template("userManagement.html", maxEmpCount = employeeCounter, emp_count=emp_count, dict=dict)

@app.route("/adminManagement")
@login_required
def adminManagement():
    employeeCounter = maxEmp()
    return render_template("adminManagement.html", maxEmpCount = employeeCounter, name=current_user.username)

@app.route("/employeeList")
@login_required
def empList():
    all_employees = employee.query.order_by(employee.created_date).all()
    emp_count = employee.query.count()
    dict = empDict()
    employeeCounter = maxEmp()

    return render_template("employeeList.html", employees=all_employees, emp_count=emp_count, dict=dict, maxEmpCount = employeeCounter)

@app.route("/employeeListRemove")
@login_required
def empListRemoveList():
    all_employees = employee.query.order_by(employee.created_date).all()
    emp_count = employee.query.count()
    dict = empDict()
    employeeCounter = maxEmp()

    return render_template("employeeListRemove.html", employees=all_employees, emp_count=emp_count, dict=dict, maxEmpCount = employeeCounter)

@app.route("/employeeListRemove/delete/<int:id>/<string:name>")
@app.route("/individualRemove/delete/<int:id>/<string:name>")
def empListRemove(id, name):
    # delete the selected employee from the db
    emp = employee.query.get_or_404(id)
    db.session.delete(emp)
    db.session.commit()

    if request.path.split('/')[1] == "employeeListRemove":
        return redirect("/employeeListRemove")
    else:
        return redirect("/" + request.path.split('/')[1] + "/" + name)

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
        date = request.form["date"]
        print(date)
        if len(empName) > 30:
            flash("Please add maximum 30 characters in the name field!", "warning")
            return redirect(request.path)
        elif len(department) > 30:
            flash("Please add maximum 30 characters in the department field!", "warning")
            return redirect(request.path)
        if date == " " or date == "":
            flash("Please add a date in the date field!", "warning")
            return redirect(request.path)

        dict = empDict()
        employeeCounter = maxEmp()
        try:
            if int(dict.get(date)) >= int(employeeCounter):
                flash(date + " is fully booked. Please select another day!", "warning")
                return redirect(request.path)
        except:
            pass

        newEmployee = employee(name=empName, dept=department, date=date)
        db.session.add(newEmployee)
        db.session.commit()
        print("Employee: " + str(empName) + ", dept: " + str(department) + ", date: " + str(date) + " has been added to the database.")
        return redirect(request.path)
    else:
        all_employees = employee.query.order_by(employee.created_date).all()
        return render_template("index.html", employees=all_employees)

@app.route("/employeeCount", methods = ["GET", "POST"])
def employeeCount():
    # read the retreived jQuery Ajax post request
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
