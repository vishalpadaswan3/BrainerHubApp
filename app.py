from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import pandas as pd
# Initialize app

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))


# Database

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Init db
db = SQLAlchemy(app)


# Init ma
ma = Marshmallow(app)


class Alldata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    phone_number = db.Column(db.String(100))
    salary = db.Column(db.Integer)
    manager_id = db.Column(db.Integer)
    department_id = db.Column(db.Integer)


class EmployeeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'phone_number',
                  'salary', 'manager_id', 'department_id')
employee_schema = EmployeeSchema()
employees_schema = EmployeeSchema(many=True)

class Company(db.Model):
    company_name = db.Column(db.String(100))
    location = db.Column(db.String(100))
    total_employees = db.Column(db.Integer)
    total_departments = db.Column(db.Integer, primary_key=True)


class CompanySchema(ma.Schema):
    class Meta:
        fields = ('company_name', 'location', 'total_employees', 'total_departments')
company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)

class Employee(db.Model):
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    age = db.Column(db.Integer)
    salary = db.Column(db.Integer)
    department_id = db.Column(db.Integer, primary_key=True)

class vpemployeeSchema(ma.Schema):
    class Meta:
        fields = ('first_name', 'last_name', 'age', 'salary', 'department_id')
vpemployee_schema = vpemployeeSchema()
vpemployees_schema = vpemployeeSchema(many=True)



@app.route("/", methods=['GET'])
def home():
    return render_template("index.html")


@app.route('/alldata', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        df = pd.read_excel(file)
        # Create the tables if they do not exist
        db.create_all()
        # Prepare employee data
        employee_data = df[['EMPLOYEE_ID', 'FIRST_NAME', 'LAST_NAME', 'PHONE_NUMBER', 'SALARY', 'MANAGER_ID', 'DEPARTMENT_ID']].rename(
        columns={'EMPLOYEE_ID': 'id', 'FIRST_NAME': 'first_name', 'LAST_NAME': 'last_name', 'PHONE_NUMBER': 'phone_number',  'SALARY': 'salary', 'MANAGER_ID': 'manager_id', 'DEPARTMENT_ID': 'department_id'}).to_dict(orient='records')
        db.session.bulk_insert_mappings(Alldata, employee_data)
        db.session.commit()
        return {"message": "Data inserted successfully"}, 201
    except Exception as e:
        return {"message": str(e)}, 500

@app.route('/alldata', methods=['GET'])
def get_employees():
    try:
        all_employees = Alldata.query.all()
        result = employees_schema.dump(all_employees)
        return {"employees": result}, 200
    except Exception as e:
        return {"message": str(e)}, 500


@app.route('/company', methods=['POST'])
def add_company_fromfile():
    try:
        file = request.files['file']
        df = pd.read_excel(file)
        # Create the tables if they do not exist
        db.create_all()
        # Prepare employee data
        company_data = df[['COMPANY_NAME', 'LOCATION', 'TOTAL_EMPLOYEES', 'TOTAL_DEPARTMENTS']].rename(
        columns={'COMPANY_NAME': 'company_name', 'LOCATION': 'location', 'TOTAL_EMPLOYEES': 'total_employees', 'TOTAL_DEPARTMENTS': 'total_departments'}).to_dict(orient='records')
        db.session.bulk_insert_mappings(Company, company_data)
        db.session.commit()
        return {"message": "Data inserted successfully"}, 201
    except Exception as e:
        return {"message": str(e)}, 500
    


@app.route('/company', methods=['GET'])
def get_companies():
    try:
        all_companies = Company.query.all()
        result = companies_schema.dump(all_companies)
        return {"companies": result}, 200
    except Exception as e:
        return {"message": str(e)}, 500


@app.route('/vpemployee', methods=['POST'])
def add_vpemployee_fromfile():
    try:
        file = request.files['file']
        df = pd.read_excel(file)
        # Create the tables if they do not exist
        db.create_all()
        # Prepare employee data
        vpemployee_data = df[['FIRST_NAME', 'LAST_NAME', 'AGE', 'SALARY', 'DEPARTMENT_ID']].rename(
        columns={'FIRST_NAME': 'first_name', 'LAST_NAME': 'last_name', 'AGE': 'age', 'SALARY': 'salary', 'DEPARTMENT_ID': 'department_id'}).to_dict(orient='records')
        db.session.bulk_insert_mappings(Employee, vpemployee_data)
        db.session.commit()
        return {"message": "Data inserted successfully"}, 201
    except Exception as e:
        return {"message": str(e)}, 500


@app.route('/vpemployee', methods=['GET'])
def get_vpemployees():
    try:
        all_vpemployees = Employee.query.all()
        result = vpemployees_schema.dump(all_vpemployees)
        return {"vpemployees": result}, 200
    except Exception as e:
        return {"message": str(e)}, 500

# Run server
if __name__ == '__main__':
    app.run(debug=True)
