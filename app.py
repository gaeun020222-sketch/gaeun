import streamlit as st
# 그래프 시각화를 위한 외부 라이브러리 (노드와 엣지 생성)
from streamlit_agraph import agraph, Node, Edge, Config

# 1. 페이지 기본 설정
# 학생들에게 보여질 웹페이지의 제목과 레이아웃(넓게 보기)을 설정합니다.
st.set_page_config(page_title="19세기 후반 정치 마당", layout="wide")

# --------------------------------------------------------------------------
# [설정] 이미지 URL 관리
# 시각화 노드에 사용할 역사적 인물 및 국가의 이미지 주소를 딕셔너리로 관리합니다.
# --------------------------------------------------------------------------
IMAGE_URLS = {
    "청나라": "https://i.ibb.co/1fXH5Ffb/chung.png", # 청나라 국기
    "일본": "https://i.ibb.co/KchxkbQJ/japan.png",     # 일본 국기
    "민씨정권": "https://i.ibb.co/tpyZWYgH/image.png",   # 명성황후
    "고종": "https://i.ibb.co/fYpjpVJ2/image.png",       # 고종 황제
    "김옥균": "https://i.ibb.co/1jFg9C6/image.png",     # 급진개화파 대표
    "온건개화파": "https://i.ibb.co/BKGYrkf3/image.png",  # 김홍집
    "흥선대원군": "https://i.ibb.co/PsJwdCrK/image.png"  # (퀴즈용 참고 이미지)
}

# --------------------------------------------------------------------------
# [초기화] 세션 상태 (Session State) 설정
# Streamlit은 상호작용 시 코드가 재실행되므로, 문제 풀이 단계와 정답 여부를 기억하기 위해 세션 상태를 사용합니다.
# --------------------------------------------------------------------------
if 'step' not in st.session_state:
    st.session_state['step'] = 1  # 현재 학생이 풀고 있는 퀴즈 번호 (1~5번)
if 'quiz_finished' not in st.session_state:
    st.session_state['quiz_finished'] = False # 모든 퀴즈를 다 풀었는지 확인하는 변수
if 'show_next' not in st.session_state:
    st.session_state['show_next'] = False # 정답 확인 후 '다음 문제' 버튼을 보여줄지 결정하는 변수

# --------------------------------------------------------------------------
# [UI] 메인 화면 구성
# --------------------------------------------------------------------------
st.title("🏛️ 탭 1: 19세기 후반 정치 마당")
# 학습 목표와 활동 안내 메시지 출력
st.markdown("""
갑신정변 직전, 조선을 둘러싼 복잡한 권력 관계를 퀴즈로 풀어봅시다.
**5문제를 모두 풀어야** 숨겨진 진짜 권력 지도가 나타납니다!
""")
st.divider()

# 화면을 좌우로 분할하여 왼쪽은 퀴즈, 오른쪽은 시각화 결과가 보이도록 배치
col_quiz, col_viz = st.columns([1, 1.5])

# --------------------------------------------------------------------------
# [Left Column] 단계별 퀴즈 로직 구현
# --------------------------------------------------------------------------
with col_quiz:
    # 퀴즈 데이터베이스 (질문, 보기, 정답, 교육적 해설 포함)
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

    # 아직 퀴즈를 다 풀지 않았을 때 (문제 풀이 진행 중)
    if not st.session_state['quiz_finished']:
        st.subheader(f"🕵️ 권력 관계 탐구 퀴즈 ({st.session_state['step']}/5)")
        
        # 현재 단계에 맞는 문제 데이터를 가져옴
        current_q = quiz_data[st.session_state['step']]
        
        # 폼(Form)을 사용하여 사용자가 선택 후 '확인' 버튼을 눌러야 제출되도록 함
        with st.form(key=f"quiz_form_{st.session_state['step']}"):
            st.markdown(f"**{current_q['q']}**")
            choice = st.radio("정답을 선택하세요:", current_q["options"], index=None)
            submit_btn = st.form_submit_button("정답 확인")
            
            # 정답 확인 버튼을 눌렀을 때의 로직
            if submit_btn:
                if choice: # 보기를 선택했을 경우
                    st.session_state['show_next'] = True # 다음 버튼을 활성화
                    
                    # 정답 여부 판단 및 피드백 제공
                    if choice == current_q["correct"]:
                        st.success("✅ 정답입니다!")
                        st.info(f"💡 해설: {current_q['explanation']}")
                    else:
                        st.error("❌ 오답입니다.")
                        # 오답일 경우 정답과 해설을 함께 보여주어 학습을 유도함
                        st.warning(f"💡 정답 및 해설: 정답은 **'{current_q['correct']}'** 입니다.\n\n{current_q['explanation']}")
                else:
                    st.warning("보기를 선택해주세요.") # 선택 없이 버튼을 누른 경우 경고

        # 정답/오답 확인 후 '다음 문제'로 넘어가는 버튼 표시
        if st.session_state['show_next']:
            if st.session_state['step'] < 5:
                # 1~4번 문제일 경우: 다음 문제로 이동 (step 증가)
                if st.button("다음 문제 풀기 ➡️"):
                    st.session_state['step'] += 1
                    st.session_state['show_next'] = False
                    st.rerun() # 화면을 새로고침하여 다음 문제 표시
            else:
                # 마지막 5번 문제일 경우: 결과 보기 버튼 표시
                if st.button("🎉 권력 관계 한 번에 보기"):
                    st.session_state['quiz_finished'] = True # 퀴즈 완료 상태로 변경
                    st.rerun()

    # 모든 퀴즈를 완료했을 때 (완료 메시지 및 다시 풀기 옵션)
    else:
        st.success("🎉 모든 퀴즈를 완료했습니다!")
        st.write("오른쪽 화면에서 19세기 후반 조선의 **진짜 권력 지도**가 나타났습니다.")
        st.markdown("---")
        # 다시 학습하고 싶은 학생을 위한 리셋 버튼
        if st.button("🔄 처음부터 다시 풀기"):
            st.session_state['step'] = 1
            st.session_state['quiz_finished'] = False
            st.session_state['show_next'] = False
            st.rerun()

