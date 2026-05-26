# app.py
import streamlit as st
import time

# =========================
# 기본 설정
# =========================
st.set_page_config(
    page_title="Pomodoro Timer",
    page_icon="🍅",
    layout="centered"
)

st.title("🍅 뽀모도로 타이머")

# =========================
# 세션 상태 초기화
# =========================
if "running" not in st.session_state:
    st.session_state.running = False

if "time_left" not in st.session_state:
    st.session_state.time_left = 25 * 60

if "mode" not in st.session_state:
    st.session_state.mode = "집중"

# =========================
# 사이드바 설정
# =========================
st.sidebar.header("⚙️ 설정")

focus_min = st.sidebar.slider("집중 시간 (분)", 1, 60, 25)
break_min = st.sidebar.slider("휴식 시간 (분)", 1, 30, 5)

# =========================
# 타이머 표시
# =========================
minutes = st.session_state.time_left // 60
seconds = st.session_state.time_left % 60

st.markdown(
    f"""
    <div style="
        text-align:center;
        font-size:80px;
        font-weight:bold;
        margin-top:30px;
        margin-bottom:30px;
    ">
        {minutes:02d}:{seconds:02d}
    </div>
    """,
    unsafe_allow_html=True
)

st.subheader(f"현재 모드: {st.session_state.mode}")

progress = 1 - (
    st.session_state.time_left /
    (
        focus_min * 60
        if st.session_state.mode == "집중"
        else break_min * 60
    )
)

st.progress(progress)

# =========================
# 버튼
# =========================
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("▶ 시작"):
        st.session_state.running = True

with col2:
    if st.button("⏸ 일시정지"):
        st.session_state.running = False

with col3:
    if st.button("🔄 리셋"):
        st.session_state.running = False
        st.session_state.mode = "집중"
        st.session_state.time_left = focus_min * 60
        st.rerun()

# =========================
# 타이머 동작
# =========================
if st.session_state.running:

    time.sleep(1)
    st.session_state.time_left -= 1

    # 시간 종료
    if st.session_state.time_left <= 0:

        if st.session_state.mode == "집중":
            st.session_state.mode = "휴식"
            st.session_state.time_left = break_min * 60
            st.toast("🎉 집중 완료! 휴식 시작!")
        else:
            st.session_state.mode = "집중"
            st.session_state.time_left = focus_min * 60
            st.toast("🔥 휴식 종료! 다시 집중!")

    st.rerun()
