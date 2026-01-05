import streamlit as st
import time

# --- プロファイル設定 ---
PROFILES = {
    "フルシティロースト": [180, 75, 95, 110, 125, 140, 155, 170, 185, 195, 205, 210, 220, 225],
    "シティーロースト": [180, 75, 95, 115, 130, 145, 160, 175, 190, 200, 210, 215],
    "浅煎り": [180, 75, 100, 120, 140, 155, 170, 185, 195, 200],
    "グアテマラSHB": [210, 75, 122, 127, 138, 145, 147, 159, 164, 168, 173, 173, 185, 187, 187, 195, 196, 207]
}

def play_sound_js():
    st.components.v1.html(
        """<script>var audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');audio.play();</script>""",
        height=0,
    )

st.set_page_config(page_title="Roast Cockpit Neo", layout="wide")

# --- スタイリッシュなCSSデザイン ---
st.markdown("""
    <style>
    /* 背景と全体の調整 */
    .stApp { background-color: #050505; }
    .main .block-container { padding-top: 2rem; }
    
    /* ステータスカード */
    .status-card {
        background: linear-gradient(145deg, #1a1a1a, #0d0d0d);
        border: 1px solid #333;
        border-radius: 15px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    .label { font-size: 0.9rem; color: #aaa; text-transform: uppercase; letter-spacing: 1px; }
    .value-temp { font-size: 5rem; color: #00ffcc; font-weight: 800; text-shadow: 0 0 20px rgba(0,255,204,0.5); line-height: 1.1; }
    .value-count { font-size: 5rem; color: #ff3366; font-weight: 800; text-shadow: 0 0 20px rgba(255,51,102,0.5); line-height: 1.1; }
    
    /* スケジュールアイテム */
    .sched-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); gap: 8px; margin-top: 20px; }
    .sched-item {
        background: #151515;
        border: 1px solid #222;
        padding: 8px;
        border-radius: 8px;
        font-family: monospace;
        color: #666;
        text-align: center;
    }
    .sched-active {
        background: #00ffcc22;
        border: 1px solid #00ffcc;
        color: #00ffcc;
        font-weight: bold;
        box-shadow: 0 0 10px rgba(0,255,204,0.3);
    }
    
    /* 水平線のカスタム */
    hr { border: 0; height: 1px; background: #333; margin: 2rem 0; }
    </style>
""", unsafe_allow_html=True)

# --- 状態管理 ---
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'running' not in st.session_state: st.session_state.running = False
if 'last_alert_min' not in st.session_state: st.session_state.last_alert_min = -1

# --- ヘッダー・設定エリア ---
col_h1, col_h2, col_h3 = st.columns([2, 1, 1])
with col_h1:
    selected_name = st.selectbox("SELECT PROFILE", list(PROFILES.keys()), label_visibility="collapsed")
    temps = PROFILES[selected_name]
with col_h2:
    if not st.session_state.running:
        if st.button("▶ START ROASTING", use_container_width=True, type="primary"):
            st.session_state.start_time = time.time()
            st.session_state.running = True
            st.session_state.last_alert_min = -1
            play_sound_js()
    else:
        if st.button("⏹ STOP / RESET", use_container_width=True):
            st.session_state.running = False
            st.session_state.start_time = None

# --- メインディスプレイ ---
placeholder = st.empty()

def render_display(min_curr, sec_curr, running):
    curr_target = temps[min_curr] if min_curr < len(temps) else temps[-1]
    countdown = 60 - sec_curr
    progress = sec_curr / 60.0

    with placeholder.container():
        # メイン数値
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="status-card"><p class="label">Target Temperature</p><p class="value-temp">{curr_target}℃</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="status-card"><p class="label">Next Measure In</p><p class="value-count">{countdown}s</p></div>', unsafe_allow_html=True)
        
        # プログレスバー（視覚的な経過）
        st.write("")
        st.progress(progress)
        
        # 経過時間表示
        st.markdown(f"<h2 style='text-align: center; color: #fff;'>ELAPSED: {min_curr:02d}:{sec_curr:02d}</h2>", unsafe_allow_html=True)
        
        st.markdown("<hr>", unsafe_allow_html=True)
        
        # スケジュールグリッド
        sched_html = '<div class="sched-grid">'
        for i, t in enumerate(temps):
            active_class = "sched-active" if i == min_curr and running else ""
            sched_html += f'<div class="sched-item {active_class}">{i}m<br>{t}℃</div>'
        sched_html += '</div>'
        st.markdown(sched_html, unsafe_allow_html=True)

# 実行中のループ
if st.session_state.running:
    while st.session_state.running:
        elapsed = int(time.time() - st.session_state.start_time)
        min_curr = elapsed // 60
        sec_curr = elapsed % 60
        
        if min_curr > st.session_state.last_alert_min:
            play_sound_js()
            st.session_state.last_alert_min = min_curr
            
        render_display(min_curr, sec_curr, True)
        time.sleep(0.5) # 更新頻度を少し上げてスムーズに
        if min_curr >= len(temps): break
else:
    # 停止中の表示
    render_display(0, 0, False)
