import streamlit as st
# 그래프 시각화를 위한 라이브러리 (관계도 표현)
from streamlit_agraph import agraph, Node, Edge, Config

# 1. 페이지 기본 설정
# 목적: 웹페이지의 제목과 레이아웃을 설정하여 학습 환경을 조성함
st.set_page_config(page_title="19세기 후반 정치 마당", layout="wide")

# --------------------------------------------------------------------------
# [공통 설정] 이미지 URL 관리
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
# 목적: 탭을 이동하거나 버튼을 눌러도 학생의 문제 풀이 현황과 대화 기록이 지워지지 않게 함
# --------------------------------------------------------------------------
if 'step' not in st.session_state:
    st.session_state['step'] = 1  # 탭1: 현재 퀴즈 번호
if 'quiz_finished' not in st.session_state:
    st.session_state['quiz_finished'] = False # 탭1: 퀴즈 완료 여부
if 'show_next' not in st.session_state:
    st.session_state['show_next'] = False # 탭1: 다음 문제 버튼 표시 여부
if "messages" not in st.session_state:
    st.session_state["messages"] = [] # 탭2: 채팅 기록 저장

# --------------------------------------------------------------------------
# [메인 UI] 탭 구성
# 목적: 학습 단계를 3단계로 나누어(정치 상황 -> 인물 대화 -> 사건 전개) 
#       학생들이 단계별로 역사를 깊이 있게 탐구하도록 구조화함 (Scaffolding)
# --------------------------------------------------------------------------
st.title("🏛️ AI 역사 탐구: 갑신정변의 재구성")
tab1, tab2, tab3 = st.tabs(["🏛️ 탭 1: 정치 마당", "💬 탭 2: 개화파와 대화", "⏳ 탭 3: 갑신정변 3일"])

