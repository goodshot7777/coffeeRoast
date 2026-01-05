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

# ページ設定：マージンを最小化
st.set_page_config(page_title="Roast Timer", layout="centered")

st.markdown("""
    <style>
    /* 全体の余白削除 */
    .main .block-container { padding: 0.5rem 1rem !important; }
    header { visibility: hidden; }
    [data-testid="stHeader"] { display: none; }
    
    /* 巨大テキストの設定 */
    .timer-card {
        text-align: center;
        background: #000;
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
        border: 2px solid #333;
    }
    .label { font-size: 1.2rem; color: #aaa; margin-bottom: 0; }
    
    /* カウントダウン（秒）を最大に */
    .countdown-value {
        font-size: 25vw; /* 画面幅の25% */
        font-weight: 900;
        color: #ff3366;
        line-height: 1;
        font-family: 'Courier New', monospace;
    }
    
    /* 経過時間を次に大きく */
    .elapsed-value {
        font-size: 15vw;
        font-weight: 700;
        color: #ffffff;
        line-height: 1;
    }

    /* ターゲット温度 */
    .temp-value {
        font-size: 12vw;
        font-weight: 700;
        color: #00ffcc;
    }

    /* プロファイルグリッドをさらに凝縮 */
    .mini-grid { 
        display: grid; 
        grid-template-columns: repeat(6, 1fr); 
        gap: 2px; 
        margin-top: 5px; 
    }
    .mini-item {
        font-size: 0.6rem; 
        background: #111; 
        color: #555;
        padding: 2px; 
        border-radius: 2px; 
        text-align: center;
    }
    .mini-active { 
        background: #00ffcc; 
        color: #000; 
        font-weight: bold; 
    }
    
    /* ボタンの高さ調整 */
    div.stButton > button { 
        height: 4rem !important; 
        font-size: 1.5rem !important; 
        font-weight: bold !important;
    }
    </style>
""", unsafe_allow_html=True)

if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'running' not in st.session_state: st.session_state.running = False
if 'last_alert_min' not in st.session_state: st.session_state.last_alert_min = -1

# --- レイアウト ---
# 1. 選択と操作
c1, c2 = st.columns([2, 1])
with c1:
    selected_name = st.selectbox("P", list(PROFILES.keys()), label_visibility="collapsed")
    temps = PROFILES[selected_name]
with c2:
    if not st.session_state.running:
        if st.button("GO", use_container_width=True, type="primary"):
            st.session_state.start_time = time.time()
            st.session_state.running = True
            st.rerun()
    else:
        if st.button("STOP", use_container_width=True):
            st.session_state.running = False
            st.session_state.start_time = None
            st.rerun()

# 2. メイン表示エリア
placeholder = st.empty()

def render_ui(elapsed_sec, running):
    min_curr = elapsed_sec // 60
    sec_curr = elapsed_sec % 60
    countdown = 60 - sec_curr
    curr_target = temps[min_curr] if min_curr < len(temps) else temps[-1]

    with placeholder.container():
        # カウントダウン（あと何秒で次の温度か）
        st.markdown(f'''
            <div class="timer-card">
                <p class="label">NEXT STEP</p>
                <p class="countdown-value">{countdown}s</p>
            </div>
        ''', unsafe_allow_html=True)

        # 経過時間とターゲット温度の並び
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown(f'''
                <div class="timer-card">
                    <p class="label">ELAPSED</p>
                    <p class="elapsed-value">{min_curr:02d}:{sec_curr:02d}</p>
                </div>
            ''', unsafe_allow_html=True)
        with col_b:
            st.markdown(f'''
                <div class="timer-card">
                    <p class="label">TARGET</p>
                    <p class="temp-value">{curr_target}°</p>
                </div>
            ''', unsafe_allow_html=True)

        # 進捗グリッド（さらに小型化）
        html_grid = '<div class="mini-grid">'
        for i, t in enumerate(temps):
            active = "mini-active" if i == min_curr and running else ""
            html_grid += f'<div class="mini-item {active}">{i}m<br>{t}</div>'
        html_grid += '</div>'
        st.markdown(html_grid, unsafe_allow_html=True)

# 実行制御
if st.session_state.running:
    while st.session_state.running:
        elapsed = int(time.time() - st.session_state.start_time)
        min_curr = elapsed // 60
        
        # 1分ごとのアラート
        if min_curr > st.session_state.last_alert_min:
            play_sound_js()
            st.session_state.last_alert_min = min_curr
        
        render_ui(elapsed, True)
        time.sleep(1)
        
        if min_curr >= len(temps):
            st.session_state.running = False
            st.rerun()
else:
    render_ui(0, False)
