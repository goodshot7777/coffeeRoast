import streamlit as st
import time

# --- プロファイル設定 ---
PROFILES = {
    "フルシティ (深煎り)": [180, 95, 110, 125, 140, 155, 170, 185, 195, 205, 210, 220, 225],
    "ハイ/シティ (中煎り)": [180, 95, 115, 130, 145, 160, 175, 190, 200, 210, 215],
    "シナモン (浅煎り)": [180, 100, 120, 140, 155, 170, 185, 195, 200]
}

def play_sound_js():
    st.components.v1.html(
        """<script>var audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');audio.play();</script>""",
        height=0,
    )

# 画面幅を最大限に使い、余計なメニューを隠す設定
st.set_page_config(page_title="Roaster", layout="centered")

st.markdown("""
    <style>
    /* ヘッダーと余白を削除 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding-top: 1rem; padding-bottom: 0rem;}
    
    /* メイン指標のボックス */
    .metric-box {
        background-color: #1e1e1e;
        border-radius: 10px;
        padding: 10px;
        text-align: center;
        margin-bottom: 5px;
    }
    .label { font-size: 14px; color: #aaa; margin-bottom: -10px; }
    .val-temp { color: #00ff00; font-size: 55px; font-weight: bold; }
    .val-time { color: #ff4b4b; font-size: 55px; font-weight: bold; }
    
    /* スケジュール表のコンパクト化 */
    .sched-grid {
        display: grid;
        grid-template-columns: 1fr 1fr; /* 2列表示 */
        gap: 4px;
        font-size: 13px;
    }
    .sched-item {
        padding: 4px 8px;
        background: #2b2b2b;
        border-radius: 4px;
        color: #ddd;
        border: 1px solid #444;
    }
    .active {
        background: #444400;
        border: 2px solid #ffff00;
        color: #fff;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- 状態管理 ---
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'running' not in st.session_state: st.session_state.running = False
if 'last_alert_min' not in st.session_state: st.session_state.last_alert_min = -1

# プロファイル選択をサイドバーではなくメイン上部にコンパクトに配置
selected_name = st.selectbox("", list(PROFILES.keys()), label_visibility="collapsed")
temps = PROFILES[selected_name]

# 操作ボタン
c1, c2 = st.columns(2)
with c1:
    if st.button("🚀 START", use_container_width=True):
        st.session_state.start_time = time.time()
        st.session_state.running = True
        st.session_state.last_alert_min = -1
        play_sound_js()
with c2:
    if st.button("⏹️ RESET", use_container_width=True):
        st.session_state.start_time = None
        st.session_state.running = False

# --- メイン表示エリア ---
display_slot = st.empty()

while st.session_state.running:
    elapsed_sec = int(time.time() - st.session_state.start_time)
    mins, secs = divmod(elapsed_sec, 60)
    
    if mins > st.session_state.last_alert_min:
        play_sound_js()
        st.session_state.last_alert_min = mins

    target_t = temps[mins] if mins < len(temps) else temps[-1]
    countdown = 60 - secs

    with display_slot.container():
        # 上段：メインメトリクス
        m1, m2 = st.columns(2)
        with m1:
            st.markdown(f'<div class="metric-box"><p class="label">目標温度</p><span class="val-temp">{target_t}℃</span></div>', unsafe_allow_html=True)
        with m2:
            st.markdown(f'<div class="metric-box"><p class="label">次まで</p><span class="val-time">{countdown}s</span></div>', unsafe_allow_html=True)
        
        st.write(f"⏱ **経過時間: {mins:02d}:{secs:02d}**")

        # 下段：スケジュール（2列グリッド）
        st.markdown('<div class="sched-grid">', unsafe_allow_html=True)
        html_sched = ""
        for i, t in enumerate(temps):
            active_class = "active" if i == mins else ""
