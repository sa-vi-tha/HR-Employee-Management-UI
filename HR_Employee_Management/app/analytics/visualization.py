
import plotly.express as px
import pandas as pd

def plot_salary_distribution(employees):
    df = pd.DataFrame([{'name': e.name, 'salary': e.salary} for e in employees])
    fig = px.bar(df, x='name', y='salary', title="Employee Salary Distribution")
    return fig

def plot_performance_trend(employees):
    df = pd.DataFrame([{'name': e.name, 'performance_score': e.performance_score} for e in employees])
    fig = px.line(df, x='name', y='performance_score', title="Employee Performance Trend")
    return fig

def plot_attendance_trend(employees):
    df = pd.DataFrame([{'name': e.name, 'attendance': e.attendance} for e in employees])
    fig = px.line(df, x='name', y='attendance', title="Employee Attendance Trend")
    return fig

def plot_productivity_trend(employees):
    df = pd.DataFrame([{'name': e.name, 'productivity': e.productivity} for e in employees])
    fig = px.line(df, x='name', y='productivity', title="Employee Productivity Trend")
    return fig