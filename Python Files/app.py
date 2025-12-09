import streamlit as st
from predictor import show_predict_page
from streamlit_option_menu import option_menu

# Page configuration
st.set_page_config(
    page_title="Salary Predictor",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stSelectbox, .stNumberInput, .stTextInput {
        border-radius: 5px;
        border: 1px solid #ced4da;
    }
    .css-1aumxhk {
        background-color: #f8f9fa;
        background-image: none;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.title("🔮 Salary Predictor")
    st.markdown("---")
    page = option_menu(
        menu_title=None,
        options=["🏠 Home", "📊 Predict", "📈 Explore"],
        icons=[],
        default_index=1,
        styles={
            "container": {"padding": "5px"},
            "nav-link": {"font-size": "16px", "text-align": "left", "margin": "5px 0"},
            "nav-link-selected": {"background-color": "#4CAF50"},
        }
    )

# Page routing
if page == "🏠 Home":
    st.title("Welcome to Salary Predictor")
    st.markdown("---")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("""
        <div style="text-align: center; padding: 30px 0;">
            <h1 style="font-size: 60px; margin: 0;">💰</h1>
            <h2 style="margin: 10px 0; color: #2c3e50;">Salary</h2>
            <h2 style="margin: 10px 0; color: #2c3e50;">Predictor</h2>
            <h1 style="font-size: 60px; margin: 0;">💵</h1>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("### Predict Software Developer Salaries with AI")
        st.markdown("""
        This application helps you estimate software developer salaries based on various factors 
        like experience, education, location, and job role. Simply navigate to the **Predict** 
        page and fill in your details to get an instant salary estimation.
        """)
        st.markdown("### How it works:")
        st.markdown("""
        - Select your job role and experience level
        - Enter your education details
        - Add your location and other relevant information
        - Get an accurate salary prediction instantly!
        """)

elif page == "📊 Predict":
    show_predict_page()
else:
    st.title("📊 Data Exploration")
    st.markdown("---")
    
    # Sample data for visualization (replace with your actual data)
    import pandas as pd
    import numpy as np
    import plotly.express as px
    
    # Sample data - replace this with your actual data loading logic
    data = {
        'Experience': ['0-2', '2-5', '5-10', '10+'],
        'Average Salary (USD)': [65000, 85000, 110000, 140000],
        'Job Role': ['Junior', 'Mid-Level', 'Senior', 'Lead/Manager']
    }
    df = pd.DataFrame(data)
    
    # Layout
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Salary by Experience Level")
        fig1 = px.bar(
            df, 
            x='Experience', 
            y='Average Salary (USD)',
            color='Job Role',
            title='Average Salary by Experience Level',
            height=400
        )
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.markdown("### Experience Distribution")
        fig2 = px.pie(
            df, 
            values='Average Salary (USD)', 
            names='Job Role',
            title='Salary Distribution by Job Role',
            height=400
        )
        st.plotly_chart(fig2, use_container_width=True)
    
    # Add some key metrics
    st.markdown("### Key Insights")
    st.markdown("""
    - 💰 **Highest Average Salary**: ${:,.2f} ({} level)
    - 📈 **Salary Growth**: {:.0f}% from entry to senior level
    - 🎓 **Most Common Experience Level**: {}
    """.format(
        df['Average Salary (USD)'].max(),
        df.loc[df['Average Salary (USD)'].idxmax(), 'Job Role'],
        ((df['Average Salary (USD)'].iloc[-1] - df['Average Salary (USD)'].iloc[0]) / df['Average Salary (USD)'].iloc[0]) * 100,
        df.loc[df['Average Salary (USD)'].idxmax(), 'Job Role']
    ))
    
    # Add some sample filters
    st.markdown("### Filter Data")
    selected_role = st.selectbox("Select Job Role", ["All"] + list(df['Job Role'].unique()))
    
    if selected_role != "All":
        filtered_df = df[df['Job Role'] == selected_role]
    else:
        filtered_df = df
    
    st.dataframe(filtered_df, use_container_width=True)