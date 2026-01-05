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

# --- カスタムCSS（デザイン一新） ---
st.markdown("""
    <style>
    .stApp { background-color: #0a0a0a; }
    .main .block-container { padding-top: 1rem; max-width: 600px; }
    
    /* 共通の数値スタイル（ここを調整すれば一括で変わります） */
    .main-value {
        font-size: 2.5rem !important; 
        font-weight: 800;
        font-family: 'Courier New', Courier, monospace;
        line-height: 1.2;
        margin: 5px 0;
    }
    
    .status-box {
        background: #151515;
        border: 1px solid #333;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .label-text {
        font-size: 0.75rem;
        color: #888;
        letter-spacing: 2px;
        text-transform: uppercase;
    }

    /* 各項目の色設定 */
    .color-temp { color: #00ffcc; text-shadow: 0 0 10px rgba(0,255,204,0.3); }
    .color-next { color: #ff3366; text-shadow: 0 0 10px rgba(255,51,102,0.3); }
    .color-elapsed { color: #ffffff; }

    /* スケジュール */
    .sched-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; margin-top: 15px; }
    .sched-item {
        background: #111;
        border: 1px solid #222;
        padding: 5px;
        border-radius: 5px;
        font-size: 0.7rem;
        color: #555;
        text-align: center;
    }
    .sched-active {
        border-color: #00ffcc;
        color: #00ffcc;
        background: #00ffcc11;
    }

    /* Streamlit標準要素の非表示・調整 */
    div[data-testid="stMetricValue"] > div { font-size: 2.5rem !important; }
    hr { border: 0; border-top: 1px solid #333; margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

# --- 状態管理 ---
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'running' not in st.session_state: st.session_state.running = False
if 'last_alert_min' not in st.session_state: st.session_state.last_alert_min = -1

# --- 操作エリア ---
sel_col, btn_col = st.columns([2, 1])
with sel_col:
    selected_name = st.selectbox("PROFILE", list(PROFILES.keys()), label_visibility="collapsed")
    temps = PROFILES[selected_name]
with btn_col:
    if not st.session_state.running:
        if st.button("▶ START", use_container_width=True, type="primary"):
            st.session_state.start_time = time.time()
            st.session_state.running = True
            st.session_state.last_alert_min = -1
            play_sound_js()
    else:
        if st.button("⏹ STOP", use_container_width=True):
            st.session_state.running = False

st.markdown("<hr>", unsafe_allow_html=True)

# --- メイン表示エリア ---
display_placeholder = st.empty()

def render(min_c, sec_c, is_running):
    target = temps[min_c] if min_c < len(temps) else temps[-1]
    next_in = 60 - sec_c
    prog = sec_c / 60.0

    with display_placeholder.container():
        # 上段：Target と Next In
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'''<div class="status-box">
                <div class="label-text">TARGET TEMP</div>
                <div class="main-value color-temp">{target}℃</div>
            </div>''', unsafe_allow_html=True)
        with c2:
            st.markdown(f'''<div class="status-box">
                <div class="label-text">NEXT MEASURE</div>
                <div class="main-value color-next">{next_in}s</div>
            </div>''', unsafe_allow_html=True)
        
        # 中段：プログレスバー
        st.progress(prog)
        
        # 中段：経過時間（ここも共通クラスを適用）
        st.markdown(f'''<div class="status-box" style="margin-top:10px;">
            <div class="label-text">ELAPSED TIME</div>
            <div class="main-value color-elapsed">{min_c:02d}:{sec_c:02d}</div>
        </div>''', unsafe_allow_html=True)

        # 下段：スケジュール
        sched_html = '<div class="sched-grid">'
        for i, t in enumerate(temps):
            active = "sched-active" if i == min_c and is_running else ""
            sched_html += f'<div class="sched-item {active}">{i}m<br>{t}℃</div>'
        sched_html += '</div>'
        st.markdown(sched_html, unsafe_allow_html=True)

# 実行制御
if st.session_state.running:
    while st.session_state.running:
        elapsed = int(time.time() - st.session_state.start_time)
        m, s = elapsed // 60, elapsed % 60
        
        if m > st.session_state.last_alert_min:
            play_sound_js()
            st.session_state.last_alert_min = m
            
        render(m, s, True)
        time.sleep(0.5)
        if m >= len(temps): break
else:
    render(0, 0, False)
