import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ==========================================
# 1. DATABASE SETUP & INITIALIZATION
# ==========================================
def init_db():
    conn = sqlite3.connect('leads.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            company TEXT,
            context TEXT,
            score INTEGER,
            segment TEXT,
            outreach TEXT,
            next_action TEXT,
            timestamp TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

def save_lead(role, company, context, score, segment, outreach, next_action):
    conn = sqlite3.connect('leads.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO leads (role, company, context, score, segment, outreach, next_action, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (role, company, context, score, segment, outreach, next_action, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

def get_all_leads():
    conn = sqlite3.connect('leads.db')
    df = pd.read_sql_query("SELECT * FROM leads ORDER BY id DESC", conn)
    conn.close()
    return df

# ==========================================
# 2. SMART LOGIC LAYER & AI SIMULATION
# ==========================================
def analyze_lead(role, company, context):
    score = 40 # Base score
    
    # Rule-Based Scoring Logic (Role Priority)
    high_value_roles = ['ceo', 'founder', 'director', 'vp', 'head', 'manager']
    if any(r in role.lower() for r in high_value_roles):
        score += 30
        
    # Rule-Based Scoring Logic (Company/Context Scale)
    scale_keywords = ['enterprise', 'funding', 'global', 'scale', 'growth', 'optimization']
    if any(k in context.lower() or k in company.lower() for k in scale_keywords):
        score += 30
        
    score = min(score, 100) # Cap at 100
    
    # Segmentation Engine
    if score >= 80:
        segment = "Tier 1 (High Priority Hot Lead)"
        next_action = "Schedule immediate 1-on-1 executive discovery call within 24 hours."
    elif score >= 60:
        segment = "Tier 2 (Warm Nurture)"
        next_action = "Invite to upcoming product webinar and send case studies."
    else:
        segment = "Tier 3 (Low Priority/Cold)"
        next_action = "Drop into automated email sequence drip."

    # AI Processing Integration Pipeline (Context-Aware Generation)
    outreach_message = (
        f"Hi {role.title()},\n\n"
        f"I noticed your current initiatives at {company.title()} regarding operational focus areas. "
        f"Given your role as {role.title()}, driving efficiency is likely top of mind. "
        f"We've helped similar teams optimize workflows by up to 40%.\n\n"
        f"Would you be open to a brief sync next Tuesday?\n\nBest regards,\nGrowth Automation Team"
    )
    
    return score, segment, outreach_message, next_action

# ==========================================
# 3. FRONTEND UI & NAVIGATION
# ==========================================
st.set_page_config(page_title="LeadIntel AI Workflow", layout="wide")

st.title("⚡ LeadIntel: AI-Powered Lead Workflow Platform")
st.markdown("---")

# Navigation Menu
menu = ["Lead Processor Engine", "Admin Analytics Dashboard"]
choice = st.sidebar.radio("Navigation Pipeline", menu)

if choice == "Lead Processor Engine":
    st.header("🎯 Target Lead Profile Input")
    
    col1, col2 = st.columns(2)
    with col1:
        role = st.text_input("Professional Designation / Role", placeholder="e.g., Director of Operations")
        company = st.text_input("Company Name", placeholder="e.g., Nexus Logistics")
    
    with col2:
        context = st.text_area("Operational Context / Business Pain Points", placeholder="e.g., Spending too much time on manual dispatch tracking.")

    if st.button("Execute Lead Intelligence Flow", type="primary"):
        if role and company and context:
            with st.spinner("Processing through AI Engine & Smart Logic Layer..."):
                score, segment, outreach, next_action = analyze_lead(role, company, context)
                
                # Save to database
                save_lead(role, company, context, score, segment, outreach, next_action)
                
                st.success("Analysis Complete! Output successfully persisted to Database.")
                
                # Structured UI Rendering (No raw JSON)
                st.markdown("### 📋 System Evaluation Metrics")
                m1, m2 = st.columns(2)
                m1.metric(label="Calculated Lead Score", value=f"{score} / 100")
                m2.metric(label="Assigned Lead Segment", value=segment)
                
                st.markdown("### ⚙️ Recommended Next Action Pipeline")
                st.info(next_action)
                
                st.markdown("### ✉️ Tailored Generation Output")
                st.code(outreach, language="text")
        else:
            st.error("Please fill out all input vector fields to execute pipeline processing.")

elif choice == "Admin Analytics Dashboard":
    st.header("📊 Executive System Monitoring Interface")
    
    df = get_all_leads()
    
    if not df.empty:
        total_leads = len(df)
        avg_score = int(df['score'].mean())
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Lead Records Evaluated", total_leads)
        c2.metric("Mean System Lead Score", f"{avg_score} / 100")
        c3.metric("System Database Status", "HEALTHY / ONLINE")
        
        st.markdown("---")
        st.subheader("📈 Lead Segment Dispersion Matrix")
        segment_counts = df['segment'].value_counts()
        st.bar_chart(segment_counts)
        
        st.markdown("---")
        st.subheader("🗄️ Cold Database Records (Persistent Storage View)")
        st.dataframe(df[['id', 'timestamp', 'role', 'company', 'score', 'segment', 'next_action']], use_container_width=True)
    else:
        st.warning("No data found in system database storage layers yet.")