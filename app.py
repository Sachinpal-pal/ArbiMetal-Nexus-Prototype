import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from deep_translator import GoogleTranslator
from datetime import datetime, timedelta

# --- 1. Global Setup ---
st.set_page_config(page_title="ArbiMetal Nexus", layout="wide", initial_sidebar_state="collapsed")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "language" not in st.session_state:
    st.session_state.language = "en"

# --- 2. CSS FOR PERFECT STICKY HEADER, LARGER UI & VISIBILITY ---
st.markdown("""
    <style>
    /* Hide Streamlit Default Headers */
    header { visibility: hidden !important; }
    [data-testid="collapsedControl"] { display: none; }
    
    /* Main Content Padding */
    .block-container { 
        padding-top: 110px !important; 
    }
    
    /* PERFECT STICKY HEADER */
    .sticky-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        background: rgba(5, 10, 15, 0.98); 
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        z-index: 999999; 
        padding: 15px 40px;
        border-bottom: 3px solid #FFD700;
        box-shadow: 0px 10px 40px rgba(0,0,0,0.9);
        display: flex;
        align-items: center;
        justify-content: space-between; 
    }
    
    /* Super Stylish Glowing Title - Made Slightly Larger */
    .main-title { 
        font-size: 50px; 
        font-weight: 900; 
        background: linear-gradient(to right, #FFD700, #FFF, #FFD700);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        text-shadow: 3px 3px 15px rgba(255, 215, 0, 0.4);
        font-family: 'Arial Black', sans-serif;
        margin: 0;
        padding: 0;
    }
    
    /* BACKGROUND IMAGE */
    .stApp {
        background-image: url("https://media.assettype.com/outlookbusiness/2025-06-11/cmj4vc4g/gold-silver-bars-stacked-financial-concept-background845403-149.avif?w=640");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #FFFFFF;
    }
    
    /* HEAVIER Dark Overlay for Better Text Visibility */
    .stApp::before {
        content: "";
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        background-color: rgba(0, 0, 0, 0.88); 
        z-index: -1;
    }
    
    /* Glass Cards */
    .glass-card { 
        background: rgba(15, 20, 25, 0.92); 
        backdrop-filter: blur(25px); 
        border-radius: 18px; 
        padding: 30px; 
        border: 1px solid rgba(255, 215, 0, 0.4); 
        box-shadow: 0 10px 40px 0 rgba(0,0,0,0.9);
        margin-top: 15px; 
        font-size: 18px; 
    }
    
    h3 { 
        color: #FFFFFF !important; 
        text-shadow: 2px 2px 8px rgba(0,0,0,1); 
        font-weight: 800; 
        font-size: 26px !important;
        margin-bottom: 15px !important;
    }
    
    .ai-summary { 
        background: rgba(20, 20, 20, 0.95); 
        border-left: 6px solid #FFD700; 
        padding: 25px; 
        border-radius: 10px; 
        font-size: 19px; 
        margin-top: 15px; 
        box-shadow: 0px 5px 15px rgba(0,0,0,0.7);
        color: #FFFFFF;
        line-height: 1.5;
    }
    
    .graph-insight { 
        background: rgba(10, 15, 20, 0.95); 
        border-left: 6px solid #00BFFF; 
        padding: 25px; 
        border-radius: 10px; 
        font-size: 18px; 
        margin-top: 15px; 
        color: #FFFFFF; 
        box-shadow: 0px 5px 15px rgba(0,0,0,0.7);
        line-height: 1.6;
    }
    
    .chat-container { border: 1px solid rgba(255,215,0,0.5); padding: 20px; border-radius: 12px; background: rgba(0,0,0,0.85); max-height: 400px; overflow-y: auto;}
    .chat-user { background-color: rgba(255, 215, 0, 0.2); padding: 12px 20px; border-radius: 18px 18px 0px 18px; margin-bottom: 15px; width: fit-content; margin-left: auto; border: 1px solid rgba(255,215,0,0.6); font-size: 17px;}
    .chat-ai { background-color: rgba(30, 30, 30, 0.95); padding: 12px 20px; border-radius: 18px 18px 18px 0px; margin-bottom: 15px; border: 1px solid #00BFFF; width: fit-content; font-size: 17px;}
    
    .stSelectbox div[data-baseweb="select"], .stDateInput div[data-baseweb="input"], .stTextInput div[data-baseweb="input"] {
        background-color: rgba(15, 15, 15, 0.9) !important;
        border: 2px solid rgba(255, 215, 0, 0.6) !important;
        border-radius: 10px !important;
        color: #FFFFFF !important;
        font-size: 18px !important; 
        padding: 8px !important; 
    }
    
    .stSelectbox label, .stDateInput label, .stTextInput label {
        color: #FFD700 !important;
        font-size: 18px !important;
        font-weight: bold !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.8);
    }
    
    [data-testid="stDataFrame"] { background: rgba(0,0,0,0.85); border-radius: 12px; font-size: 16px; }
    
    .sticky-header .stSelectbox { margin-bottom: 0px; width: 200px;}
    </style>
    
    <!-- STICKY HEADER HTML -->
    <div class="sticky-header">
        <h1 class="main-title">ArbiMetal Nexus</h1>
    </div>
""", unsafe_allow_html=True)

