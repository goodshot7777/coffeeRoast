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

# スマホ向けに余白を極限までカット
st.set_page_config(page_title="Roast Cockpit", layout="centered")

st.markdown("""
    <style>
    /* スマホ画面の上下余白をゼロにする */
    .main .block-container { padding: 0.5rem 1rem; }
    header { visibility: hidden; }
    
    /* 巨大な数値表示 */
    .hero-container { text-align: center; margin: 0.5rem 0; }
    .hero-label { font-size: 0.8rem; color: #888; margin-bottom: -10px; }
    .hero-value-temp { font-size: 6.5rem; color: #00ffcc; font-weight: 900; line-height: 1; }
    .hero-value-count { font-size: 5.5rem; color: #ff3366; font-weight: 900; line-height: 1; }
    
    /* スケジュールの超コンパクト表示 */
    .mini-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 4px; margin-top: 10px; }
    .mini-item {
        font-size: 0.65rem; background: #1a1a1a; color: #444;
        padding: 2px; border-radius: 4px; text-align: center; border: 1px solid #222;
    }
    .mini-active { background: #00ffcc; color: #000; font-weight: bold; border-color: #fff; }
    
    /* ボタンを少し小さく */
    div.stButton > button { height: 3rem; font-size: 1.2rem !important; }
    </style>
""", unsafe_allow_html=True)

if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'running' not in st.session_state: st.session_state.running = False
if 'last_alert_min' not in st.session_state: st.session_state.last_alert_min = -1

# --- 操作エリア（1行に凝縮） ---
c_nav1, c_nav2 = st.columns([3, 2])
with c_nav1:
    selected_name = st.selectbox("P", list(PROFILES.keys()), label_visibility="collapsed")
    temps = PROFILES[selected_name]
with c_nav2:
    if not st.session_state.running:
        if st.button("START", use_container_width=True, type="primary"):
            st.session_state.start_time = time.time()
            st.session_state.running = True
    else:
        if st.button("RESET", use_container_width=True):
            st.session_state.running = False
            st.session_state.start_time = None

# --- メインディスプレイ ---
placeholder = st.empty()

def render_mobile(min_curr, sec_curr, running):
    curr_target = temps[min_curr] if min_curr < len(temps) else temps[-1]
    countdown = 60 - sec_curr
    
    with placeholder.container():
        # メインターゲット温度
        st.markdown(f'''
            <div class="hero-container">
                <p class="hero-label">TARGET TEMP</p>
                <p class="hero-value-temp">{curr_target}°</p>
            </div>
        ''', unsafe_allow_html=True)
        
        # カウントダウン
        st.markdown(f'''
            <div class="hero-container">
                <p class="hero-label">COUNTDOWN</p>
                <p class="hero-value-count">{countdown}s</p>
            </div>
        ''', unsafe_allow_html=True)
        
        # 経過時間
        st.markdown(f"<p style='text-align: center; color: #fff; margin:0;'>ELAPSED: {min_curr:02d}:{sec_curr:02d}</p>", unsafe_allow_html=True)
        
        # コンパクトな進捗管理（5列のミニチップ）
        html_grid = '<div class="mini-grid">'
        for i, t in enumerate(temps):
            active_class = "mini-active" if i == min_curr and running else ""
            html_grid += f'<div class="mini-item {active_class}">{i}m<br>{t}</div>'
        html_grid += '</div>'
        st.markdown(html_grid, unsafe_allow_html=True)

if st.session_state.running:
    while st.session_state.running:
        elapsed = int(time.time() - st.session_state.start_time)
        min_curr = elapsed // 60
        sec_curr = elapsed % 60
        if min_curr > st.session_state.last_alert_min:
            play_sound_js()
            st.session_state.last_alert_min = min_curr
        render_mobile(min_curr, sec_curr, True)
        time.sleep(1)
        if min_curr >= len(temps): break
else:
    render_mobile(0, 0, False)
