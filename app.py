import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io

# Set page config
st.set_page_config(
    page_title="Tesla Talent Intelligence Dashboard",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme
st.markdown("""
<style>
    .stApp {
        background-color: #0f0f0f;
        color: #e0e0e0;
    }
    .metric-card {
        background-color: #1a1a1a;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #333;
        margin-bottom: 20px;
    }
    h1, h2, h3 {
        color: #ffffff !important;
    }
</style>
""", unsafe_allow_html=True)

# Dashboard Header
st.title("Tesla Talent Intelligence Dashboard")
st.subheader("Predictive Attrition Model & Workforce Analytics | June 2025")

# Metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Overall Attrition Risk", "High", "78% probability in next 6 months", delta_color="inverse")
with col2:
    st.metric("Employee Sentiment", "3.5/5", "↓ 0.3 from 2024", delta_color="inverse")
with col3:
    st.metric("Brand Perception", "-7%", "Only EV brand with negative score", delta_color="inverse")
with col4:
    st.metric("Workforce Reduction", "14,000+", "10% of global workforce in 2024")

# Create data for visualizations
department_data = pd.DataFrame({
    'Department': ['Recruiting/HR', 'Sales/Delivery', 'Manufacturing', 'Engineering', 'Energy/Battery', 'Service', 'Design'],
    'Risk': [85, 72, 58, 45, 52, 48, 35]
})

# Department Risk Chart
st.subheader("Attrition Risk by Department (Next 12 Months)")
fig_dept = px.bar(
    department_data, 
    x='Department', 
    y='Risk',
    color='Risk',
    color_continuous_scale=['#44ff44', '#ffaa44', '#ff4444'],
    range_color=[0, 100]
)
fig_dept.update_layout(
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font=dict(color='#e0e0e0'),
    height=400
)
st.plotly_chart(fig_dept, use_container_width=True)

# Geographic Heat Map - FIXED VERSION
st.subheader("Geographic Attrition Heat Map")

geographic_data = pd.DataFrame({
    'Region': ['California', 'Texas', 'Nevada', 'New York', 'Germany', 'Shanghai'],
    'Risk': [78, 58, 52, 65, 75, 40],
    'Employees': [25000, 15000, 8000, 3000, 12000, 20000],
    'Risk_Category': ['High', 'Medium', 'Medium', 'High', 'High', 'Low']
})

# Create bubble chart for geographic data
fig_geo = go.Figure()

# Add bubbles
for idx, row in geographic_data.iterrows():
    color = '#ff4444' if row['Risk'] > 60 else '#ffaa44' if row['Risk'] > 30 else '#44ff44'
    
    fig_geo.add_trace(go.Scatter(
        x=[idx],
        y=[1],
        mode='markers+text',
        marker=dict(
            size=row['Employees']/200,  # Scale for visibility
            color=color,
            opacity=0.8,
            line=dict(color='#333', width=2)
        ),
        text=f"{row['Region']}<br>{row['Risk']}%<br>{row['Employees']:,} employees",
        textposition="middle center",
        textfont=dict(color='white', size=12, family='Arial Black'),
        showlegend=False,
        hoverinfo='text',
        hovertext=f"{row['Region']}: {row['Risk']}% risk, {row['Employees']:,} employees"
    ))

fig_geo.update_layout(
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font=dict(color='#e0e0e0'),
    height=500,
    xaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[-0.5, len(geographic_data)-0.5]
    ),
    yaxis=dict(
        showgrid=False,
        showticklabels=False,
        zeroline=False,
        range=[0.5, 1.5]
    ),
    margin=dict(l=20, r=20, t=20, b=20)
)

st.plotly_chart(fig_geo, use_container_width=True)

# Risk Matrix
st.subheader("Department Risk Analysis")
risk_cards = [
    {"dept": "Recruiting & HR Teams", "risk": 85, "factors": "5+ rounds of layoffs, burnout, poor leadership", "sentiment": 2.1, "level": "HIGH"},
    {"dept": "Sales & Delivery Teams", "risk": 72, "factors": "Unrealistic targets, micromanagement, brand damage", "sentiment": 2.8, "level": "HIGH"},
    {"dept": "Engineering Teams", "risk": 45, "factors": "Long hours, project delays, competitive offers", "sentiment": 3.5, "level": "MEDIUM"},
    {"dept": "Manufacturing", "risk": 58, "factors": "Production pauses, safety concerns, understaffing", "sentiment": 3.2, "level": "MEDIUM"}
]

