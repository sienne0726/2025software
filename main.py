import streamlit as st
from datetime import datetime

# Baskin-Robbins 스타일 키오스크 (Streamlit)
# 이 파일을 streamlit cloud에 올리려면 이 파일을 깃허브 저장소에 넣고
# Streamlit Cloud에서 해당 저장소와 연결하면 됩니다.

st.set_page_config(page_title="베스킨라빈스 키오스크 🍨", page_icon="🍦", layout="centered")

st.title("베스킨라빈스 키오스크 🍨")
st.write("안녕하세요! 오늘 어떤 달콤한 선택을 도와드릴까요? 😊")

# 1) 매장 식사 or 포장
st.header("1. 이용 방식 선택")
service_type = st.radio("매장에서 드실 건가요, 포장해 가실 건가요?", ("매장 (Eat-in)", "포장 (Takeout)"))

# 2) 용기 선택 (용기마다 선택 가능한 맛이 제한된다 가정)
st.header("2. 용기 선택")
container_options = {
    "컵(싱글) - 1스쿱": {"price": 3000, "max_scoops": 1},
    "컵(더블) - 2스쿱": {"price": 5500, "max_scoops": 2},
    "컵(패밀리) - 4스쿱": {"price": 10000, "max_scoops": 4},
    "콘(1스쿱) - 바삭한 콘": {"price": 3500, "max_scoops": 1},
    "파인트(가정용) - 2~4인분": {"price": 18000, "max_scoops": 6},
}

container = st.selectbox("원하시는 용기를 골라주세요:", list(container_options.keys()))
max_scoops = container_options[container]["max_scoops"]
base_price = container_options[container]["price"]

st.write(f"선택: **{container}** — 기본 가격: {base_price:,}원 — 최대 스쿱: {max_scoops}개")

# 3) 용기에 맞는 아이스크림 맛 선택
st.header("3. 맛 선택 🍨")

# 예시 맛 목록 (간단화). 실제 매장과 다를 수 있음.
all_flavors = {
    "싱글/더블용": [
        "바닐라 클래식", "초콜릿 듀오", "스트로베리 스윗", "민트 초콜릿 칩",
        "쿠키 앤 크림", "망고 스파클", "그린티", "카라멜 리본"
    ],
    "콘전용": ["바닐라 클래식", "초콜릿 듀오", "민트 초콜릿 칩", "망고 스파클"],
    "패밀리/파인트용": [
        "바닐라 클래식", "초콜릿 듀오", "쿠키 앤 크림", "그린티",
        "스트로베리 스윗", "카라멜 리본", "아몬드 봉봉"
    ]
}

# 용기에 따라 제공되는 맛 분기
if "콘" in container:
    available = all_flavors["콘전용"]
elif "파인트" in container or "패밀리" in container:
    available = all_flavors["패밀리/파인트용"]
else:
    available = all_flavors["싱글/더블용"]

st.write("용기에 맞는 맛만 고를 수 있어요. 맛을 고르실 때 스쿱 수를 참고해주세요.")

# 스쿱 수 선택
scoops = st.number_input("원하시는 스쿱 수를 입력하세요:", min_value=1, max_value=max_scoops, value=1, step=1)

# 맛 선택 (복수 선택 허용: 스쿱 수 만큼 선택해야 함)
selected_flavors = st.multiselect(f"{scoops}개 맛 선택 (용기에 맞는 맛만):", available)

# 선택된 맛 개수 검증
if len(selected_flavors) != scoops:
    st.warning(f"스쿱 수({scoops})와 선택한 맛 개수({len(selected_flavors)})가 일치해야 합니다. 🍦")

# 4) 가격 계산 및 결제 방식 선택
st.header("4. 결제 및 확인 💳💵")

# 가격 규칙: 기본 용기 가격에 추가 스쿱(기본 1스쿱 포함시 약간의 조정)
# 이미 base_price는 용기 기준 가격(예시). 추가 스쿱이 있다면 스쿱당 가격을 더함.
per_extra_scoop = 2500  # 1스쿱 초과 시 스쿱당 비용

# 실제 가격 산정
# 가정: base_price는 해당 용기의 기본(권장) 가격. 사용자가 스쿱을 줄이거나 늘리면 조정.
# 더 간단하게: 최종 = base_price + (scoops - 1) * per_extra_scoop
final_price = base_price + max(0, scoops - 1) * per_extra_scoop

st.write(f"최종 가격: **{final_price:,}원**")

# 결제수단 선택
payment_method = st.selectbox("결제 수단을 선택해주세요:", ("카드결제 💳", "현금결제 💵"))

# 추가 옵션: 영수증, 포장 박스 등
receipt = st.checkbox("영수증 필요합니다", value=True)
utensils = st.checkbox("스푼/포크 필요", value=False)

# 확인 버튼
if st.button("주문 확정 ✅"):
    if len(selected_flavors) != scoops:
        st.error("맛 선택 개수가 스쿱 수와 맞지 않습니다. 먼저 맞춰주세요. 🙏")
    else:
        # 주문 요약
        st.success("주문이 접수되었습니다! 감사합니다 😊")
        st.markdown("---")
        st.subheader("주문 요약 🧾")
        st.write(f"- 이용 방식: **{service_type}**")
        st.write(f"- 용기: **{container}**")
        st.write(f"- 스쿱 수: **{scoops}개**")
        st.write(f"- 선택한 맛: {', '.join(selected_flavors)}")
        st.write(f"- 결제: **{payment_method}**")
        st.write(f"- 영수증: {'발행' if receipt else '미발행'}")
        st.write(f"- 스푼/포크: {'포함' if utensils else '미포함'}")
        st.write(f"- 최종 결제금액: **{final_price:,}원**")
        st.markdown("---")

        # 간단한 안내 문구
        if service_type.startswith("매장"):
            st.info("주문이 준비되면 바코드 또는 주문번호로 알려드릴게요. 잠시만 기다려주세요! ⏳")
        else:
            st.info("포장 주문은 준비 후 카운터에서 찾아가실 수 있어요. 좋은 하루 되세요! 🎁")

        # 영수증 / 결제 처리 시뮬레이션 메시지
        if payment_method.startswith("카드"):
            st.write("카드 모듈로 결제 진행 중... (테스트 모드)")
        else:
            st.write("현금 결제 선택하셨습니다. 카운터에서 결제해주세요.")

        # 주문시간과 간단 주문번호 생성
        order_time = datetime.now().strftime("%Y%m%d-%H%M%S")
        order_number = f"BR{order_time}"
        st.write(f"주문번호: **{order_number}**")
        st.balloons()

st.write("\n---\n")
st.write("도움 필요하시면 직원에게 말씀해주세요. 맛있는 하루 되세요! 🍨✨")
