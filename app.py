import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

# 페이지 설정
st.set_page_config(page_title="19세기 후반 정치 마당", layout="wide")

# --------------------------------------------------------------------------
# [설정] 이미지 URL 관리
# --------------------------------------------------------------------------
IMAGE_URLS = {
    "청나라": "https://i.ibb.co/1fXH5Ffb/chung.png",
    "일본": "https://i.ibb.co/KchxkbQJ/japan.png",
    "민씨정권": "https://i.ibb.co/tpyZWYgH/image.png",
    "고종": "https://i.ibb.co/fYpjpVJ2/image.png",
    "김옥균": "https://i.ibb.co/1jFg9C6/image.png",
    "온건개화파": "https://i.ibb.co/BKGYrkf3/image.png",
    "흥선대원군": "https://i.ibb.co/PsJwdCrK/image.png"
}

# --------------------------------------------------------------------------
# [초기화] 세션 상태 (Session State) 설정
# --------------------------------------------------------------------------
if 'step' not in st.session_state:
    st.session_state['step'] = 1  # 현재 퀴즈 단계 (1~5)
if 'quiz_finished' not in st.session_state:
    st.session_state['quiz_finished'] = False # 모든 퀴즈 완료 여부
if 'show_next' not in st.session_state:
    st.session_state['show_next'] = False # 다음 버튼 표시 여부

# --------------------------------------------------------------------------
# [UI] 타이틀 및 레이아웃
# --------------------------------------------------------------------------
st.title("🏛️ 탭 1: 19세기 후반 정치 마당")
st.markdown("""
갑신정변 직전, 조선을 둘러싼 복잡한 권력 관계를 퀴즈로 풀어봅시다.
**5문제를 모두 풀어야** 숨겨진 권력 지도가 나타납니다!
""")
st.divider()

# 화면 분할 (왼쪽: 퀴즈 / 오른쪽: 시각화 안내)
col_quiz, col_viz = st.columns([1, 1.5])

# --------------------------------------------------------------------------
# [Left Column] 단계별 퀴즈 로직
# --------------------------------------------------------------------------
with col_quiz:
    # 퀴즈 데이터 (질문, 보기, 정답, 해설)
    quiz_data = {
        1: {
            "q": "Q1. 고종의 아버지 '흥선대원군'과 부인 '명성황후(민씨 세력)'의 사이는 어땠을까요?",
            "options": ["① 우리는 한 가족! 사이좋게 조선을 다스리자.", "② 서로 권력을 잡으려고 다투는 라이벌!"],
            "correct": "② 서로 권력을 잡으려고 다투는 라이벌!",
            "explanation": "흥선대원군은 쫓겨났지만 여전히 힘이 세고, 명성황후는 시아버지와 대립하고 있어요."
        },
        2: {
            "q": "Q2. 임오군란을 진압해 준 대가로, 당시 조선에 군대를 두고 간섭하던 나라는?",
            "options": ["① 청나라", "② 미국"],
            "correct": "① 청나라",
            "explanation": "당시 조선 정부(민씨 정권)는 이 나라의 말을 아주 잘 들어야 했어요."
        },
        3: {
            "q": "Q3. 당시 권력을 잡은 '민씨 정권'과 김홍집 같은 '온건 개화파'의 관계는?",
            "options": ["① 서로 싫어하는 원수 사이 (개화 반대!)", "② 우린 파트너! (청나라와 친하게 지내며 천천히 바꾸자)"],
            "correct": "② 우린 파트너! (청나라와 친하게 지내며 천천히 바꾸자)",
            "explanation": "민씨 정권은 청나라의 보호 아래 천천히 개화하고 싶어 했어요."
        },
        4: {
            "q": "Q4. 청나라를 밀어내고 조선의 새로운 주인이 되고 싶어 기회를 엿보던 나라는?",
            "options": ["① 미국", "② 일본"],
            "correct": "② 일본",
            "explanation": "이 나라는 조선을 차지하기 위해 청나라와 계속 눈치 싸움을 하고 있었어요."
        },
        5: {
            "q": "Q5. 일본 공사가 김옥균에게 은밀하게 건넨 제안은?",
            "options": ["① 우리랑 사이좋게 지내자.", "② 너희가 청나라를 몰아내면, 우리가 군대와 돈을 빌려줄게."],
            "correct": "② 너희가 청나라를 몰아내면, 우리가 군대와 돈을 빌려줄게.",
            "explanation": "일본은 김옥균을 이용해 청나라 세력을 조선에서 몰아내려는 속셈이 있었답니다."
        }
    }

    # 퀴즈 진행 중일 때 (1~5단계)
    if not st.session_state['quiz_finished']:
        st.subheader(f"🕵️ 권력 관계 탐구 퀴즈 ({st.session_state['step']}/5)")
        current_q = quiz_data[st.session_state['step']]
        
        with st.form(key=f"quiz_form_{st.session_state['step']}"):
            st.markdown(f"**{current_q['q']}**")
            choice = st.radio("정답을 선택하세요:", current_q["options"], index=None)
            submit_btn = st.form_submit_button("정답 확인")
            
            if submit_btn:
                if choice: # 선택을 했을 때만 로직 실행
                    st.session_state['show_next'] = True # 다음 버튼 활성화
                    
                    if choice == current_q["correct"]:
                        st.success("✅ 정답입니다!")
                        st.info(f"💡 해설: {current_q['explanation']}")
                    else:
                        st.error("❌ 오답입니다.")
                        st.warning(f"💡 정답 및 해설: 정답은 **'{current_q['correct']}'** 입니다.\n\n{current_q['explanation']}")
                else:
                    st.warning("보기를 선택해주세요.")

        # '다음 문제' 버튼 (정답 확인을 눌러야 나타남)
        if st.session_state['show_next']:
            if st.session_state['step'] < 5:
                if st.button("다음 문제 풀기 ➡️"):
                    st.session_state['step'] += 1
                    st.session_state['show_next'] = False
                    st.rerun()
            else:
                if st.button("🎉 권력 관계 한 번에 보기"):
                    st.session_state['quiz_finished'] = True
                    st.rerun()

    # 모든 퀴즈 완료 시 (왼쪽 화면)
    else:
        st.success("🎉 모든 퀴즈를 완료했습니다!")
        st.write("오른쪽 화면에서 19세기 후반 조선의 **진짜 권력 지도**가 나타났습니다.")
        st.markdown("---")
        if st.button("🔄 처음부터 다시 풀기"):
            st.session_state['step'] = 1
            st.session_state['quiz_finished'] = False
            st.session_state['show_next'] = False
            st.rerun()

