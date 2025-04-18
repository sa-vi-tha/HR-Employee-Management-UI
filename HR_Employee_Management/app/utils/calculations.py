
def calculate_incentive(salary, performance_score):
    return salary * (performance_score / 100)

def calculate_bonus(salary, performance_score):
    return salary * (performance_score / 100) * 0.1

def calculate_payroll(salary, attendance, productivity):
    base_salary = salary
    attendance_bonus = base_salary * (attendance / 100)
    productivity_bonus = base_salary * (productivity / 100)
    total_salary = base_salary + attendance_bonus + productivity_bonus
    return total_salary
def calculate_payroll(base_salary, incentive, bonus):
    return base_salary + incentive + bonus