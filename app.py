import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import requests
from io import BytesIO
from PIL import Image
import datetime
import time
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path
import base64

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Cyberpunk Stock Tracker", page_icon="💹", layout="wide")

# ---------------------------------------------------------
# APPLY CYBERPUNK CSS
# ---------------------------------------------------------
with open("cyberpunk_style_embedded.css", "r", encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------------------------------------------------
# VIDEO BACKGROUND
# ---------------------------------------------------------
VIDEO_URL = "https://github.com/eviltosh/final_cyberpunk_quotes_redux_V4/releases/download/v2.0/cyberpunk_light.mp4"

components.html(f"""
    <video id="bgvid" autoplay muted loop playsinline
        style="
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            object-fit: cover;
            z-index: -5;
            opacity: 1.0;
        ">
        <source src="{VIDEO_URL}" type="video/mp4">
    </video>

    <script>
        document.addEventListener('click', function unmuteVideo() {{
            var v = document.getElementById('bgvid');
            if (v) {{
                v.muted = false;
                v.volume = 1.0;
                v.play();
            }}
            document.removeEventListener('click', unmuteVideo);
        }});
    </script>
""", height=0, width=0)

# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------
st.markdown("""
<div style='text-align:center; margin-top: -20px;'>
    <h1 class='cyberpunk-title'>CYBERPUNK QUOTES</h1>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
st.sidebar.header("⚙️ Controls")
tickers_input = st.sidebar.text_input("Enter stock tickers (comma-separated):", "AAPL, TSLA, NVDA")
period = st.sidebar.selectbox("Select time range:", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "max"])
refresh_rate = st.sidebar.slider("Auto-refresh interval (seconds):", 10, 300, 60)

# API Key
st.sidebar.subheader("🔑 API Keys")
finnhub_api = st.sidebar.text_input("Finnhub API key", value="", type="password")

# Background Images
st.sidebar.subheader("🌅 Chart Background")
bg_choice = st.sidebar.selectbox("Select Background Image:", ["Beach 1", "Beach 2", "Classic", "None"])

# ---------------------------------------------------------
# Load Background Image
# ---------------------------------------------------------
bg_image = None
try:
    if bg_choice == "Beach 1":
        bg_image = Image.open("images/1.jpg")
    elif bg_choice == "Beach 2":
        bg_image = Image.open("images/2.jpg")
    elif bg_choice == "Classic":
        bg_image = None
except:
    bg_image = None

# ---------------------------------------------------------
# CACHING FUNCTIONS
# ---------------------------------------------------------
@st.cache_data(ttl=3600)
def get_stock_data(ticker, period):
    return yf.Ticker(ticker).history(period=period)

@st.cache_data(ttl=3600)
def get_info_cached(ticker):
    return yf.Ticker(ticker).get_info()

@st.cache_data(ttl=1800)
def get_company_news(symbol, api_key):
    if not api_key:
        return []
    url = "https://finnhub.io/api/v1/company-news"
    today = datetime.date.today()
    past = today - datetime.timedelta(days=30)
    params = {"symbol": symbol, "from": past.isoformat(), "to": today.isoformat(), "token": api_key}
    try:
        r = requests.get(url, params=params, timeout=10)
        return [n for n in r.json() if n.get("headline") and n.get("url")] if r.status_code == 200 else []
    except:
        return []

def pil_to_data_uri(img):
    buf = BytesIO()
    img.save(buf, format="PNG")
    encoded = base64.b64encode(buf.getvalue()).decode()
    return f"data:image/png;base64,{encoded}"

# ---------------------------------------------------------
# MAIN EXECUTION
# ---------------------------------------------------------
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

if "last_refresh" not in st.session_state:
    st.session_state["last_refresh"] = time.time()
else:
    if time.time() - st.session_state["last_refresh"] > refresh_rate:
        st.session_state["last_refresh"] = time.time()
        st.rerun()

# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
for ticker in tickers:
    try:
        info = get_info_cached(ticker)
        hist = get_stock_data(ticker, period)

        if hist.empty:
            st.warning(f"No data for {ticker}")
            continue

        # ---------------------------------------------------------
        # HEADER + LOGO
        # ---------------------------------------------------------
        logo_url = info.get("logo_url")
        if not logo_url:
            domain = info.get("website", "").replace("https://", "").replace("http://", "").split("/")[0]
            if domain:
                logo_url = f"https://logo.clearbit.com/{domain}"

        c1, c2 = st.columns([1, 4])
        with c1:
            if logo_url:
                try:
                    r = requests.get(logo_url, timeout=5)
                    if r.status_code == 200:
                        st.image(Image.open(BytesIO(r.content)), width=100)
                except:
                    pass
        with c2:
            st.markdown(f"### {info.get('shortName', ticker)}")
            st.caption(f"{info.get('sector', 'N/A')} | {info.get('industry', 'N/A')}")

        # ---------------------------------------------------------
        # CYBERPUNK NEON GLOW PLOTLY CHART (No Volume)
        # ---------------------------------------------------------
        fig = go.Figure()

        # Optional background image (beach)
        if bg_image:
            try:
                uri = pil_to_data_uri(bg_image)
                fig.add_layout_image(
                    dict(
                        source=uri,
                        xref="paper", yref="paper",
                        x=0, y=1,
                        sizex=1, sizey=1,
                        xanchor="left", yanchor="top",
                        sizing="stretch",
                        opacity=0.5,
                        layer="below"
                    )
                )
            except:
                pass

        # OUTER NEON GLOW
        fig.add_trace(go.Scatter(
            x=hist.index,
            y=hist["Close"],
            mode="lines",
            line=dict(color="rgba(0,255,255,0.25)", width=16),
            hoverinfo="skip",
            showlegend=False
        ))

        # INNER NEON GLOW
        fig.add_trace(go.Scatter(
            x=hist.index,
            y=hist["Close"],
            mode="lines",
            line=dict(color="rgba(0,255,255,0.6)", width=8),
            hoverinfo="skip",
            showlegend=False
        ))

        # MAIN SHARP LINE
        fig.add_trace(go.Scatter(
            x=hist.index,
            y=hist["Close"],
            mode="lines",
            line=dict(color="#00FFFF", width=3),
            name=f"{ticker} Close",
            hovertemplate="<b>Date:</b> %{x}<br><b>Price:</b> $%{y:.2f}<extra></extra>"
        ))

        fig.update_layout(
            title=f"{ticker} Stock Price ({period})",
            xaxis_title="Date",
            yaxis_title="Price ($)",
            template="plotly_dark",
            hovermode="x unified",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=480
        )

        st.plotly_chart(fig, use_container_width=True)

        # ---------------------------------------------------------
        # METRICS
        # ---------------------------------------------------------
        c1, c2, c3, c4 = st.columns(4)
        price = info.get("currentPrice")
        cap = info.get("marketCap")
        high = info.get("fiftyTwoWeekHigh")
        low = info.get("fiftyTwoWeekLow")
        with c1: st.metric("Current Price", f"${price:,.2f}" if price else "N/A")
        with c2: st.metric("Market Cap", f"${cap:,.0f}" if cap else "N/A")
        with c3: st.metric("52w High / Low", f"${high} / ${low}")
        with c4:
            hist_5d = get_stock_data(ticker, "5d")
            if len(hist_5d) >= 2:
                ch = hist_5d["Close"].iloc[-1] - hist_5d["Close"].iloc[-2]
                pct = (ch / hist_5d["Close"].iloc[-2]) * 100
                st.metric("Daily Change", f"${ch:.2f}", f"{pct:.2f}%")

        # ---------------------------------------------------------
        # COMPANY INFO
        # ---------------------------------------------------------
        summary = info.get("longBusinessSummary", "No description.")
        if summary.strip():
            with st.expander("📘 Company Info"):
                st.write(summary)
        else:
            st.info("No company description available.")

        st.markdown("---")

        # ---------------------------------------------------------
        # NEWS
        # ---------------------------------------------------------
        st.subheader(f"📰 {ticker} Recent News")
        news = [] if not finnhub_api else get_company_news(ticker, finnhub_api)
        if news:
            for n in news[:5]:
                dt = datetime.datetime.fromtimestamp(n.get("datetime", 0)).strftime("%b %d, %Y")
                st.markdown(
                    f"<div class='news-card'><a href='{n.get('url')}' target='_blank'><b>{n.get('headline')}</b></a><br><small>{n.get('source', 'Unknown')} | {dt}</small></div>",
                    unsafe_allow_html=True
                )
        else:
            if finnhub_api:
                st.info("No recent news available.")

        st.markdown("<hr>", unsafe_allow_html=True)

    except Exception as e:
        st.error(f"Error loading {ticker}: {e}")




