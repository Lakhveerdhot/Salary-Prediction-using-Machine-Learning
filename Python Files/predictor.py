import streamlit as st
import pickle
import numpy as np
import pandas as pd
from model_final import prepare_dataframe
from streamlit_extras.stylable_container import stylable_container

# Custom CSS for the prediction page
st.markdown("""
<style>
    .prediction-card {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-top: 2rem;
    }
    .prediction-value {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        margin: 1rem 0;
    }
    .section-title {
        color: #2c3e50;
        border-bottom: 2px solid #4CAF50;
        padding-bottom: 0.5rem;
        margin-top: 1.5rem;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
</style>
""", unsafe_allow_html=True)

def load_model():
    with open('Model/model_3.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

model = data["MODEL"]
label_encoders = data["LABEL_ENCODERS"]
scaler = data["SCALER"]

def show_predict_page():
    st.title("💰 Salary Prediction")
    st.markdown("### Fill in your details to get an accurate salary estimation")
    st.markdown("---")

    age = (
        "Select Age",
        "18-24 years old",
        "25-34 years old",
        "35-44 years old",
        "45-54 years old",
        "55-64 years old",
        "65 years or older",
        "Prefer not to say"
    )

    dev_type = [
        'Select Job Role',
        'Senior Executive (C-Suite, VP, etc.)', 
        'Developer, back-end', 
        'Developer, front-end', 
        'Developer, full-stack', 
        'System administrator', 
        'Developer, QA or test', 
        'Designer', 
        'Data scientist or machine learning specialist', 
        'Data or business analyst', 
        'Security professional', 
        'Research & Development role', 
        'Developer, mobile',
        'Database administrator', 
        'Developer, embedded applications or devices', 
        'Developer, desktop or enterprise applications', 
        'Engineer, data', 
        'Product manager', 
        'Academic researcher', 
        'Cloud infrastructure engineer', 
        'Other (please specify):', 
        'Developer Experience', 
        'Engineering manager', 
        'DevOps specialist', 
        'Engineer, site reliability', 
        'Project manager', 
        'Blockchain', 
        'nan', 
        'Developer, game or graphics', 
        'Developer Advocate', 
        'Hardware Engineer', 
        'Educator', 
        'Scientist', 
        'Marketing or sales professional', 
        'Student'
    ]

    orgsize = [
        'Select Organisation Size',
        '2 to 9 employees', 
        '5,000 to 9,999 employees', 
        '100 to 499 employees', 
        '20 to 99 employees', 
        '1,000 to 4,999 employees', 
        '10 to 19 employees', 
        '10,000 or more employees', 
        '500 to 999 employees', 
        'Just me - I am a freelancer, sole proprietor, etc.', 
        'I don’t know',
        "NAN"
    ]

    aiselect = ['Yes', "No, and I don't plan to", 'No, but I plan to soon']

    remoteworkselect = ['Remote', 'Hybrid (some remote, some in-person)', 'In-person',"Other"]

    currency = ['USD\tUnited States dollar', 'INR\tIndian rupee']
    education_level = [
        'Bachelor’s degree (B.A., B.S., B.Eng., etc.)', 
        'Some college/university study without earning a degree', 
        'Master’s degree (M.A., M.S., M.Eng., MBA, etc.)', 
        'Primary/elementary school', 
        'Professional degree (JD, MD, Ph.D, Ed.D, etc.)', 
        'Associate degree (A.A., A.S., etc.)', 
        'Secondary school (e.g. American high school, German Realschule or Gymnasium, etc.)', 
        'Something else'
    ]

    with st.container():
        st.markdown("### Personal Information")
        col1, col2 = st.columns(2)
        with col1:
            age_input = st.selectbox("Age", age, index=0, key="age_select")
        with col2:
            education_input = st.selectbox("Education Level", ["Select Education"] + education_level, index=0, key="education_select")
        
        st.markdown("### Professional Information")
        col3, col4 = st.columns(2)
        with col3:
            dev_type_input = st.selectbox("Job Role", dev_type, index=0, key="job_role_select")
            experience_input = st.slider("Years of Experience", 0, 50, 3)
        with col4:
            orgsize_input = st.selectbox("Organisation Size", ["Select Organisation Size"] + orgsize, index=0, key="org_size_select")
            yearscodepro_input = st.slider("Years of Professional Experience", 0, 50, 3)
        
        st.markdown("---")
        
        aiselect_input = st.selectbox("Do you currently use AI tools in your development process?", ["Select an option"] + aiselect, index=0, key="ai_tools_select")
        currency_input = st.selectbox("Which currency do you use day-to-day? If your answer is complicated, please pick the one you're most comfortable estimating in", ["Select Currency"] + currency, index=0, key="currency_select")
        yearscode_input = st.slider("Years of Coding Experience", 0, 50, 3)
        remotework_input = st.selectbox("Current Work Situation", ["Select Work Situation"] + remoteworkselect, index=0, key="work_situation_select")
        databases_input = st.text_input("Databases you have worked with (separated by ;)", "")
        languages_input = st.text_input("Programming Languages you have worked with (separated by ;)", "")
        learning_sources_input = st.text_input("Learning Sources you have used (separated by ;)", "")

    ok = st.button("🚀 Calculate My Salary", use_container_width=True, type="primary")
    if ok:
        if age_input == "Select Age" or dev_type_input == "Select Job Role" or orgsize_input == "Select Organisation Size":
            st.error("Please fill in all the required fields")
        else:
            with st.spinner('🧠 Analyzing your profile...'):
                map_ =  {
                   'Age': [age_input],
                   'AISelect': [aiselect_input],
                   'OrgSize':[orgsize_input],
                   'DevType':[dev_type_input],
                   'YearsCode':[yearscode_input],
                   'WorkExp': [experience_input],
                   'YearsCodePro': [yearscodepro_input],
                   "RemoteWork": [remotework_input],
                   'Currency': [currency_input],
                   "EdLevel": [education_input],
                   "LanguageHaveWorkedWith": [databases_input],
                   "DatabaseHaveWorkedWith": [languages_input],
                   "LearnCode": [learning_sources_input]
                }
                df = pd.DataFrame(map_)
                salary = prepare_dataframe(df, model, label_encoders, scaler)
                st.subheader(f"The estimated annual salary is ${salary[0]:.2f}")

show_predict_page()