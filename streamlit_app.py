import streamlit as st
import time

# --- プロファイル設定 ---
PROFILES = {
    "フルシティ (深口)": [180, 95, 110, 125, 140, 155, 170, 185, 195, 205, 210, 220, 225],
    "シティ (中深)": [180, 95, 115, 130, 145, 160, 175, 190, 200, 210, 215],
    "浅煎り": [180, 100, 120, 140, 155, 170, 185, 195, 200]
}

def play_sound_js():
    st.components.v1.html(
        """<script>var audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');audio.play();</script>""",
        height=0,
    )

st.set_page_config(page_title="Roast Cockpit", layout="wide")

# --- 1画面に収めるための専用CSS ---
st.markdown("""
    <style>
    /* 全体の余白を削る */
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    /* メトリックボックス */
    .status-box { background-color: #0e1117; border: 2px solid #333; border-radius: 10px; padding: 10px; text-align: center; }
    .label { font-size: 1.2rem; color: #888; margin-bottom: 0px; }
    .value-temp { font-size: 5.5rem; color: #00ff00; font-weight: bold; line-height: 1; }
    .value-count { font-size: 5.5rem; color: #ff4b4b; font-weight: bold; line-height: 1; }
    /* スケジュールリストをコンパクトに */
    .sched-item { font-size: 0.9rem; padding: 2px 10px; border-radius: 5px; margin: 2px 0; border-left: 3px solid #444; color: #888; }
    .sched-active { background-color: #1f1f00; border-left: 5px solid #ffff00; color: #fff; font-weight: bold; font-size: 1.1rem; }
    </style>
""", unsafe_allow_html=True)

# --- 状態管理 ---
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'running' not in st.session_state: st.session_state.running = False
if 'last_alert_min' not in st.session_state: st.session_state.last_alert_min = -1

# --- ヘッダー・設定エリア ---
col_head1, col_head2 = st.columns([2, 1])
with col_head1:
    selected_name = st.selectbox("Profile", list(PROFILES.keys()), label_visibility="collapsed")
    temps = PROFILES[selected_name]
with col_head2:
    if not st.session_state.running:
        if st.button("🚀 START", use_container_width=True):
            st.session_state.start_time = time.time()
            st.session_state.running = True
            play_sound_js()
    else:
        if st.button("⏹️ RESET", use_container_width=True):
            st.session_state.start_
