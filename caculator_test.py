import streamlit as st

st.set_page_config(page_title="위암 위험지수 계산기", layout="centered")
st.title("📊 위암 위험지수 계산기")
st.markdown("각 항목에 해당하는 경우 '예'를 선택해주세요. 흡연/음주를 선택한 경우에는 추가 정보를 입력합니다.")

# 위험 요인 및 기본 점수 (공공데이터 기반)
risk_factors = {
    "결핵 발병 이력": 4.1,
    "음주 여부": 56.8,
    "심장질환 발병 이력": 37.5,
    "간질환 발병 이력": 2.6,
    "암 발병 이력": 2.7,
    "고혈압 보유 여부": 36.9,
    "과거 흡연 이력": 42.5,
    "현재 흡연 이력": 8.2,
    "당뇨병 발병 이력": 16.7,
}

user_input = {}
smoking_amount = 0
drinking_amount = 0

st.subheader("📝 건강 상태 입력")

for factor in risk_factors:
    user_input[factor] = st.radio(f"{factor}:", ("아니오", "예"), key=factor)

    if factor in ["과거 흡연 이력", "현재 흡연 이력"] and user_input[factor] == "예":
        smoking_amount = st.number_input("하루 평균 흡연량 (개비)", min_value=0, max_value=100, value=0, step=1, key=f"{factor}_smoke")

    if factor == "음주 여부" and user_input[factor] == "예":
        drinking_amount = st.number_input("한 번 마시는 평균 소주 병 수", min_value=0.0, max_value=5.0, value=0.0, step=0.1, key="alcohol")

# 계산 버튼
if st.button("위험지수 계산하기"):
    total_score = 0
    max_score = sum(risk_factors.values())

    for factor, response in user_input.items():
        if response == "예":
            score = risk_factors[factor]

            # 흡연 위험도 비례 반영
            if factor in ["과거 흡연 이력", "현재 흡연 이력"]:
                proportion = min(smoking_amount / 20, 1.5)
                score *= proportion

            # 음주 위험도 비례 반영
            if factor == "음주 여부":
                proportion = min(drinking_amount / 1.0, 2.0)
                score *= proportion

            total_score += score

    risk_percent = (total_score / max_score) * 100 if max_score != 0 else 0

    st.success(f"✅ 당신의 위암 위험지수는 **{risk_percent:.2f}%** 입니다.")

    if risk_percent >= 70:
        st.error("⚠️ 매우 높은 위험도! 정밀 검진을 강력히 권장합니다.")
    elif risk_percent >= 40:
        st.warning("⚠️ 중간 정도의 위험. 건강 관리에 신경 써야 합니다.")
    else:
        st.info("💡 낮은 위험도입니다. 현재 건강 상태를 잘 유지하세요.")