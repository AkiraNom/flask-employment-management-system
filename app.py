from flask import Flask, render_template, redirect, request, url_for
# from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db = SQLAlchemy(app)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    mail = db.Column(db.String(100), nullable=False)
    is_remote = db.Column(db.Boolean)
    department = db.Column(db.String(100))
    year = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"Employee {self.id}"


@app.route("/", methods=["GET","POST"])
def index():
    return redirect(url_for('employee_list'))

@app.route("/add_employee", methods=["POST","GET"])
def add_employee():
    if request.method=="GET":
        return render_template("add_employee.html")
    if request.method=="POST":
        form_name = request.form.get('name')
        form_mail = request.form.get('mail')
        form_is_remote = request.form.get('is_remote', default=False, type=bool)
        form_department = request.form.get('department')
        form_year = request.form.get('year', default=0, type=int)

        employee = Employee(
            name=form_name,
            mail=form_mail,
            is_remote=form_is_remote,
            department=form_department,
            year=form_year
        )
        db.session.add(employee)
        db.session.commit()
        return redirect("/add_employee")


@app.route("/employees")
def employee_list():
    employees = Employee.query.all()
    return render_template("employee_list.html", employees=employees)

@app.route("/employees/<int:id>")
def employee_detail(id):
    employee = Employee.query.get_or_404(id)
    return render_template("employee_detail.html", employee=employee)

@app.route("/employees/<int:id>/edit")
def employee_edit(id):
    employee = Employee.query.get_or_404(id)
    return render_template("employee_edit.html", employee=employee)

@app.route("/employees/<int:id>/update", methods=["POST"])
def employee_update(id):
    employee = Employee.query.get_or_404(id)
    employee.name = request.form.get('name')
    employee.mail = request.form.get('mail')
    employee.is_remote = request.form.get('is_remote', default=False, type=bool)
    employee.department = request.form.get('department')
    employee.year = request.form.get('year', default=0, type=int)

    db.session.merge(employee)
    db.session.commit()
    return redirect(url_for("employee_list"))

@app.route("/employees/<int:id>/delete", methods=["POST"])
def employee_delete(id):
    delete_employee = Employee.query.get_or_404(id)

    try:
        db.session.delete(delete_employee)
        db.session.commit()
        return redirect(url_for("employee_list"))

    except Exception as e:
        return f"Exception:{e}"

if __name__ in "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
