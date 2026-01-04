import streamlit as st
import time
import base64

# --- 焙煎プロファイルの設定 ---
PROFILES = {
    "フルシティ (深煎り)": {
        "temps": [180, 95, 110, 125, 140, 155, 170, 185, 195, 205, 210, 220, 225],
        "desc": "2爆ぜ開始直後で煎り止め。力強い苦味とコク。"
    },
    "ハイ/シティ (中煎り)": {
        "temps": [180, 95, 115, 130, 145, 160, 175, 190, 200, 210, 215],
        "desc": "1爆ぜ終了〜2爆ぜ前。酸味と苦味のバランス重視。"
    },
    "シナモン (浅煎り)": {
        "temps": [180, 100, 120, 140, 155, 170, 185, 195, 200],
        "desc": "1爆ぜのピーク付近で煎り止め。爽やかな酸味。"
    }
}

# --- アラート音の生成 (ブラウザで再生するためのHTML) ---
def play_sound():
    # 短い「ピッ」という電子音のBase64（ダミーデータではなく簡易的なもの）
    audio_html = """
        <audio autoplay>
            <source src="https://the-q.p-e-w.net/mp3/pishi.mp3" type="audio/mp3">
        </audio>
    """
    st.components.v1.html(audio_html, height=0)

st.set_page_config(page_title="Roast Master Pro", layout="centered")

# --- サイドバー設定 ---
st.sidebar.header("📋 プロファイル選択")
selected_profile_name = st.sidebar.selectbox("狙いの煎り加減", list(PROFILES.keys()))
profile_data = PROFILES[selected_profile_name]
st.sidebar.info(profile_data["desc"])

st.title("🔥 鍋焙煎アシスタント")

# --- 状態管理 ---
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'running' not in st.session_state:
    st.session_state.running = False
if 'last_alert_min' not in st.session_state:
    st.session_state.last_alert_min = -1

# --- 操作ボタン ---
col1, col2 = st.columns(2)
with col1:
    if st.button("🚀 焙煎開始 (投入)", use_container_width=True):
        st.session_state.start_time = time.time()
        st.session_state.running = True
        st.session_state.last_alert_min = -1
with col2:
    if st.button("⏹️ リセット", use_container_width=True):
        st.session_state.start_time = None
        st.session_state.running = False

# --- メイン表示エリア ---
display_area = st.empty()

while st.session_state.running:
    elapsed_sec = int(time.time() - st.session_state.start_time)
    minutes = elapsed_sec // 60
    seconds = elapsed_sec % 60
    
    # 1分ごとにアラートを鳴らす
    if minutes > st.session_state.last_alert_min:
        play_sound()
        st.session_state.last_alert_min = minutes

    # 目標温度の取得
    temps = profile_data["temps"]
    target_temp = temps[minutes] if minutes < len(temps) else temps[-1]
    
    # 次の1分までの残り秒数
    next_check_in = 60 - seconds

    with display_area.container():
        # タイマー表示
        st.markdown(f"""
        <div style="text-align: center; background-color: #f0f2f6; padding: 20px; border-radius: 15px; margin-bottom: 20px;">
            <p style="font-size: 20px; color: #666;">経過時間</p>
            <h1 style="font-size: 80px; margin: 0; color: #31333F;">{minutes:02d}:{seconds:02d}</h1>
        </div>
        """, unsafe_allow_html=True)

        # 温度表示
        st.markdown(f"""
        <div style="text-align: center; background-color: #1f77b4; padding: 30px; border-radius: 15px; color: white;">
            <p style="font-size: 24px; margin-bottom: 10px;">現在の目標温度</p>
            <h1 style="font-size: 110px; margin: 0;">{target_temp}<span style="font-size: 40px;">℃</span></h1>
            <p style="font-size: 18px; opacity: 0.8;">※次の計測まであと {next_check_in} 秒</p>
        </div>
        """, unsafe_allow_html=True)

    time.sleep(1)