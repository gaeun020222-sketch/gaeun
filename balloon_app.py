import streamlit as st
import time
import random

# 페이지 설정
st.set_page_config(
    page_title="🎈 풍선 날아가기 게임",
    page_icon="🎈",
    layout="wide"
)

# CSS 스타일 추가
st.markdown("""
<style>
@keyframes balloon-fly {
    0% {
        transform: translateY(0px) rotate(0deg);
        opacity: 1;
    }
    50% {
        transform: translateY(-200px) rotate(180deg);
        opacity: 0.8;
    }
    100% {
        transform: translateY(-400px) rotate(360deg);
        opacity: 0;
    }
}

.balloon {
    font-size: 3rem;
    animation: balloon-fly 3s ease-out forwards;
    position: relative;
    display: inline-block;
    margin: 10px;
}

.balloon-container {
    height: 500px;
    overflow: hidden;
    position: relative;
    background: linear-gradient(to bottom, #87CEEB 0%, #98FB98 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
}

.flying-balloon {
    position: absolute;
    font-size: 2rem;
    animation: balloon-fly 3s ease-out forwards;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-10px);
    }
    60% {
        transform: translateY(-5px);
    }
}

.bounce {
    animation: bounce 1s infinite;
}

.stats {
    background-color: #f0f2f6;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
}
</style>
""", unsafe_allow_html=True)

# 세션 상태 초기화
if 'balloon_count' not in st.session_state:
    st.session_state.balloon_count = 0
if 'balloons' not in st.session_state:
    st.session_state.balloons = []

# 제목
st.title("🎈 풍선 날아가기 게임")
st.markdown("버튼을 눌러서 풍선을 날려보세요!")

# 사이드바에 통계 표시
with st.sidebar:
    st.header("📊 통계")
    st.metric("날린 풍선 수", st.session_state.balloon_count)
    
    if st.button("🔄 리셋"):
        st.session_state.balloon_count = 0
        st.session_state.balloons = []
        st.rerun()

# 메인 컨테이너
balloon_container = st.container()

# 풍선 색상과 이모지
balloon_colors = ["🎈", "🎈", "🎈", "🎈", "🎈", "🎈", "🎈", "🎈", "🎈", "🎈"]
balloon_emojis = ["🎈", "🎈", "🎈", "🎈", "🎈"]

# 버튼들
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎈 풍선 하나 날리기", type="primary", use_container_width=True):
        st.session_state.balloon_count += 1
        st.session_state.balloons.append({
            'id': len(st.session_state.balloons),
            'emoji': random.choice(balloon_emojis),
            'timestamp': time.time()
        })
        st.rerun()

with col2:
    if st.button("🎈🎈 풍선 두 개 날리기", type="secondary", use_container_width=True):
        for _ in range(2):
            st.session_state.balloon_count += 1
            st.session_state.balloons.append({
                'id': len(st.session_state.balloons),
                'emoji': random.choice(balloon_emojis),
                'timestamp': time.time()
            })
        st.rerun()

with col3:
    if st.button("🎈🎈🎈 풍선 세 개 날리기", type="secondary", use_container_width=True):
        for _ in range(3):
            st.session_state.balloon_count += 1
            st.session_state.balloons.append({
                'id': len(st.session_state.balloons),
                'emoji': random.choice(balloon_emojis),
                'timestamp': time.time()
            })
        st.rerun()

# 풍선 애니메이션 표시 영역
with balloon_container:
    st.markdown('<div class="balloon-container">', unsafe_allow_html=True)
    
    # 현재 날아가는 풍선들 표시
    for balloon in st.session_state.balloons:
        # 풍선이 3초 이상 지났으면 제거
        if time.time() - balloon['timestamp'] > 3:
            continue
            
        # 풍선 위치 계산 (랜덤한 x 위치)
        x_position = random.randint(50, 400)
        y_position = 400 - int((time.time() - balloon['timestamp']) * 100)
        
        if y_position > 0:
            st.markdown(f'''
            <div class="flying-balloon" style="left: {x_position}px; top: {y_position}px;">
                {balloon['emoji']}
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# 오래된 풍선들 제거
current_time = time.time()
st.session_state.balloons = [b for b in st.session_state.balloons if current_time - b['timestamp'] < 3]

# 자동 새로고침 (애니메이션을 위해)
if st.session_state.balloons:
    time.sleep(0.1)
    st.rerun()

# 하단에 설명
st.markdown("---")
st.markdown("""
### 🎮 게임 방법
1. **풍선 하나 날리기**: 풍선 하나를 날려보세요
2. **풍선 두 개 날리기**: 풍선 두 개를 동시에 날려보세요  
3. **풍선 세 개 날리기**: 풍선 세 개를 동시에 날려보세요

### ✨ 특징
- 풍선이 하늘로 날아가면서 회전합니다
- 각 풍선은 3초 동안 애니메이션됩니다
- 사이드바에서 날린 풍선 수를 확인할 수 있습니다
- 리셋 버튼으로 통계를 초기화할 수 있습니다
""")

# 풍선이 날아가는 효과음 (선택사항)
if st.session_state.balloon_count > 0 and st.session_state.balloon_count % 10 == 0:
    st.balloons()  # Streamlit의 내장 풍선 효과

