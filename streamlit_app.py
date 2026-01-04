import streamlit as st
import time

# --- プロファイル設定 ---
PROFILES = {
    "フルシティ (深煎り)": [180, 95, 110, 125, 140, 155, 170, 185, 195, 205, 210, 220, 225],
    "ハイ/シティ (中煎り)": [180, 95, 115, 130, 145, 160, 175, 190, 200, 210, 215],
    "シナモン (浅煎り)": [180, 100, 120, 140, 155, 170, 185, 195, 200]
}

# --- 音を鳴らすためのJavaScript ---
# ブラウザの制限を回避するため、この関数を呼び出すことで音を鳴らします
def play_sound_js():
    st.components.v1.html(
        """
        <script>
        var audio = new Audio('https://actions.google.com/sounds/v1/alarms/beep_short.ogg');
        audio.play();
        </script>
        """,
        height=0,
    )

st.set_page_config(page_title="Roast Master Pro", layout="centered")

# --- カスタムCSS ---
st.markdown("""
    <style>
    .metric-container { background-color: #1e1e1e; padding: 20px; border-radius: 15px; color: #ffffff; text-align: center; margin-bottom: 10px; }
    .target-temp { color: #00ff00; font-size: 70px !important; font-weight: bold; }
    .countdown { color: #ff4b4b; font-size: 70px !important; font-weight: bold; }
    .active-row { background-color: #333300; border: 2px solid #ffff00; border-radius: 8px; font-weight: bold; padding: 10px; }
    .schedule-row { padding: 8px; border-bottom: 1px solid #444; color: #ccc; }
    </style>
""", unsafe_allow_html=True)

st.title("🔥 Roast Assistant")

# --- サイドバー設定 ---
selected_name = st.sidebar.selectbox("プロファイル切替", list(PROFILES.keys()))
temps = PROFILES[selected_name]

# --- 状態管理 ---
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'running' not in st.session_state:
    st.session_state.running = False
if 'last_alert_min' not in st.session_state:
    st.session_state.last_alert_min = -1

# --- 操作ボタン ---
# スマホで音を出すために、何らかのボタンを最低1回押す必要があります
st.info("⚠️ スマホの場合、開始ボタンを押すことで音が許可されます。")

c1, c2 = st.columns(2)
with c1:
    if st.button("🚀 焙煎開始 (音を許可)", use_container_width=True):
        st.session_state.start_time = time.time()
        st.session_state.running = True
        st.session_state.last_alert_min = -1
        play_sound_js() # 開始時に一度鳴らしてブラウザの許可を取る
with c2:
    if st.button("⏹️ リセット", use_container_width=True):
        st.session_state.start_time = None
        st.session_state.running = False

# --- メイン表示エリア ---
main_display = st.empty()
schedule_display = st.empty()

while st.session_state.running:
    elapsed_sec = int(time.time() - st.session_state.start_time)
    minutes = elapsed_sec // 60
    seconds = elapsed_sec % 60
    
    # 1分ごとに音を鳴らすロジック
    if minutes > st.session_state.last_alert_min:
        play_sound_js()
        st.session_state.last_alert_min = minutes

    # 表示用データ
    countdown_sec = 60 - seconds
    curr_target = temps[minutes] if minutes < len(temps) else temps[-1]
    
    with main_display.container():
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown(f'<div class="metric-container">予定温度<br><span class="target-temp">{curr_target}℃</span></div>', unsafe_allow_html=True)
        with col_r:
            st.markdown(f'<div class="metric-container">次まであと<br><span class="countdown">{countdown_sec}s</span></div>', unsafe_allow_html=True)
        st.write(f"⏱ **経過時間: {minutes:02d}:{seconds:02d}**")

    with schedule_display.container():
        st.write("---")
        st.subheader("全体スケジュール")
        for i, t in enumerate(temps):
            active_class = "active-row" if i == minutes else ""
            mark = " 👈 今ここ" if i == minutes else ""
            st.markdown(f'<div class="schedule-row {active_class}">{i}分目： {t} ℃{mark}</div>', unsafe_allow_html=True)

    time.sleep(1)
