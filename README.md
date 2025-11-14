# 💹 **Cyberpunk Quotes — Neon Stock Dashboard**
### ⚡ Now featuring a **fullscreen cyberpunk animated background**

Cyberpunk Quotes is a fully immersive, neon-styled stock market dashboard built with **Streamlit**, offering real-time stock data, company insights, and latest news — all wrapped in a futuristic UI powered by glowing visuals and a looping cyberpunk video background.

---

## 🎬 **🔥 New Feature: Fullscreen Animated Video Background**
Your dashboard now supports a **looping MP4 video** playing behind the entire app for a cinematic cyberpunk effect.

To use your own video, place it here:

```
/videos/cyberpunk_light.mp4
```

The app automatically plays it in fullscreen using native HTML5 video.

---

## 🚀 **Features**
- 🔍 Search multiple tickers at once  
- 📈 Neon cyberpunk glow charts (matplotlib + mplcyberpunk)  
- 🎬 Fullscreen animated MP4 background  
- 🎨 Custom chart backgrounds + user uploads  
- 📰 Real-time company news (Finnhub API required)  
- 🧠 Auto-refresh mode  
- 📱 Mobile-optimized layout  
- 💼 Company info with expandable cyberpunk styling  
- 🖥️ Compatible with Streamlit Cloud + Android APK builds  

---

## 🗂️ **Project Structure**
```
/app.py                           # Main Streamlit application
/cyberpunk_style_embedded.css     # Neon UI theme
/requirements.txt                 # Python dependencies
/videos/cyberpunk_light.mp4       # Background video (NEW)
```

You MUST include the `/videos/` folder exactly like this for Streamlit Cloud compatibility.

---

## 🔑 **API Keys (Finnhub)**
To enable news features:

1. Get your free API key from https://finnhub.io  
2. Enter it in the sidebar under **🔑 API Keys**

---

## 🛠️ **Installation**
Clone the repository:

```
git clone https://github.com/<your-username>/<your-repo>.git
cd <your-repo>
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the app:

```
streamlit run app.py
```

---

## 🌐 **Deployment on Streamlit Cloud**
1. Push your repo to GitHub  
2. Ensure this path exists:

```
/videos/cyberpunk_light.mp4
```

3. Deploy via https://share.streamlit.io  
4. Video will autoplay as fullscreen background

---

## 📦 **Android APK Support**
If you build your Streamlit app into an APK:

- The video still works offline  
- No base64 needed  
- No external URLs  
- Lightweight MP4 recommended (1–3 MB)

---

## ✨ **Customization Tips**
Want to use a different background video?

Just replace:

```
videos/cyberpunk_light.mp4
```

with your own file (same name recommended).

To adjust brightness:

```css
opacity: 0.25;
```

Change it inside the embedded HTML block.

---

## 🖤 **Credits**
Built with:

- Streamlit  
- yFinance  
- mplcyberpunk  
- Plotly  
- Pillow  
- Finnhub API  

Cyberpunk theme handcrafted by Wizard Q & Dev.  
🔥 Stay neon.
