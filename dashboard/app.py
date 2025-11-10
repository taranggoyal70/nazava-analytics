"""
Shopee Analytics Platform - Streamlit Dashboard
Main entry point
"""

import streamlit as st
import sys
import os
import json
import hashlib
from datetime import datetime
import urllib.parse
import secrets

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, use environment variables directly

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Page configuration
st.set_page_config(
    page_title="Nazava Analytics - Login",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Google OAuth Configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID')  # Set in environment
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', 'YOUR_GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI = "http://localhost:8501"  # Your app URL

# Authentication functions
USERS_FILE = os.path.join(os.path.dirname(__file__), 'users.json')

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_google_oauth_url():
    """Generate Google OAuth URL"""
    params = {
        'client_id': GOOGLE_CLIENT_ID,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
        'prompt': 'consent'
    }
    return f"https://accounts.google.com/o/oauth2/v2/auth?{urllib.parse.urlencode(params)}"

def handle_google_callback():
    """Handle Google OAuth callback"""
    # Check if we have the code parameter
    query_params = st.query_params
    if 'code' in query_params:
        # In a real implementation, you would exchange the code for tokens
        # For now, we'll simulate successful authentication
        st.session_state.logged_in = True
        st.session_state.username = "google_user"
        st.session_state.oauth_provider = "google"
        return True
    return False

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def signup(username, password, email):
    users = load_users()
    if username in users:
        return False, "Username already exists"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    users[username] = {
        'password': hash_password(password),
        'email': email,
        'created_at': datetime.now().isoformat()
    }
    save_users(users)
    return True, "Account created successfully!"

def login(username, password):
    users = load_users()
    if username not in users:
        return False, "Username not found"
    if users[username]['password'] != hash_password(password):
        return False, "Incorrect password"
    return True, "Login successful!"

# Initialize demo user
if not os.path.exists(USERS_FILE):
    demo_users = {
        'demo': {
            'password': hash_password('demo123'),
            'email': 'demo@nazava.com',
            'created_at': datetime.now().isoformat()
        }
    }
    save_users(demo_users)

# Handle Google OAuth callback
if handle_google_callback():
    st.switch_page("pages/1_Overview.py")

# Check if already logged in - redirect to Overview
if 'logged_in' in st.session_state and st.session_state.logged_in:
    st.switch_page("pages/1_Overview.py")

# Custom CSS
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding and default navigation */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Keep navigation visible but styled */
    
    /* Force light theme */
    .stApp {
        background: #f8f9fa;
    }
    
    [data-testid="stAppViewContainer"] {
        background: #f8f9fa;
    }
    
    [data-testid="stHeader"] {
        background: transparent;
    }
    
    /* Main container */
    .main {
        background: #f8f9fa;
    }
    
    .block-container {
        padding: 2rem 3rem;
        max-width: 1400px;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(79, 172, 254, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Metric cards */
    div[data-testid="metric-container"] {
        background: #ffffff;
        padding: 1.8rem;
        border-radius: 16px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        border-left: 5px solid #4facfe;
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 20px rgba(79, 172, 254, 0.15);
        border-left-color: #00f2fe;
    }
    
    div[data-testid="metric-container"] label {
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        color: #64748b !important;
        text-transform: uppercase;
        letter-spacing: 0.8px;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
        font-weight: 800 !important;
        color: #1e293b !important;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricDelta"] {
        font-size: 0.9rem !important;
        font-weight: 600 !important;
    }
    
    /* Section headers */
    h2 {
        color: #1a202c;
        font-weight: 700;
        margin-top: 2rem;
        margin-bottom: 1rem;
        font-size: 1.8rem;
        border-left: 4px solid #4facfe;
        padding-left: 1rem;
    }
    
    h3 {
        color: #2d3748;
        font-weight: 600;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        font-size: 1.3rem;
    }
    
    h4 {
        color: #4a5568;
        font-weight: 600;
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
    }
    
    p {
        color: #4a5568;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    /* Cards and containers */
    .element-container {
        margin-bottom: 1rem;
    }
    
    /* Buttons */
    .stButton > button {
        width: 100%;
        background: #4facfe;
        color: white;
        border: none;
        padding: 1rem 1.5rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
        text-transform: none;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 172, 254, 0.5);
        background: #3d9de8;
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Primary portal buttons */
    .stButton > button[kind="primary"] {
        background: #4facfe;
        font-size: 1.05rem;
        padding: 1.1rem 2rem;
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 12px;
        border: none;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 3px solid #e2e8f0;
        box-shadow: 2px 0 10px rgba(0,0,0,0.05);
    }
    
    section[data-testid="stSidebar"] > div {
        padding-top: 2rem;
    }
    
    section[data-testid="stSidebar"] h1 {
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1.2rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #0f172a;
        font-size: 1rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-top: 2rem;
        margin-bottom: 1rem;
        border-bottom: 3px solid #4facfe;
        padding-bottom: 0.6rem;
    }
    
    section[data-testid="stSidebar"] .stMarkdown {
        color: #1a202c;
        font-size: 1rem;
        line-height: 1.8;
        font-weight: 500;
    }
    
    section[data-testid="stSidebar"] .stMarkdown strong {
        color: #0f172a;
        font-weight: 700;
        font-size: 1.05rem;
    }
    
    section[data-testid="stSidebar"] .stMarkdown em {
        color: #4facfe;
        font-style: normal;
        font-weight: 600;
    }
    
    section[data-testid="stSidebar"] .stMarkdown ul {
        list-style: none;
        padding-left: 0;
    }
    
    section[data-testid="stSidebar"] .stMarkdown li {
        color: #1e293b;
        font-size: 1rem;
        font-weight: 500;
        padding: 0.4rem 0;
        margin-left: 0.5rem;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p {
        color: #1e293b;
        font-size: 0.95rem;
        margin: 0.3rem 0;
    }
    
    section[data-testid="stSidebar"] a {
        color: #4facfe;
        text-decoration: none;
    }
    
    section[data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        border: none;
        color: white;
        font-weight: 600;
        padding: 0.75rem 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 8px rgba(79, 172, 254, 0.3);
    }
    
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 172, 254, 0.4);
    }
    
    /* Sidebar page links - make them blue */
    section[data-testid="stSidebar"] a {
        color: #4facfe !important;
        text-decoration: none !important;
        font-weight: 500 !important;
        transition: all 0.2s;
    }
    
    section[data-testid="stSidebar"] a:hover {
        color: #00f2fe !important;
        padding-left: 0.5rem;
    }
    
    /* Page navigation items */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        background: white;
        padding: 1rem 0;
    }
    
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] li {
        margin: 0.2rem 0;
    }
    
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a {
        background: #ffffff !important;
        color: #0f172a !important;
        padding: 1rem 1.2rem !important;
        border-radius: 8px !important;
        margin: 0.4rem 0.8rem !important;
        display: flex !important;
        align-items: center !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.2s ease !important;
        border: 2px solid #cbd5e1 !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08) !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a:hover {
        background: #dbeafe !important;
        color: #1e40af !important;
        border-color: #60a5fa !important;
        transform: translateX(3px) !important;
        box-shadow: 0 3px 8px rgba(79, 172, 254, 0.3) !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"] {
        background: #4facfe !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        border-color: #4facfe !important;
        box-shadow: 0 4px 12px rgba(79, 172, 254, 0.5) !important;
    }
    
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] a[aria-current="page"]:hover {
        background: #2563eb !important;
        color: #ffffff !important;
        border-color: #2563eb !important;
        transform: translateX(3px) !important;
    }
    
    /* Make sure page names are visible */
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] span {
        color: inherit !important;
        font-size: inherit !important;
        font-weight: inherit !important;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: all 0.3s;
        border: 2px solid transparent;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(79, 172, 254, 0.2);
        border-color: #4facfe;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    .feature-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #1a202c;
        margin-bottom: 0.75rem;
    }
    
    .feature-desc {
        color: #4a5568;
        font-size: 1rem;
        line-height: 1.7;
    }
    
    /* Divider */
    hr {
        margin: 2rem 0;
        border: none;
        height: 1px;
        background: linear-gradient(90deg, transparent, #cbd5e0, transparent);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem;
        color: #718096;
        font-size: 0.9rem;
        margin-top: 3rem;
    }
</style>
""", unsafe_allow_html=True)

# Hide sidebar on login page
st.markdown("""
<style>
    section[data-testid="stSidebar"] {
        display: none;
    }
</style>
""", unsafe_allow_html=True)

# Modern Login/Signup Page with Beautiful Design
st.markdown("""
<style>
    .login-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        min-height: 100vh;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: -5rem -5rem;
        padding: 2rem;
    }
    .login-card {
        background: white;
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        padding: 3rem;
        max-width: 480px;
        width: 100%;
    }
    .google-btn {
        background: white;
        border: 2px solid #e2e8f0;
        padding: 0.75rem 1.5rem;
        border-radius: 12px;
        font-weight: 600;
        color: #1a202c;
        cursor: pointer;
        transition: all 0.3s;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.75rem;
        margin-bottom: 1.5rem;
    }
    .google-btn:hover {
        border-color: #4facfe;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(79, 172, 254, 0.3);
    }
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 1.5rem 0;
    }
    .divider::before,
    .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #e2e8f0;
    }
    .divider span {
        padding: 0 1rem;
        color: #94a3b8;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2.5, 1])

with col2:
    # Header with gradient background
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2.5rem;">
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    width: 80px; height: 80px; border-radius: 20px; 
                    display: inline-flex; align-items: center; justify-content: center;
                    box-shadow: 0 10px 30px rgba(79, 172, 254, 0.4);
                    margin-bottom: 1.5rem;">
            <span style="font-size: 3rem;">💧</span>
        </div>
        <h1 style="color: #0f172a; font-size: 2.5rem; font-weight: 800; margin: 0.5rem 0;">
            Nazava Analytics
        </h1>
        <p style="color: #64748b; font-size: 1rem; margin: 0;">
            AI-Powered E-Commerce Intelligence Platform
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Sign Up"])
    
    with tab1:
        st.markdown("<h3 style='text-align: center; color: #0f172a; margin-bottom: 1.5rem;'>Welcome Back</h3>", unsafe_allow_html=True)
        
        # Professional Google Sign In Button
        st.markdown("""
        <style>
            .google-signin-btn {
                background: white;
                border: 1px solid #dadce0;
                border-radius: 4px;
                padding: 12px 16px;
                display: flex;
                align-items: center;
                justify-content: center;
                gap: 12px;
                cursor: pointer;
                transition: all 0.2s;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                margin-bottom: 1.5rem;
            }
            .google-signin-btn:hover {
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                border-color: #d2d2d2;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Google button with proper styling - Login
        # Check if credentials are configured
        if GOOGLE_CLIENT_ID == 'YOUR_GOOGLE_CLIENT_ID' or not GOOGLE_CLIENT_ID:
            # Demo mode - button logs in directly
            if st.button("🌐 Sign in with Google (Demo Mode)", key="google_demo_login", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "demo_google_user"
                st.balloons()
                st.switch_page("pages/1_Overview.py")
            st.info("💡 **Demo Mode:** Google OAuth credentials not configured. Button will log you in directly. See `GOOGLE_OAUTH_SETUP.md` to enable real Google authentication.")
        else:
            # Real OAuth mode
            google_oauth_url = get_google_oauth_url()
            
            st.markdown(f"""
            <a href="{google_oauth_url}" target="_self" style="text-decoration: none;">
                <button style="
                    width: 100%;
                    background: white;
                    border: 1px solid #dadce0;
                    color: #3c4043;
                    font-weight: 500;
                    font-size: 14px;
                    padding: 11px 16px;
                    border-radius: 4px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    cursor: pointer;
                    transition: all 0.2s;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 12px;
                    font-family: 'Google Sans', Roboto, Arial, sans-serif;
                " onmouseover="this.style.boxShadow='0 2px 8px rgba(0,0,0,0.15)'; this.style.background='#f8f9fa';" 
                   onmouseout="this.style.boxShadow='0 1px 3px rgba(0,0,0,0.1)'; this.style.background='white';">
                    <svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
                        <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                        <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                        <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
                        <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.3-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
                    </svg>
                    <span>Sign in with Google</span>
                </button>
            </a>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Add Google logo and styling
        st.markdown("""
        <style>
            /* Style Google buttons */
            button[data-testid="baseButton-secondary"] {
                background: white !important;
                border: 1px solid #dadce0 !important;
                color: #3c4043 !important;
                font-weight: 500 !important;
                font-size: 14px !important;
                padding: 10px 16px !important;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
                transition: all 0.2s !important;
            }
            button[data-testid="baseButton-secondary"]:hover {
                box-shadow: 0 2px 8px rgba(0,0,0,0.15) !important;
                border-color: #d2d2d2 !important;
                background: #f8f9fa !important;
            }
            /* Add Google icon before text */
            button[data-testid="baseButton-secondary"]::before {
                content: "";
                display: inline-block;
                width: 18px;
                height: 18px;
                margin-right: 12px;
                background-image: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTgiIGhlaWdodD0iMTgiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld0JveD0iMCAwIDQ4IDQ4Ij48cGF0aCBmaWxsPSIjRUE0MzM1IiBkPSJNMjQgOS41YzMuNTQgMCA2LjcxIDEuMjIgOS4yMSAzLjZsNi44NS02Ljg1QzM1LjkgMi4zOCAzMC40NyAwIDI0IDAgMTQuNjIgMCA2LjUxIDUuMzggMi41NiAxMy4yMmw3Ljk4IDYuMTlDMTIuNDMgMTMuNzIgMTcuNzQgOS41IDI0IDkuNXoiLz48cGF0aCBmaWxsPSIjNDI4NUY0IiBkPSJNNDYuOTggMjQuNTVjMC0xLjU3LS4xNS0zLjA5LS4zOC00LjU1SDI0djkuMDJoMTIuOTRjLS41OCAyLjk2LTIuMjYgNS40OC00Ljc4IDcuMThsNy43MyA2YzQuNTEtNC4xOCA3LjA5LTEwLjM2IDcuMDktMTcuNjV6Ii8+PHBhdGggZmlsbD0iI0ZCQkMwNSIgZD0iTTEwLjUzIDI4LjU5Yy0uNDgtMS40NS0uNzYtMi45OS0uNzYtNC41OXMuMjctMy4xNC43Ni00LjU5bC03Ljk4LTYuMTlDLjkyIDE2LjQ2IDAgMjAuMTIgMCAyNGMwIDMuODguOTIgNy41NCAyLjU2IDEwLjc4bDcuOTctNi4xOXoiLz48cGF0aCBmaWxsPSIjMzRBODUzIiBkPSJNMjQgNDhjNi40OCAwIDExLjkzLTIuMTMgMTUuODktNS44MWwtNy43My02Yy0yLjE1IDEuNDUtNC45MiAyLjMtOC4xNiAyLjMtNi4yNiAwLTExLjU3LTQuMjItMTMuNDctOS45MWwtNy45OCA2LjE5QzYuNTEgNDIuNjIgMTQuNjIgNDggMjQgNDh6Ii8+PC9zdmc+');
                background-size: contain;
                background-repeat: no-repeat;
                vertical-align: middle;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Divider
        st.markdown("""
        <div class="divider">
            <span>or continue with email</span>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username", label_visibility="collapsed")
            st.markdown('<p style="font-size: 0.85rem; color: #64748b; margin: -0.5rem 0 0.5rem 0;">Username</p>', unsafe_allow_html=True)
            
            password = st.text_input("Password", type="password", placeholder="Enter your password", label_visibility="collapsed")
            st.markdown('<p style="font-size: 0.85rem; color: #64748b; margin: -0.5rem 0 1rem 0;">Password</p>', unsafe_allow_html=True)
            
            col_a, col_b = st.columns([1, 1])
            with col_a:
                remember = st.checkbox("Remember me", value=True)
            with col_b:
                st.markdown('<p style="text-align: right; margin-top: 0.5rem;"><a href="#" style="color: #4facfe; text-decoration: none; font-size: 0.9rem;">Forgot password?</a></p>', unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("🚀 Sign In", use_container_width=True)
            
            if submit:
                if username and password:
                    success, message = login(username, password)
                    if success:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.success("✅ " + message)
                        st.info("🚀 Redirecting to Overview...")
                        st.balloons()
                        st.switch_page("pages/1_Overview.py")
                    else:
                        st.error("❌ " + message)
                else:
                    st.warning("⚠️ Please fill in all fields")
        
        # Features (removed demo credentials)
        st.markdown("""
        <div style="margin-top: 2rem; padding: 1.5rem; background: #f8f9fa; border-radius: 12px;">
            <p style="color: #0f172a; margin: 0 0 1rem 0; font-weight: 600; text-align: center;">What's Inside</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 0.75rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #10b981;">✓</span>
                    <span style="color: #64748b; font-size: 0.85rem;">89.18% XGBoost ML</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #10b981;">✓</span>
                    <span style="color: #64748b; font-size: 0.85rem;">1,006% Campaign ROI</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #10b981;">✓</span>
                    <span style="color: #64748b; font-size: 0.85rem;">16 Dashboard Pages</span>
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="color: #10b981;">✓</span>
                    <span style="color: #64748b; font-size: 0.85rem;">Real-time Analytics</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("<h3 style='text-align: center; color: #0f172a; margin-bottom: 1.5rem;'>Create Your Account</h3>", unsafe_allow_html=True)
        
        # Google button with proper styling - Signup
        # Check if credentials are configured
        if GOOGLE_CLIENT_ID == 'YOUR_GOOGLE_CLIENT_ID' or not GOOGLE_CLIENT_ID:
            # Demo mode - button logs in directly
            if st.button("🌐 Sign up with Google (Demo Mode)", key="google_demo_signup", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "demo_google_user"
                st.balloons()
                st.switch_page("pages/1_Overview.py")
            st.info("💡 **Demo Mode:** Google OAuth credentials not configured. Button will log you in directly.")
        else:
            # Real OAuth mode
            google_oauth_url_signup = get_google_oauth_url()
            
            st.markdown(f"""
            <a href="{google_oauth_url_signup}" target="_self" style="text-decoration: none;">
                <button style="
                    width: 100%;
                    background: white;
                    border: 1px solid #dadce0;
                    color: #3c4043;
                    font-weight: 500;
                    font-size: 14px;
                    padding: 11px 16px;
                    border-radius: 4px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                    cursor: pointer;
                    transition: all 0.2s;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    gap: 12px;
                    font-family: 'Google Sans', Roboto, Arial, sans-serif;
                " onmouseover="this.style.boxShadow='0 2px 8px rgba(0,0,0,0.15)'; this.style.background='#f8f9fa';" 
                   onmouseout="this.style.boxShadow='0 1px 3px rgba(0,0,0,0.1)'; this.style.background='white';">
                    <svg width="18" height="18" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48">
                        <path fill="#EA4335" d="M24 9.5c3.54 0 6.71 1.22 9.21 3.6l6.85-6.85C35.9 2.38 30.47 0 24 0 14.62 0 6.51 5.38 2.56 13.22l7.98 6.19C12.43 13.72 17.74 9.5 24 9.5z"/>
                        <path fill="#4285F4" d="M46.98 24.55c0-1.57-.15-3.09-.38-4.55H24v9.02h12.94c-.58 2.96-2.26 5.48-4.78 7.18l7.73 6c4.51-4.18 7.09-10.36 7.09-17.65z"/>
                        <path fill="#FBBC05" d="M10.53 28.59c-.48-1.45-.76-2.99-.76-4.59s.27-3.14.76-4.59l-7.98-6.19C.92 16.46 0 20.12 0 24c0 3.88.92 7.54 2.56 10.78l7.97-6.19z"/>
                        <path fill="#34A853" d="M24 48c6.48 0 11.93-2.13 15.89-5.81l-7.73-6c-2.15 1.45-4.92 2.3-8.16 2.30-6.26 0-11.57-4.22-13.47-9.91l-7.98 6.19C6.51 42.62 14.62 48 24 48z"/>
                    </svg>
                    <span>Sign up with Google</span>
                </button>
            </a>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Divider
        st.markdown("""
        <div class="divider">
            <span>or sign up with email</span>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("signup_form"):
            new_username = st.text_input("Username", placeholder="Choose a username", label_visibility="collapsed")
            st.markdown('<p style="font-size: 0.85rem; color: #64748b; margin: -0.5rem 0 0.5rem 0;">Username</p>', unsafe_allow_html=True)
            
            new_email = st.text_input("Email", placeholder="your@email.com", label_visibility="collapsed")
            st.markdown('<p style="font-size: 0.85rem; color: #64748b; margin: -0.5rem 0 0.5rem 0;">Email Address</p>', unsafe_allow_html=True)
            
            new_password = st.text_input("Password", type="password", placeholder="At least 6 characters", label_visibility="collapsed")
            st.markdown('<p style="font-size: 0.85rem; color: #64748b; margin: -0.5rem 0 0.5rem 0;">Password</p>', unsafe_allow_html=True)
            
            confirm_password = st.text_input("Confirm", type="password", placeholder="Re-enter password", label_visibility="collapsed")
            st.markdown('<p style="font-size: 0.85rem; color: #64748b; margin: -0.5rem 0 1rem 0;">Confirm Password</p>', unsafe_allow_html=True)
            
            agree = st.checkbox("I agree to the Terms of Service and Privacy Policy", value=False)
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit = st.form_submit_button("✨ Create Account", use_container_width=True)
            
            if submit:
                if not agree:
                    st.warning("⚠️ Please agree to the Terms of Service")
                elif new_username and new_email and new_password and confirm_password:
                    if new_password != confirm_password:
                        st.error("❌ Passwords don't match")
                    else:
                        success, message = signup(new_username, new_password, new_email)
                        if success:
                            st.success("✅ " + message)
                            st.info("👉 Please switch to the Login tab and sign in")
                        else:
                            st.error("❌ " + message)
                else:
                    st.warning("⚠️ Please fill in all fields")
        
        # Benefits
        st.markdown("""
        <div style="margin-top: 2rem; padding: 1.5rem; background: linear-gradient(135deg, #e6f3ff 0%, #f0f9ff 100%); border-radius: 12px; border-left: 4px solid #4facfe;">
            <p style="color: #0f172a; margin: 0 0 1rem 0; font-weight: 600; text-align: center;">🎯 Join 1,000+ Businesses</p>
            <p style="color: #64748b; font-size: 0.9rem; text-align: center; line-height: 1.6;">
                Get instant access to AI-powered sales forecasting, customer segmentation,
                campaign optimization, and 16 comprehensive analytics pages.
            </p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style="text-align: center; color: #94a3b8; font-size: 0.9rem; padding: 2rem;">
    <p><strong>Nazava Analytics Platform</strong> v2.0.0</p>
    <p style="margin-top: 0.5rem;">
        🔮 XGBoost ML (89.18%) &nbsp;|
        🎯 K-Means Segmentation &nbsp;|
        💰 Campaign ROI (1,006%)
    </p>
    <p style="margin-top: 1rem; font-size: 0.85rem;">
        Built with ❤️ using Streamlit, Plotly & XGBoost
    </p>
</div>
""", unsafe_allow_html=True)