# --------------------------------------------------------------------------
# [Right Column] 권력 관계 시각화 (Graph)
# 퀴즈를 다 풀기 전에는 그래프를 숨겨두어 학습 동기를 유발합니다.
# --------------------------------------------------------------------------
with col_viz:
    st.subheader("📊 19세기 후반 조선의 권력 지도")

    if st.session_state['quiz_finished']:
        # [학습 완료 상태] 퀴즈 내용을 바탕으로 구성된 '진짜 권력 관계도'를 보여줍니다.
        
        nodes = []
        # (1) 노드(인물/국가) 정의: size 속성을 통해 권력의 크기를 시각적으로 표현
        # 청나라(50)와 민씨정권(45)을 크게 설정하여 당시의 막강한 권력을 강조
        nodes.append(Node(id="Qing", label="청나라", size=50, shape="circularImage", image=IMAGE_URLS["청나라"]))
        nodes.append(Node(id="Min", label="민씨 정권\n(명성황후)", size=45, shape="circularImage", image=IMAGE_URLS["민씨정권"]))
        nodes.append(Node(id="Japan", label="일본", size=40, shape="circularImage", image=IMAGE_URLS["일본"]))
        
        # 김옥균(25)과 고종(25)은 작게 설정하여 개혁파의 입지가 좁았음을 표현
        nodes.append(Node(id="Kim", label="김옥균\n(급진개화파)", size=25, shape="circularImage", image=IMAGE_URLS["김옥균"]))
        nodes.append(Node(id="Gojong", label="고종", size=25, shape="circularImage", image=IMAGE_URLS["고종"]))
        nodes.append(Node(id="Moderate", label="온건개화파\n(김홍집)", size=30, shape="circularImage", image=IMAGE_URLS["온건개화파"]))

        # (2) 엣지(관계) 정의: color와 스타일을 통해 관계의 성격을 표현
        edges = []
        # 파란색 실선: 강력한 간섭 또는 협력 관계
        edges.append(Edge(source="Qing", target="Min", label="간섭/보호", color="#0000FF", width=3))
        edges.append(Edge(source="Min", target="Moderate", label="협력", color="#0000FF"))
        # 파란색 점선: 은밀한 약속
        edges.append(Edge(source="Kim", target="Japan", label="지원 약속", color="#0000FF", dashes=True))
        # 빨간색 굵은 선: 타도해야 할 적대 관계
        edges.append(Edge(source="Kim", target="Qing", label="타도 대상", color="#FF0000", width=4))
        edges.append(Edge(source="Kim", target="Min", label="대립", color="#FF0000", width=3))
        # 국가 간 라이벌 관계
        edges.append(Edge(source="Qing", target="Japan", label="조선 지배권 다툼", color="#FF0000", dashes=True))
        # 초록색: 설득과 동조
        edges.append(Edge(source="Kim", target="Gojong", label="개혁 설득", color="green"))

        # 그래프의 물리 엔진 및 스타일 설정
        config = Config(
            width=700,
            height=600,
            directed=True, # 화살표 방향 표시
            physics=True,  # 노드 간의 밀고 당기는 물리 효과 적용
            hierarchical=False,
            nodeHighlightBehavior=True,
            highlightColor="#F7A7A6",
            collapsible=False
        )

        # 설정한 노드와 엣지를 바탕으로 그래프 렌더링
        return_value = agraph(nodes=nodes, edges=edges, config=config)

        # 시각화 자료에 대한 해석 가이드 제공
        st.info("""
        💡 **시각화 해석하기**
        * **노드 크기:** 청나라와 민씨 정권의 점이 매우 크죠? 당시 권력을 장악하고 있었음을 의미합니다. 반면 김옥균과 고종은 상대적으로 힘이 약했습니다.
        * **빨간 선 (대립):** 김옥균은 거대한 청나라, 그리고 그들과 손잡은 민씨 정권과 싸워야 했습니다.
        * **파란 선 (협력):** 힘이 부족했던 김옥균은 결국 일본의 손을 잡는 선택을 하게 됩니다.
        """)

    else:
        # [학습 진행 중 상태] 퀴즈를 풀기 전에는 그래프를 보여주지 않음 (잠금 화면)
        st.info("👈 왼쪽의 퀴즈를 모두 풀면 권력 지도가 나타납니다.")
        st.image("https://cdn-icons-png.flaticon.com/512/610/610333.png", width=100, caption="잠겨있음")
    # ... (탭 1 코드는 생략, 위쪽에 이어짐) ...
