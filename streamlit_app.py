import streamlit as st
import time

# --- 1. 設定 & プロファイル ---
PROFILES = {
    "フルシティ": [180, 75, 95, 110, 125, 140, 155, 170, 185, 195, 205, 210, 220, 225],
    "シティー": [180, 75, 95, 115, 130, 145, 160, 175, 190, 200, 210, 215],
    "浅煎り": [180, 75, 100, 120, 140, 155, 170, 185, 195, 200],
    "グアテマラ": [210, 75, 122, 127, 138, 145, 147, 159, 164, 168, 173, 173, 185, 187, 187, 195, 196, 207]
}

def play_sound_js():
    # 音を鳴らすJavaScript
    st.components.v1.html(
        """<script>var audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');audio.play();</script>""",
        height=0,
    )

# --- 2. ページ構成 & UIデザイン (CSS) ---
st.set_page_config(page_title="Roast Timer", layout="centered")

st.markdown("""
    <style>
    /* 余白を徹底的に排除 */
    .main .block-container { padding: 0.5rem !important; }
    [data-testid="stHeader"] { display: none; }
    
    /* 視認性重視のカードデザイン */
    .timer-box {
        text-align: center;
        background: #000;
        border-radius: 12px;
        padding: 5px;
        margin-bottom: 5px;
        border: 1px solid #333;
    }
    .label { font-size: 0.9rem; color: #888; margin: 0; }
    
    /* 文字サイズ：vw（画面幅）を使ってスマホ全画面に対応 */
    .val-countdown { font-size: 28vw; font-weight: 900; color: #ff3366; line-height: 1; font-family: monospace; }
    .val-elapsed { font-size: 14vw; font-weight: 700; color: #fff; line-height: 1; }
    .val-temp { font-size: 14vw; font-weight: 700; color: #00ffcc; line-height: 1; }
    
    /* 進捗グリッド */
    .grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 2px; }
    .item { font-size: 0.6rem; background: #111; color: #444; padding: 2px; border-radius: 2px; text-align: center; }
    .active { background: #00ffcc; color: #000; font-weight: bold; }
    
    /* ボタンを押しやすく */
    div.stButton > button { height: 4rem !important; font-size: 1.5rem !important; width: 100%; }
    </style>
""", unsafe_allow_html=True)

# --- 3. セッション状態の管理 ---
if 'start_time' not in st.session_state: st.session_state.start_time = None
if 'running' not in st.session_state: st.session_state.running = False
if 'last_alert_min' not in st.session_state: st.session_state.last_alert_min = -1

# --- 4. 操作パネル ---
c1, c2 = st.columns([2, 1])
with c1:
    selected = st.selectbox("Select Profile", list(PROFILES.keys()), label_visibility="collapsed")
    temps = PROFILES[selected]
with c2:
    if not st.session_state.running:
        if st.button("START"):
            st.session_state.start_time = time.time()
            st.session_state.running = True
            st.session_state.last_alert_min = -1
            st.rerun()
    else:
        if st.button("RESET"):
            st.session_state.running = False
            st.rerun()

# --- 5. メイン表示関数 ---
def render_display(elapsed_sec):
    min_curr = elapsed_sec // 60
    sec_curr = elapsed_sec % 60
    countdown = 60 - sec_curr
    curr_target = temps[min_curr] if min_curr < len(temps) else temps[-1]
    
    # 巨大なカウントダウン
    st.markdown(f'<div class="timer-box"><p class="label">NEXT STEP</p><p class="val-countdown">{countdown:02d}</p></div>', unsafe_allow_html=True)
    
    # 経過時間とターゲット
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown(f'<div class="timer-box"><p class="label">ELAPSED</p><p class="val-elapsed">{min_curr:02d}:{sec_curr:02d}</p></div>', unsafe_allow_html=True)
    with col_r:
        st.markdown(f'<div class="timer-box"><p class="label">TARGET</p><p class="val-temp">{curr_target}°</p></div>', unsafe_allow_html=True)
    
    # 小型グリッド
    grid_html = '<div class="grid">'
    for i, t in enumerate(temps):
        status = "active" if i == min_curr and st.session_state.running else ""
        grid_html += f'<div class="item {status}">{i}m<br>{t}</div>'
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

# --- 6. 実行ループ ---
display_area = st.empty()

if st.session_state.running:
    while st.session_state.running:
        now = time.time()
        elapsed = int(now - st.session_state.start_time)
        min_curr = elapsed // 60
        
        # 1分ごとの音通知
        if min_curr > st.session_state.last_alert_min:
            play_sound_js()
            st.session_state.last_alert_min = min_curr
            
        with display_area.container():
            render_display(elapsed)
            
        if min_curr >= len(temps):
            st.session_state.running = False
            st.success("焙煎完了！")
            break
            
        time.sleep(0.5) # 更新頻度を上げてスムーズに
else:
    with display_area.container():
        render_display(0)