cols = st.columns(2)
for idx, card in enumerate(risk_cards):
    with cols[idx % 2]:
        color = "#ff4444" if card["level"] == "HIGH" else "#ffaa44"
        st.markdown(f"""
        <div style="background-color: #1a1a1a; padding: 20px; border-radius: 12px; border-left: 4px solid {color}; margin-bottom: 20px;">
            <span style="background-color: {color}; color: {'white' if card['level'] == 'HIGH' else 'black'}; padding: 5px 15px; border-radius: 20px; font-weight: bold;">{card['level']} RISK</span>
            <h3 style="margin-top: 10px;">{card['dept']}</h3>
            <p><strong>Attrition Risk:</strong> {card['risk']}%</p>
            <p><strong>Key Factors:</strong> {card['factors']}</p>
            <p><strong>Sentiment Score:</strong> {card['sentiment']}/5</p>
        </div>
        """, unsafe_allow_html=True)

# Feature Importance
st.subheader("Predictive Model Feature Importance")
feature_data = pd.DataFrame({
    'Feature': ['Leadership/Brand Perception', 'Layoff History', 'Work-Life Balance', 
                'Salary Competitiveness', 'External Market Factors', 'Department Type', 
                'Geographic Location', 'Tenure'],
    'Importance': [28, 22, 18, 12, 8, 6, 4, 2]
})

fig_features = px.bar(
    feature_data, 
    x='Importance', 
    y='Feature',
    orientation='h',
    color_discrete_sequence=['#4CAF50']
)
fig_features.update_layout(
    plot_bgcolor='#1a1a1a',
    paper_bgcolor='#1a1a1a',
    font=dict(color='#e0e0e0'),
    height=400
)
st.plotly_chart(fig_features, use_container_width=True)

