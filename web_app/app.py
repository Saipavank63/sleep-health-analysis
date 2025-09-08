import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add the project root to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set page configuration
st.set_page_config(
    page_title="Sleep Health Analysis",
    page_icon="🌙",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 2rem;
    }
    .stAlert {
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

def calculate_health_risk_score(sleep_duration, quality_score, deep_sleep_pct, 
                              rem_sleep_pct, age, stress_level, heart_rate):
    """Calculate health risk score based on sleep patterns and age."""
    risk_score = 0
    
    # Sleep duration risks
    if sleep_duration < 6:
        risk_score += 30
    elif sleep_duration < 7:
        risk_score += 15
    elif sleep_duration > 9:
        risk_score += 10
    
    # Sleep quality risks
    if quality_score < 60:
        risk_score += 25
    elif quality_score < 75:
        risk_score += 15
    
    # Sleep stage risks
    if deep_sleep_pct < 15:
        risk_score += 20
    if rem_sleep_pct < 20:
        risk_score += 15
    
    # Age-related risks
    if age >= 60:
        risk_score += 20
    elif age >= 45:
        risk_score += 10
    
    # Stress-related risks
    if stress_level >= 8:
        risk_score += 25
    elif stress_level >= 6:
        risk_score += 15
    
    # Heart rate risks
    if heart_rate > 75:
        risk_score += 15
    elif heart_rate < 55:
        risk_score += 10
    
    return min(100, risk_score)

def predict_health_conditions(sleep_duration, quality_score, deep_sleep_pct, 
                            rem_sleep_pct, age, stress_level, heart_rate):
    """Predict potential health conditions."""
    conditions = []
    
    if sleep_duration < 6 and heart_rate > 70:
        conditions.append('Increased cardiovascular risk')
    
    if sleep_duration < 6 or sleep_duration > 9:
        conditions.append('Metabolic disorder risk')
    
    if deep_sleep_pct < 15 or rem_sleep_pct < 20:
        conditions.append('Cognitive decline risk')
    
    if stress_level > 7 and quality_score < 70:
        conditions.append('Mental health vulnerability')
    
    if age > 50 and deep_sleep_pct < 18:
        conditions.append('Age-related sleep disorder risk')
    
    return conditions

def estimate_life_expectancy_impact(sleep_duration, quality_score, stress_level, age):
    """Estimate the potential impact on life expectancy."""
    base_impact = 0
    
    if sleep_duration < 6:
        base_impact -= 3
    elif sleep_duration < 7:
        base_impact -= 1.5
    elif sleep_duration > 9:
        base_impact -= 1
        
    if quality_score < 60:
        base_impact -= 2
    elif quality_score < 75:
        base_impact -= 1
    
    if stress_level > 7:
        base_impact -= 2
    
    age_factor = 1 + (age - 30) / 100 if age > 30 else 1
    
    return base_impact * age_factor

def get_recommendations(sleep_duration, quality_score, deep_sleep_pct, 
                       rem_sleep_pct, stress_level):
    """Generate personalized recommendations."""
    recommendations = []
    
    if sleep_duration < 7:
        recommendations.append("🕒 Increase sleep duration to at least 7 hours")
    if quality_score < 75:
        recommendations.append("🛏️ Improve sleep quality through better sleep hygiene")
    if stress_level > 6:
        recommendations.append("🧘‍♀️ Implement stress management techniques")
    if deep_sleep_pct < 15:
        recommendations.append("💪 Focus on improving deep sleep through exercise")
    if rem_sleep_pct < 20:
        recommendations.append("⏰ Improve REM sleep by maintaining regular sleep patterns")
    
    return recommendations

# Main app
st.title("🌙 Sleep Health Analysis")
st.markdown("### Interactive Health Assessment Tool")

# Sidebar for user input
with st.sidebar:
    st.header("Enter Your Sleep Data")
    
    age = st.slider("Age", 18, 100, 35)
    sleep_duration = st.slider("Sleep Duration (hours)", 4.0, 12.0, 7.0, 0.1)
    quality_score = st.slider("Sleep Quality Score (0-100)", 0, 100, 75)
    stress_level = st.slider("Stress Level (0-10)", 0, 10, 5)
    deep_sleep_pct = st.slider("Deep Sleep Percentage", 0, 40, 20)
    rem_sleep_pct = st.slider("REM Sleep Percentage", 0, 40, 25)
    heart_rate = st.slider("Average Heart Rate During Sleep", 40, 100, 65)

# Calculate metrics
risk_score = calculate_health_risk_score(
    sleep_duration, quality_score, deep_sleep_pct, 
    rem_sleep_pct, age, stress_level, heart_rate
)

conditions = predict_health_conditions(
    sleep_duration, quality_score, deep_sleep_pct, 
    rem_sleep_pct, age, stress_level, heart_rate
)

life_impact = estimate_life_expectancy_impact(
    sleep_duration, quality_score, stress_level, age
)

recommendations = get_recommendations(
    sleep_duration, quality_score, deep_sleep_pct, 
    rem_sleep_pct, stress_level
)

# Display results in main area
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Health Risk Score", f"{risk_score:.0f}/100")
    
with col2:
    st.metric("Sleep Quality", f"{quality_score:.0f}/100")
    
with col3:
    st.metric("Life Expectancy Impact", f"{life_impact:.1f} years")

# Visual representation of sleep stages
fig = go.Figure()
fig.add_trace(go.Bar(
    x=['Deep Sleep', 'REM Sleep', 'Light Sleep'],
    y=[deep_sleep_pct, rem_sleep_pct, 100-deep_sleep_pct-rem_sleep_pct],
    marker_color=['#1f77b4', '#2ca02c', '#ff7f0e']
))
fig.update_layout(
    title="Sleep Stages Distribution",
    yaxis_title="Percentage",
    showlegend=False
)
st.plotly_chart(fig)

# Health conditions
st.subheader("🏥 Potential Health Conditions")
if conditions:
    for condition in conditions:
        st.warning(condition)
else:
    st.success("No significant health risks detected")

# Recommendations
st.subheader("💡 Personalized Recommendations")
for rec in recommendations:
    st.info(rec)

# Sleep tracking feature
st.subheader("📊 Sleep Tracking")
if st.button("Add Today's Sleep Data"):
    st.session_state.setdefault('sleep_history', [])
    st.session_state.sleep_history.append({
        'date': datetime.now().strftime('%Y-%m-%d'),
        'duration': sleep_duration,
        'quality': quality_score,
        'risk_score': risk_score
    })
    st.success("Sleep data added successfully!")

if hasattr(st.session_state, 'sleep_history') and st.session_state.sleep_history:
    history_df = pd.DataFrame(st.session_state.sleep_history)
    fig = px.line(history_df, x='date', y=['duration', 'quality', 'risk_score'],
                  title='Your Sleep History')
    st.plotly_chart(fig)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center'>
        <p>🌙 Sleep Health Analysis Tool - For Educational Purposes Only</p>
        <p>Always consult with healthcare professionals for medical advice.</p>
    </div>
""", unsafe_allow_html=True)