# ==========================================================================
# [탭 1] 19세기 후반 정치 마당 (퀴즈 + 관계도)
# ==========================================================================
with tab1:
    st.header("🕵️ 19세기 후반, 조선의 권력 지도는?")
    st.markdown("퀴즈를 풀며 당시 복잡했던 나라 안팎의 권력 관계를 파헤쳐 봅시다.")
    st.divider()

    col_quiz, col_viz = st.columns([1, 1.5])

    # [좌측] 퀴즈 영역
    with col_quiz:
        # 퀴즈 데이터 (질문, 보기, 정답, 해설)
        quiz_data = {
            1: {
                "q": "Q1. 고종의 아버지 '흥선대원군'과 부인 '명성황후(민씨 세력)'의 사이는?",
                "options": ["① 우리는 한 가족! 사이좋게 지내자.", "② 서로 권력을 잡으려고 다투는 라이벌!"],
                "correct": "② 서로 권력을 잡으려고 다투는 라이벌!",
                "explanation": "흥선대원군은 쫓겨났지만 여전히 힘이 세고, 명성황후는 시아버지와 대립했어요."
            },
            2: {
                "q": "Q2. 임오군란을 진압해 준 대가로 조선에 간섭하던 나라는?",
                "options": ["① 청나라", "② 미국"],
                "correct": "① 청나라",
                "explanation": "당시 민씨 정권은 청나라의 말을 아주 잘 들어야 했습니다."
            },
            3: {
                "q": "Q3. 민씨 정권과 김홍집(온건 개화파)의 관계는?",
                "options": ["① 서로 싫어하는 원수", "② 우린 파트너! (청나라와 친하게 지내며 천천히)"],
                "correct": "② 우린 파트너! (청나라와 친하게 지내며 천천히)",
                "explanation": "민씨 정권은 청나라의 보호 아래 천천히 개화하고 싶어 했어요."
            },
            4: {
                "q": "Q4. 청나라를 밀어내고 조선을 차지하려던 나라는?",
                "options": ["① 미국", "② 일본"],
                "correct": "② 일본",
                "explanation": "일본은 청나라와 계속 눈치 싸움을 하고 있었어요."
            },
            5: {
                "q": "Q5. 일본이 김옥균에게 건넨 은밀한 제안은?",
                "options": ["① 사이좋게 지내자.", "② 청나라를 몰아내면 군대와 돈을 빌려줄게."],
                "correct": "② 청나라를 몰아내면 군대와 돈을 빌려줄게.",
                "explanation": "일본은 김옥균을 이용해 청나라 세력을 몰아내려는 속셈이 있었죠."
            }
        }

        # 퀴즈 진행 로직
        if not st.session_state['quiz_finished']:
            st.subheader(f"문제 {st.session_state['step']} / 5")
            current_q = quiz_data[st.session_state['step']]
            
            with st.form(key=f"quiz_form_{st.session_state['step']}"):
                st.markdown(f"**{current_q['q']}**")
                choice = st.radio("정답 선택:", current_q["options"], index=None)
                submit_btn = st.form_submit_button("정답 확인")
                
                if submit_btn:
                    if choice:
                        st.session_state['show_next'] = True
                        if choice == current_q["correct"]:
                            st.success("✅ 정답입니다!")
                            st.info(f"해설: {current_q['explanation']}")
                        else:
                            st.error("❌ 오답입니다.")
                            st.warning(f"정답: {current_q['correct']}\n\n해설: {current_q['explanation']}")
                    else:
                        st.warning("보기를 선택해주세요.")

            # 다음 버튼
            if st.session_state['show_next']:
                if st.session_state['step'] < 5:
                    if st.button("다음 문제 ➡️"):
                        st.session_state['step'] += 1
                        st.session_state['show_next'] = False
                        st.rerun()
                else:
                    if st.button("🎉 권력 지도 확인하기"):
                        st.session_state['quiz_finished'] = True
                        st.rerun()
        else:
            st.success("퀴즈 완료! 오른쪽에서 권력 지도를 확인하세요.")
            if st.button("🔄 퀴즈 다시 풀기"):
                st.session_state['step'] = 1
                st.session_state['quiz_finished'] = False
                st.session_state['show_next'] = False
                st.rerun()

    # [우측] 시각화 영역
    with col_viz:
        st.subheader("📊 권력 관계 시각화")
        if st.session_state['quiz_finished']:
            # 결과: 퀴즈 완료 시 노드 크기와 색상으로 권력 관계를 시각화함
            nodes = [
                Node(id="Qing", label="청나라", size=50, shape="circularImage", image=IMAGE_URLS["청나라"]),
                Node(id="Min", label="민씨 정권", size=45, shape="circularImage", image=IMAGE_URLS["민씨정권"]),
                Node(id="Japan", label="일본", size=40, shape="circularImage", image=IMAGE_URLS["일본"]),
                Node(id="Kim", label="김옥균", size=25, shape="circularImage", image=IMAGE_URLS["김옥균"]),
                Node(id="Gojong", label="고종", size=25, shape="circularImage", image=IMAGE_URLS["고종"]),
                Node(id="Moderate", label="온건개화파", size=30, shape="circularImage", image=IMAGE_URLS["온건개화파"])
            ]
            edges = [
                Edge(source="Qing", target="Min", label="간섭", color="blue", width=3),
                Edge(source="Min", target="Moderate", label="협력", color="blue"),
                Edge(source="Kim", target="Japan", label="약속", color="blue", dashes=True),
                Edge(source="Kim", target="Qing", label="타도", color="red", width=4),
                Edge(source="Kim", target="Min", label="대립", color="red", width=3),
                Edge(source="Qing", target="Japan", label="견제", color="red", dashes=True),
                Edge(source="Kim", target="Gojong", label="설득", color="green")
            ]
            config = Config(width=700, height=600, directed=True, physics=True, nodeHighlightBehavior=True, highlightColor="#F7A7A6")
            agraph(nodes=nodes, edges=edges, config=config)
            
            st.info("💡 **해석:** 청나라(큰 점)의 간섭이 심하고, 김옥균(작은 점)은 이에 맞서기 위해 일본과 손을 잡은 위태로운 상황입니다.")
        else:
            st.info("👈 왼쪽 퀴즈를 모두 풀어야 지도가 나타납니다.")
            st.image("https://cdn-icons-png.flaticon.com/512/610/610333.png", width=100)


