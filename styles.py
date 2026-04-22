"""Custom CSS styles for MediCharge Analytics."""

def get_custom_css():
    return """
    <style>
    /* ===== GLOBAL ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    .stApp {
        background-color: #F4FAF7;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    /* Ensure text is visible even if Streamlit is in dark mode */
    .stMarkdown p, .stMarkdown li, .stMarkdown span {
        color: #374151 !important;
    }

    /* Add padding so the menu button doesn't overlap content */
    .block-container {
        padding-top: 4.5rem !important;
        padding-bottom: 5rem !important;
    }

    /* Hide default Streamlit header/footer */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ===== SIDEBAR ===== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1B5E40 0%, #145234 100%);
        color: white;
    }
    section[data-testid="stSidebar"] .stMarkdown p,
    section[data-testid="stSidebar"] .stMarkdown li,
    section[data-testid="stSidebar"] .stMarkdown h1,
    section[data-testid="stSidebar"] .stMarkdown h2,
    section[data-testid="stSidebar"] .stMarkdown h3,
    section[data-testid="stSidebar"] label {
        color: white !important;
    }
    section[data-testid="stSidebar"] .stRadio label span {
        color: white !important;
    }
    section[data-testid="stSidebar"] .stRadio div[role="radiogroup"] label {
        color: white !important;
    }
    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.2);
    }
    
    section[data-testid="stSidebar"] img {
        border-radius: 0 0 12px 12px;
    }

    /* ===== HEADINGS ===== */
    h1, h2, h3, h4 {
        color: #2E7D5E !important;
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }

    /* ===== HERO BANNER ===== */
    .hero-banner {
        background: linear-gradient(rgba(30,90,60,0.82), rgba(30,90,60,0.82)), url('https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=1400') center/cover no-repeat;
        padding: 3rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(46,125,94,0.25);
        position: relative;
        overflow: hidden;
    }
    .hero-banner::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.05) 0%, transparent 70%);
        animation: pulse 8s ease-in-out infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.1); }
    }
    .hero-banner h1 {
        color: white !important;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        position: relative;
        z-index: 1;
    }
    .hero-banner p {
        color: rgba(255,255,255,0.9) !important;
        font-size: 1.15rem;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }

    /* ===== KPI CARDS ===== */
    .kpi-card {
        background: white;
        border-left: 5px solid #2E7D5E;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
        text-align: center;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    .kpi-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(46,125,94,0.15);
    }
    .kpi-label {
        font-size: 0.85rem;
        color: #6B7280;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }
    .kpi-value {
        font-size: 1.8rem;
        font-weight: 800;
        color: #2E7D5E;
    }

    /* ===== SECTION HEADERS ===== */
    .section-header {
        background: linear-gradient(90deg, #E8F5E9, transparent);
        padding: 0.8rem 1.2rem;
        border-left: 4px solid #2E7D5E;
        border-radius: 0 8px 8px 0;
        margin: 2rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 700;
        color: #1B5E40;
    }

    /* ===== INSIGHT CARDS ===== */
    .insight-card {
        background: white;
        border: 1px solid #C8E6C9;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    }
    .insight-card h4 {
        color: #1B5E40 !important;
        margin-bottom: 0.8rem;
    }

    /* ===== PREDICTION RESULT ===== */
    .prediction-card {
        background: linear-gradient(135deg, #2E7D5E, #1B5E40);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        color: white;
        box-shadow: 0 8px 32px rgba(46,125,94,0.3);
        margin-bottom: 1.5rem;
    }
    .prediction-card h3 {
        color: rgba(255,255,255,0.85) !important;
        font-size: 1rem;
        font-weight: 500;
        margin-bottom: 0.3rem;
    }
    .prediction-card .charge-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: white;
    }

    /* ===== RISK BADGES ===== */
    .risk-low {
        background: #E8F5E9; color: #2E7D32;
        padding: 0.5rem 1.5rem; border-radius: 50px;
        font-weight: 700; display: inline-block; font-size: 1.05rem;
    }
    .risk-medium {
        background: #FFF8E1; color: #F57F17;
        padding: 0.5rem 1.5rem; border-radius: 50px;
        font-weight: 700; display: inline-block; font-size: 1.05rem;
    }
    .risk-high {
        background: #FFEBEE; color: #C62828;
        padding: 0.5rem 1.5rem; border-radius: 50px;
        font-weight: 700; display: inline-block; font-size: 1.05rem;
    }

    /* ===== BUTTONS ===== */
    .stButton > button {
        background: linear-gradient(135deg, #2E7D5E, #1B5E40) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.6rem 2rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 12px rgba(46,125,94,0.3) !important;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #256B4E, #0F3D2A) !important;
        box-shadow: 0 6px 20px rgba(46,125,94,0.4) !important;
        transform: translateY(-2px) !important;
    }

    /* ===== DOWNLOAD BUTTON ===== */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #2E7D5E, #1B5E40) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    /* ===== FORM CARD ===== */
    .form-card {
        background: white;
        border: 2px solid #C8E6C9;
        border-radius: 16px;
        padding: 1.8rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    }
    .form-card h3 {
        color: #1B5E40 !important;
        text-align: center;
        margin-bottom: 1rem;
    }

    /* ===== STYLED TABLE ===== */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .styled-table thead th {
        background: #2E7D5E;
        color: white;
        padding: 0.8rem 1rem;
        text-align: left;
        font-weight: 600;
    }
    .styled-table tbody td {
        padding: 0.6rem 1rem;
        border-bottom: 1px solid #E8F5E9;
        color: #374151;
    }
    .styled-table tbody tr:hover {
        background: #F0FFF4;
    }

    /* ===== DATAFRAME ===== */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
    }

    /* ===== METRIC OVERRIDE ===== */
    [data-testid="stMetric"] {
        background: white;
        border-left: 5px solid #2E7D5E;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    }
    [data-testid="stMetricLabel"] {
        color: #6B7280 !important;
    }
    [data-testid="stMetricValue"] {
        color: #2E7D5E !important;
        font-weight: 800 !important;
    }

    /* ===== TABS ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 0.5rem 1.5rem;
        font-weight: 600;
    }

    /* ===== MOBILE MEDIA QUERIES ===== */
    @media (max-width: 768px) {
        .block-container {
            padding-top: 4.5rem !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-bottom: 6rem !important;
        }
        .hero-banner {
            padding: 2rem 1.5rem;
            margin-bottom: 1.5rem;
        }
        .hero-banner h1 {
            font-size: 1.8rem;
        }
        .hero-banner p {
            font-size: 1rem;
        }
        .kpi-card {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .kpi-value {
            font-size: 1.4rem;
        }
        .section-header {
            font-size: 1.1rem;
            padding: 0.6rem 1rem;
            margin: 1.5rem 0 0.8rem 0;
        }
        .insight-card {
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .prediction-card {
            padding: 1.5rem;
        }
        .prediction-card .charge-value {
            font-size: 2rem;
        }
        .form-card {
            padding: 1.2rem;
        }
        .styled-table {
            display: block;
            overflow-x: auto;
            white-space: nowrap;
        }
        .styled-table thead th, .styled-table tbody td {
            padding: 0.5rem;
            font-size: 0.9rem;
        }
        /* Adjust plotly chart containers on mobile if needed */
        [data-testid="stPlotlyChart"] {
            margin-bottom: 1rem;
        }
    }
    </style>
    """
