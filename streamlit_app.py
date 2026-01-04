import streamlit as st
import time

# --- プロファイル設定 ---
PROFILES = {
    "フルシティロースト": [180, 75, 95, 110, 125, 140, 155, 170, 185, 195, 205, 210, 220, 225],
    "シティーロースト": [180, 75, 95, 115, 130, 145, 160, 175, 190, 200, 210, 215],
    "浅煎り": [180, 75, 100, 120, 140, 155, 170, 185, 195, 200]
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
            st.session_state.start_time = None
            st.session_state.running = False

# --- メインコックピット表示 ---
placeholder = st.empty()

while st.session_state.running:
    elapsed = int(time.time() - st.session_state.start_time)
    min_curr = elapsed // 60
    sec_curr = elapsed % 60
    
    # 1分ごとのアラート
    if min_curr > st.session_state.last_alert_min:
        play_sound_js()
        st.session_state.last_alert_min = min_curr

    curr_target = temps[min_curr] if min_curr < len(temps) else temps[-1]
    countdown = 60 - sec_curr

    with placeholder.container():
        # メインの数字エリア
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="status-box"><p class="label">次計測で狙う温度</p><p class="value-temp">{curr_target}℃</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="status-box"><p class="label">計測まであと</p><p class="value-count">{countdown}s</p></div>', unsafe_allow_html=True)
        
        st.markdown(f"**🕒 経過時間: {min_curr:02d}:{sec_curr:02d}**")
        
        # スケジュールを2列で表示（1画面に収めるため）
        st.write("---")
        col_list1, col_list2 = st.columns(2)
        for i, t in enumerate(temps):
            active_class = "sched-active" if i == min_curr else ""
            target_col = col_list1 if i < 7 else col_list2
            target_col.markdown(f'<div class="sched-item {active_class}">{i}min: {t}℃</div>', unsafe_allow_html=True)

    time.sleep(1)

if not st.session_state.running:
    st.write("準備ができたらSTARTを押してください。")
    # 停止中もスケジュールだけは見せる
    col_list1, col_list2 = st.columns(2)
    for i, t in enumerate(temps):
        target_col = col_list1 if i < 7 else col_list2
        target_col.markdown(f'<div class="sched-item">{i}min: {t}℃</div>', unsafe_allow_html=True)


