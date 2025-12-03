import streamlit as st
import pandas as pd
import plotly.express as px

st.title("🏛️ 역사 시뮬레이터: 갑신정변의 3일")

# 1. 사이드바: 역사적 변수 조절 (Input)
st.sidebar.header("1884년, 당신의 선택은?")
japan_support = st.sidebar.slider("일본의 지원을 얼마나 믿습니까?", 0, 100, 80) # 실제 역사는 높았음
public_mind = st.sidebar.slider("백성들의 지지를 얻기 위한 정책은?", 0, 100, 10) # 실제 역사는 낮았음
military_power = st.sidebar.slider("자주 국방력 준비 수준", 0, 100, 20)

# 2. 알고리즘: 성공 확률 계산 (Algorithm)
# 성공 공식: 민심이 가장 중요하고, 외세 의존도가 너무 높으면 오히려 감점되도록 설계
success_rate = (public_mind * 0.5) + (military_power * 0.3) + (japan_support * 0.2)
if japan_support > 70 and military_power < 30: # 외세 의존이 심하면 패널티
    success_rate -= 20 

# 3. 데이터 시각화: 레이더 차트 (Output)
st.subheader("📊 혁명 성공 분석 결과")

# 데이터 프레임 생성
data = pd.DataFrame(dict(
    r=[public_mind, military_power, japan_support, success_rate],
    theta=['민심(백성)', '자주 국방력', '일본 의존도', '성공 확률']
))

# 레이더 차트 그리기
fig = px.line_polar(data, r='r', theta='theta', line_close=True)
fig.update_traces(fill='toself')
st.plotly_chart(fig)

# 4. 결과 텍스트 및 챗봇 유도
if success_rate < 50:
    st.error(f"성공 확률 {success_rate:.1f}%: 3일 천하로 끝났습니다. 😢")
    st.info("💡 김옥균 AI에게 조언을 구해보세요! (오른쪽 버튼)")
else:
    st.success(f"성공 확률 {success_rate:.1f}%: 역사가 바뀌었습니다! 새로운 조선이 탄생했습니다. 🎉")
