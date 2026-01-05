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

# --- 高コントラストCSSデザイン ---
st.markdown("""
    <style>
    .stApp { background-color: #000000; }
    .main .block-container { padding-top: 1rem; max-width: 600px; }
    
    /* 共通数値スタイル（サイズ統一） */
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

    /* 各項目の色（高コントラスト設定） */
    .color-temp { color: #00ffcc; } /* ターゲット温度：明るいシアン */
    .color-next { color: #ff3366; } /* 次の計測：明るいピンク */
    .color-elapsed { color: #ffffff; } /* 経過時間：白 */

    /* スケジュールグリッド（ここを重点的に修正） */
    .sched-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; margin-top: 20px; }
    
    /* 非アクティブ状態：黒背景に白文字・白枠 */
    .sched-item {
        background: #000000;
        border: 2px solid #ffffff;
        padding: 8px 5px;
        border-radius: 8px;
        font-size: 0.85rem;
        color: #ffffff; /* 純粋な白に変更 */
        text-align: center;
        font-weight: 800;
    }
    
    /* アクティブ状態：黄背景に黒文字（最高コントラスト） */
    .sched-active {
        background: #ffff00 !important;
        border-color: #ffff00 !important;
        color: #000000 !important;
        box-shadow: 0 0 15px #ffff00;
    }

    hr { border: 0; border-top: 2px solid #ffffff; margin: 20px 0; }
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
        # 上段
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
        
        # 中段
        st.markdown(f'''<div class="status-box" style="margin-top:10px; border-color: #ffffff;">
            <div class="label-text">ELAPSED TIME</div>
            <div class="main-value color-elapsed">{min_c:02d}:{sec_c:02d}</div>
        </div>''', unsafe_allow_html=True)

        # 下段：スケジュール（高コントラスト版）
        sched_html = '<div class="sched-grid">'
        for i, t in enumerate(temps):
            active_class = "sched-active" if i == min_c and is_running else ""
            sched_html += f'<div class="sched-item {active_class}">{i}m<br>{t}℃</div>'
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
