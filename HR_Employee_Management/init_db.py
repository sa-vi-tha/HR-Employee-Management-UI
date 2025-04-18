from app import create_app, db
from app.models import Employee, Feedback, Payroll, Leave, Attendance, PerformanceReview

app = create_app()

with app.app_context():
   
    db.create_all()

   
    employee1 = Employee(
        name="John Doe",
        role="Manager",
        salary=50000,
        performance_score=85,
        attrition_risk=0,
        attendance=95,
        productivity=90
    )
    employee2 = Employee(
        name="Jane Smith",
        role="Developer",
        salary=60000,
        performance_score=90,
        attrition_risk=1,
        attendance=90,
        productivity=85
    )

    db.session.add(employee1)
    db.session.add(employee2)
    db.session.commit()

    print("Database tables created and sample data added successfully!")