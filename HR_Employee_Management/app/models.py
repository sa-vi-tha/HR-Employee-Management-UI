from app import db

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    performance_score = db.Column(db.Float, nullable=True)  
    attrition_risk = db.Column(db.Float, nullable=True)   
    attendance = db.Column(db.Float, nullable=True)       
    productivity = db.Column(db.Float, nullable=True)     
    
class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    reviewer = db.Column(db.String(100), nullable=False)
    feedback_type = db.Column(db.String(50), nullable=False) 

class Payroll(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    salary = db.Column(db.Float, nullable=False)
    incentives = db.Column(db.Float, default=0.0)

class Leave(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    reason = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default="Pending")  

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), nullable=False)  

class PerformanceReview(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    review_date = db.Column(db.Date, nullable=False)
    reviewer = db.Column(db.String(100), nullable=False)
    performance_score = db.Column(db.Float, nullable=False)
    comments = db.Column(db.Text, nullable=True)