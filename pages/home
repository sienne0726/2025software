# app.py
import streamlit as st

# 페이지 제목
st.set_page_config(page_title="깡통 체크", layout="wide")

# --- 사이드바 탭 메뉴 ---
tabs = ["내 집 찾기", "장바구니", "현재 위험도", "로그인"]
selected_tab = st.sidebar.selectbox("메뉴 선택", tabs)

# --- 내 집 찾기 탭 ---
if selected_tab == "내 집 찾기":
    st.title("🏠 내 집 찾기")
    st.write("보증금 사기 위험을 체크할 집 주소를 입력하세요.")
    address = st.text_input("집 주소 입력")
    if st.button("체크"):
        # 예시 체크 로직 (실제는 DB/API 연동 필요)
        st.success(f"{address}에 대한 위험도를 분석했습니다. 안전합니다!")

# --- 장바구니 탭 ---
elif selected_tab == "장바구니":
    st.title("🛒 장바구니")
    st.write("체크하고 싶은 집을 장바구니에 추가하세요.")
    # 예시: 단순 목록
    houses = st.text_area("장바구니 목록", "예: 강남구 OO아파트\n서초구 XX빌라")
    if st.button("장바구니 확인"):
        st.info("장바구니에 있는 집들의 위험도를 확인하세요.")

# --- 현재 위험도 탭 ---
elif selected_tab == "현재 위험도":
    st.title("⚠️ 현재 위험도")
    st.write("선택된 지역/집의 위험도를 시각화합니다.")
    # 예시 데이터
    import pandas as pd
    import plotly.express as px

    data = pd.DataFrame({
        "지역": ["강남", "서초", "송파", "마포", "용산"],
        "위험도": [2, 3, 1, 4, 2]
    })
    fig = px.bar(data, x="지역", y="위험도", color="위험도", range_y=[0,5],
                 color_continuous_scale="Reds")
    st.plotly_chart(fig)

# --- 로그인 탭 ---
elif selected_tab == "로그인":
    st.title("🔑 로그인")
    st.write("계정을 입력하세요.")
    username = st.text_input("아이디")
    password = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        # 간단 예제: 실제 DB 연동 필요
        if username and password:
            st.success(f"{username}님 로그인 성공!")
        else:
            st.error("아이디와 비밀번호를 입력해주세요.")