# NEW TRANSLATION LOGIC USING DEEP-TRANSLATOR
def translate(text, dest_lang):
    if dest_lang == "en" or not text: return text
    try: return GoogleTranslator(source='auto', target=dest_lang).translate(text)
    except: return text 

# --- 3. Language Selector ---
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col_lang = st.columns([4, 1.5])
with col_lang:
    lang_map = {"English": "en", "हिन्दी (Hindi)": "hi", "Español (Spanish)": "es"}
    sel_lang = st.selectbox("🌐 Language", list(lang_map.keys()), key="lang_selector")
    lang = lang_map[sel_lang]

# --- 4. Inputs ---
st.markdown("---")
st.markdown(f"### 📍 {translate('Location & Market Configuration', lang)}")
col_reg, col_state, col_metal, col_date = st.columns(4)

with col_reg:
    regions = {
        "Global (Wall Street)": {"currency": "USD", "forex": None, "tax": 0.0, "unit": "Base Unit", "mult": 1},
        "India (Local Shop)": {"currency": "INR", "forex": "INR=X", "tax": 0.15, "unit": "10 Grams / Local Unit", "mult": (10/31.103)},
        "UAE (Dubai Gold Souk)": {"currency": "AED", "forex": "AED=X", "tax": 0.05, "unit": "10 Grams / Local Unit", "mult": (10/31.103)},
        "Europe (Retail)": {"currency": "EUR", "forex": "EUR=X", "tax": 0.20, "unit": "10 Grams / Local Unit", "mult": (10/31.103)}
    }
    sel_reg = st.selectbox(translate("Select Region", lang), list(regions.keys()))
    reg_data = regions[sel_reg]

with col_state:
    state_premium = 0.0
    if sel_reg == "India (Local Shop)":
        states = {
            "Delhi (Base)": 0.0, "Andhra Pradesh (+0.9%)": 0.009, "Karnataka (+0.8%)": 0.008, 
            "Maharashtra (+1.2%)": 0.012, "Tamil Nadu (+1.0%)": 0.010, "Uttar Pradesh (+0.7%)": 0.007
        } 
        sel_state = st.selectbox(translate("Select State", lang), list(states.keys()))
        state_premium = states[sel_state]
    else:
        st.selectbox(translate("State/Province", lang), ["National Average"], disabled=True)

with col_metal:
    metals = {"Gold": "GC=F", "Silver": "SI=F", "Copper": "HG=F", "Platinum": "PL=F", "Palladium": "PA=F", "Aluminum": "ALI=F"}
    sel_metal = st.selectbox(translate("Select Commodity", lang), list(metals.keys()))
    ticker = metals[sel_metal]

with col_date:
    today = datetime.now()
    sel_date = st.date_input(translate("Search Specific Date", lang), value=today, min_value=today - timedelta(days=365), max_value=today)

# --- 5. Data Engine ---
@st.cache_data(ttl=1800)
def get_market_data(ticker, forex_ticker):
    df = yf.Ticker(ticker).history(period="1y")[['Open', 'High', 'Low', 'Close']].dropna()
    df.index = df.index.tz_localize(None)
    if forex_ticker:
        forex_df = yf.Ticker(forex_ticker).history(period="1y")[['Close']].rename(columns={'Close': 'Forex'})
        forex_df.index = forex_df.index.tz_localize(None)
        df = df.join(forex_df, how='left').ffill()
    else:
        df['Forex'] = 1.0
    return df

with st.spinner(translate('Loading Data...', lang)):
    df = get_market_data(ticker, reg_data['forex'])

total_multiplier = reg_data['mult'] * df['Forex'] * (1 + reg_data['tax'] + state_premium)
for col in ['Open', 'High', 'Low', 'Close']:
    df[col] = df[col] * total_multiplier

df['Near_Term'] = df['Close'].rolling(window=20).mean()
df['Long_Term'] = df['Close'].rolling(window=60).mean()
df.dropna(inplace=True)

curr = reg_data['currency']
unit = reg_data['unit']

# --- 6. AI Market Analyst ---
latest_near = df['Near_Term'].iloc[-1]
latest_long = df['Long_Term'].iloc[-1]

if latest_near > latest_long * 1.02:
    ai_msg = f"The {sel_metal} market is facing a SHORTAGE. Prices are highly inflated. WAIT before buying. If you own it, SELL at a premium."
elif latest_near < latest_long * 0.98:
    ai_msg = f"{sel_metal} is UNDERVALUED. Prices are cheaper than the historical average. Excellent time to BUY."
