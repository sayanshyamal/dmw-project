"""
MediCharge Analytics — Insurance Cost Predictor & Analyzer
Main Streamlit application with 5 pages.
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

from styles import get_custom_css
import charts
import streamlit.components.v1 as components

# ===================================================================
# PAGE CONFIG (must be first Streamlit command)
# ===================================================================
st.set_page_config(
    page_title="MediCharge Analytics",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ===================================================================
# HAMBURGER MENU TOGGLE & SIDEBAR CONTROL
# ===================================================================
st.markdown(
    """
    <style>
    /* Hide Streamlit's default collapse arrow button */
    [data-testid="collapsedControl"] {
        display: none !important;
    }

    /* Smooth transition on sidebar */
    [data-testid="stSidebar"] {
        transition: margin-left 0.3s ease-in-out,
                    min-width 0.3s ease-in-out,
                    max-width 0.3s ease-in-out,
                    transform 0.3s ease-in-out !important;
    }

    /* Prevent content flash inside sidebar during transition */
    [data-testid="stSidebar"] > div:first-child {
        transition: opacity 0.2s ease-in-out !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Inject JavaScript toggle system via components.html ---
components.html(
    """
    <script>
    (function() {
        const doc = window.parent.document;
        const sidebar = doc.querySelector('[data-testid="stSidebar"]');
        if (!sidebar) return;

        // ── Persistent state on the parent window ──
        if (typeof window.parent._sidebarOpen === 'undefined') {
            window.parent._sidebarOpen = window.parent.innerWidth >= 768;
        }

        // ── Create hamburger button (once) ──
        let btn = doc.getElementById('hamburger-toggle-btn');
        if (!btn) {
            btn = doc.createElement('button');
            btn.id = 'hamburger-toggle-btn';
            btn.innerHTML = '&#9776; Menu';
            btn.style.cssText = `
                position: fixed;
                top: 14px;
                left: 290px;
                z-index: 1000000;
                background: #2E7D5E;
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 8px 14px;
                font-size: 18px;
                font-family: 'Segoe UI', sans-serif;
                font-weight: 600;
                cursor: pointer;
                box-shadow: 0 2px 10px rgba(0,0,0,0.25);
                transition: background 0.2s ease, transform 0.15s ease, left 0.3s ease-in-out;
                display: flex;
                align-items: center;
                gap: 6px;
                user-select: none;
            `;
            btn.addEventListener('mouseenter', function() {
                this.style.background = '#245f49';
                this.style.transform = 'scale(1.05)';
            });
            btn.addEventListener('mouseleave', function() {
                this.style.background = '#2E7D5E';
                this.style.transform = 'scale(1)';
            });
            doc.body.appendChild(btn);
        }

        // ── Create mobile overlay (once) ──
        let overlay = doc.getElementById('sidebar-overlay');
        if (!overlay) {
            overlay = doc.createElement('div');
            overlay.id = 'sidebar-overlay';
            overlay.style.cssText = `
                display: none;
                position: fixed;
                top: 0; left: 0;
                width: 100vw; height: 100vh;
                background: rgba(0, 0, 0, 0.5);
                z-index: 998;
                transition: opacity 0.3s ease-in-out;
            `;
            doc.body.appendChild(overlay);
        }

        // ── Apply sidebar state ──
        function updateSidebar() {
            const isMobile = window.parent.innerWidth < 768;
            const isOpen   = window.parent._sidebarOpen;

            if (isOpen) {
                sidebar.style.minWidth   = '280px';
                sidebar.style.maxWidth   = '280px';
                sidebar.style.transform  = 'translateX(0)';
                sidebar.style.visibility = 'visible';
                sidebar.style.overflow   = 'auto';
                if (sidebar.firstElementChild) {
                    sidebar.firstElementChild.style.opacity = '1';
                }
                // Position button just outside the sidebar
                btn.style.left = isMobile ? '10px' : '290px';
                if (isMobile) {
                    sidebar.style.position = 'fixed';
                    sidebar.style.top      = '0';
                    sidebar.style.left     = '0';
                    sidebar.style.height   = '100vh';
                    sidebar.style.zIndex   = '999999';
                    overlay.style.display  = 'block';
                    setTimeout(function(){ overlay.style.opacity = '1'; }, 10);
                } else {
                    overlay.style.display = 'none';
                }
            } else {
                sidebar.style.minWidth   = '0px';
                sidebar.style.maxWidth   = '0px';
                sidebar.style.transform  = 'translateX(-280px)';
                sidebar.style.overflow   = 'hidden';
                if (sidebar.firstElementChild) {
                    sidebar.firstElementChild.style.opacity = '0';
                }
                // Move button to the left edge when sidebar is hidden
                btn.style.left = '10px';
                overlay.style.opacity = '0';
                setTimeout(function(){ overlay.style.display = 'none'; }, 300);
            }
        }

        // ── Click handlers ──
        btn.onclick = function() {
            window.parent._sidebarOpen = !window.parent._sidebarOpen;
            updateSidebar();
        };

        overlay.onclick = function() {
            window.parent._sidebarOpen = false;
            updateSidebar();
        };

        // ── Handle window resize (auto-close on mobile, auto-open on desktop) ──
        window.parent.removeEventListener('resize', window.parent._sidebarResizeHandler);
        window.parent._sidebarResizeHandler = function() {
            const isMobile = window.parent.innerWidth < 768;
            if (isMobile && window.parent._sidebarOpen) {
                window.parent._sidebarOpen = false;
                updateSidebar();
            }
        };
        window.parent.addEventListener('resize', window.parent._sidebarResizeHandler);

        // ── Initial render ──
        updateSidebar();
    })();
    </script>
    """,
    height=0,
)

# ===================================================================
# INJECT CUSTOM CSS
# ===================================================================
st.markdown(get_custom_css(), unsafe_allow_html=True)

# ===================================================================
# DATA LOADING
# ===================================================================
DATA_DIR = os.path.dirname(os.path.abspath(__file__))

@st.cache_data
def load_data():
    raw_path = os.path.join(DATA_DIR, "hospital data.csv")
    clean_path = os.path.join(DATA_DIR, "cleaned_data.csv")
    if not os.path.exists(raw_path):
        return None, None
    raw = pd.read_csv(raw_path)
    clean = pd.read_csv(clean_path) if os.path.exists(clean_path) else None
    return raw, clean

raw_df, clean_df = load_data()

if raw_df is None:
    st.error("❌ **hospital data.csv** not found! Please place the dataset file in the same folder as app.py.")
    st.stop()

# ===================================================================
# ML MODEL
# ===================================================================
@st.cache_resource
def train_model(_clean_df):
    df = _clean_df.copy()
    # Ensure boolean columns are numeric
    for c in df.columns:
        if df[c].dtype == 'bool' or df[c].dtype == 'object':
            df[c] = df[c].astype(int)
    X = df.drop('charges', axis=1)
    y = df['charges']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    r2 = r2_score(y_test, model.predict(X_test))
    return model, list(X.columns), r2

model, feature_cols, r2_score_val = train_model(clean_df)

# ===================================================================
# HELPER: FORMAT CURRENCY
# ===================================================================
def fmt_inr(val):
    """Format a number as Indian Rupees with commas."""
    s = f"{val:,.2f}"
    return f"₹{s}"

def fmt_inr_int(val):
    return f"₹{val:,.0f}"

# ===================================================================
# SIDEBAR NAVIGATION
# ===================================================================
with st.sidebar:
    st.markdown("## 🏥 MediCharge Analytics")
    st.markdown("##### Insurance Cost Predictor & Analyzer")
    st.markdown("---")
    page = st.radio(
        "Navigate",
        [
            "🏠 Home / Overview",
            "📊 Exploratory Data Analysis",
            "🔍 Data Insights",
            "🤖 Charge Predictor",
            "📋 Dataset Viewer",
        ],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        "<small style='color:rgba(255,255,255,0.5)'>Built with Streamlit & Scikit-learn<br>© 2026 MediCharge Analytics</small>",
        unsafe_allow_html=True,
    )

# ===================================================================
# PAGE 1 — HOME / OVERVIEW
# ===================================================================
if page == "🏠 Home / Overview":
    # Hero banner
    st.markdown(
        """
        <div class="hero-banner">
            <h1>🏥 MediCharge Analytics</h1>
            <p>Analyze and predict medical insurance charges using real hospital data.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # KPI row
    total = len(raw_df)
    avg_charge = raw_df['charges'].mean()
    max_charge = raw_df['charges'].max()
    smoker_pct = (raw_df['smoker'].str.lower() == 'yes').mean() * 100

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Total Records</div><div class="kpi-value">{total:,}</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Average Charge</div><div class="kpi-value">{fmt_inr_int(avg_charge)}</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">Highest Charge</div><div class="kpi-value">{fmt_inr_int(max_charge)}</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="kpi-card"><div class="kpi-label">% Smokers</div><div class="kpi-value">{smoker_pct:.1f}%</div></div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # About section
    col_a, col_b = st.columns([3, 2])
    with col_a:
        st.markdown('<div class="section-header">📋 About the Project</div>', unsafe_allow_html=True)
        st.markdown(
            """
            This application provides a comprehensive analysis of medical insurance charges
            based on patient demographics and health indicators. Using a real-world hospital
            dataset, we explore how factors like **age**, **BMI**, **smoking status**, and
            **region** influence insurance costs. A trained **Linear Regression** model allows
            users to predict their own insurance charges interactively.
            """
        )

        st.markdown('<div class="section-header">📊 Dataset Columns</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <table class="styled-table">
            <thead><tr><th>Column</th><th>Type</th><th>Description</th></tr></thead>
            <tbody>
            <tr><td><b>age</b></td><td>Integer</td><td>Patient age (18–64)</td></tr>
            <tr><td><b>sex</b></td><td>String</td><td>Gender — male / female</td></tr>
            <tr><td><b>bmi</b></td><td>Float</td><td>Body Mass Index</td></tr>
            <tr><td><b>children</b></td><td>Integer</td><td>Number of dependent children</td></tr>
            <tr><td><b>smoker</b></td><td>String</td><td>Smoking status — yes / no</td></tr>
            <tr><td><b>region</b></td><td>String</td><td>Residential region in India</td></tr>
            <tr><td><b>charges</b></td><td>Float</td><td>Medical insurance charge (₹)</td></tr>
            </tbody></table>
            """,
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown('<div class="section-header">🔑 Key Findings</div>', unsafe_allow_html=True)
        st.markdown(
            """
            <div class="insight-card">
            <ul style="line-height:2.2; color:#374151; font-size:1.02rem;">
                <li>🚬 <b>Smokers pay ~3× more</b> in insurance charges than non-smokers</li>
                <li>📈 <b>Age positively correlates</b> with higher insurance costs</li>
                <li>⚖️ <b>BMI above 30</b> (Obese category) significantly increases charges</li>
                <li>🗺️ <b>Southeast region</b> shows the highest average charges</li>
                <li>👶 <b>Number of children</b> has minimal impact on overall charges</li>
            </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ===================================================================
# PAGE 2 — EXPLORATORY DATA ANALYSIS
# ===================================================================
elif page == "📊 Exploratory Data Analysis":
    st.markdown("# 📊 Exploratory Data Analysis")
    st.markdown("Interactive visualizations to explore distributions, relationships, and patterns in the insurance dataset.")

    # Section A — Distributions
    st.markdown('<div class="section-header">A — Distribution Analysis</div>', unsafe_allow_html=True)
    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.plotly_chart(charts.histogram(raw_df, 'age', 'Age Distribution'), use_container_width=True)
    with r1c2:
        st.plotly_chart(charts.histogram(raw_df, 'bmi', 'BMI Distribution'), use_container_width=True)
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.plotly_chart(charts.histogram(raw_df, 'children', 'Children Distribution'), use_container_width=True)
    with r2c2:
        st.plotly_chart(charts.histogram(raw_df, 'charges', 'Charges Distribution'), use_container_width=True)

    # Section B — Categorical
    st.markdown('<div class="section-header">B — Categorical Distribution</div>', unsafe_allow_html=True)
    b1, b2, b3 = st.columns(3)
    with b1:
        st.plotly_chart(charts.categorical_bar(raw_df, 'sex', 'Sex Distribution'), use_container_width=True)
    with b2:
        st.plotly_chart(charts.categorical_bar(raw_df, 'smoker', 'Smoker Distribution'), use_container_width=True)
    with b3:
        st.plotly_chart(charts.categorical_bar(raw_df, 'region', 'Region Distribution'), use_container_width=True)

    # Section C — Avg charges by category
    st.markdown('<div class="section-header">C — Average Charges by Category</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        st.plotly_chart(charts.avg_charge_bar(raw_df, 'sex', 'Avg Charge by Sex'), use_container_width=True)
    with c2:
        st.plotly_chart(charts.avg_charge_bar(raw_df, 'smoker', 'Avg Charge by Smoker'), use_container_width=True)
    with c3:
        st.plotly_chart(charts.avg_charge_bar(raw_df, 'region', 'Avg Charge by Region'), use_container_width=True)

    # Section D — Scatter plots
    st.markdown('<div class="section-header">D — Scatter Plots</div>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    with s1:
        st.plotly_chart(charts.scatter_smoker(raw_df, 'age', 'Age vs Charges'), use_container_width=True)
    with s2:
        st.plotly_chart(charts.scatter_smoker(raw_df, 'bmi', 'BMI vs Charges'), use_container_width=True)
    with s3:
        st.plotly_chart(charts.scatter_basic(raw_df, 'children', 'Children vs Charges'), use_container_width=True)

    # Section E — Box plot
    st.markdown('<div class="section-header">E — Box Plot Comparison</div>', unsafe_allow_html=True)
    st.plotly_chart(charts.box_smoker(raw_df), use_container_width=True)

# ===================================================================
# PAGE 3 — DATA INSIGHTS
# ===================================================================
elif page == "🔍 Data Insights":
    st.markdown("# 🔍 Data Insights")
    st.markdown("Deep-dive analytics with storytelling visualizations and key statistical insights.")

    # 1. Correlation Heatmap
    st.markdown('<div class="section-header">1 — Correlation Heatmap</div>', unsafe_allow_html=True)
    left, right = st.columns([3, 2])
    with left:
        st.plotly_chart(charts.correlation_heatmap(raw_df), use_container_width=True)
    with right:
        st.markdown('<div class="insight-card"><h4>🔗 Correlation Insights</h4>', unsafe_allow_html=True)
        corr = raw_df[['age', 'bmi', 'children', 'charges']].corr()
        st.markdown(f"""
        - **Age ↔ Charges**: r = {corr.loc['age','charges']:.3f} — moderate positive correlation
        - **BMI ↔ Charges**: r = {corr.loc['bmi','charges']:.3f} — weak positive correlation
        - **Children ↔ Charges**: r = {corr.loc['children','charges']:.3f} — very weak correlation
        - Age and BMI are nearly independent of each other
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    st.info("💡 Smoking status (categorical) has the strongest effect on charges but doesn't appear in the numeric correlation matrix.")

    # 2. Region × Smoker
    st.markdown('<div class="section-header">2 — Charge Distribution by Region & Smoker Status</div>', unsafe_allow_html=True)
    st.plotly_chart(charts.region_smoker_bar(raw_df), use_container_width=True)
    st.info("💡 Smokers consistently pay 3–4× more across all regions. The Southeast region has the highest smoker charges.")

    # 3. BMI category
    st.markdown('<div class="section-header">3 — BMI Category Analysis</div>', unsafe_allow_html=True)
    l3, r3 = st.columns([3, 2])
    with l3:
        st.plotly_chart(charts.bmi_category_bar(raw_df), use_container_width=True)
    with r3:
        st.markdown('<div class="insight-card"><h4>⚖️ BMI Categories</h4>', unsafe_allow_html=True)
        st.markdown("""
        | Category | BMI Range |
        |---|---|
        | Underweight | < 18.5 |
        | Normal | 18.5 – 25 |
        | Overweight | 25 – 30 |
        | Obese | > 30 |
        """)
        st.markdown('</div>', unsafe_allow_html=True)
    st.info("💡 Obese patients (BMI > 30) have the highest average insurance charges, driven largely by the combined effect of obesity and smoking.")

    # 4. Age group
    st.markdown('<div class="section-header">4 — Age Group Analysis</div>', unsafe_allow_html=True)
    st.plotly_chart(charts.age_group_bar(raw_df), use_container_width=True)
    st.info("💡 Senior patients (51+) pay significantly more, reflecting increased health risks with age.")

    # 5. Top 10 highest-charge patients
    st.markdown('<div class="section-header">5 — Risk Score Summary: Top 10 Highest-Charge Patients</div>', unsafe_allow_html=True)
    top10 = raw_df.nlargest(10, 'charges')[['age', 'bmi', 'smoker', 'region', 'charges']].reset_index(drop=True)
    top10.index = top10.index + 1
    top10['charges'] = top10['charges'].apply(lambda v: fmt_inr(v))
    st.dataframe(top10, use_container_width=True)
    st.info("💡 All of the top 10 highest-charge patients are smokers, reinforcing that smoking is the single biggest cost driver.")

# ===================================================================
# PAGE 4 — CHARGE PREDICTOR
# ===================================================================
elif page == "🤖 Charge Predictor":
    st.markdown("# 🤖 Insurance Charge Predictor")
    st.markdown("Enter patient details to get an instant prediction of medical insurance charges using our trained Linear Regression model.")

    left_col, right_col = st.columns([2, 3])

    with left_col:
        st.markdown('<div class="form-card"><h3>🩺 Enter Patient Details</h3>', unsafe_allow_html=True)
        age = st.slider("Age", 18, 80, 30, key="pred_age")
        sex = st.radio("Sex", ["Male", "Female"], horizontal=True, key="pred_sex")
        bmi = st.slider("BMI", 10.0, 55.0, 25.0, step=0.1, key="pred_bmi")
        children = st.selectbox("Number of Children", [0, 1, 2, 3, 4, 5], key="pred_children")
        smoker = st.radio("Smoker", ["No", "Yes"], horizontal=True, key="pred_smoker")
        region = st.selectbox("Region", ["Northeast", "Northwest", "Southeast", "Southwest"], key="pred_region")
        predict_btn = st.button("🔮 Predict My Charge", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with right_col:
        if predict_btn:
            # Build input
            input_dict = {
                'age': age,
                'bmi': bmi,
                'children': float(children),
                'sex_male': 1 if sex == "Male" else 0,
                'smoker_yes': 1 if smoker == "Yes" else 0,
                'region_northwest': 1 if region == "Northwest" else 0,
                'region_southeast': 1 if region == "Southeast" else 0,
                'region_southwest': 1 if region == "Southwest" else 0,
            }
            input_df = pd.DataFrame([input_dict])
            # Ensure column order matches training
            for c in feature_cols:
                if c not in input_df.columns:
                    input_df[c] = 0
            input_df = input_df[feature_cols]

            prediction = max(model.predict(input_df)[0], 0)

            # Result card
            st.markdown(
                f"""
                <div class="prediction-card">
                    <h3>Predicted Insurance Charge</h3>
                    <div class="charge-value">{fmt_inr(prediction)}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Gauge
            st.plotly_chart(charts.gauge_chart(prediction), use_container_width=True)

            # Risk label
            if prediction < 10000:
                st.markdown('<div style="text-align:center"><span class="risk-low">🟢 Low Risk</span></div>', unsafe_allow_html=True)
            elif prediction < 25000:
                st.markdown('<div style="text-align:center"><span class="risk-medium">🟡 Medium Risk</span></div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align:center"><span class="risk-high">🔴 High Risk</span></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Comparison bar
            avg_c = raw_df['charges'].mean()
            max_c = raw_df['charges'].max()
            st.plotly_chart(charts.comparison_bar(prediction, avg_c, max_c), use_container_width=True)

            # Model accuracy
            st.markdown(
                f"""
                <div class="insight-card" style="text-align:center;">
                    <b>Model Accuracy (R² Score):</b>
                    <span style="font-size:1.4rem; color:#2E7D5E; font-weight:800; margin-left:0.5rem;">
                        {r2_score_val * 100:.1f}%
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            # Placeholder prompt
            st.markdown(
                """
                <div class="insight-card" style="text-align:center; padding:4rem 2rem;">
                    <h3 style="color:#6B7280 !important;">👈 Fill in the patient details and click <b>Predict</b></h3>
                    <p style="color:#9CA3AF;">Your predicted insurance charge and risk analysis will appear here.</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Feature importance (always visible below)
    st.markdown('<div class="section-header">📊 Key Factors Affecting Your Charge</div>', unsafe_allow_html=True)
    st.plotly_chart(charts.feature_importance_bar(model, feature_cols), use_container_width=True)

# ===================================================================
# PAGE 5 — DATASET VIEWER
# ===================================================================
elif page == "📋 Dataset Viewer":
    st.markdown("# 📋 Dataset Viewer")
    st.markdown("Browse, filter, and download the raw hospital insurance dataset.")

    # Sidebar filters
    with st.sidebar:
        st.markdown("### 🔎 Filters")
        f_region = st.multiselect("Region", raw_df['region'].unique().tolist(), default=raw_df['region'].unique().tolist())
        f_smoker = st.radio("Smoker Status", ["Both", "Yes", "No"], key="filt_smoker")
        f_sex = st.radio("Sex", ["Both", "Male", "Female"], key="filt_sex")
        f_age = st.slider("Age Range", int(raw_df['age'].min()), int(raw_df['age'].max()),
                          (int(raw_df['age'].min()), int(raw_df['age'].max())), key="filt_age")
        f_bmi = st.slider("BMI Range", float(raw_df['bmi'].min()), float(raw_df['bmi'].max()),
                          (float(raw_df['bmi'].min()), float(raw_df['bmi'].max())), step=0.1, key="filt_bmi")
        f_charge = st.slider("Charge Range (₹)", float(raw_df['charges'].min()), float(raw_df['charges'].max()),
                             (float(raw_df['charges'].min()), float(raw_df['charges'].max())), step=100.0, key="filt_charge")

    # Apply filters
    filtered = raw_df.copy()
    filtered = filtered[filtered['region'].isin(f_region)]
    if f_smoker != "Both":
        filtered = filtered[filtered['smoker'].str.lower() == f_smoker.lower()]
    if f_sex != "Both":
        filtered = filtered[filtered['sex'].str.lower() == f_sex.lower()]
    filtered = filtered[(filtered['age'] >= f_age[0]) & (filtered['age'] <= f_age[1])]
    filtered = filtered[(filtered['bmi'] >= f_bmi[0]) & (filtered['bmi'] <= f_bmi[1])]
    filtered = filtered[(filtered['charges'] >= f_charge[0]) & (filtered['charges'] <= f_charge[1])]

    # Display
    st.dataframe(filtered, use_container_width=True, height=480)

    # Summary stats
    st.markdown('<div class="section-header">📈 Filtered Dataset Summary</div>', unsafe_allow_html=True)
    s1, s2, s3 = st.columns(3)
    with s1:
        st.metric("Filtered Records", f"{len(filtered):,}")
    with s2:
        st.metric("Mean Charge", fmt_inr_int(filtered['charges'].mean()) if len(filtered) > 0 else "N/A")
    with s3:
        st.metric("Max Charge", fmt_inr_int(filtered['charges'].max()) if len(filtered) > 0 else "N/A")

    # Download
    st.download_button(
        "⬇️ Download Filtered Data as CSV",
        data=filtered.to_csv(index=False).encode('utf-8'),
        file_name="filtered_hospital_data.csv",
        mime="text/csv",
        use_container_width=True,
    )
