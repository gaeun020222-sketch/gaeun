import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="영어 단어 퀴즈", page_icon="📝")

# 테스트할 단어 목록 (여기에 원하는 단어를 추가하거나 수정하세요)
WORD_LIST = {
    "apple": "사과",
    "banana": "바나나",
    "computer": "컴퓨터",
    "programming": "프로그래밍",
    "streamlit": "스트림릿",
    "python": "파이썬",
    "challenge": "도전",
    "learning": "학습",
    "vocabulary": "어휘",
    "application": "애플리케이션",
    "developer": "개발자",
    "interface": "인터페이스"
}

# 세션 상태 초기화 함수
def initialize_test():
    """새로운 테스트를 위해 세션 상태를 초기화합니다."""
    # 단어 목록을 랜덤으로 섞습니다.
    words = list(WORD_LIST.items())
    random.shuffle(words)
    
    st.session_state.words = words
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.show_result = False
    st.session_state.user_answer = ""

# 세션 상태가 초기화되지 않았으면 초기화 함수 호출
if 'words' not in st.session_state:
    initialize_test()

# --- UI 구성 ---

st.title("📝 영어 단어 암기 테스트")
st.write("제시된 영어 단어의 한국어 뜻을 입력하세요.")

# 사이드바: 새 테스트 시작 버튼
with st.sidebar:
    st.header("메뉴")
    if st.button("새 테스트 시작", use_container_width=True, type="primary"):
        initialize_test()
        st.rerun()

# 점수판
col1, col2 = st.columns(2)
col1.metric("맞춘 개수", f"{st.session_state.score} / {len(WORD_LIST)}")
col2.metric("진행도", f"{st.session_state.current_index} / {len(WORD_LIST)}")

st.markdown("---")

# 테스트가 끝났을 때
if st.session_state.current_index >= len(st.session_state.words):
    st.success(f"🎉 모든 문제를 다 풀었습니다! 최종 점수: {st.session_state.score} / {len(WORD_LIST)}")
    st.balloons()
    st.write("새로운 테스트를 시작하려면 왼쪽 사이드바의 '새 테스트 시작' 버튼을 누르세요.")

# 테스트 진행 중일 때
else:
    # 현재 문제 가져오기
    english_word, korean_meaning = st.session_state.words[st.session_state.current_index]

    # 문제 표시
    st.subheader(f"문제 {st.session_state.current_index + 1}")
    st.header(f"**{english_word}**")

    # 답변 입력 폼
    with st.form(key="answer_form"):
        user_answer = st.text_input("정답을 입력하세요:", key="answer_input")
        submit_button = st.form_submit_button("정답 확인")

    # 정답 확인 버튼을 눌렀을 때
    if submit_button:
        st.session_state.user_answer = user_answer
        st.session_state.show_result = True

    # 결과 표시
    if st.session_state.show_result:
        user_ans = st.session_state.user_answer.strip()
        
        if user_ans == korean_meaning:
            st.success(f"**정답입니다!** 👍")
            # 점수 업데이트는 "다음 문제" 버튼을 누를 때 한 번만 수행
        else:
            st.error(f"**오답입니다.** 땡!")
            st.info(f"정답은 **'{korean_meaning}'** 입니다.")

        # 다음 문제로 넘어가는 버튼
        if st.button("다음 문제로", use_container_width=True):
            # 정답이었을 경우에만 점수 증가
            if user_ans == korean_meaning:
                st.session_state.score += 1
            
            # 다음 문제로 인덱스 이동 및 상태 초기화
            st.session_state.current_index += 1
            st.session_state.show_result = False
            st.session_state.user_answer = ""
            st.rerun() # 화면을 새로고침하여 다음 문제를 표시

st.markdown("---")
st.info("사이드바의 '새 테스트 시작' 버튼을 눌러 언제든지 퀴즈를 다시 시작할 수 있습니다.")