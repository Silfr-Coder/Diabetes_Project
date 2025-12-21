import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bmi_calculator import BMICalculator
from diabetes_dataset import DiabetesDataset

# page configuration
st.set_page_config(
    page_title="Diabetes Analysis Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and Description
st.title("Diabetes Analysis Dashboard")
st.markdown(
    """
    This dashboard provides insights into diabetes data, including visualizations and statistical analyses.
    Explore the various sections to understand the patterns and correlations in the dataset.
    """
)

# sidebar for navigation
page = st.sidebar.selectbox(
    "Select a page:",
    ["Home", "Data Overview", "BMI Calculator",
     "Statistical Analysis & Insights", "About"]
)

# load data

# streamlit cache to optimize data loading


@st.cache_data
# function to load data
def load_data():
    return DiabetesDataset("./data/processed/diabetes_cleaned.csv")


try:
    df = load_data()

    if page == "Home":
        st.header("Welcome to the Diabetes Analysis Project")
        st.write("""
                 This dashboard provides interactive visualizations and tools for 
        exploring diabetes-related data and health metrics.
        """)

        # Display basic stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Records", df.get_record_count())
        with col2:
            st.metric("Features", df.get_feature_count())
        with col3:
            st.metric("Data Quality", f"{df.get_data_quality()}%")
    elif page == "Data Overview":
        st.header("Data Overview")

        # st.header("Dataset Preview")
        st.dataframe(df.get_preview(10), use_container_width=True)

        # Show statistics
        st.subheader("Statistical Summary")
        st.dataframe(df.get_summary(), use_container_width=True)

    elif page == "BMI Calculator":
        st.header("🧮 BMI Calculator")

        col1, col2 = st.columns(2)

        with col1:
            weight = st.number_input(
                "Enter your weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
            height = st.number_input(
                "Enter your height (m)", min_value=0.5, max_value=2.5, value=1.7, step=0.01)

        if st.button("Calculate BMI"):
            # create instance of BMICalculator
            calc = BMICalculator(weight=weight, height=height)
            bmi = calc.calculate_bmi()
            category = calc.get_category()

            with col2:
                st.metric("Your BMI", f"{bmi:.2f}")

                if category == "Underweight":
                    st.info(f"Category: {category}")
                elif category == "Normal weight":
                    st.success(f"Category: {category}")
                elif category == "Overweight":
                    st.warning(f"Category: {category}")
                else:
                    st.error(f"Category: {category}")

    elif page == "Analysis & Insights":
        st.header("📈 Analysis & Insights")
        st.write("Coming soon: Advanced visualizations and statistical analysis")

except FileNotFoundError:
    st.error("Data file not found. Please ensure 'diabetes_cleaned.csv' is in the data/processed/ folder.")

# Footer
st.markdown("---")
st.caption("Built with Streamlit | Diabetes Analysis Project")
