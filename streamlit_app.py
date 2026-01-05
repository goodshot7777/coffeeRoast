import streamlit as st
import time

# --- プロファイル設定 ---
PROFILES = {
    "フルシティ": [180, 75, 95, 110, 125, 140, 155, 170, 185, 195, 205, 210, 220, 225],
    "シティー": [180, 75, 95, 115, 130, 145, 160, 175, 190, 200, 210, 215],
    "浅煎り": [180, 75, 100, 120, 140, 155, 170, 185, 195, 200],
    "グアテマラ": [210, 75, 122, 127, 138, 145, 147, 159, 164, 168, 173, 173, 185, 187, 187, 195, 196, 207]
}

def play_sound_js():
    st.components.v1.html(
        """<script>var audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');audio.play();</script>""",
        height=0,
    )

st.set_page_config(page_title="Roast Cockpit", layout="centered")

# --- スマホ・一画面完結型CSS ---
st.markdown("""
    <style>
    /* 全体背景と余白の除去 */
    .stApp { background-color: #000000; }
    .main .block-container { padding: 0.2rem 0.5rem; }
    header { visibility: hidden; }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    
    /* 数値エリアのスタイリング */
    .display-unit { text-align: center; margin-bottom: -10px; }
    .label-text { font-size: 1rem; color: #ffffff; font-weight: bold; margin-bottom: -5px; }
    
    /* ターゲット温度：蛍光イエローで最大化 */
    .val-temp { 
        font-size: 28vw; /* 画面幅に対して最大化 */
        color: #ffff00; 
        font-weight: 900; 
        line-height: 1;
        text-shadow: 0 0 15px rgba(255, 255, 0, 0.4);
    }
    
    /* カウントダウン：オレンジで最大化 */
    .val-count { 
        font-size: 24vw; 
        color: #ff6600; 
        font-weight: 900; 
        line-height: 0.9;
        text-shadow: 0 0 15px rgba(255, 102, 0, 0.4);
    }

    /* 下部スケジュール一覧の視認性向上 */
    .mini-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 3px; margin-top: 5px; }
    .mini-item {
        font-size: 0.7rem; background: #333333; color: #ffffff; /* グレー背景に白文字で視認性UP */
        padding: 4px 0; border-radius: 4px; text-align: center;
    }
    .mini-active { 
        background: #ffffff; color: #000000; font-weight: 900; 
        box-shadow: 0 0 10px #ffffff;
    }
    
    /* セレクトボックスとボタンの調整 */
    .stSelectbox div { font-size: 1rem !important; }
    </style>
""", unsafe_allow_html=True)
