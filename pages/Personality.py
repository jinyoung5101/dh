import streamlit as st

st.set_page_config(
    page_title="연애 성격 코치",
    page_icon="💖",
    layout="centered"
)

st.title("💖 연애 성격 코치")
st.write("간단한 질문에 답하면 당신의 연애 성향과 보완점을 알려드립니다.")

questions = [
    "새로운 사람과 쉽게 친해지는 편이다.",
    "상대방의 기분을 잘 살피는 편이다.",
    "서운한 일이 있으면 바로 말하는 편이다.",
    "질투가 많은 편이다.",
    "상대방에게 자주 연락하는 편이다.",
    "혼자만의 시간도 중요하다고 생각한다.",
    "갈등이 생기면 대화를 통해 해결하려고 한다.",
    "감정을 솔직하게 표현하는 편이다.",
    "상대방의 실수를 잘 이해해주는 편이다.",
    "상대에게 기대는 편이다."
]

answers = []

st.subheader("성격 테스트")

for i, q in enumerate(questions):
    score = st.slider(
        q,
        min_value=1,
        max_value=5,
        value=3,
        key=f"q{i}"
    )
    answers.append(score)

if st.button("결과 보기"):
    try:
        total = sum(answers)

        st.divider()

        if total >= 32:
            personality = "다정한 연애가"
            strength = [
                "공감 능력이 뛰어남",
                "상대를 배려함",
                "관계를 오래 유지할 가능성이 높음"
            ]
            weakness = [
                "상대에게 너무 맞추지 않기",
                "자신의 의견도 표현하기",
                "과도한 희생 줄이기"
            ]

        elif total >= 22:
            personality = "균형형 연애가"
            strength = [
                "감정 조절이 좋음",
                "현실적인 연애 가능",
                "건강한 거리 유지"
            ]
            weakness = [
                "감정 표현 늘리기",
                "상대방 칭찬 자주 하기",
                "관심 표현 적극적으로 하기"
            ]

        else:
            personality = "독립형 연애가"
            strength = [
                "자기 주관이 강함",
                "감정에 휘둘리지 않음",
                "현실적인 판단 가능"
            ]
            weakness = [
                "감정 표현 연습하기",
                "연락 빈도 늘리기",
                "상대 입장에서 생각하기"
            ]

        st.success(f"당신의 연애 성향은 **{personality}** 입니다.")

        st.subheader("✨ 연애 강점")

        for item in strength:
            st.write(f"✔️ {item}")

        st.subheader("📈 보완하면 좋은 점")

        for item in weakness:
            st.write(f"🔹 {item}")

        st.subheader("💕 연애 코치의 조언")

        advice = """
        좋은 연애는 완벽한 사람이 되는 것이 아니라
        서로를 이해하려는 노력에서 시작됩니다.

        상대방의 마음을 추측하기보다 대화를 통해 확인하고,
        자신의 감정도 솔직하게 표현해보세요.
        """

        st.info(advice)

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
