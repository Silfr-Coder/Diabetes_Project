import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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


@st.cache_data
def load_data():
    df = pd.read_csv("./data/processed/diabetes_cleaned.csv")
    return df


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
            st.metric("Total Records", len(df))
        with col2:
            st.metric("Features", len(df.columns))
        with col3:
            missing = df.isnull().sum().sum()
            total = len(df) * len(df.columns)
            quality = (1 - missing / total) * 100
            st.metric("Data Quality", f"{quality:.1f}%")
    elif page == "Data Overview":
        st.header("Data Overview")

        # st.header("Dataset Preview")
        st.dataframe(df.head(10), use_container_width=True)

        # Show statistics
        st.subheader("Statistical Summary")
        st.dataframe(df.describe(), use_container_width=True)

    elif page == "BMI Calculator":
        st.header("🧮 BMI Calculator")

        col1, col2 = st.columns(2)

        with col1:
            weight = st.number_input(
                "Enter your weight (kg)", min_value=1.0, max_value=300.0, value=70.0)
            height = st.number_input(
                "Enter your height (m)", min_value=0.5, max_value=2.5, value=1.7, step=0.01)

        if st.button("Calculate BMI"):
            bmi = weight / (height ** 2)

            with col2:
                st.metric("Your BMI", f"{bmi:.2f}")

                if bmi < 18.5:
                    st.info("Category: Underweight")
                elif 18.5 <= bmi < 25:
                    st.success("Category: Normal weight")
                elif 25 <= bmi < 30:
                    st.warning("Category: Overweight")
                else:
                    st.error("Category: Obese")

    elif page == "Analysis & Insights":
        st.header("📈 Analysis & Insights")
        st.write("Coming soon: Advanced visualizations and statistical analysis")

except FileNotFoundError:
    st.error("Data file not found. Please ensure 'diabetes_cleaned.csv' is in the data/processed/ folder.")

# Footer
st.markdown("---")
st.caption("Built with Streamlit | Diabetes Analysis Project")
