import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sleep_analyzer import SleepAnalyzer
from datetime import datetime, timedelta
from dotenv import load_dotenv

import traceback
from style import load_css

load_dotenv()

st.set_page_config(
    page_title="Sleep Analysis Dashboard",
    page_icon="💤",
    layout="wide"
)

def handle_error(func):
    """Decorator for error handling"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"😔 Oops! {str(e)}")
            if os.getenv("DEBUG") == "true":
                st.error(f"Debug info: {traceback.format_exc()}")
            return None
    return wrapper

@handle_error
def create_visualizations(df):
    # Enhanced color scheme for better visual appeal
    plot_bgcolor = "rgba(15, 28, 46, 0.8)"
    paper_bgcolor = "rgba(30, 42, 58, 0.9)"
    font_color = "#FFFFFF"
    
    # Enhanced color palette
    color_palette = ["#4B9CD3", "#60A5FA", "#93C5FD", "#DBEAFE", "#EFF6FF"]
    color_palette_2 = ["#4B9CD3", "#F59E0B", "#10B981", "#EF4444", "#8B5CF6"]

    # Overview Tab
    fig_overview = px.box(df, x='University_Year', y='Sleep_Duration', color='Gender',
                          title="Sleep Duration Distribution by University Year", 
                          notched=True,
                          color_discrete_sequence=color_palette_2)
    fig_overview.update_layout(
        plot_bgcolor=plot_bgcolor, 
        paper_bgcolor=paper_bgcolor, 
        font_color=font_color,
        title_font_size=18,
        title_font_color="#4B9CD3",
        showlegend=True,
        legend=dict(bgcolor="rgba(30, 42, 58, 0.8)", bordercolor="rgba(75, 156, 211, 0.3)"),
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    # Impact Analysis Tab
    fig_impact = px.scatter(df, x='Study_Hours', y='Sleep_Quality', size='Sleep_Duration',
                            color='University_Year', title="Study Hours vs Sleep Quality Impact",
                            hover_name='Gender', size_max=60,
                            color_discrete_sequence=color_palette_2)
    fig_impact.update_layout(
        plot_bgcolor=plot_bgcolor, 
        paper_bgcolor=paper_bgcolor, 
        font_color=font_color,
        title_font_size=18,
        title_font_color="#4B9CD3",
        showlegend=True,
        legend=dict(bgcolor="rgba(30, 42, 58, 0.8)", bordercolor="rgba(75, 156, 211, 0.3)"),
        margin=dict(l=50, r=50, t=80, b=50)
    )

    # Sleep Cycles Tab
    total_stages = df[['Awake', 'Light', 'Deep', 'REM']].sum()
    sleep_stages_data = {
        'stage': total_stages.index,
        'value': total_stages.values
    }
    fig_sunburst = px.sunburst(sleep_stages_data,
                               names='stage',
                               parents=['Sleep Stages'] * 4,
                               values='value',
                               title='Sleep Cycle Distribution Analysis',
                               color='stage',
                               color_discrete_map={
                                   'Awake': '#F59E0B', 'Light': '#60A5FA',
                                   'Deep': '#10B981', 'REM': '#8B5CF6'
                               })
    fig_sunburst.update_layout(
        plot_bgcolor=plot_bgcolor,
        paper_bgcolor=paper_bgcolor,
        font_color=font_color,
        title_font_size=18,
        title_font_color="#4B9CD3",
        margin=dict(l=50, r=50, t=80, b=50)
    )

    # 3D Factors
    fig_3d = px.scatter_3d(df, x='Screen_Time', y='Physical_Activity', z='Sleep_Duration',
                           color='Caffeine_Intake', size='Sleep_Quality',
                           title="3D Analysis: Screen Time, Activity & Sleep Duration", 
                           opacity=0.8,
                           color_continuous_scale=color_palette)
    fig_3d.update_layout(
        plot_bgcolor=plot_bgcolor, 
        paper_bgcolor=paper_bgcolor, 
        font_color=font_color,
        title_font_size=18,
        title_font_color="#4B9CD3",
        scene=dict(
            bgcolor=plot_bgcolor,
            xaxis=dict(backgroundcolor=plot_bgcolor, gridcolor="rgba(75, 156, 211, 0.2)"),
            yaxis=dict(backgroundcolor=plot_bgcolor, gridcolor="rgba(75, 156, 211, 0.2)"),
            zaxis=dict(backgroundcolor=plot_bgcolor, gridcolor="rgba(75, 156, 211, 0.2)")
        ),
        margin=dict(l=50, r=50, t=80, b=50)
    )

    # Sleep Patterns Over Time
    if 'Date' not in df.columns:
        df['Date'] = pd.to_datetime(df['Weekday_Sleep_Start'].apply(lambda x: (datetime.now() - timedelta(days=np.random.randint(0, 365))).strftime('%Y-%m-%d')))

    fig_animated = px.scatter(df, x='Date', y='Sleep_Duration', color='Gender',
                              size='Sleep_Quality',
                              title="Sleep Duration Patterns Over Time", 
                              range_y=[0, 12],
                              color_discrete_sequence=color_palette_2)
    fig_animated.update_layout(
        plot_bgcolor=plot_bgcolor, 
        paper_bgcolor=paper_bgcolor, 
        font_color=font_color,
        title_font_size=18,
        title_font_color="#4B9CD3",
        showlegend=True,
        legend=dict(bgcolor="rgba(30, 42, 58, 0.8)", bordercolor="rgba(75, 156, 211, 0.3)"),
        margin=dict(l=50, r=50, t=80, b=50)
    )

    # Trend Analysis
    df_sorted = df.sort_values('Date')
    fig_trend = px.line(df_sorted, x='Date', y='Sleep_Duration', 
                        title='Sleep Duration Trend Analysis', 
                        markers=True,
                        color_discrete_sequence=["#4B9CD3"])
    fig_trend.update_layout(
        plot_bgcolor=plot_bgcolor, 
        paper_bgcolor=paper_bgcolor, 
        font_color=font_color,
        title_font_size=18,
        title_font_color="#4B9CD3",
        margin=dict(l=50, r=50, t=80, b=50)
    )

    return {
        "Overview": fig_overview,
        "Impact Analysis": fig_impact,
        "Sleep Cycles": fig_sunburst,
        "3D Factors": fig_3d,
        "Sleep Patterns": fig_animated,
        "Trend Analysis": fig_trend
    }


def get_recommendations(analysis_results):
    recommendations = []
    if analysis_results['avg_duration'] < 7:
        recommendations.append("Consider increasing your sleep duration to at least 7 hours for better health.")
    if analysis_results['quality_score'] < 6:
        recommendations.append("Improve sleep quality by creating a restful environment and avoiding caffeine before bed.")
    if analysis_results['consistency_score'] < 6:
        recommendations.append("Try to maintain a consistent sleep schedule, even on weekends, to improve your circadian rhythm.")
    
    if not recommendations:
        recommendations.append("Your sleep patterns seem healthy. Keep up the good work!")
        
    return recommendations


def generate_sample_data(n_samples=50):
    # dates = [datetime.now() - timedelta(days=i) for i in range(n_samples)]
    start_time = datetime.strptime("22:00", "%H:%M")
    time_deltas = [timedelta(minutes=int(i)) for i in np.random.normal(0, 30, n_samples)]
    
    data = {
        'Student_ID': np.arange(n_samples),
        'Age': np.random.randint(18, 26, n_samples),
        'Gender': np.random.choice(['Male', 'Female'], n_samples),
        'University_Year': np.random.choice(['1st Year', '2nd Year', '3rd Year'], n_samples),
        'Sleep_Duration': np.random.normal(7, 1.5, n_samples),
        'Study_Hours': np.random.normal(5, 2, n_samples),
        'Screen_Time': np.random.normal(4, 1.5, n_samples),
        'Caffeine_Intake': np.random.randint(0, 5, n_samples),
        'Physical_Activity': np.random.normal(45, 20, n_samples),
        'Sleep_Quality': np.random.randint(4, 10, n_samples),
        'Weekday_Sleep_Start': [(start_time + delta).strftime("%H:%M") for delta in time_deltas],
        'Weekend_Sleep_Start': [(start_time + delta + timedelta(hours=1)).strftime("%H:%M") for delta in time_deltas],
        'Weekday_Sleep_End': [(start_time + delta + timedelta(hours=np.random.normal(7, 1))).strftime("%H:%M") for delta in time_deltas],
        'Weekend_Sleep_End': [(start_time + delta + timedelta(hours=np.random.normal(8, 1.5))).strftime("%H:%M") for delta in time_deltas]
    }
    return pd.DataFrame(data)

load_css('style.css')

# Enhanced Header with animated elements
st.markdown("""
<div style="text-align: center; margin-bottom: 3rem;">
    <div style="position: relative; display: inline-block;">
        <h1 style="margin-bottom: 0.5rem; position: relative; z-index: 2;">🌙 Sleep Analysis Dashboard</h1>
        <div style="position: absolute; top: -10px; left: -10px; right: -10px; bottom: -10px; 
                    background: linear-gradient(135deg, rgba(75, 156, 211, 0.1), rgba(96, 165, 250, 0.1)); 
                    border-radius: 20px; z-index: 1; animation: pulse 3s ease-in-out infinite;"></div>
    </div>
    <p style="font-size: 1.2rem; color: #E5E7EB; margin-bottom: 2rem; line-height: 1.6;">
        Discover insights about your sleep patterns and get personalized recommendations for better sleep health
    </p>
    <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-top: 1rem;">
        <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.2), rgba(96, 165, 250, 0.2)); 
                    border: 1px solid rgba(75, 156, 211, 0.4); border-radius: 12px; padding: 0.8rem 1.5rem;">
            <span style="color: #FFFFFF; font-weight: 600;">📊 Data Analysis</span>
        </div>
        <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.2), rgba(96, 165, 250, 0.2)); 
                    border: 1px solid rgba(75, 156, 211, 0.4); border-radius: 12px; padding: 0.8rem 1.5rem;">
            <span style="color: #FFFFFF; font-weight: 600;">💡 AI Insights</span>
        </div>
        <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.2), rgba(96, 165, 250, 0.2)); 
                    border: 1px solid rgba(75, 156, 211, 0.4); border-radius: 12px; padding: 0.8rem 1.5rem;">
            <span style="color: #FFFFFF; font-weight: 600;">🎯 Recommendations</span>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Enhanced info box with interactive elements
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.15), rgba(96, 165, 250, 0.1)); 
            border: 1px solid rgba(75, 156, 211, 0.4); 
            border-radius: 16px; 
            padding: 2rem; 
            margin-bottom: 2rem;
            backdrop-filter: blur(20px);
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;">
    <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; 
                background: linear-gradient(90deg, #4B9CD3, #60A5FA, #93C5FD);"></div>
    <div style="display: flex; align-items: center; gap: 16px;">
        <div style="background: linear-gradient(135deg, #4B9CD3, #60A5FA); 
                    border-radius: 50%; width: 60px; height: 60px; 
                    display: flex; align-items: center; justify-content: center;
                    box-shadow: 0 4px 16px rgba(75, 156, 211, 0.3);">
            <span style="font-size: 1.8rem;">💬</span>
        </div>
        <div style="flex: 1;">
            <strong style="color: #4B9CD3; font-size: 1.2rem; display: block; margin-bottom: 0.5rem;">
                🤖 AI Sleep Expert Available!
            </strong>
            <p style="margin: 0; color: #E5E7EB; line-height: 1.6; font-size: 1rem;">
                Navigate to the 'Chat with Expert' page from the sidebar to get personalized sleep advice, 
                detailed insights, and actionable recommendations tailored to your sleep patterns.
            </p>
            <div style="margin-top: 1rem; display: flex; gap: 0.5rem; flex-wrap: wrap;">
                <span style="background: rgba(75, 156, 211, 0.2); border-radius: 8px; padding: 0.3rem 0.8rem; 
                           font-size: 0.9rem; color: #E5E7EB;">💡 Personalized Tips</span>
                <span style="background: rgba(75, 156, 211, 0.2); border-radius: 8px; padding: 0.3rem 0.8rem; 
                           font-size: 0.9rem; color: #E5E7EB;">📊 Data Analysis</span>
                <span style="background: rgba(75, 156, 211, 0.2); border-radius: 8px; padding: 0.3rem 0.8rem; 
                           font-size: 0.9rem; color: #E5E7EB;">🎯 Sleep Optimization</span>
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.2), rgba(96, 165, 250, 0.1)); 
                    border: 1px solid rgba(75, 156, 211, 0.3); border-radius: 16px; padding: 1.5rem; margin-bottom: 1rem;">
            <h2 style="color: #4B9CD3; margin-bottom: 0.8rem; font-size: 1.5rem;">⚙️ Dashboard Controls</h2>
            <p style="color: #E5E7EB; font-size: 0.95rem; line-height: 1.5; margin-bottom: 0;">
                Configure your data source and customize your sleep analysis experience
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    data_option = st.selectbox("📊 Data Source", ["Upload CSV", "Manual Entry", "Use Sample Data"])
    
    if data_option == "Upload CSV":
        uploaded_file = st.file_uploader("📁 Upload your CSV", type=["csv"])
    elif data_option == "Manual Entry":
        uploaded_file = None
        st.markdown("""
        <div style="background: rgba(75, 156, 211, 0.1); border: 1px solid rgba(75, 156, 211, 0.3); 
                    border-radius: 8px; padding: 1rem; margin-bottom: 1rem;">
            <p style="color: #E5E7EB; font-size: 0.9rem; margin: 0;">
                📝 Enter your sleep data manually below
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        uploaded_file = None

if uploaded_file:
    df = pd.read_csv(uploaded_file)
elif data_option == "Manual Entry":
    # Manual Data Entry Form
    st.markdown("""
    <div style="margin: 2rem 0;">
        <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.15), rgba(96, 165, 250, 0.1)); 
                    border: 1px solid rgba(75, 156, 211, 0.4); border-radius: 20px; padding: 2rem; margin-bottom: 2rem;
                    backdrop-filter: blur(20px); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);">
            <h2 style="color: #4B9CD3; margin-bottom: 1rem; font-size: 1.8rem; text-align: center;">
                📝 Manual Sleep Data Entry
            </h2>
            <p style="color: #E5E7EB; margin-bottom: 0; text-align: center; font-size: 1.1rem; line-height: 1.6;">
                Enter your sleep data for comprehensive analysis and personalized insights
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for form
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(15, 28, 46, 0.95), rgba(30, 42, 58, 0.95)); 
                    border: 1px solid rgba(75, 156, 211, 0.4); 
                    border-radius: 20px; 
                    padding: 2rem; 
                    margin-bottom: 1.5rem;
                    backdrop-filter: blur(20px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    position: relative;
                    overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; 
                        background: linear-gradient(90deg, #4B9CD3, #60A5FA, #93C5FD);"></div>
            <h3 style="color: #4B9CD3; margin-bottom: 1.5rem; font-size: 1.4rem; display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">👤</span> Personal Information
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        age = st.number_input("Age", min_value=15, max_value=80, value=20, step=1)
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        university_year = st.selectbox("University Year", ["1st Year", "2nd Year", "3rd Year", "4th Year", "Graduate"])
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(15, 28, 46, 0.95), rgba(30, 42, 58, 0.95)); 
                    border: 1px solid rgba(75, 156, 211, 0.4); 
                    border-radius: 20px; 
                    padding: 2rem; 
                    margin-bottom: 1.5rem;
                    backdrop-filter: blur(20px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    position: relative;
                    overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; 
                        background: linear-gradient(90deg, #4B9CD3, #60A5FA, #93C5FD);"></div>
            <h3 style="color: #4B9CD3; margin-bottom: 1.5rem; font-size: 1.4rem; display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">🌙</span> Sleep Data
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        sleep_duration = st.slider("Sleep Duration (hours)", min_value=3.0, max_value=12.0, value=7.5, step=0.5)
        sleep_quality = st.slider("Sleep Quality (1-10)", min_value=1, max_value=10, value=7, step=1)
        
        # Sleep timing
        weekday_start = st.time_input("Weekday Sleep Start Time", value=datetime.strptime("22:00", "%H:%M").time())
        weekday_end = st.time_input("Weekday Sleep End Time", value=datetime.strptime("07:00", "%H:%M").time())
        weekend_start = st.time_input("Weekend Sleep Start Time", value=datetime.strptime("23:00", "%H:%M").time())
        weekend_end = st.time_input("Weekend Sleep End Time", value=datetime.strptime("08:00", "%H:%M").time())
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(15, 28, 46, 0.95), rgba(30, 42, 58, 0.95)); 
                    border: 1px solid rgba(75, 156, 211, 0.4); 
                    border-radius: 20px; 
                    padding: 2rem; 
                    margin-bottom: 1.5rem;
                    backdrop-filter: blur(20px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                    position: relative;
                    overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; 
                        background: linear-gradient(90deg, #4B9CD3, #60A5FA, #93C5FD);"></div>
            <h3 style="color: #4B9CD3; margin-bottom: 1.5rem; font-size: 1.4rem; display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1.2rem;">📚</span> Study & Lifestyle
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        study_hours = st.slider("Study Hours per Day", min_value=0.0, max_value=12.0, value=5.0, step=0.5)
        screen_time = st.slider("Screen Time (hours)", min_value=0.0, max_value=16.0, value=4.0, step=0.5)
        caffeine_intake = st.slider("Caffeine Intake (cups)", min_value=0, max_value=10, value=2, step=1)
        physical_activity = st.slider("Physical Workout(minutes/day)", min_value=0, max_value=180, value=45, step=5)
    
    # Add multiple entries option
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(15, 28, 46, 0.95), rgba(30, 42, 58, 0.95)); 
                border: 1px solid rgba(75, 156, 211, 0.4); 
                border-radius: 20px; 
                padding: 2rem; 
                margin: 1.5rem 0;
                backdrop-filter: blur(20px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                position: relative;
                overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; 
                    background: linear-gradient(90deg, #4B9CD3, #60A5FA, #93C5FD);"></div>
        <h3 style="color: #4B9CD3; margin-bottom: 1.5rem; font-size: 1.4rem; display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.2rem;">📊</span> Data Management
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    col3, col4 = st.columns(2)
    
    with col3:
        if st.button("🚀 Generate Analysis", type="primary"):
            # Create data dictionary
            manual_data = {
                'Student_ID': [1],
                'Age': [age],
                'Gender': [gender],
                'University_Year': [university_year],
                'Sleep_Duration': [sleep_duration],
                'Study_Hours': [study_hours],
                'Screen_Time': [screen_time],
                'Caffeine_Intake': [caffeine_intake],
                'Physical_Activity': [physical_activity],
                'Sleep_Quality': [sleep_quality],
                'Weekday_Sleep_Start': [weekday_start.strftime("%H:%M")],
                'Weekend_Sleep_Start': [weekend_start.strftime("%H:%M")],
                'Weekday_Sleep_End': [weekend_end.strftime("%H:%M")],
                'Weekend_Sleep_End': [weekend_end.strftime("%H:%M")]
            }
            
            df = pd.DataFrame(manual_data)
            st.session_state['manual_data'] = df
            st.success("✅ Data entered successfully! Scroll down to see your analysis.")
            st.balloons()
    
    with col4:
        if st.button("🗑️ Clear Data", type="secondary"):
            if 'manual_data' in st.session_state:
                del st.session_state['manual_data']
            st.success("✅ Data cleared successfully!")
            st.rerun()
    
    # Add multiple days option
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(15, 28, 46, 0.95), rgba(30, 42, 58, 0.95)); 
                border: 1px solid rgba(75, 156, 211, 0.4); 
                border-radius: 20px; 
                padding: 2rem; 
                margin: 1.5rem 0;
                backdrop-filter: blur(20px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
                position: relative;
                overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; 
                    background: linear-gradient(90deg, #4B9CD3, #60A5FA, #93C5FD);"></div>
        <h3 style="color: #4B9CD3; margin-bottom: 1rem; font-size: 1.4rem; display: flex; align-items: center; gap: 0.5rem;">
            <span style="font-size: 1.2rem;">📅</span> Add Multiple Days
        </h3>
        <p style="color: #E5E7EB; font-size: 1rem; line-height: 1.5; margin-bottom: 0;">
            Want to track multiple days? Use this quick form to generate comprehensive sleep data:
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    num_days = st.number_input("Number of days to add", min_value=1, max_value=30, value=7, step=1)
    
    if st.button("📊 Generate Multiple Days Data"):
        # Generate multiple days of data with some variation
        import random
        
        multiple_data = []
        for i in range(num_days):
            # Add some realistic variation to the data
            sleep_var = random.uniform(-1, 1)
            quality_var = random.randint(-2, 2)
            study_var = random.uniform(-1, 1)
            
            day_data = {
                'Student_ID': i + 1,
                'Age': age,
                'Gender': gender,
                'University_Year': university_year,
                'Sleep_Duration': max(3, min(12, sleep_duration + sleep_var)),
                'Study_Hours': max(0, min(12, study_hours + study_var)),
                'Screen_Time': screen_time,
                'Caffeine_Intake': caffeine_intake,
                'Physical_Activity': physical_activity,
                'Sleep_Quality': max(1, min(10, sleep_quality + quality_var)),
                'Weekday_Sleep_Start': weekday_start.strftime("%H:%M"),
                'Weekend_Sleep_Start': weekend_start.strftime("%H:%M"),
                'Weekday_Sleep_End': weekday_end.strftime("%H:%M"),
                'Weekend_Sleep_End': weekend_end.strftime("%H:%M")
            }
            multiple_data.append(day_data)
        
        df = pd.DataFrame(multiple_data)
        st.session_state['manual_data'] = df
        st.success(f"✅ Generated {num_days} days of sleep data! Scroll down to see your analysis.")
        st.balloons()
    
    # Show current data if exists
    if 'manual_data' in st.session_state:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.15), rgba(96, 165, 250, 0.1)); 
                    border: 1px solid rgba(75, 156, 211, 0.4); 
                    border-radius: 16px; 
                    padding: 1.5rem; 
                    margin: 1.5rem 0;
                    backdrop-filter: blur(20px);
                    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                    position: relative;
                    overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; 
                        background: linear-gradient(90deg, #4B9CD3, #60A5FA, #93C5FD);"></div>
            <h4 style="color: #4B9CD3; margin-bottom: 1rem; font-size: 1.2rem; display: flex; align-items: center; gap: 0.5rem;">
                <span style="font-size: 1rem;">📋</span> Current Data Summary
            </h4>
        </div>
        """, unsafe_allow_html=True)
        
        current_df = st.session_state['manual_data']
        st.dataframe(current_df, use_container_width=True)
        
        # Download option
        csv = current_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Data as CSV",
            data=csv,
            file_name="my_sleep_data.csv",
            mime="text/csv"
        )
    
    # Check if manual data exists in session state
    if 'manual_data' in st.session_state:
        df = st.session_state['manual_data']
    else:
        # Show placeholder message
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.15), rgba(96, 165, 250, 0.1)); 
                    border: 1px solid rgba(75, 156, 211, 0.4); 
                    border-radius: 20px; 
                    padding: 3rem; 
                    margin: 3rem 0;
                    backdrop-filter: blur(20px);
                    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
                    text-align: center;
                    position: relative;
                    overflow: hidden;">
            <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; 
                        background: linear-gradient(90deg, #4B9CD3, #60A5FA, #93C5FD, #DBEAFE);"></div>
            <h3 style="color: #4B9CD3; margin-bottom: 1.5rem; font-size: 1.8rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
                <span style="font-size: 1.5rem;">📊</span> Ready to Analyze Your Sleep?
            </h3>
            <p style="color: #E5E7EB; font-size: 1.2rem; line-height: 1.7; margin-bottom: 2rem;">
                Fill in your sleep data above and click "Generate Analysis" to get personalized insights and recommendations!
            </p>
            <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem;">
                <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.3), rgba(96, 165, 250, 0.2)); 
                            border: 1px solid rgba(75, 156, 211, 0.4); border-radius: 12px; padding: 0.8rem 1.5rem;">
                    <span style="color: #FFFFFF; font-weight: 600; font-size: 1rem;">🌙 Sleep Duration</span>
                </div>
                <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.3), rgba(96, 165, 250, 0.2)); 
                            border: 1px solid rgba(75, 156, 211, 0.4); border-radius: 12px; padding: 0.8rem 1.5rem;">
                    <span style="color: #FFFFFF; font-weight: 600; font-size: 1rem;">📚 Study Hours</span>
                </div>
                <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.3), rgba(96, 165, 250, 0.2)); 
                            border: 1px solid rgba(75, 156, 211, 0.4); border-radius: 12px; padding: 0.8rem 1.5rem;">
                    <span style="color: #FFFFFF; font-weight: 600; font-size: 1rem;">💻 Screen Time</span>
                </div>
            </div>
            <div style="background: rgba(75, 156, 211, 0.1); border: 1px solid rgba(75, 156, 211, 0.3); 
                        border-radius: 12px; padding: 1rem; margin-top: 1rem;">
                <p style="color: #E5E7EB; font-size: 0.95rem; margin: 0;">
                    💡 <strong>Tip:</strong> Use the "Generate Multiple Days Data" feature to create comprehensive sleep patterns for better analysis.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        df = generate_sample_data()  # Use sample data as placeholder
else:
    df = generate_sample_data()

# Data processing for sleep cycles
quality_bins = [0, 5, 8, 11]
quality_labels = ['Poor', 'Good', 'Excellent']
df['Quality_Category'] = pd.cut(df['Sleep_Quality'], bins=quality_bins, labels=quality_labels, right=False)

stage_percentages = {
    'Poor': {'Awake': 0.20, 'Light': 0.55, 'Deep': 0.15, 'REM': 0.10},
    'Good': {'Awake': 0.10, 'Light': 0.50, 'Deep': 0.20, 'REM': 0.20},
    'Excellent': {'Awake': 0.05, 'Light': 0.45, 'Deep': 0.25, 'REM': 0.25}
}

for stage in ['Awake', 'Light', 'Deep', 'REM']:
    df[stage] = df.apply(
        lambda row: row['Sleep_Duration'] * stage_percentages[row['Quality_Category']][stage],
        axis=1
    )

analyzer = SleepAnalyzer()
analysis_results = analyzer.analyze(df)
st.session_state['analysis_results'] = analysis_results
st.session_state['df'] = df

st.markdown("""
    <div style="display: flex; justify-content: space-around; gap: 1rem;">
        <div class="metric-card"><h3>Avg Sleep Duration</h3><p>{:.1f}h</p></div>
        <div class="metric-card"><h3>Sleep Quality</h3><p>{:.1f}/10</p></div>
        <div class="metric-card"><h3>Consistency</h3><p>{:.1f}/10</p></div>
        <div class="metric-card"><h3>Activity Impact</h3><p>{:.0f}min/day</p></div>
    </div>
""".format(
    analysis_results['avg_duration'],
    analysis_results['quality_score'],
    analysis_results['consistency_score'],
    df['Physical_Activity'].mean()
), unsafe_allow_html=True)

# Enhanced Recommendations Section
st.markdown("""
<div style="margin: 3rem 0;">
    <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.15), rgba(96, 165, 250, 0.1)); 
                border: 1px solid rgba(75, 156, 211, 0.4); 
                border-radius: 20px; 
                padding: 2rem; 
                margin-bottom: 2rem;
                backdrop-filter: blur(20px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                text-align: center;
                position: relative;
                overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 3px; 
                    background: linear-gradient(90deg, #4B9CD3, #60A5FA, #93C5FD);"></div>
        <h2 style="color: #4B9CD3; margin-bottom: 1rem; font-size: 1.8rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
            <span style="font-size: 1.5rem;">💡</span> Personalized Recommendations
        </h2>
        <p style="color: #E5E7EB; font-size: 1.1rem; line-height: 1.6; margin-bottom: 0;">
            Based on your sleep analysis, here are tailored recommendations to improve your sleep quality
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

recommendations = get_recommendations(analysis_results)
for i, rec in enumerate(recommendations):
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.15), rgba(96, 165, 250, 0.1)); 
                border: 1px solid rgba(75, 156, 211, 0.4); 
                border-radius: 16px; 
                padding: 1.5rem; 
                margin-bottom: 1rem;
                backdrop-filter: blur(20px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                position: relative;
                overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 2px; 
                    background: linear-gradient(90deg, #4B9CD3, #60A5FA);"></div>
        <div style="display: flex; align-items: center; gap: 16px;">
            <div style="background: linear-gradient(135deg, #4B9CD3, #60A5FA); 
                        border-radius: 50%; width: 50px; height: 50px; 
                        display: flex; align-items: center; justify-content: center;
                        box-shadow: 0 4px 16px rgba(75, 156, 211, 0.3);">
                <span style="font-size: 1.3rem;">✨</span>
            </div>
            <p style="margin: 0; color: #E5E7EB; line-height: 1.6; font-size: 1.1rem; flex: 1;">{rec}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

charts = create_visualizations(df.copy())
tab_names = ["Overview", "Impact Analysis", "Sleep Cycles", "3D Factors", "Sleep Patterns", "Trend Analysis"]
tabs = st.tabs(tab_names)

for tab, name in zip(tabs, tab_names):
    with tab:
        st.plotly_chart(charts.get(name), use_container_width=True)

# Additional Information and Tips Section
st.markdown("""
<div style="margin: 4rem 0 3rem 0;">
    <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.15), rgba(96, 165, 250, 0.1)); 
                border: 1px solid rgba(75, 156, 211, 0.4); 
                border-radius: 20px; 
                padding: 2.5rem; 
                margin-bottom: 2rem;
                backdrop-filter: blur(20px);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
                text-align: center;
                position: relative;
                overflow: hidden;">
        <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; 
                    background: linear-gradient(90deg, #4B9CD3, #60A5FA, #93C5FD, #DBEAFE);"></div>
        <h2 style="color: #4B9CD3; margin-bottom: 1rem; font-size: 2rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
            <span style="font-size: 1.8rem;">🌙</span> Sleep Science & Tips
        </h2>
        <p style="color: #E5E7EB; font-size: 1.1rem; line-height: 1.6; margin-bottom: 0;">
            Discover the science behind sleep and learn practical tips for better sleep health
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

# Create columns for different information sections
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(15, 28, 46, 0.9), rgba(30, 42, 58, 0.9)); 
                border: 1px solid rgba(75, 156, 211, 0.3); 
                border-radius: 16px; 
                padding: 1.5rem; 
                margin-bottom: 1rem;
                backdrop-filter: blur(10px);">
        <h3 style="color: #4B9CD3; margin-bottom: 1rem;">💡 Why Sleep Matters</h3>
        <ul style="color: #E5E7EB; line-height: 1.6; padding-left: 1.2rem;">
            <li><strong>Memory Consolidation:</strong> Sleep helps process and store new information</li>
            <li><strong>Physical Recovery:</strong> Muscles repair and grow during deep sleep</li>
            <li><strong>Immune System:</strong> Sleep strengthens your body's defense mechanisms</li>
            <li><strong>Mental Health:</strong> Quality sleep reduces stress and improves mood</li>
            <li><strong>Academic Performance:</strong> Better sleep = better focus and learning</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(15, 28, 46, 0.9), rgba(30, 42, 58, 0.9)); 
                border: 1px solid rgba(75, 156, 211, 0.3); 
                border-radius: 16px; 
                padding: 1.5rem; 
                margin-bottom: 1rem;
                backdrop-filter: blur(10px);">
        <h3 style="color: #4B9CD3; margin-bottom: 1rem;">🎯 Sleep Cycle Stages</h3>
        <div style="color: #E5E7EB; line-height: 1.6;">
            <p><strong>🌅 Awake:</strong> Brief awakenings during sleep (5-10% of night)</p>
            <p><strong>🌊 Light Sleep:</strong> Transition phase (45-55% of night)</p>
            <p><strong>🌌 Deep Sleep:</strong> Physical restoration (20-25% of night)</p>
            <p><strong>💭 REM Sleep:</strong> Dreaming & memory processing (20-25% of night)</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Tips Section
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.1), rgba(96, 165, 250, 0.1)); 
            border: 1px solid rgba(75, 156, 211, 0.3); 
            border-radius: 16px; 
            padding: 2rem; 
            margin: 2rem 0;
            backdrop-filter: blur(10px);">
    <h3 style="color: #4B9CD3; margin-bottom: 1.5rem; text-align: center;">🌟 Pro Tips for Better Sleep</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1rem;">
        <div style="background: rgba(30, 42, 58, 0.5); border-radius: 12px; padding: 1rem;">
            <h4 style="color: #60A5FA; margin-bottom: 0.5rem;">🌅 Morning Routine</h4>
            <ul style="color: #E5E7EB; font-size: 0.9rem; line-height: 1.5;">
                <li>Get sunlight within 30 minutes of waking</li>
                <li>Exercise in the morning, not evening</li>
                <li>Eat a protein-rich breakfast</li>
            </ul>
        </div>
        <div style="background: rgba(30, 42, 58, 0.5); border-radius: 12px; padding: 1rem;">
            <h4 style="color: #60A5FA; margin-bottom: 0.5rem;">🌙 Evening Routine</h4>
            <ul style="color: #E5E7EB; font-size: 0.9rem; line-height: 1.5;">
                <li>Dim lights 2 hours before bed</li>
                <li>Avoid screens 1 hour before sleep</li>
                <li>Create a relaxing bedtime ritual</li>
            </ul>
        </div>
        <div style="background: rgba(30, 42, 58, 0.5); border-radius: 12px; padding: 1rem;">
            <h4 style="color: #60A5FA; margin-bottom: 0.5rem;">🏠 Sleep Environment</h4>
            <ul style="color: #E5E7EB; font-size: 0.9rem; line-height: 1.5;">
                <li>Keep room cool (65-68°F/18-20°C)</li>
                <li>Use blackout curtains</li>
                <li>Invest in a comfortable mattress</li>
            </ul>
        </div>
        <div style="background: rgba(30, 42, 58, 0.5); border-radius: 12px; padding: 1rem;">
            <h4 style="color: #60A5FA; margin-bottom: 0.5rem;">🍽️ Nutrition Tips</h4>
            <ul style="color: #E5E7EB; font-size: 0.9rem; line-height: 1.5;">
                <li>Avoid caffeine after 2 PM</li>
                <li>Don't eat large meals 3 hours before bed</li>
                <li>Consider magnesium-rich foods</li>
            </ul>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Fun Facts Section
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(15, 28, 46, 0.9), rgba(30, 42, 58, 0.9)); 
            border: 1px solid rgba(75, 156, 211, 0.3); 
            border-radius: 16px; 
            padding: 2rem; 
            margin: 2rem 0;
            backdrop-filter: blur(10px);">
    <h3 style="color: #4B9CD3; margin-bottom: 1.5rem; text-align: center;">🤓 Did You Know?</h3>
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem;">
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🕐</div>
            <p style="color: #E5E7EB; font-size: 0.9rem; margin: 0;">Humans spend 1/3 of their lives sleeping</p>
        </div>
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🧠</div>
            <p style="color: #E5E7EB; font-size: 0.9rem; margin: 0;">Your brain is more active during REM sleep than when awake</p>
        </div>
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">🌍</div>
            <p style="color: #E5E7EB; font-size: 0.9rem; margin: 0;">Sleep deprivation affects 1 in 3 adults worldwide</p>
        </div>
        <div style="text-align: center; padding: 1rem;">
            <div style="font-size: 2rem; margin-bottom: 0.5rem;">⚡</div>
            <p style="color: #E5E7EB; font-size: 0.9rem; margin: 0;">Just 1 night of poor sleep can reduce cognitive performance by 30%</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Call to Action
st.markdown("""
<div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.25), rgba(96, 165, 250, 0.2)); 
            border: 2px solid rgba(75, 156, 211, 0.6); 
            border-radius: 20px; 
            padding: 3rem; 
            margin: 3rem 0;
            backdrop-filter: blur(20px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
            text-align: center;
            position: relative;
            overflow: hidden;">
    <div style="position: absolute; top: 0; left: 0; right: 0; height: 4px; 
                background: linear-gradient(90deg, #4B9CD3, #60A5FA, #93C5FD, #DBEAFE);"></div>
    <h3 style="color: #4B9CD3; margin-bottom: 1.5rem; font-size: 1.8rem; display: flex; align-items: center; justify-content: center; gap: 0.5rem;">
        <span style="font-size: 1.5rem;">🚀</span> Ready to Optimize Your Sleep?
    </h3>
    <p style="color: #E5E7EB; font-size: 1.2rem; line-height: 1.7; margin-bottom: 2rem;">
        Use the AI Sleep Expert in the sidebar to get personalized advice, track your progress, and discover 
        sleep optimization strategies tailored just for you!
    </p>
    <div style="display: flex; justify-content: center; gap: 1rem; flex-wrap: wrap; margin-bottom: 1.5rem;">
        <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.4), rgba(96, 165, 250, 0.3)); 
                    border: 1px solid rgba(75, 156, 211, 0.5); border-radius: 12px; padding: 1rem 1.5rem;">
            <span style="color: #FFFFFF; font-weight: 600; font-size: 1rem;">💬 Chat with AI Expert</span>
        </div>
        <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.4), rgba(96, 165, 250, 0.3)); 
                    border: 1px solid rgba(75, 156, 211, 0.5); border-radius: 12px; padding: 1rem 1.5rem;">
            <span style="color: #FFFFFF; font-weight: 600; font-size: 1rem;">📊 Track Your Progress</span>
        </div>
        <div style="background: linear-gradient(135deg, rgba(75, 156, 211, 0.4), rgba(96, 165, 250, 0.3)); 
                    border: 1px solid rgba(75, 156, 211, 0.5); border-radius: 12px; padding: 1rem 1.5rem;">
            <span style="color: #FFFFFF; font-weight: 600; font-size: 1rem;">🎯 Get Personalized Tips</span>
        </div>
    </div>
    <div style="background: rgba(75, 156, 211, 0.1); border: 1px solid rgba(75, 156, 211, 0.3); 
                border-radius: 12px; padding: 1rem; margin-top: 1rem;">
        <p style="color: #E5E7EB; font-size: 0.95rem; margin: 0;">
            🌟 <strong>Start your journey to better sleep today!</strong> Your personalized sleep optimization plan awaits.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

