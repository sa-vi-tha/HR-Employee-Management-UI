
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from app import db
from app.models import Employee

def train_attrition_model():
    employees = Employee.query.all()
    data = pd.DataFrame([{
        'salary': e.salary,
        'performance_score': e.performance_score,
        'attrition_risk': e.attrition_risk,
        'attendance': e.attendance,
        'productivity': e.productivity
    } for e in employees])

    if len(data['attrition_risk'].unique()) < 2:
        raise ValueError("The target variable 'attrition_risk' must have at least two classes (0 and 1).")

    X = data[['salary', 'performance_score', 'attendance', 'productivity']]
    y = data['attrition_risk']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    return model

def predict_attrition_risk(model, employees):
   
    X = pd.DataFrame([{
        'salary': e.salary,
        'performance_score': e.performance_score,
        'attendance': e.attendance,
        'productivity': e.productivity
    } for e in employees])
    
    try:
        if hasattr(model, "predict_proba"):
            predictions = model.predict_proba(X)[:, 1] 
        else:
            predictions = model.predict(X)
            
    except IndexError:
        predictions = [0.0] * len(employees) 
        print("Warning: Model predicted only one class. Defaulting to 0 for all employees.")

    return predictions



