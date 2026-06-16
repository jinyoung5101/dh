import streamlit as st
from google import genai
from google.genai import types

# =========================
# 페이지 설정
# =========================
st.set_page_config(
    page_title="Love Coach AI",
    page_icon="❤️",
    layout="centered"
)

# =========================
# 제목
# =========================
st.title("❤️ Love Coach AI")
st.caption("Gemini 2.5 Flash Lite 기반 AI 연애 코칭 챗봇")

# =========================
# API 키
# =========================
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("Secrets에 GEMINI_API_KEY를 등록해주세요.")
    st.stop()

# =========================
# Gemini 클라이언트
# =========================
try:
    client = genai.Client(api_key=api_key)
except Exception as e:
    st.error(f"Gemini 클라이언트 생성 실패: {e}")
    st.stop()

# =========================
# 시스템 프롬프트
# =========================
SYSTEM_PROMPT = """
너는 전문 연애 코치다.

역할:
- 썸 상담
- 고백 상담
- 연애 갈등 상담
- 장거리 연애 상담
- 이별 상담

규칙:
- 사용자의 감정을 존중한다.
- 먼저 공감한다.
- 현실적인 조언을 제공한다.
- 상대방을 조종하는 방법은 알려주지 않는다.
- 건강한 관계를 우선한다.
- 친절하고 자연스럽게 대화한다.

답변 형식:

❤️ 공감

🔍 상황 분석

💡 조언

🌱 추천 행동
"""

# =========================
# 세션 상태
# =========================
if "messages" not in st.session_state:
    st.session_state.messages = []

# =========================
# 첫 실행 안내
# =========================
if len(st.session_state.messages) == 0:
    st.info(
        """
💕 안녕하세요! 연애 고민이 있다면 편하게 이야기해주세요.

예시 질문
• 썸남이 연락이 줄었어요
• 고백해도 될까요?
• 헤어진 전애인이 생각나요
• 장거리 연애가 힘들어요
• 연애를 시작하는 게 무서워요
"""
    )

# =========================
# 이전 대화 출력
# =========================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =========================
# 사용자 입력
# =========================
user_input = st.chat_input(
    "연애 고민을 이야기해보세요..."
)

if user_input:

    # 사용자 메시지 저장
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.chat_message("assistant"):

        placeholder = st.empty()

        try:

            history_text = ""

            for msg in st.session_state.messages:

                role = (
                    "사용자"
                    if msg["role"] == "user"
                    else "상담사"
                )

                history_text += (
                    f"{role}: {msg['content']}\n"
                )

            prompt = f"""
{SYSTEM_PROMPT}

다음은 지금까지의 대화 내용이다.

{history_text}

상담사 답변:
"""

            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.8,
                    max_output_tokens=700,
                )
            )

            ai_response = response.text

            placeholder.markdown(ai_response)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": ai_response
                }
            )

        except Exception as e:

            error_message = (
                f"❌ 오류가 발생했어요.\n\n{str(e)}"
            )

            placeholder.error(error_message)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": error_message
                }
            )

# =========================
# 사이드바
# =========================
with st.sidebar:

    st.header("❤️ Love Coach")

    st.metric(
        "대화 수",
        len(st.session_state.messages) // 2
    )

    if st.button("🗑️ 대화 초기화"):
        st.session_state.messages = []
        st.rerun()

    st.markdown("---")

    st.markdown("""
### 💡 예시 질문

- 썸남이 연락이 줄었어요
- 고백해도 될까요?
- 헤어진 전애인이 생각나요
- 장거리 연애가 힘들어요
- 연애를 시작하는 게 무서워요

### 🤖 사용 모델

gemini-2.5-flash-lite
""")
