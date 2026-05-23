import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from src.predictor import CareerPredictor

# ==============================================================================
# 1. PAGE ENGINE & CORE CONFIG
# ==============================================================================
st.set_page_config(
    page_title="Career Intelligence System",
    page_icon="⚡",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# Initialize Backend Logic
@st.cache_resource
def load_predictor():
    return CareerPredictor()

predictor = load_predictor()

# ==============================================================================
# 2. ULTRA-PREMIUM HUD INJECTION (Fixed for Perfect Label Visibility)
# ==============================================================================
st.html("""
    <style>
        @import url('https://googleapis.com');
        
        /* Smooth Fluid Canvas */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
            font-family: 'Plus Jakarta Sans', sans-serif !important;
            background: linear-gradient(180deg, #F8FAFC 0%, #F1F5F9 100%) !important;
        }
        
        [data-testid="stHeader"] {
            background: rgba(248, 250, 252, 0.4) !important;
            backdrop-filter: blur(20px);
        }

        /* Glassmorphism Floating Deck Cards */
        .premium-card {
            background: rgba(255, 255, 255, 0.85) !important;
            backdrop-filter: blur(16px);
            border: 1px solid rgba(226, 232, 240, 0.8) !important;
            border-radius: 24px !important;
            padding: 28px !important;
            box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.02), 0 12px 30px -4px rgba(15, 23, 42, 0.03) !important;
            margin-bottom: 24px !important;
            transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1) !important;
        }
        
        .premium-card:hover {
            transform: translateY(-6px) !important;
            background: #FFFFFF !important;
            box-shadow: 0 30px 40px -10px rgba(15, 23, 42, 0.06), 0 10px 20px -5px rgba(15, 23, 42, 0.02) !important;
            border-color: #CBD5E1 !important;
        }

        /* Modern Dashboard Micro-Typography Labels */
        .section-tag {
            color: #475569 !important;
            font-size: 12px !important;
            font-weight: 800 !important;
            letter-spacing: 0.12em !important;
            text-transform: uppercase !important;
            margin-bottom: 20px !important;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        /* FIX: FORCE ALL STREAMLIT INPUT LABELS TO BE ULTRA-VISIBLE BLACK */
        label[data-testid="stWidgetLabel"],
        label[data-testid="stWidgetLabel"] p,
        div[data-testid="stWidgetLabel"] label,
        .stSlider label,
        .stSelectbox label {
            color: #0F172A !important;
            font-size: 13.5px !important;
            font-weight: 700 !important;
            opacity: 1 !important;
            visibility: visible !important;
            margin-bottom: 8px !important;
            display: inline-block !important;
        }
        
        /* Modern Inputs Style */
        .stTextInput input, .stNumberInput input, .stSelectbox div[data-baseweb="select"], .stTextArea textarea {
            border-radius: 14px !important;
            border: 1px solid #CBD5E1 !important;
            background-color: #FFFFFF !important;
            color: #0F172A !important;
            padding: 12px 16px !important;
            font-size: 14px !important;
            transition: all 0.2s ease;
        }
        
        .stTextInput input:focus, .stNumberInput input:focus {
            border-color: #4F46E5 !important;
            box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.12) !important;
        }
        
        /* Glowing Gradient Execution Button */
        div[data-testid="stButton"] button {
            background: linear-gradient(135deg, #4F46E5 0%, #2563EB 100%) !important;
            color: white !important;
            border: none !important;
            padding: 16px 28px !important;
            border-radius: 14px !important;
            font-weight: 700 !important;
            font-size: 15px !important;
            width: 100% !important;
            letter-spacing: -0.2px !important;
            box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25) !important;
            transition: all 0.3s ease;
        }
        div[data-testid="stButton"] button:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(79, 70, 229, 0.4) !important;
        }
    </style>
""")

# ==============================================================================
# 3. GLOWING GLASS HEADER COMPONENT
# ==============================================================================
st.markdown("""
    <div style="background: linear-gradient(135deg, #0A0F1D 0%, #1E1B4B 100%); padding: 44px 48px; border-radius: 28px; color: white; margin-bottom: 36px; box-shadow: 0 25px 30px -10px rgba(10, 15, 29, 0.15); border: 1px solid rgba(255,255,255,0.04);">
        <div>
            <span style="background: linear-gradient(90deg, #6366F1, #3B82F6); color: white; padding: 5px 14px; border-radius: 50px; font-size: 11px; font-weight: 800; letter-spacing: 1px; text-transform: uppercase; box-shadow: 0 4px 10px rgba(99, 102, 241, 0.2);">
                PORTFOLIO PROJECT
            </span>
            <h1 style="margin: 14px 0 6px 0; font-size: 38px; font-weight: 800; letter-spacing: -1.2px; color: white;">
                Career Intelligence System
            </h1>
            <p style="margin: 0; opacity: 0.75; font-size: 16px; font-weight: 400; color: #E2E8F0;">
                Algorithmic execution matrix providing objective talent diagnostics and pricing forecast benchmarks.
            </p>
        </div>
    </div>
""", unsafe_allow_html=True)
# ==============================================================================
# 4. SPLIT CONTROL GRID ASSEMBLY
# ==============================================================================
layout_left, layout_right = st.columns([1, 2.3], gap="large")

# ─── LEFT SIDE: CONTROL DECK OPERATOR PANEL ───
with layout_left:
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-tag"> PROFILE CONTROL DECK</div>', unsafe_allow_html=True)
    
    role = st.text_input("Target/Current Designation", "Data Analyst")
    skills = st.text_area("Acquired Skills", placeholder="e.g., Testing, Developer, Javascript")
    
    ctrl_col1, ctrl_col2 = st.columns(2)
    with ctrl_col1:
        experience = st.number_input("Experience (Years)", 0, 40, 2)
        ai_score = st.slider("Internal AI Score", 0, 100, 75)
    with ctrl_col2:
        projects = st.number_input("Production Projects", 0, 50, 1)
        education = st.selectbox("Education Stratum", ["Bachelor", "Master", "PhD", "Diploma", "Other"])
        
    current_salary = st.number_input("Current Salary (₹)", min_value=100000, step=50000, value=300000)
    
    st.markdown('<div style="margin-top: 25px;"></div>', unsafe_allow_html=True)
    run_analysis = st.button("⚡ Run Predictive Core Analysis")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── RIGHT SIDE: DYNAMIC HIGH-END ANALYSIS HUBS ───
with layout_right:
    if run_analysis:
        if not skills.strip():
            st.error("Operation halted. Please populate your skill parameters on the left hub.")
        else:
            # Execute Predictive Engine Pipeline
            result = predictor.predict(
                skills, experience, projects, ai_score, education, current_salary, role
            )
            
            # ─── ROW 1: PRESTIGE SCORE CARDS ───
            st.markdown('<div class="section-tag"> STAGE 1: CLASSIFIER DIAGNOSTICS</div>', unsafe_allow_html=True)
            col1, col2 = st.columns(2, gap="medium")
            
            with col1:
                hiring_status = result["Hire Decision"]
                badge_color = "#10B981" if hiring_status.lower() == "hire" else "#EF4444"
                bg_badge = "rgba(16, 185, 129, 0.12)" if hiring_status.lower() == "hire" else "rgba(239, 68, 68, 0.12)"
                
                st.markdown(f"""
                    <div class="premium-card" style="height: 190px; display: flex; flex-direction: column; justify-content: space-between;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <span style="color: #64748B; font-size: 11px; font-weight: 800; letter-spacing:0.5px;">HIRE CLASSIFIER TARGET</span>
                            <span style="background-color: {bg_badge}; color: {badge_color}; padding: 5px 12px; border-radius: 30px; font-size: 11px; font-weight: 700; text-transform:uppercase;">System Output</span>
                        </div>
                        <div style="margin-bottom: 5px;">
                            <h1 style="margin:0; font-size: 48px; font-weight: 800; color: #0F172A; letter-spacing:-1px;">{hiring_status}</h1>
                            <p style="margin:4px 0 0 0; color: #64748B; font-size: 13.5px;">Model Prediction</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
            with col2:
                confidence_val = float(result['Confidence (%)'])
                st.markdown(f"""
                    <div class="premium-card" style="height: 190px; display: flex; flex-direction: column; justify-content: space-between;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <span style="color: #64748B; font-size: 11px; font-weight: 800; letter-spacing:0.5px;">PROBABILITY ACCURACY</span>
                            <span style="background-color: rgba(59, 130, 246, 0.12); color: #2563EB; padding: 5px 12px; border-radius: 30px; font-size: 11px; font-weight: 700; text-transform:uppercase;">Confidence</span>
                        </div>
                        <div style="margin-bottom: 2px;">
                            <h3 style="margin:0; font-size: 36px; font-weight:800; color:#0F172A; letter-spacing:-0.8px;">{confidence_val}%</h3>
                        </div>
                """, unsafe_allow_html=True)
                
                fig_bar = go.Figure(go.Bar(
                    x=[confidence_val], y=[''], orientation='h',
                    marker=dict(color='#2563EB', line=dict(width=0)),
                    hovertemplate="%{x}%<extra></extra>"
                ))
                fig_bar.update_layout(
                    xaxis=dict(range=[0, 100], showgrid=False, visible=False),
                    yaxis=dict(showgrid=False, visible=False),
                    margin=dict(l=0, r=0, t=4, b=4), height=18,
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False})
                st.markdown("</div>", unsafe_allow_html=True)

            # ─── ROW 2: ALIGNMENT CARDS ───
            st.markdown('<div class="section-tag" style="margin-top: 18px;"> STAGE 2: STRATEGIC ALIGNMENT INSIGHTS</div>', unsafe_allow_html=True)
            rec_col1, rec_col2 = st.columns(2, gap="medium")
            
            with rec_col1:
                role_switch = "RE-ROUTE ADVOCATION" if result["Role Switch Recommended"] else "STABLE SECTOR ALIGNMENT"
                role_color = "#4F46E5" if result["Role Switch Recommended"] else "#64748B"
                st.markdown(f"""
                    <div class="premium-card" style="min-height: 230px; display: flex; flex-direction: column; justify-content: flex-start;">
                        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                            <div style="background-color: rgba(79, 70, 229, 0.08); color: #4F46E5; width: 38px; height: 38px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size:16px;">🔄</div>
                            <h3 style="margin:0; font-size: 16px; color: #0F172A; font-weight: 700;">Role Path Mapping</h3>
                        </div>
                        <span style="color: {role_color}; font-size: 12px; font-weight:800; letter-spacing:0.5px;">{role_switch}</span>
                        <p style="font-size: 14px; color: #475569; margin: 10px 0 0 0; line-height: 1.6; font-weight: 400;">{result["Role Switch Reason"]}</p>
                    </div>
                """, unsafe_allow_html=True)
                
            with rec_col2:
                comp_switch = "TRANSITION OPPORTUNITY" if result["Company Switch Recommended"] else "ORGANIZATIONAL RETENTION"
                comp_color = "#8B5CF6" if result["Company Switch Recommended"] else "#64748B"
                st.markdown(f"""
                    <div class="premium-card" style="min-height: 230px; display: flex; flex-direction: column; justify-content: flex-start;">
                        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
                            <div style="background-color: rgba(139, 92, 246, 0.08); color: #8B5CF6; width: 38px; height: 38px; border-radius: 12px; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size:16px;">🏢</div>
                            <h3 style="margin:0; font-size: 16px; color: #0F172A; font-weight: 700;">Company Placement Strategy</h3>
                        </div>
                        <span style="color: {comp_color}; font-size: 12px; font-weight:800; letter-spacing:0.5px;">{comp_switch}</span>
                        <p style="font-size: 14px; color: #475569; margin: 10px 0 0 0; line-height: 1.6; font-weight: 400;">{result["Company Switch Reason"]}</p>
                    </div>
                """, unsafe_allow_html=True)

            # ─── ROW 3: COMPENSATION VISUAL BLOCK ───
            st.markdown('<div class="section-tag" style="margin-top: 18px;"> STAGE 3: COMPENSATION ANCHOR SYSTEM</div>', unsafe_allow_html=True)
            
            st.markdown(f"""
                <div class="premium-card">
                    <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; margin-bottom:24px;">
                        <div>
                            <span style="color: #64748B; font-size: 11px; font-weight: 800; letter-spacing:0.5px;">PREDICTED ANCHOR CEILING BASE</span>
                            <h2 style="margin:4px 0 0 0; font-size:32px; font-weight:800; color:#10B981; letter-spacing:-0.5px;">₹{result['Predicted Salary']:,}</h2>
                        </div>
                        <div style="background-color:rgba(16, 185, 129, 0.06); border: 1px solid rgba(16, 185, 129, 0.15); padding: 12px 18px; border-radius:14px; max-width:320px;">
                            <p style="margin:0; font-size:12.5px; color:#15803D; font-weight:500; line-height:1.5;">
                                💡 Expected compensation scale ceiling tracking optimization models.
                            </p>
                        </div>
                    </div>
            """, unsafe_allow_html=True)
            
            # Dynamic Market Benchmark Configuration
            market_avg_estimate = current_salary * 1.25 if current_salary < result['Predicted Salary'] else current_salary * 0.9
            
                        # --- Dynamic Market Benchmark Data ---
            salary_chart_data = pd.DataFrame({
                'Metric Tier': ['Current Base Pay', 'Market Average Base', 'Predicted Scale Cap'], 
                'Compensation (₹)': [current_salary, market_avg_estimate, result['Predicted Salary']] 
            }) 

            # --- Plotly Bar Graph Logic ---
            fig_salary = px.bar( 
                salary_chart_data, 
                x='Metric Tier', 
                y='Compensation (₹)', 
                color='Metric Tier', 
                color_discrete_map={ 
                    'Current Base Pay': '#94A3B8', 
                    'Market Average Base': '#6366F1', 
                    'Predicted Scale Cap': '#10B981' 
                }, 
                text_auto=',.0f' 
            ) 

            fig_salary.update_layout( 
                showlegend=False, 
                xaxis_title=None, 
                yaxis_title=None, 
                margin=dict(l=20, r=20, t=30, b=10), 
                height=260, 
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                bargap=0.45, 
                xaxis=dict( 
                    tickfont=dict(size=12, color='#0F172A', family='Plus Jakarta Sans', weight='bold'), 
                    showline=True, 
                    linecolor='#E2E8F0' 
                ), 
                yaxis=dict( 
                    showgrid=True, 
                    gridcolor='#E2E8F0', 
                    tickfont=dict(size=11, color='#64748B', family='Plus Jakarta Sans'), 
                    tickformat=',.0f' 
                ) 
            ) 

            fig_salary.update_traces( 
                textfont=dict(size=12, color='#0F172A', family='Plus Jakarta Sans', weight='bold'), 
                textposition='outside', 
                cliponaxis=False 
            ) 

            st.plotly_chart(fig_salary, use_container_width=True, config={'displayModeBar': False}) 
            st.markdown('</div>', unsafe_allow_html=True) 

    else: 
        # Initial Welcome Placeholder View State
        st.markdown(""" 
            <div style="border: 2px dashed #CBD5E1; border-radius: 24px; padding: 90px 40px; text-align: center; color: #94A3B8; margin-top:32px; background: rgba(255,255,255,0.6); backdrop-filter: blur(10px);">
                <div style="font-size: 52px; margin-bottom: 20px;">⚡</div>
                <h3 style="margin:0 0 6px 0; color: #334155; font-size: 19px; font-weight:700; letter-spacing:-0.3px;">Diagnostic Engine Pipeline Standby</h3>
                <p style="margin:0; font-size: 14.5px; color: #64748B; line-height:1.5;">Configure your talent vector matrices on the left control hub and execute the analysis trigger to compile your prediction models.</p>
            </div>
        """, unsafe_allow_html=True) 

# ============================================================================== 
# 5. CONSOLIDATED BRANDED FOOTER 
# ============================================================================== 
st.markdown(""" 
    <div style="margin-top: 70px; border-top: 1px solid #E2E8F0; padding-top: 24px; text-align: center; padding-bottom: 24px;">
        <p style="margin:0; font-size: 11.5px; color: #94A3B8; font-weight: 600; letter-spacing: 0.08em;">
            POWERED BY ENGINE PIPELINES • EXPLAINABLE MACHINE LEARNING OPERATIONS
        </p>
    </div>
""", unsafe_allow_html=True)