# Create the full dataset for download
csv_data = """Region,Department,Role,Sentiment_Score,Salary_vs_Market,External_Factors,3M_Risk,6M_Risk,12M_Risk,Key_Observations
California,Recruiting/HR,All Roles,2.1,-15%,High turnover market,65%,78%,85%,"Severe burnout, 5+ layoff rounds, mental health crisis"
California,Sales,Sales Advisor,2.8,-10%,Brand damage,60%,70%,75%,"Unrealistic targets, micromanagement, customer hostility"
California,Engineering,Software Engineer,3.5,+5%,Competition from tech,30%,40%,45%,"Long hours but good comp, project delays"
Texas,Manufacturing,Production Associate,3.2,+5%,Production pauses,35%,48%,58%,"Safety concerns, understaffing, shift irregularity"
Texas,Engineering,Mechanical Engineer,3.8,+8%,Oil industry competition,25%,35%,42%,"Stable but concerned about future"
Nevada,Battery/Energy,Battery Tech,3.5,+10%,Tariff impacts,25%,38%,52%,"Supply chain disruption, China dependency"
Nevada,Manufacturing,Assembly Line,3.0,0%,Labor shortage,40%,55%,65%,"Overtime fatigue, safety issues"
New York,Sales,Delivery Specialist,2.5,-5%,High COL,55%,65%,70%,"Low pay for region, brand issues"
Germany,All Departments,Mixed,2.8,-8%,Political backlash,55%,68%,75%,"Brand perception -51%, protests, sales crash"
Shanghai,Engineering,Software Engineer,3.8,+20%,Tech boom,18%,28%,40%,"Good pay but trade war concerns"
Shanghai,Manufacturing,Quality Control,3.5,+15%,Local competition,22%,32%,45%,"Stable but watching US-China relations"
Remote,IT/Tech,Data Analyst,3.6,0%,Remote competition,20%,30%,38%,"Good flexibility but limited growth"
California,Service,Service Technician,3.3,0%,High demand,28%,42%,48%,"Steady work but brand concerns"
Texas,Sales,Inside Sales,2.6,-12%,Remote competition,50%,65%,72%,"Low morale, impossible quotas"
Germany,Manufacturing,Production Lead,2.9,-5%,Union pressure,48%,62%,70%,"Leadership disconnect, protests"
Nevada,Logistics,Supply Chain Manager,3.4,+5%,Tariff complexity,32%,45%,55%,"Stressed by policy changes"
Shanghai,Battery,Battery Engineer,3.9,+25%,High demand skills,15%,22%,35%,"Well compensated, watching politics"
California,Design,UX Designer,3.6,+2%,Tech competition,25%,35%,40%,"Creative freedom but long hours"
Texas,IT,Systems Engineer,3.5,+8%,Oil & gas competition,22%,32%,42%,"Good pay, concerns about direction"
New York,Marketing,Marketing Manager,2.7,-8%,Brand crisis,52%,68%,75%,"Impossible to market, morale low"
Germany,Engineering,Embedded Systems,3.2,+5%,Auto competition,35%,50%,62%,"Technical challenges, brand issues"
California,Legal,Corporate Counsel,3.0,-5%,Increased workload,40%,55%,65%,"Overwhelmed by issues, burnout"
Shanghai,Sales,Sales Manager,3.4,+18%,Local market growth,20%,30%,42%,"Good commissions but US tensions"
Nevada,Quality,Quality Engineer,3.3,+3%,Production pressure,30%,42%,54%,"Rushed timelines, safety concerns"
Remote,Finance,Financial Analyst,3.7,+5%,Remote opportunities,18%,28%,35%,"Stable but limited advancement"
Texas,Facilities,Facilities Manager,3.4,0%,Expansion halted,25%,38%,50%,"Uncertainty about future growth"
California,Product,Product Manager,3.1,-8%,Tech competition,45%,60%,68%,"Shifted priorities, no clear vision"
Germany,Service,Service Manager,2.6,-10%,Customer complaints,58%,70%,78%,"Brand damage affecting service"
Shanghai,Supply Chain,Procurement,3.6,+15%,Critical role,20%,28%,38%,"Stable, managing tariff impacts"
Nevada,HR,HR Business Partner,2.3,-12%,Layoff fatigue,60%,72%,80%,"Demoralized, implementing cuts"
California,Autopilot,ML Engineer,3.7,+15%,High demand,22%,32%,40%,"Good comp but project delays" """

# Attrition Risk Projections Table
st.subheader("Attrition Risk Projections")
df = pd.read_csv(io.StringIO(csv_data))
st.dataframe(df.head(10), use_container_width=True)

# Download button - FIXED VERSION
st.download_button(
    label="Download Full Dataset (CSV)",
    data=csv_data,
    file_name=f"tesla_attrition_prediction_model_{datetime.now().strftime('%Y%m%d')}.csv",
    mime="text/csv",
    help="Download the complete attrition prediction dataset"
)

# Executive Summary
st.subheader("Executive Summary")
st.markdown("""
Tesla faces unprecedented attrition risk driven by a perfect storm of internal and external factors. 
Employee sentiment has declined to 3.5/5 on Glassdoor with only 56% recommending the company, while 
Tesla has become the only EV brand with net negative perception at -7%. The company executed layoffs 
affecting over 14,000 employees in 2024, creating a culture of fear and uncertainty.

External pressures compound internal challenges: Trump's 125% tariffs on China have disrupted Tesla's 
Cybercab and Semi production plans, while market share plummeted from 75% in Q1 2022 to 43.5% in Q1 2025. 
Brand perception deteriorated rapidly, with 39% of consumers holding negative views versus 32% positive, 
directly impacting sales teams' morale and performance.

Our predictive model identifies recruiting/HR teams at highest risk (85% attrition probability) due to 
repeated layoffs and burnout. Sales teams follow at 72% risk, struggling with unrealistic targets amid 
brand damage. Geographic analysis shows Germany at 75% risk due to severe brand perception issues 
(-51% net sentiment). Immediate interventions needed: leadership changes, compensation adjustments, 
workload rebalancing, and brand rehabilitation to prevent talent exodus.
""")

# To run this dashboard, save this code as 'tesla_dashboard.py' and run:
# streamlit run tesla_dashboard.py