else:
    ai_msg = f"The {sel_metal} market is STABLE. You can buy or sell based on your budget."

st.markdown("---")
st.markdown(f"### 🤖 {translate('AI Market Analyst Summary', lang)}")
st.markdown(f"<div class='ai-summary'><b>{translate(ai_msg, lang)}</b></div>", unsafe_allow_html=True)

# --- 7. Chart & Insights ---
st.markdown(f"<br>### 📈 {translate('1-Year Price Trend', lang)}", unsafe_allow_html=True)
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name=translate('Live Price', lang), line=dict(color='#FFD700', width=3))) 
fig.add_trace(go.Scatter(x=df.index, y=df['Long_Term'], name=translate('Historical Average', lang), line=dict(color='#00BFFF', width=2.5, dash='dot'))) 

fig.update_layout(
    template="plotly_dark", 
    plot_bgcolor='rgba(0,0,0,0.6)', 
    paper_bgcolor='rgba(0,0,0,0)', 
    height=450, 
    margin=dict(l=0, r=0, t=20, b=0), 
    hovermode="x unified",
    font=dict(color='#FFFFFF', size=14) 
)
fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')
fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.1)')

st.plotly_chart(fig, use_container_width=True)

max_val = df['Close'].max()
min_val = df['Close'].min()
max_date = df['Close'].idxmax().strftime('%d %b %Y')
min_date = df['Close'].idxmin().strftime('%d %b %Y')
current_val = df['Close'].iloc[-1]

trend = "upward" if current_val > df['Close'].iloc[0] else "downward"

insight_text = f"**{translate('Graph Analysis Details:', lang)}**<br>"
insight_text += f"1. In the last 1 year, the lowest price was **{curr} {min_val:,.2f}** on {min_date}.<br>"
insight_text += f"2. The highest price reached was **{curr} {max_val:,.2f}** on {max_date}.<br>"
insight_text += f"3. Currently, the price is **{curr} {current_val:,.2f}**, which shows an overall **{trend}** trend for the year.<br>"
insight_text += f"4. The blue dotted line shows the 60-day average. When the gold line (current price) is above it, it means the market is heated."

st.markdown(f"<div class='graph-insight'>{translate(insight_text, lang)}</div>", unsafe_allow_html=True)

# --- 8. Specific Date Deep-Dive ---
st.markdown("---")
target_date = pd.to_datetime(sel_date)
closest_date_idx = df.index.get_indexer([target_date], method='nearest')[0]
closest_date = df.index[closest_date_idx]
date_data = df.iloc[closest_date_idx]

dt_str = closest_date.strftime('%d %B %Y')

deep_dive_text = f"**{translate('Market Details for', lang)} {dt_str}**<br>"
deep_dive_text += f"• **{translate('Opening Rate', lang)}:** {curr} {date_data['Open']:,.2f} per {unit}<br>"
deep_dive_text += f"• **{translate('Closing Rate', lang)}:** {curr} {date_data['Close']:,.2f} per {unit}<br>"
deep_dive_text += f"• **{translate('Daily High', lang)}:** {curr} {date_data['High']:,.2f}<br>"
deep_dive_text += f"• **{translate('Daily Low', lang)}:** {curr} {date_data['Low']:,.2f}"

st.markdown(f"<div class='glass-card'>{deep_dive_text}</div>", unsafe_allow_html=True)

# --- 9. Virtual AI Analyst Chatbot ---
st.markdown("---")
st.markdown(f"### 💬 {translate('Chat with AI Virtual Analyst', lang)}")

chat_placeholder = st.container()
with chat_placeholder:
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.chat_history:
        if msg['role'] == 'user':
            st.markdown(f"<div class='chat-user'>{msg['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-ai'>🤖 {msg['content']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

user_query = st.text_input(translate("Ask a question (e.g., Should I buy today?)", lang), key="chat_input")
if st.button(translate("Send", lang)) and user_query:
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    
    q_lower = user_query.lower()
    if "buy" in q_lower or "kharid" in q_lower:
        reply = "YES, indicators say buy." if latest_near < latest_long else "WAIT, prices are high or stable."
    elif "sell" in q_lower or "bech" in q_lower:
        reply = "YES, good time to sell." if latest_near > latest_long else "HOLD, price is not at a premium yet."
    else:
        reply = "Please read the AI summary and Graph insights above for detailed guidance."
        
    st.session_state.chat_history.append({"role": "assistant", "content": translate(reply, lang)})
    st.rerun()

# --- 10. Raw Tabular Data ---
st.markdown("---")
st.markdown(f"### 🗃️ {translate('Raw Tabular Data', lang)} ({curr})")
display_df = df[['Open', 'High', 'Low', 'Close']].sort_index(ascending=False)
display_df.index = display_df.index.strftime('%Y-%m-%d')
st.dataframe(display_df, use_container_width=True, height=400)
