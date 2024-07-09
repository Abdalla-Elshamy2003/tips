from tkinter import Image
from PIL import Image
import requests
from io import BytesIO
import streamlit as st # type: ignore
import pandas   as pd # type: ignor
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Tips Dashboard",
    layout="wide",
    page_icon=None,
    initial_sidebar_state="expanded"
)

# Load data
df = pd.read_csv('C:/Users/dell/OneDrive/Desktop/coursese_machinfy/session7/tips.csv')

# Load image
image_url = "https://th.bing.com/th/id/R.b9237d15458b596b74817cf45a12e7d3?rik=qS1Xt6zVIs4V1w&riu=http%3a%2f%2fwww.spanprogram.com%2ftips-opcional.png&ehk=vOgzdp7snguYUJY9yW1CkrpYwKYwqTmPP04ge%2btzdZY%3d&risl=&pid=ImgRaw&r=0"
image = st.image(image_url, width=150)

# Introduction section
st.title("Welcome to the Tips Dashboard!")
st.markdown("""
    This dashboard provides insights into tips data. Explore key metrics, filter your data, and visualize trends interactively.
    Use the button below to access the dashboard:
    """)

# Main page content
if "go_to_dashboard" not in st.session_state:
    st.session_state.go_to_dashboard = False

if not st.session_state.go_to_dashboard:
    if st.button("Go to Dashboard"):
        st.session_state.go_to_dashboard = True
else:
    # Calculate metrics (example)
    max_total_bill = df['total_bill'].max()
    min_total_bill = df['total_bill'].min()
    max_tips = df['tip'].max()
    min_tips = df['tip'].min()
    total_bill_sum = df['total_bill'].sum()


    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric(label="Max Total Bill", value=max_total_bill)
    with col2:
        st.metric(label="Min Total Bill", value=min_total_bill)
    with col3:
        st.metric(label="Total Bill Sum", value=total_bill_sum)
    with col4:
        st.metric(label="Max Tips", value=max_tips)
    with col5:
        st.metric(label="Min Tips", value=min_tips)

    # Filters (example)
    st.sidebar.header("Filters for Categorical Variables")
    cat_filters = st.sidebar.selectbox("Select Filters", [None, "sex", "smoker", "day", "time"])
    Rows_filters = st.sidebar.selectbox("Rows Filters", [None, "sex", "smoker", "day", "time"])
    Colums_filters = st.sidebar.selectbox("Columns Filters", [None, "sex", "smoker", "day", "time"])

    st.sidebar.header("Filters for Numerical Variables")
    total_bill_range = st.sidebar.slider("Total Bill Range", float(df["total_bill"].min()), float(df["total_bill"].max()), (float(df["total_bill"].min()), float(df["total_bill"].max())))
    tip_range = st.sidebar.slider("Tip Range", float(df["tip"].min()), float(df["tip"].max()), (float(df["tip"].min()), float(df["tip"].max())))

    # Apply filters (example)
    filtered_data = df[(df["total_bill"] >= total_bill_range[0]) & (df["total_bill"] <= total_bill_range[1]) &
                       (df["tip"] >= tip_range[0]) & (df["tip"] <= tip_range[1])]

    if cat_filters:
        filtered_data = filtered_data[filtered_data[cat_filters].notna()]
    if Rows_filters:
        filtered_data = filtered_data[filtered_data[Rows_filters].notna()]
    if Colums_filters:
        filtered_data = filtered_data[filtered_data[Colums_filters].notna()]

    # Scatter plot (example)
    fig = px.scatter(filtered_data, x="total_bill", y="tip", color=cat_filters, size="size", hover_data=["smoker", "day"],
                     title="Scatter Plot of Total Bill vs Tip",
                     facet_col=Colums_filters,
                     facet_row=Rows_filters)
    st.plotly_chart(fig)

    # Additional plots (example)
    col1, col2, col3 = st.columns(3)
    with col1:
        fig1 = px.bar(filtered_data, x="sex", y="total_bill", color=cat_filters, title="Total Bill by Sex")
        st.plotly_chart(fig1)
    with col2:
        fig2 = px.pie(filtered_data, names='smoker', values='tip', title="Tip Distribution by Smoker", color=cat_filters)
        st.plotly_chart(fig2)
    with col3:
        fig3 = px.pie(filtered_data, names='day', values='tip', title="Tip Distribution by Day", hole=0.4, color=cat_filters)
        st.plotly_chart(fig3)


# Add links to LinkedIn, GitHub, Kaggle
    st.markdown("### Follow Me:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("[![LinkedIn](https://img.shields.io/badge/LinkedIn-Abdalla%20Elshamy-blue)](https://www.linkedin.com/in/abdalla-elshamy-30619824b/)")
    with col2:
        st.markdown("[![GitHub](https://img.shields.io/badge/GitHub-Abdalla--Elshamy2003-green)](https://github.com/Abdalla-Elshamy2003)")
    with col3:
        st.markdown("[![Kaggle](https://img.shields.io/badge/Kaggle-Abdalla%20Elshamy-orange)](https://www.kaggle.com/abdallaelshamy)")

 
    st.markdown("Created by ENG: Abdalla Elshamy")


    # Add a button to go back to the main page
    st.sidebar.button("Back to Main Page", on_click=lambda: st.session_state.pop("go_to_dashboard", None))
