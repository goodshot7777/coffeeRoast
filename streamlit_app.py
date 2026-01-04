import streamlit as st
import time

# --- 焙煎プロファイルの設定 ---
PROFILES = {
    "フルシティ (深煎り)": [180, 95, 110, 125, 140, 155, 170, 185, 195, 205, 210, 220, 225],
    "ハイ/シティ (中煎り)": [180, 95, 115, 130, 145, 160, 175, 190, 200, 210, 215],
    "シナモン (浅煎り)": [180, 100, 120, 140, 155, 170, 185, 195, 200]
}

st.set_page_config(page_title="Roast Master Pro", layout="centered")

# --- カスタムCSSで見た目を強化 ---
st.markdown("""
    <style>
    .metric-container {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 15px;
        color: #ffffff;
        text-align: center;
        margin-bottom: 10px;
    }
    .target-temp { color: #00ff00; font-size: 80px !important; font-weight: bold; }
    .countdown { color: #ff4b4b; font-size: 80px !important; font-weight: bold; }
    .schedule-row { font-size: 18px; padding: 5px; border-bottom: 1px solid #444; }
    .active-row { background-color: #333300; border: 2px solid #ffff00; border-radius: 8px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- サイドバー設定 ---
selected_name = st.sidebar.selectbox("プロファイル切替", list(PROFILES.keys()))
temps = PROFILES[selected_name]

st.title("🔥 Roast Assistant")

# --- 状態管理 ---
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'running' not in st.session_state:
    st.session_state.running = False

# --- 操作ボタン ---
c1, c2 = st.columns(2)
with c1:
    if st.button("🚀 焙煎開始 (投入)", use_container_width=True):
        st.session_state.start_time = time.time()
        st.session_state.running = True
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
    
    # 1分ごとのカウントダウン
    countdown_sec = 60 - seconds
    # 今の目標温度
    curr_target = temps[minutes] if minutes < len(temps) else temps[-1]
    
    with main_display.container():
        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown(f'<div class="metric-container">予定温度<br><span class="target-temp">{curr_target}℃</span></div>', unsafe_allow_html=True)
        with col_right:
            # 計測直前（10秒前）になったら色を変えるなどの演出も可能
            st.markdown(f'<div class="metric-container">次まであと<br><span class="countdown">{countdown_sec}s</span></div>', unsafe_allow_html=True)
        
        st.write(f"**経過時間: {minutes:02d}:{seconds:02d}**")

    # --- 予定温度の全体表示 (リスト形式) ---
    with schedule_display.container():
        st.write("---")
        st.subheader("全体スケジュール")
        for i, t in enumerate(temps):
            active_class = "active-row" if i == minutes else ""
            st.markdown(f'<div class="schedule-row {active_class}">{i}分目： {t} ℃ {" ← 今ココ" if i == minutes else ""}</div>', unsafe_allow_html=True)

    if minutes >= len(temps) + 2: # 予定時間を大幅に過ぎたら停止
        st.session_state.running = False

    time.sleep(1)