# ==========================================================================
# [탭 2] 상대 개화파와 채팅하기 (페르소나 챗봇)
# ==========================================================================
with tab2:
    st.header("💬 조선의 미래를 논하다 - 개화파와의 대화")
    st.markdown("""
    서로 다른 미래를 꿈꾸는 **김홍집(온건개화파)**과 **김옥균(급진개화파)**.
    한 명을 선택하여 그들의 속마음을 들어보고, 역사적 입장을 이해해 봅시다.
    """)
    st.divider()

    col_left, col_right = st.columns([1, 2])
    
    # [좌측] 인물 선택
    with col_left:
        st.subheader("🗣️ 대화 상대 선택")
        # 목적: 학습자가 대화하고 싶은 대상을 주도적으로 선택하게 함
        speaker = st.radio(
            "누구와 대화하시겠습니까?",
            ("김홍집 (온건개화파)", "김옥균 (급진개화파)")
        )
        
        # 선택한 인물의 기본 정보(CK) 표시
        if speaker == "김홍집 (온건개화파)":
            st.image(IMAGE_URLS["온건개화파"], width=200)
            st.info("**김홍집**: 청나라와 친하게 지내며, 서양의 기술만 천천히 받아들여야 합니다.")
        else:
            st.image(IMAGE_URLS["김옥균"], width=200)
            st.error("**김옥균**: 청나라의 간섭을 끊고, 일본처럼 법과 제도까지 빠르게 바꿔야 합니다!")

    # [우측] 채팅 인터페이스
    with col_right:
        st.subheader(f"{speaker}님과의 대화")
        
        # 인물이 바뀌면 대화 기록 초기화
        if "current_speaker" not in st.session_state:
            st.session_state["current_speaker"] = speaker
        if st.session_state["current_speaker"] != speaker:
            st.session_state["messages"] = []
            st.session_state["current_speaker"] = speaker

        # 대화 기록 표시
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # 질문 선택지 제공 (Scaffolding)
        # 목적: 학생들이 핵심적인 역사 쟁점에 대해 질문하도록 유도함
        st.markdown("---")
        st.caption("👇 궁금한 내용을 선택하여 질문해보세요.")
        
        questions = {
            "김홍집 (온건개화파)": [
                "청나라와의 관계는 어떻게 해야 합니까?",
                "개화의 속도는 어때야 합니까?",
                "김옥균의 생각에 대해 어떻게 생각하시나요?"
            ],
            "김옥균 (급진개화파)": [
                "왜 청나라를 그토록 싫어하십니까?",
                "일본의 힘을 빌리는 것이 위험하지 않나요?",
                "어떤 나라를 만들고 싶으신가요?"
            ]
        }
        
        btn_cols = st.columns(3)
        for idx, q in enumerate(questions[speaker]):
            if btn_cols[idx].button(f"Q{idx+1}. {q}"):
                # 사용자 질문 추가
                st.session_state["messages"].append({"role": "user", "content": q})
                
                # AI 답변 (CK 기반의 Rule-based 답변)
                # 목적: 역사적 사실에 근거한 정확한 답변을 제공하여 오개념 방지
                answer = ""
                if speaker == "김홍집 (온건개화파)":
                    if idx == 0: answer = "청나라는 우리를 보호해 준 큰 나라입니다. 그들과 척을 져서는 안 됩니다."
                    elif idx == 1: answer = "급할수록 체합니다. 우리의 정신은 지키고 기술만 천천히 받아들여야 합니다."
                    elif idx == 2: answer = "그는 너무 위험합니다! 외세를 등에 업고 나라를 뒤집으려 하다니요."
                else: # 김옥균
                    if idx == 0: answer = "청나라는 사사건건 간섭만 합니다! 그들의 그늘에서 벗어나야 자주 독립국이 됩니다."
                    elif idx == 1: answer = "위험해도 어쩔 수 없습니다. 청나라를 몰아내기 위해 일본의 힘을 이용하는 것입니다."
                    elif idx == 2: answer = "신분 차별 없는 평등하고 능력 중심의 현대적인 나라를 만들고 싶습니다!"

                st.session_state["messages"].append({"role": "assistant", "content": answer})
                st.rerun()

    # 다음 탭 이동 버튼
    st.divider()
    if st.button("다음 미션으로 (갑신정변 3일) ➡️"):
        st.info("상단 탭에서 '⏳ 탭 3: 갑신정변 3일'을 클릭해주세요!")

# ==========================================================================
# [탭 3] 갑신정변 3일 (준비 중)
# ==========================================================================
with tab3:
    st.header("⏳ 운명의 3일: 갑신정변 시뮬레이션")
    st.info("이곳에는 3일간의 긴박한 사건 전개 과정이 들어갈 예정입니다.")
