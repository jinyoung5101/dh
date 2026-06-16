import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="💕 다이어트 연애 코치",
    page_icon="💕",
    layout="centered"
)

# 음식 데이터베이스
food_db = {
    "닭가슴살": {"cal": 165, "carb": 0, "protein": 31, "fat": 3.6},
    "계란": {"cal": 78, "carb": 0.6, "protein": 6, "fat": 5},
    "고구마": {"cal": 130, "carb": 31, "protein": 2, "fat": 0.2},
    "바나나": {"cal": 105, "carb": 27, "protein": 1.3, "fat": 0.4},
    "현미밥": {"cal": 215, "carb": 45, "protein": 5, "fat": 1.8},
    "사과": {"cal": 95, "carb": 25, "protein": 0.5, "fat": 0.3},
    "두부": {"cal": 90, "carb": 2, "protein": 10, "fat": 5},
    "연어": {"cal": 208, "carb": 0, "protein": 20, "fat": 13},
    "샐러드": {"cal": 50, "carb": 10, "protein": 2, "fat": 0.5},
    "아몬드(10알)": {"cal": 70, "carb": 2.5, "protein": 2.6, "fat": 6},
    "햄버거": {"cal": 550, "carb": 45, "protein": 25, "fat": 30},
    "피자(1조각)": {"cal": 285, "carb": 36, "protein": 12, "fat": 10},
    "라면": {"cal": 500, "carb": 80, "protein": 10, "fat": 16}
}

st.title("💕 다이어트 연애 코치")
st.markdown("### 🥗 식단을 분석하고 연애 자신감도 함께 챙겨보세요!")

st.divider()

# 몸무게 입력
weight = st.number_input(
    "⚖️ 현재 몸무게(kg)",
    min_value=30.0,
    max_value=250.0,
    value=60.0,
    step=0.1
)

st.write(f"현재 입력 몸무게 : **{weight:.1f}kg**")

st.divider()

# 음식 선택
selected_foods = st.multiselect(
    "🍽️ 오늘 먹은 음식을 선택하세요",
    list(food_db.keys())
)

if st.button("💕 식단 분석하기"):

    try:
        if not selected_foods:
            st.warning("음식을 하나 이상 선택해주세요 😊")
            st.stop()

        total_cal = 0
        total_carb = 0
        total_protein = 0
        total_fat = 0

        rows = []

        for food in selected_foods:
            data = food_db[food]

            total_cal += data["cal"]
            total_carb += data["carb"]
            total_protein += data["protein"]
            total_fat += data["fat"]

            rows.append({
                "음식": food,
                "칼로리(kcal)": data["cal"],
                "탄수화물(g)": data["carb"],
                "단백질(g)": data["protein"],
                "지방(g)": data["fat"]
            })

        st.subheader("📋 음식 상세 정보")
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

        st.divider()

        st.subheader("📊 총 영양 분석")

        st.metric("🔥 총 칼로리", f"{total_cal:.0f} kcal")

        macro_sum = total_carb + total_protein + total_fat

        carb_ratio = total_carb / macro_sum * 100
        protein_ratio = total_protein / macro_sum * 100
        fat_ratio = total_fat / macro_sum * 100

        st.write(f"🍚 탄수화물 : {carb_ratio:.1f}%")
        st.progress(min(carb_ratio / 100, 1.0))

        st.write(f"🍗 단백질 : {protein_ratio:.1f}%")
        st.progress(min(protein_ratio / 100, 1.0))

        st.write(f"🥑 지방 : {fat_ratio:.1f}%")
        st.progress(min(fat_ratio / 100, 1.0))

        st.divider()

        st.subheader("🧑‍⚕️ 다이어트 코치 피드백")

        if total_cal < 1200:
            st.info("💡 섭취량이 다소 적습니다. 너무 무리한 다이어트는 피하세요.")
        elif total_cal <= 2000:
            st.success("✅ 적절한 수준의 섭취량으로 보입니다.")
        else:
            st.warning("⚠️ 칼로리가 높은 편입니다. 활동량을 늘려보세요.")

        if protein_ratio >= 25:
            st.success("💪 단백질 섭취가 좋은 편입니다.")
        else:
            st.warning("🍗 단백질을 조금 더 늘려보는 것을 추천합니다.")

        if fat_ratio > 40:
            st.warning("🥑 지방 비율이 높은 편입니다.")

        if carb_ratio > 60:
            st.warning("🍚 탄수화물 비율이 높습니다.")

        st.divider()

        st.subheader("💕 연애 자신감 코치")

        messages = [
            "😊 건강한 습관은 자신감을 만들어 줍니다!",
            "💖 꾸준한 관리가 매력을 더욱 빛나게 합니다.",
            "🌸 오늘의 작은 노력이 내일의 멋진 만남을 만듭니다.",
            "✨ 자신을 아끼는 사람은 더욱 매력적으로 보입니다.",
            "💕 건강한 식습관도 자기관리의 중요한 매력 포인트입니다."
        ]

        idx = int(weight) % len(messages)

        st.success(messages[idx])

    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")
