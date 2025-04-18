from flask import jsonify, request, current_app
from app.models import Employee, Feedback, Payroll
from app import db

def init_app(app):
    @app.route('/employees', methods=['GET'])
    def get_employees():
        employees = Employee.query.all()
        return jsonify([{'id': e.id, 'name': e.name, 'role': e.role, 'salary': e.salary} for e in employees])

    @app.route('/feedback', methods=['POST'])
    def add_feedback():
        data = request.get_json()
        new_feedback = Feedback(employee_id=data['employee_id'], feedback=data['feedback'], reviewer=data['reviewer'])
        db.session.add(new_feedback)
        db.session.commit()
        return jsonify({'message': 'Feedback added successfully'})

    @app.route('/payroll/<int:employee_id>', methods=['GET'])
    def get_payroll(employee_id):
        payroll = Payroll.query.filter_by(employee_id=employee_id).first()
        return jsonify({'salary': payroll.salary, 'incentives': payroll.incentives})
    
    @app.route('/leave', methods=['POST'])
    def apply_leave():
        data = request.get_json()
        new_leave = Leave(
            employee_id=data['employee_id'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d'),
            reason=data['reason'],
            status="Pending"
        )
        db.session.add(new_leave)
        db.session.commit()
        return jsonify({'message': 'Leave application submitted successfully'})

    @app.route('/attendance', methods=['POST'])
    def mark_attendance():
        data = request.get_json()
        new_attendance = Attendance(
            employee_id=data['employee_id'],
            date=datetime.strptime(data['date'], '%Y-%m-%d'),
            status=data['status']
        )
        db.session.add(new_attendance)
        db.session.commit()
        return jsonify({'message': 'Attendance marked successfully'})


    @app.route('/leave/balance/<int:employee_id>', methods=['GET'])
    def get_leave_balance(employee_id):
      leaves = Leave.query.filter_by(employee_id=employee_id).all()
      total_leave_days = sum((leave.end_date - leave.start_date).days for leave in leaves)
      return jsonify({'leave_balance': 30 - total_leave_days}) 

    @app.route('/attendance/real-time/<int:employee_id>', methods=['GET'])
    def get_real_time_attendance(employee_id):
       attendance = Attendance.query.filter_by(employee_id=employee_id).order_by(Attendance.date.desc()).first()
       return jsonify({'date': attendance.date.strftime('%Y-%m-%d'), 'status': attendance.status})
    
    @app.route('/performance_review', methods=['POST'])
    def create_performance_review():
        data = request.get_json()
        new_review = PerformanceReview(
            employee_id=data['employee_id'],
            role=data['role'],
            metrics=data['metrics'],
            scores=data['scores']
        )
        db.session.add(new_review)
        db.session.commit()
        return jsonify({'message': 'Performance review created successfully'})