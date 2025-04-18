import streamlit as st
from app import create_app, db
from app.models import Employee, Feedback, Leave, Attendance, PerformanceReview
from app.analytics.visualization import plot_salary_distribution, plot_performance_trend, plot_attendance_trend, plot_productivity_trend
from app.ml.attrition_prediction import train_attrition_model, predict_attrition_risk
from app.utils.calculations import calculate_incentive, calculate_bonus, calculate_payroll
from datetime import datetime
import os

app = create_app()

with app.app_context():
    db.create_all()
    employees = Employee.query.all()
    print(f"Employees in database: {employees}")  


st.markdown(
    """
    <style>
    :root {
        --primary: #1a2c5e;
        --secondary: #3f37c9;
        --accent: #1a2c5e;
        --dark: #1a2c5e;
        --light: #f8f9fa;
        --success: #4cc9f0;
        --warning: #5e1a2c;
        --danger: #b5179e;
        --text: #2b2d42;
        --gray: #adb5bd;
    }


    /* Set slider filled track color (this is the WORKING selector) */
    .stSlider [aria-valuenow]::before {
        background-color: black !important;
    }

    /* Optional: style the handle (knob) */
    .stSlider [role="slider"] {
        background-color: black !important;
        border: 1px solid #000 !important;
    }
    
    /* Base styling */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Main app container */
    .stApp {
        background-color: #f5f7fb;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1a2c5e!important;
    }

    /* Sidebar title */
    [data-testid="stSidebar"] h1 {
        color: white !important;
        padding: 10px;
    }

/* Sidebar buttons */
.stButton>button {
    width: 100%;
    margin-bottom: 10px;
    text-align: left;
    padding: 10px 15px;
    border-radius: 5px;
    background-color: #1a2c5e; /* This controls the button background color */
    color: white !important; /* This controls the text color */
    border: none;
    font-weight: bold;
    font-size: 1em;
    min-height: 44px;
    transition: all 0.3s ease;
}

.stButton>button:hover {
    background-color: #1a2c5e !important; /* Hover background color */
    transform: translateY(-1px);
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

    
    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        color: var(--dark) !important;
        font-weight: 700 !important;
    }
    
    /* Card styling */
    .card {
        background: white;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
        border-left: 4px solid var(--primary);
    }
    
    /* Form styling */
    .stTextInput>div>div>input, 
    .stNumberInput>div>div>input,
    .stTextArea>div>div>textarea,
    .stSelectbox>div>div>select,
    .stDateInput>div>div>input {
        border-radius: 8px !important;
        border: 1px solid var(--gray) !important;
        padding: 10px 12px !important;
    }
    
    /* Button styling */
    .stButton>button {
        background: var(--primary);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: var(--secondary);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(67, 97, 238, 0.2);
    }
    
    



    /* Dataframe styling */
    .stDataFrame {
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Metric styling */
    .stMetric {
        background: white;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        border-left: 4px solid var(--primary);
    }
    
    /* Tab styling */
    [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    [data-baseweb="tab"] {
        background: white;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        margin: 0 4px !important;
        transition: all 0.3s ease;
    }
    
    [data-baseweb="tab"]:hover {
        background: var(--light) !important;
    }
    
    [aria-selected="true"] {
        background: var(--primary) !important;
        color: white !important;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--light);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--gray);
        border-radius: 4px;
    }
    
    /* Responsive layout */
    @media (max-width: 768px) {
        .stButton>button {
            width: 100%;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown(
    """
    <div style="padding: 16px 0 32px 0; text-align: center;">
        <h1 style="color: white; margin: 0;">HR Management </h1>
        <p style="color: rgba(255,255,255,0.7); margin: 0; font-size: 14px;">Employee Management Dashboard</p>
    </div>
    """, 
    unsafe_allow_html=True
)


nav_options = {
    "👤 Employee Management": "employee",
    "📊 Analytics Dashboard": "dashboard",
    "💰 Payroll & Compensation": "payroll",
    "🗓 Attendance Tracking": "attendance",
    "📝 Performance Reviews": "performance",
    "🔮 Predictive Analytics": "predictive",
    "⚙️ System Settings": "settings"
}


if 'current_page' not in st.session_state:
    st.session_state.current_page = "👤 Employee Management"


for option in nav_options.keys():
    if st.sidebar.button(option, key=f"nav_{option}"):
        st.session_state.current_page = option



# Main content area
st.markdown(
    f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px;">
        <h1>{st.session_state.current_page}</h1>
        <div style="color: var(--gray); font-size: 14px;">{datetime.now().strftime('%A, %B %d, %Y')}</div>
    </div>
    """,
    unsafe_allow_html=True
)


