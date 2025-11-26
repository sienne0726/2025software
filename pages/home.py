import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="깡통체크", layout="wide")

# ------------------------------
# 샘플 데이터: 지역별 평균 보증금 + 전세가율 + 좌표
# ------------------------------
def load_sample_market():
    return pd.DataFrame([
        {"지역":"강남구","평균보증금":25000,"전세가율":0.55},
        {"지역":"서초구","평균보증금":22000,"전세가율":0.52},
        {"지역":"송파구","평균보증금":15000,"전세가율":0.48},
        {"지역":"마포구","평균보증금":12000,"전세가율":0.40},
        {"지역":"용산구","평균보증금":20000,"전세가율":0.50},
    ])

market = load_sample_market()

# ------------------------------
# 위험도 계산 함수
# ------------------------------
def calc_risk(deposit, monthly, region, sensitivity, mortgage, seizure, provisional):
    base = 0

    # 지역 평균과 비교
    region_row = market[market["지역"] == region].iloc[0]
    avg = region_row["평균보증금"]
    ratio = deposit / avg

    # 보증금이 높을수록 위험 ↑
    if ratio > 1.3:
        base += 30
    elif ratio > 1.1:
        base += 15
    else:
        base += 5

    # 감정 민감도 반영
    base *= sensitivity

    # 등기부 위험 요소
    if mortgage:      # 근저당
        base += 20
    if seizure:       # 가압류
        base += 25
    if provisional:   # 가처분
        base += 25

    # 월세가 너무 낮을 경우 깡통 리스크
    if monthly < 20:
        base += 10

    # 스코어 정규화
    if base > 100:
        base = 100
    return base

# ------------------------------
# 신호등 표시
# ------------------------------
def risk_light(score):
    if score >= 70:
        return "🔴 **깡통 위험 (높음)**"
    elif score >= 40:
        return "🟡 **보통 (주의 필요)**"
    else:
        return "🟢 **안전**"

# ------------------------------
# 탭 생성
# ------------------------------
tabs = st.tabs(["🏠 위치·기본 정보", "📊 위험도 분석", "📄 계약서 체크리스트",
                "🧾 등기부 해석", "🆘 사후 대응 도우미", "👥 워크스페이스"])

# -----------------------------------------
# 1) 위치·기본 정보 입력
# -----------------------------------------
with tabs[0]:
    st.header("🏠 위치·기본 정보 입력")

    address = st.text_input("📍 집 주소를 입력하세요", "")
    region = st.selectbox("📌 지역 선택", market["지역"].tolist())
    deposit = st.number_input("💰 보증금 (만원)", min_value=0, value=10000)
    monthly = st.number_input("💵 월세 (만원)", min_value=0, value=50)

    st.info("계속해서 '위험도 분석' 탭으로 이동하세요!")

# -----------------------------------------
# 2) 위험도 분석
# -----------------------------------------
with tabs[1]:
    st.header("📊 보증금 위험도 분석")

    st.subheader("⚙️ 사용자 민감도 조절")
    sensitivity = st.slider("예민함 정도", 0.5, 2.0, 1.0)

    st.subheader("📘 등기부 위험요소 체크")
    col1, col2, col3 = st.columns(3)
    mortgage = col1.checkbox("근저당")
    seizure = col2.checkbox("가압류")
    provisional = col3.checkbox("가처분")

    if st.button("🔍 위험도 분석 실행"):
        score = calc_risk(deposit, monthly, region, sensitivity,
                          mortgage, seizure, provisional)

        st.metric("위험도 점수", f"{score}/100")
        st.write(risk_light(score))

        st.write("---")
        st.subheader("💡 지역 평균 정보")
        region_row = market[market["지역"] == region].iloc[0]
        st.write(f"- 평균 보증금: {region_row['평균보증금']}만원")
        st.write(f"- 전세가율: {region_row['전세가율']*100:.1f}%")

# -----------------------------------------
# 3) 계약서 체크리스트
# -----------------------------------------
with tabs[2]:
    st.header("📄 전·월세 계약서 체크리스트")

    items = [
        "등기부등본 확인했는가?",
        "근저당, 가압류 여부 확인했는가?",
        "집주인 실소유자 확인했는가?",
        "특약사항에 원상복구 조항 포함 여부?",
        "관리비 항목 명확히 기재했는가?",
        "계약 만료 이전 중도 해지 조항 확인?",
        "전세보증보험 가입 가능 여부 확인?"
    ]

    for i in items:
        st.checkbox(i)

    st.success("체크리스트를 모두 확인했다면 위험도가 크게 줄어듭니다!")

# -----------------------------------------
# 4) 등기부 해석 도우미
# -----------------------------------------
with tabs[3]:
    st.header("🧾 등기부 해석 도우미")

    text = st.text_area("등기부등본 주요 항목을 입력하세요 (예: 근저당 3천만원 설정)")
    if st.button("📘 해석하기"):
        if "근저당" in text:
            st.warning("근저당 발견: 채무가 있을 수 있어 매우 주의해야 합니다.")
        if "가압류" in text:
            st.error("가압류 발견: 법적 분쟁 중일 수 있습니다.")
        if "가처분" in text:
            st.error("가처분 발견: 소유권 관련 분쟁 가능성이 있습니다.")
        if text.strip() == "":
            st.info("아무 정보도 입력되지 않았습니다.")
        else:
            st.success("등기부 분석 완료!")

# -----------------------------------------
# 5) 사후 대응 도우미
# -----------------------------------------
with tabs[4]:
    st.header("🆘 사후 대응 도우미")

    scenario = st.selectbox("상황 선택",
                            ["보증금 반환 지연", "집주인 연락 두절", "수리 미이행", "계약 위반"])

    if st.button("대응 가이드 보기"):
        if scenario == "보증금 반환 지연":
            st.write("1) 문자/카톡 기록 보관\n2) 내용증명 발송\n3) 주택도시보증공사(HUG) 신청 가능 여부 확인\n4) 법률구조공단 상담")
        elif scenario == "집주인 연락 두절":
            st.write("1) 연락 시도 기록 저장\n2) 내용증명 발송\n3) 주민센터 통해 소유자 확인\n4) 변호사 상담")
        else:
            st.write("📌 상황에 따른 추가 조언이 필요하면 문의하세요.")

# -----------------------------------------
# 6) 워크스페이스
# -----------------------------------------
with tabs[5]:
    st.header("👥 워크스페이스 — 가족/룸메와 집 함께 보기")

    memo = st.text_area("공유할 메모 작성")
    if st.button("메모 저장"):
        st.success("메모가 저장되었습니다! (실서비스에서는 DB 연동 필요)")

    st.info("Streamlit Cloud에서는 URL 공유만으로도 실시간 의견 교환 가능합니다.")