# --------------------------------------------------------------------------
# [탭 2 구현] 상대 개화파와 채팅하기 (Historical Persona Chatbot)
# 목적: 학생들이 딱딱한 텍스트 대신, 역사적 인물(페르소나)과 상호작용하며
#       당시의 정치적 입장과 사상을 맥락적으로 이해하도록 돕기 위함입니다.
# --------------------------------------------------------------------------
with tab2:
    # 학생들에게 활동의 목표와 배경을 설명하는 헤더
    st.header("💬 탭 2: 조선의 미래를 논하다 - 개화파와의 대화")
    st.markdown("""
    1884년의 조선, 두 명의 정치가가 서로 다른 미래를 꿈꾸고 있습니다.
    **김홍집(온건개화파)**과 **김옥균(급진개화파)** 중 한 명을 선택하여 그들의 속마음을 들어보세요.
    """)
    st.divider()

    # 화면 레이아웃 분할 (좌측: 인물 선택 / 우측: 대화창)
    # 목적: 인물 정보를 선택하는 영역과 대화하는 영역을 구분하여 집중도를 높임
    col_left, col_right = st.columns([1, 2])
    
    # [좌측 영역] 대화 상대(페르소나) 선택
    with col_left:
        st.subheader("🗣️ 대화 상대 선택")
        
        # 라디오 버튼을 통해 학생이 대화하고 싶은 역사적 인물을 선택하게 함
        # 주의: 여기 적힌 이름("김홍집 (온건개화파)")이 아래 questions 딕셔너리의 키와 정확히 일치해야 합니다.
        speaker = st.radio(
            "누구와 이야기를 나누시겠습니까?",
            ("김홍집 (온건개화파)", "김옥균 (급진개화파)")
        )
        
        # 선택된 인물에 따라 시각 자료(사진)와 핵심 사상(CK)을 보여줌
        # 결과: 학생들은 대화 전에 해당 인물의 기본 입장을 시각적으로 인지하게 됨
        if speaker == "김홍집 (온건개화파)":
            st.image("https://i.ibb.co/BKGYrkf3/image.png", width=200) # 김홍집 이미지
            st.info("""
            **김홍집**
            - 소속: 온건개화파
            - 입장: "청나라와 좋은 관계를 유지하며, 조선의 전통을 지키되 서양 기술만 받아들여야 합니다." (동도서기)
            """)
        else:
            st.image("https://i.ibb.co/1jFg9C6/image.png", width=200) # 김옥균 이미지
            st.error("""
            **김옥균**
            - 소속: 급진개화파
            - 입장: "청나라의 간섭을 끊고, 일본처럼 기술뿐만 아니라 제도와 사상까지 싹 바꿔야 합니다!" (문명개화)
            """)

    # [우측 영역] 챗봇 인터페이스 구현
    with col_right:
        st.subheader(f"{speaker}님과의 대화")
        
        # [세션 상태 관리] 대화 기록 유지 및 인물 변경 시 초기화
        # 목적: 인물이 바뀌면 이전 대화 내용이 섞이지 않도록 리셋하여 혼란을 방지함
        if "current_speaker" not in st.session_state:
            st.session_state["current_speaker"] = speaker
        
        if st.session_state["current_speaker"] != speaker:
            st.session_state["messages"] = [] # 대화 기록 삭제
            st.session_state["current_speaker"] = speaker # 현재 화자 업데이트
            
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

        # (1) 대화 기록 출력
        # 결과: 저장된 대화 내용을 화면에 표시하여 대화의 흐름을 유지함
        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # (2) 질문 선택지 제공 (Scaffolding)
        # 목적: 학생들이 무엇을 질문해야 할지 모르는 상황을 방지하고, 
        #       수업 목표(CK)에 맞는 핵심 질문을 하도록 유도하는 비계(Scaffolding) 역할
        st.markdown("---")
        st.write("**어떤 것이 궁금한가요? (버튼을 눌러 질문하세요)**")
        
        # 인물별 맞춤형 질문 리스트 데이터
        # 주의: 이 딕셔너리의 키(Key)가 위에서 설정한 speaker 변수의 값과 정확히 같아야 KeyError가 안 납니다.
        questions = {
            "김홍집 (온건개화파)": [
                "청나라와의 관계는 어떻게 해야 합니까?",
                "개화(변화)의 속도는 어때야 합니까?",
                "김옥균의 생각에 대해 어떻게 생각하시나요?"
            ],
            "김옥균 (급진개화파)": [
                "왜 청나라를 그토록 싫어하십니까?",
                "일본의 힘을 빌리는 것이 위험하지 않나요?",
                "어떤 나라를 만들고 싶으신가요?"
            ]
        }
        
        # 질문 버튼을 가로로 배치하여 선택 용이성 높임
        btn_cols = st.columns(3)
        
        # 현재 선택된 인물(speaker)에 맞는 질문들을 가져와서 버튼으로 만듦
        for idx, q in enumerate(questions[speaker]):
            # 버튼을 누르면 해당 질문이 채팅창에 입력되고 AI 답변이 생성됨
            if btn_cols[idx].button(f"Q{idx+1}. {q}"):
                # 사용자 질문을 채팅 기록에 추가
                st.session_state["messages"].append({"role": "user", "content": q})
                
                # [AI 답변 생성 로직] (Rule-based)
                # 실제 LLM 연동 대신, 역사적 사실(CK)에 기반한 정해진 답변을 출력하여 
                # Hallucination(거짓 정보)을 방지하고 교육적 정확성을 확보함
                answer = ""
                if speaker == "김홍집 (온건개화파)":
                    if idx == 0:
                        answer = "청나라는 오랫동안 우리를 보호해 준 큰 나라입니다. 임오군란 때도 도와주지 않았습니까? 그들과 척을 져서는 안 됩니다."
                    elif idx == 1:
                        answer = "급할수록 체하는 법입니다. 우리의 훌륭한 정신과 도덕은 지키고, 서양의 편리한 기술만 천천히 받아들이면 됩니다. (동도서기)"
                    elif idx == 2:
                        answer = "그는 너무 급해요! 일본을 등에 업고 나라를 뒤집으려 하다니... 그러다간 조선이 큰 혼란에 빠질 겁니다."
                else: # 김옥균
                    if idx == 0:
                        answer = "청나라는 사사건건 우리 내정에 간섭하며 발목을 잡고 있습니다! 그들의 그늘에서 벗어나지 않으면 조선은 영원히 약소국으로 남을 겁니다."
                    elif idx == 1:
                        answer = "위험할 수도 있겠지요. 하지만 이대로 청나라에게 먹히는 것보단 낫습니다. 이이제이(오랑캐로 오랑캐를 제압한다)의 심정으로 일본을 이용하는 것입니다."
                    elif idx == 2:
                        answer = "신분 차별 없는 평등한 세상, 능력 있는 사람이 대우받는 자주적인 독립 국가를 만들고 싶습니다!"

                # AI(페르소나)의 답변을 채팅 기록에 추가
                st.session_state["messages"].append({"role": "assistant", "content": answer})
                # 화면을 새로고침하여 업데이트된 대화 내용을 즉시 보여줌
                st.rerun()

    # 3. 학습 흐름 연결 (Navigation)
    # 목적: 탭 2 활동이 끝나면 자연스럽게 다음 단계(탭 3)로 넘어가도록 유도하는 버튼
    st.divider()
    col_next = st.columns([6, 1]) # 오른쪽 끝에 버튼 배치
    with col_next[1]:
        if st.button("다음 미션으로 ➡️", key="go_to_tab3"):
            # 실제로는 탭 전환 로직이 필요하나, 현재는 안내 메시지로 대체
            st.info("탭 3: '갑신정변 3일' 페이지로 이동합니다! (실제 앱에서는 탭이 자동 전환되도록 구현 가능)")