# --------------------------------------------------------------------------
# [Right Column] 권력 관계 시각화 (Graph) - 퀴즈 완료 전에는 숨김
# --------------------------------------------------------------------------
with col_viz:
    st.subheader("📊 19세기 후반 조선의 권력 지도")

    if st.session_state['quiz_finished']:
        # [상태 B] 퀴즈 완료: 권력의 크기와 관계가 드러남!
        
        nodes = []
        # (1) 노드 정의
        nodes.append(Node(id="Qing", label="청나라", size=50, shape="circularImage", image=IMAGE_URLS["청나라"]))
        nodes.append(Node(id="Min", label="민씨 정권\n(명성황후)", size=45, shape="circularImage", image=IMAGE_URLS["민씨정권"]))
        nodes.append(Node(id="Japan", label="일본", size=40, shape="circularImage", image=IMAGE_URLS["일본"]))
        nodes.append(Node(id="Kim", label="김옥균\n(급진개화파)", size=25, shape="circularImage", image=IMAGE_URLS["김옥균"]))
        nodes.append(Node(id="Gojong", label="고종", size=25, shape="circularImage", image=IMAGE_URLS["고종"]))
        nodes.append(Node(id="Moderate", label="온건개화파\n(김홍집)", size=30, shape="circularImage", image=IMAGE_URLS["온건개화파"]))

        # (2) 엣지 정의
        edges = []
        edges.append(Edge(source="Qing", target="Min", label="간섭/보호", color="#0000FF", width=3))
        edges.append(Edge(source="Min", target="Moderate", label="협력", color="#0000FF"))
        edges.append(Edge(source="Kim", target="Japan", label="지원 약속", color="#0000FF", dashes=True))
        edges.append(Edge(source="Kim", target="Qing", label="타도 대상", color="#FF0000", width=4))
        edges.append(Edge(source="Kim", target="Min", label="대립", color="#FF0000", width=3))
        edges.append(Edge(source="Qing", target="Japan", label="조선 지배권 다툼", color="#FF0000", dashes=True))
        edges.append(Edge(source="Kim", target="Gojong", label="개혁 설득", color="green"))

        # 그래프 설정
        config = Config(
            width=700,
            height=600,
            directed=True, 
            physics=True, 
            hierarchical=False,
            nodeHighlightBehavior=True,
            highlightColor="#F7A7A6",
            collapsible=False
        )

        return_value = agraph(nodes=nodes, edges=edges, config=config)

        st.info("""
        💡 **시각화 해석하기**
        * **노드 크기:** 청나라와 민씨 정권의 점이 매우 크죠? 당시 권력을 장악하고 있었음을 의미합니다. 반면 김옥균과 고종은 상대적으로 힘이 약했습니다.
        * **빨간 선 (대립):** 김옥균은 거대한 청나라, 그리고 그들과 손잡은 민씨 정권과 싸워야 했습니다.
        * **파란 선 (협력):** 힘이 부족했던 김옥균은 결국 일본의 손을 잡는 선택을 하게 됩니다.
        """)

    else:
        # [상태 A] 퀴즈 진행 중: 그래프 숨김 (안내 메시지만 표시)
        st.info("👈 왼쪽의 퀴즈를 모두 풀면 권력 지도가 나타납니다.")
        st.image("https://cdn-icons-png.flaticon.com/512/610/610333.png", width=100, caption="잠겨있음") # 잠금 아이콘 예시