with app.app_context():
    if st.session_state.current_page == "👤 Employee Management":
       
        with st.expander("➕ Add New Employee", expanded=True):
            with st.form("employee_form"):
                cols = st.columns(3)
                with cols[0]:
                    first_name = st.text_input("First Name")
                    email = st.text_input("Email")
                    department = st.selectbox("Department", ["Engineering", "Marketing", "HR", "Finance", "Operations"])
                with cols[1]:
                    last_name = st.text_input("Last Name")
                    phone = st.text_input("Phone")
                    position = st.selectbox("Position", ["Manager", "Developer", "Analyst", "Director", "Specialist"])
                with cols[2]:
                    hire_date = st.date_input("Hire Date")
                    salary = st.number_input("Salary", min_value=0, step=1000)
                    status = st.selectbox("Status", ["Active", "On Leave", "Terminated"])
                
                submitted = st.form_submit_button("Save Employee")
                if submitted:
                    st.success("Employee record saved successfully!")
        
        st.markdown("### Employee Directory")
        if employees:
            employee_data = []
            for emp in employees:
                employee_data.append({
                    "ID": emp.id,
                    "Name": emp.name,
                    "Position": emp.role,
                    "Department": "Engineering",  
                    "Salary": f"${emp.salary:,.2f}",
                    "Status": "Active"  
                })
            
            st.dataframe(
                employee_data,
                use_container_width=True,
                column_config={
                    "Salary": st.column_config.NumberColumn(format="$%.2f")
                },
                hide_index=True
            )
        else:
            st.warning("No employee records found.")

    elif st.session_state.current_page == "📊 Analytics Dashboard":
        cols = st.columns(3)
        with cols[0]:
            st.metric("Total Employees", len(employees))
        with cols[1]:
            avg_salary = sum(e.salary for e in employees) / len(employees) if employees else 0
            st.metric("Average Salary", f"${avg_salary:,.2f}")
        with cols[2]:
            avg_perf = sum(e.performance_score for e in employees) / len(employees) if employees else 0
            st.metric("Avg Performance", f"{avg_perf:.1f}/100")
        
        st.markdown("### Key Metrics")
        tab1, tab2, tab3 = st.tabs(["Performance", "Attendance", "Productivity"])
        
        with tab1:
            fig = plot_performance_trend(employees)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            fig = plot_attendance_trend(employees)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            fig = plot_productivity_trend(employees)
            st.plotly_chart(fig, use_container_width=True)

    elif st.session_state.current_page == "💰 Payroll & Compensation":
        st.markdown("### Payroll Calculator")
        
        selected_employee = st.selectbox("Select Employee", [e.name for e in employees])
        employee = next(e for e in employees if e.name == selected_employee)
        
        cols = st.columns(3)
        with cols[0]:
            st.metric("Base Salary", f"${employee.salary:,.2f}")
        with cols[1]:
            incentive = calculate_incentive(employee.salary, employee.performance_score)
            st.metric("Incentive", f"${incentive:,.2f}")
        with cols[2]:
            bonus = calculate_bonus(employee.salary, employee.performance_score)
            st.metric("Bonus", f"${bonus:,.2f}")
        
        payroll =  calculate_payroll(employee.salary, bonus, incentive )

        
        st.markdown(f"""
        <div class="card">
            <h3>Payroll Summary</h3>
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid #eee;">
                    <td style="padding: 8px 0;">Base Salary</td>
                    <td style="text-align: right;">${employee.salary:,.2f}</td>
                </tr>
                <tr style="border-bottom: 1px solid #eee;">
                    <td style="padding: 8px 0;">Incentive</td>
                    <td style="text-align: right;">${incentive:,.2f}</td>
                </tr>
                <tr style="border-bottom: 1px solid #eee;">
                    <td style="padding: 8px 0;">Bonus</td>
                    <td style="text-align: right;">${bonus:,.2f}</td>
                </tr>
                <tr style="font-weight: bold; border-top: 2px solid var(--dark);">
                    <td style="padding: 12px 0;">Total Payroll</td>
                    <td style="text-align: right;">${payroll:.2f}</td>
                </tr>
            </table>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.current_page == "🗓 Attendance Tracking":
        tab1, tab2 = st.tabs(["Mark Attendance", "Leave Management"])
        
        with tab1:
            st.markdown("### Daily Attendance")
            with st.form("attendance_form"):
                date = st.date_input("Date", datetime.today())
                employee = st.selectbox("Employee", [e.name for e in employees])
                status = st.selectbox("Status", ["Present", "Absent", "Late", "On Leave"])
                
                submitted = st.form_submit_button("Submit")
                if submitted:
                    st.success(f"Attendance recorded for {employee}")
        
        with tab2:
            st.markdown("### Leave Requests")
            with st.form("leave_form"):
                cols = st.columns(2)
                with cols[0]:
                    employee = st.selectbox("Employee", [e.name for e in employees])
                    start_date = st.date_input("Start Date")
                with cols[1]:
                    leave_type = st.selectbox("Leave Type", ["Vacation", "Sick", "Personal", "Bereavement"])
                    end_date = st.date_input("End Date")
                
                reason = st.text_area("Reason for Leave")
                
                submitted = st.form_submit_button("Submit Request")
                if submitted:
                    st.success("Leave request submitted for approval")

    elif st.session_state.current_page == "📝 Performance Reviews":
        st.markdown("### Employee Performance")
        
        selected_employee = st.selectbox("Select Employee", [e.name for e in employees])
        employee = next(e for e in employees if e.name == selected_employee)
        
        cols = st.columns(3)
        with cols[0]:
            st.metric("Current Score", f"{employee.performance_score}/100")
        with cols[1]:
            st.metric("Trend", "↑ 5%")
        with cols[2]:
            risk_color = "var(--warning)" if employee.attrition_risk > 0.7 else "var(--success)"
            st.metric("Attrition Risk", f"{employee.attrition_risk*100:.0f}%", delta_color="off")
        
        
        
        st.markdown("### Submit Feedback")
        with st.form("feedback_form"):
            reviewer = st.text_input("Reviewer Name")
            feedback = st.text_area("Feedback Comments")
            rating = st.slider("Performance Rating", 1, 5, 3)
            st.write("You selected:", rating)
            
            submitted = st.form_submit_button("Submit Review")
            if submitted:
                st.success("Performance review submitted successfully")

    elif st.session_state.current_page == "🔮 Predictive Analytics":
        st.markdown("### Attrition Risk Analysis")
        
        model = train_attrition_model()
        
        cols = st.columns(2)
        with cols[0]:
            selected_employee = st.selectbox("Select Employee", [e.name for e in employees])
            employee = next(e for e in employees if e.name == selected_employee)
            
            risk_score = predict_attrition_risk(model, [employee])[0]
            
            if risk_score > 0.7:
                risk_status = "High Risk"
                risk_color = "var(--warning)"
            elif risk_score > 0.4:
                risk_status = "Medium Risk"
                risk_color = "var(--accent)"
            else:
                risk_status = "Low Risk"
                risk_color = "var(--success)"
            
            st.markdown(
                f"""
                <div class="card">
                    <h3>Risk Assessment</h3>
                    <div style="display: flex; align-items: center; margin: 16px 0;">
                        <div style="width: 100px; height: 100px; border-radius: 50%; 
                            background: conic-gradient({risk_color} 0% {risk_score*100}%, #eee {risk_score*100}% 100%); 
                            display: flex; align-items: center; justify-content: center; margin-right: 20px;">
                            <div style="font-size: 24px; font-weight: bold; color: {risk_color};">{risk_score*100:.0f}%</div>
                        </div>
                        <div>
                            <h3 style="color: {risk_color}; margin: 0;">{risk_status}</h3>
                            <p style="color: var(--gray); margin: 4px 0 0 0;">Attrition Probability</p>
                        </div>
                    </div>
                    <p>Recommendation: { "Immediate retention actions needed" if risk_score > 0.7 else "Monitor closely" if risk_score > 0.4 else "Low priority" }</p>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with cols[1]:
            st.markdown("### Risk Factors")
            risk_factors = [
                {"factor": "Job Satisfaction", "score": 0.85, "impact": "High"},
                {"factor": "Compensation", "score": 0.72, "impact": "Medium"},
                {"factor": "Work-Life Balance", "score": 0.68, "impact": "Medium"},
                {"factor": "Career Growth", "score": 0.91, "impact": "High"},
            ]
            
            for factor in risk_factors:
                st.markdown(
                    f"""
                    <div style="margin-bottom: 12px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 4px;">
                            <span>{factor['factor']}</span>
                            <span style="font-weight: bold; color: { 'var(--warning)' if factor['score'] > 0.7 else 'var(--accent)' if factor['score'] > 0.4 else 'var(--success)' };">
                                {factor['score']*100:.0f}%
                            </span>
                        </div>
                        <div style="height: 6px; background: #eee; border-radius: 3px;">
                            <div style="width: {factor['score']*100}%; height: 100%; background: { 'var(--warning)' if factor['score'] > 0.7 else 'var(--accent)' if factor['score'] > 0.4 else 'var(--success)' }; border-radius: 3px;"></div>
                        </div>
                        <div style="font-size: 12px; color: var(--gray); margin-top: 4px;">Impact: {factor['impact']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    elif st.session_state.current_page == "⚙️ System Settings":
        st.markdown("### Integration Settings")
        
        with st.expander("HRMS API Configuration"):
            with st.form("api_config"):
                api_url = st.text_input("API Endpoint URL", "https://api.hrms.com/v1")
                api_key = st.text_input("API Key", type="password")
                sync_frequency = st.selectbox("Sync Frequency", ["Daily", "Weekly", "Monthly"])
                
                saved = st.form_submit_button("Save Configuration")
                if saved:
                    st.success("API configuration saved")
        
        with st.expander("Data Export"):
            export_format = st.selectbox("Format", ["CSV", "JSON", "Excel"])
            include_data = st.multiselect("Include", ["Employee Data", "Attendance", "Payroll", "Performance"])
            
            if st.button("Generate Export"):
                st.success(f"Export generated in {export_format} format")
                
        
        with st.expander("User Management"):
            st.markdown("### System Users")
            st.dataframe([
                {"Username": "admin", "Role": "Administrator", "Last Login": "2023-06-15"},
                {"Username": "hr_manager", "Role": "HR Manager", "Last Login": "2023-06-14"},
                {"Username": "payroll_staff", "Role": "Payroll", "Last Login": "2023-06-10"}
            ], hide_index=True)
            
            if st.button("Add New User"):
                st.info("User management functionality would be implemented here")