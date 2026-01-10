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

st.set_page_config(page_title="ROAST TIMER", layout="wide")

# --- 高コントラストCSSデザイン ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .main .block-container { padding-top: 1rem; max-width: 600px; }
    
    .main-value {
        font-size: 2.5rem !important; 
        font-weight: 900;
        font-family: 'Arial Black', sans-serif;
        line-height: 1.2;
        margin: 5px 0;
    }
    
    .status-box {
        background: #111111;
        border: 2px solid #ffffff;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        margin-bottom: 10px;
    }
    
    .label-text {
        font-size: 0.8rem;
        color: #ffffff;
        font-weight: bold;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .color-temp { color: #00ffcc; }
    .color-next { color: #ff3366; }
    .color-elapsed { color: #ffffff; }

    .sched-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-top: 20px; }
    
    .sched-item {
        background: #000000;
        border: 2px solid #ffffff;
        padding: 8px 5px;
        border-radius: 8px;
        font-size: 0.85rem;
        color: #ffffff;
        text-align: center;
        font-weight: 800;
    }
    
    .sched-active {
        background: #ffff00 !important;
        border-color: #ffff00 !important;
        color: #000000 !important;
        box-shadow: 0 0 15px #ffff00;
    }

    hr { border: 0; border-top: 2px solid #ffffff; margin: 20px 0; }
    </style>
""", unsafe_allow_html=True)

# --- 状態管理の初期化 ---
if 'running' not in st.session_state: st.session_state.running = False
if 'paused' not in st.session_state: st.session_state.paused = False
if 'total_elapsed' not in st.session_state: st.session_state.total_elapsed = 0.0
if 'last_tick' not in st.session_state: st.session_state.last_tick = 0.0
if 'last_alert_min' not in st.session_state: st.session_state.last_alert_min = -1

# --- 操作エリア ---
sel_col, btn_col = st.columns([1.5, 1.5])

with sel_col:
    selected_name = st.selectbox("PROFILE", list(PROFILES.keys()), label_visibility="collapsed")
    temps = PROFILES[selected_name]

with btn_col:
    if not st.session_state.running:
        if st.button("▶ START", use_container_width=True, type="primary"):
            st.session_state.running = True
            st.session_state.paused = False
            st.session_state.total_elapsed = 0.0
            st.session_state.last_tick = time.time()
            st.session_state.last_alert_min = -1
            play_sound_js()
            st.rerun()
    else:
        c_p, c_s = st.columns(2)
        with c_p:
            if not st.session_state.paused:
                if st.button("Ⅱ PAUSE", use_container_width=True):
                    st.session_state.paused = True
                    st.rerun()
            else:
                if st.button("▶ RESUME", use_container_width=True):
                    st.session_state.paused = False
                    st.session_state.last_tick = time.time()
                    st.rerun()
        with c_s:
            if st.button("⏹ STOP", use_container_width=True):
                st.session_state.running = False
                st.session_state.paused = False
                st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# --- メイン表示エリア ---
display_placeholder = st.empty()

# 引数を (経過秒数, 実行フラグ) の2つに統一
def render(total_sec, is_running):
    m_c = int(total_sec // 60)
    s_c = int(total_sec % 60)
    target = temps[m_c] if m_c < len(temps) else temps[-1]
    next_in = 60 - s_c
    prog = s_c / 60.0

    with display_placeholder.container():
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
        
        st.progress(prog)
        
        st.markdown(f'''<div class="status-box" style="margin-top:10px;">
            <div class="label-text">ELAPSED TIME</div>
            <div class="main-value color-elapsed">{m_c:02d}:{s_c:02d}</div>
        </div>''', unsafe_allow_html=True)

        sched_html = '<div class="sched-grid">'
        for i, t in enumerate(temps):
            active_class = "sched-active" if i == m_c and is_running else ""
            sched_html += f'<div class="sched-item {active_class}">{i}m<br>{t}℃</div>'
        sched_html += '</div>'
        st.markdown(sched_html, unsafe_allow_html=True)

# --- 実行ループ ---
if st.session_state.running:
    while st.session_state.running:
        if not st.session_state.paused:
            now = time.time()
            st.session_state.total_elapsed += now - st.session_state.last_tick
            st.session_state.last_tick = now
            
            m_now = int(st.session_state.total_elapsed // 60)
            if m_now > st.session_state.last_alert_min:
                play_sound_js()
                st.session_state.last_alert_min = m_now
        
        # 正しい引数(2つ)で呼び出し
        render(st.session_state.total_elapsed, st.session_state.running)
        
        if int(st.session_state.total_elapsed // 60) >= len(temps):
            st.session_state.running = False
            break
            
        time.sleep(0.2)
else:
    # ここがエラーの原因でした：render(0, 0, False) から 修正
    render(0.0, False)

