import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import time

# 1. 페이지 기본 설정
# 목적: 웹페이지의 기본 레이아웃을 설정합니다.
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
# [상태 관리] 세션 스테이트 초기화
# 목적: 화면이 바뀌어도 학생의 학습 진행 상황(현재 페이지, 퀴즈 점수, 채팅 단계 등)을 기억하기 위함
# --------------------------------------------------------------------------
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'tab1' # 시작 페이지: tab1

# 탭 1용 변수
if 'step' not in st.session_state:
    st.session_state['step'] = 1
if 'quiz_finished' not in st.session_state:
    st.session_state['quiz_finished'] = False
if 'show_next' not in st.session_state:
    st.session_state['show_next'] = False

# 탭 2용 변수 (채팅)
if 'chat_role' not in st.session_state:
    st.session_state['chat_role'] = None # 학생이 선택한 역할
if 'chat_stage' not in st.session_state:
    st.session_state['chat_stage'] = 0 # 대화 진행 단계 (0:인사 ~ 5:종료)
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = [] # 채팅 기록

# --------------------------------------------------------------------------
# [페이지 1] 탭 1: 정치 마당 (퀴즈 + 시각화)
# --------------------------------------------------------------------------
def render_tab1():
    st.title("🏛️ 1단계: 19세기 후반, 조선의 권력 지도")
    st.markdown("퀴즈를 풀며 당시 복잡했던 나라 안팎의 권력 관계를 파헤쳐 봅시다.")
    st.divider()

    col_quiz, col_viz = st.columns([1, 1.5])

    # [좌측] 퀴즈 영역
    with col_quiz:
        quiz_data = {
            1: {"q": "Q1. 고종의 아버지 '흥선대원군'과 부인 '명성황후'의 사이는?", "options": ["① 우리는 한 가족!", "② 서로 권력을 잡으려고 다투는 라이벌!"], "correct": "② 서로 권력을 잡으려고 다투는 라이벌!", "expl": "흥선대원군은 쫓겨났지만 여전히 힘이 세고, 명성황후는 시아버지와 대립했어요."},
            2: {"q": "Q2. 임오군란을 진압해 준 대가로 조선에 간섭하던 나라는?", "options": ["① 청나라", "② 미국"], "correct": "① 청나라", "expl": "당시 민씨 정권은 청나라의 말을 아주 잘 들어야 했습니다."},
            3: {"q": "Q3. 민씨 정권과 김홍집(온건 개화파)의 관계는?", "options": ["① 서로 싫어하는 원수", "② 우린 파트너! (청나라와 친하게 지내며 천천히)"], "correct": "② 우린 파트너! (청나라와 친하게 지내며 천천히)", "expl": "민씨 정권은 청나라의 보호 아래 천천히 개화하고 싶어 했어요."},
            4: {"q": "Q4. 청나라를 밀어내고 조선을 차지하려던 나라는?", "options": ["① 미국", "② 일본"], "correct": "② 일본", "expl": "일본은 청나라와 계속 눈치 싸움을 하고 있었어요."},
            5: {"q": "Q5. 일본이 김옥균에게 건넨 은밀한 제안은?", "options": ["① 사이좋게 지내자.", "② 청나라를 몰아내면 군대와 돈을 빌려줄게."], "correct": "② 청나라를 몰아내면 군대와 돈을 빌려줄게.", "expl": "일본은 김옥균을 이용해 청나라 세력을 몰아내려는 속셈이 있었죠."}
        }

        if not st.session_state['quiz_finished']:
            st.subheader(f"문제 {st.session_state['step']} / 5")
            current_q = quiz_data[st.session_state['step']]
            
            with st.form(key=f"quiz_form_{st.session_state['step']}"):
                st.markdown(f"**{current_q['q']}**")
                choice = st.radio("정답 선택:", current_q["options"], index=None)
                submit_btn = st.form_submit_button("정답 확인")
                
                if submit_btn:
                    if choice == current_q["correct"]:
                        st.success("✅ 정답입니다!")
                        st.info(f"해설: {current_q['expl']}")
                        st.session_state['show_next'] = True
                    else:
                        st.error("❌ 오답입니다.")
                        st.warning(f"힌트: {current_q['expl']}")

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
            st.success("1단계 미션 성공! 오른쪽 권력 지도를 확인하세요.")

    # [우측] 시각화 영역
    with col_viz:
        st.subheader("📊 권력 관계 시각화")
        if st.session_state['quiz_finished']:
            # 노드와 엣지 설정 (이전과 동일)
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
            
            # [다음 탭으로 이동 버튼]
            st.divider()
            col_next_btn = st.columns([4, 1])
            with col_next_btn[1]:
                # 목적: 1단계 학습(CK)을 마치고 2단계 심화 학습(PK: 롤플레잉)으로 자연스럽게 유도
                if st.button("다음 미션 도전하기 ➡️", type="primary"):
                    st.session_state['current_page'] = 'tab2'
                    st.rerun()
        else:
            st.info("👈 왼쪽 퀴즈를 모두 풀어야 지도가 나타납니다.")
            st.image("https://cdn-icons-png.flaticon.com/512/610/610333.png", width=100)

# --------------------------------------------------------------------------
# [페이지 2] 탭 2: 개화파와 대화 (롤플레잉 챗봇)
# --------------------------------------------------------------------------
def render_tab2():
    st.title("💬 2단계: 역사 속으로 - 개화파와의 대화")
    st.markdown("당신은 이제 역사 속 인물이 되어, 상대방과 조선의 미래를 논하게 됩니다.")
    st.divider()

    # 1. 역할 선택 (아직 역할을 선택하지 않았을 때)
    if st.session_state['chat_role'] is None:
        st.subheader("🎭 당신은 누구입니까?")
        col1, col2 = st.columns(2)
        
        with col1:
            st.image(IMAGE_URLS["김옥균"], width=150)
            if st.button("나는 '김옥균' (급진개화파)"):
                st.session_state['chat_role'] = 'Kim_Ok'
                # 초기 멘트 설정 (상대방: 김홍집)
                st.session_state['chat_history'].append({"role": "assistant", "content": "안녕, 김옥균! 나는 김홍집이야."})
                st.session_state['chat_stage'] = 1
                st.rerun()
                
        with col2:
            st.image(IMAGE_URLS["온건개화파"], width=150)
            if st.button("나는 '김홍집' (온건개화파)"):
                st.session_state['chat_role'] = 'Kim_Hong'
                # 초기 멘트 설정 (상대방: 김옥균)
                st.session_state['chat_history'].append({"role": "assistant", "content": "반갑소, 김홍집 대감. 나는 김옥균이오."})
                st.session_state['chat_stage'] = 1
                st.rerun()

    # 2. 채팅 인터페이스 (역할 선택 후)
    else:
        # 현재 내 역할과 상대방 표시
        my_name = "김옥균" if st.session_state['chat_role'] == 'Kim_Ok' else "김홍집"
        opponent_name = "김홍집" if st.session_state['chat_role'] == 'Kim_Ok' else "김옥균"
        
        st.info(f"🎭 당신의 역할: **{my_name}** | 대화 상대: **{opponent_name}**")

        # 채팅 기록 표시
        for msg in st.session_state['chat_history']:
            with st.chat_message(msg['role']):
                st.write(msg['content'])

        # 사용자 입력 처리 (st.chat_input 사용)
        # 목적: 학생이 직접 텍스트를 입력하며 능동적으로 사고하게 함 (단순 클릭 X)
        if prompt := st.chat_input("메세지를 입력하세요..."):
            # 사용자 메세지 추가
            st.session_state['chat_history'].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # --- 챗봇 응답 로직 (Rule-based Scenario) ---
            # 목적: 스토리텔링 방식으로 역사적 맥락을 자연스럽게 전달하고, 학생의 답변 내용을 확인하여 피드백 제공
            
            stage = st.session_state['chat_stage']
            response = ""
            
            # [시나리오 A] 내가 김옥균일 때 (상대: 김홍집)
            if st.session_state['chat_role'] == 'Kim_Ok':
                if stage == 1: # 인사 후 첫 질문
                    response = "우리는 둘 다 개화를 해야 한다고 주장하는 개화파이지만, 그 방법에 대해서는 생각이 다르지.\n\n조선이 개항을 하고 나서 청이 우리에게 지나치게 간섭하고 있잖아. 김옥균, 너는 이런 상황에서 **청과의 관계**를 어떻게 해야 한다고 생각해?"
                    st.session_state['chat_stage'] = 2
                
                elif stage == 2: # 청나라 관계 답변 확인
                    if any(word in prompt for word in ['끊', '청산', '자주', '배격', '몰아', '없애']):
                        response = "맞아. 나 김홍집은 청과의 관계를 유지해야 한다고 생각하지만, 너는 청나라와의 관계를 끊어야 한다고 주장했지."
                        time.sleep(1) # 자연스러운 대화 텀
                        response += "\n\n우리는 서양의 것을 어디까지 받아들일지에 대해서도 의견이 달라. 너의 의견은 어때? (예: 기술만 vs 사상과 제도까지)"
                        st.session_state['chat_stage'] = 3
                    else:
                        response = "음, 다시 한번 생각해봐. 너(김옥균)는 청나라의 간섭을 아주 싫어했잖아. 자주적인 나라가 되려면 관계를 어떻게 해야 할까?"
                
                elif stage == 3: # 개화 범위 답변 확인
                    if any(word in prompt for word in ['사상', '제도', '법', '모두', '전부', '함께']):
                        response = "맞아. 나 김홍집은 '동도서기'라 하여 기술만 받아들이자고 했지만, 너는 사상과 제도까지 싹 바꿔야 한다고 주장했어 (문명개화론)."
                        time.sleep(1)
                        response += "\n\n나와 입장이 다른 개화파를 만나 이야기를 나눠볼 수 있어서 무척 즐거웠어. 다음에 또 만나!"
                        st.session_state['chat_stage'] = 4 # 종료 단계
                    else:
                        response = "정말 그렇게 생각해? 너는 일본의 메이지 유신을 본받아 기술뿐만 아니라 법과 제도까지 바꿔야 한다고 주장했었어."

            # [시나리오 B] 내가 김홍집일 때 (상대: 김옥균) - 반대 로직
            else:
                if stage == 1:
                    response = "우리는 뜻을 같이하는 동지였으나 지금은 갈라졌구려. 김홍집 대감, 청나라 군대가 우리 궁궐을 지키고 있는 이 상황이 마음에 드시오? 청과의 관계를 어찌해야 하겠소?"
                    st.session_state['chat_stage'] = 2
                elif stage == 2:
                    if any(word in prompt for word in ['유지', '친하', '지속', '함께', '섬겨', '보호']):
                        response = "그렇군요. 당신은 청나라의 보호 아래 안정을 원하시는군요. 하지만 나는 청나라를 몰아내야 한다고 생각하오."
                        time.sleep(1)
                        response += "\n\n그렇다면 개화는 어떻게 하시려오? 서양의 모든 것을 받아들여야 하지 않겠소?"
                        st.session_state['chat_stage'] = 3
                    else:
                        response = "아니오 대감, 당신은 온건개화파이지 않소? 청나라와 척을 지면 나라가 위험하다고 생각하지 않았소?"
                elif stage == 3:
                    if any(word in prompt for word in ['기술', '전통', '지키', '바탕', '동도서기']):
                        response = "역시 우리는 생각이 다르군요. 당신은 조선의 정신을 지키며 기술만 배우자(동도서기)는 입장이고, 나는 뿌리부터 바꿔야 한다는 입장이니 말이오."
                        time.sleep(1)
                        response += "\n\n오늘 대화로 서로의 차이를 확실히 알게 되었소. 각자의 길에서 최선을 다합시다."
                        st.session_state['chat_stage'] = 4
                    else:
                        response = "그건 내(김옥균) 생각이오. 당신은 조선의 유교적 질서는 지켜야 한다고 생각하지 않소?"

            # 챗봇 응답 출력 및 기록
            with st.chat_message("assistant"):
                st.write(response)
            st.session_state['chat_history'].append({"role": "assistant", "content": response})

            # [미션 완료 및 다음 단계 이동]
            if st.session_state['chat_stage'] == 4:
                st.success("🎉 대화 미션 완료! 자신의 역사적 입장을 잘 표현했습니다.")
                col_actions = st.columns(2)
                with col_actions[0]:
                    if st.button("🔄 다른 인물로 다시 대화하기"):
                        st.session_state['chat_role'] = None
                        st.session_state['chat_history'] = []
                        st.session_state['chat_stage'] = 0
                        st.rerun()
                with col_actions[1]:
                    if st.button("다음 미션 도전하기 (갑신정변 3일) ➡️", type="primary"):
                        st.session_state['current_page'] = 'tab3'
                        st.rerun()

# --------------------------------------------------------------------------
# [페이지 3] 탭 3: 갑신정변 3일 (준비 중)
# --------------------------------------------------------------------------
def render_tab3():
    st.title("⏳ 3단계: 운명의 3일, 갑신정변 시뮬레이션")
    st.info("이곳에서는 3일간의 긴박한 사건 전개 과정을 체험하게 됩니다.")
    if st.button("⬅️ 처음으로 돌아가기"):
        st.session_state['current_page'] = 'tab1'
        st.rerun()

# --------------------------------------------------------------------------
# [메인 로직] 현재 페이지 상태에 따라 화면 렌더링
# --------------------------------------------------------------------------
if st.session_state['current_page'] == 'tab1':
    render_tab1()
elif st.session_state['current_page'] == 'tab2':
    render_tab2()
elif st.session_state['current_page'] == 'tab3':
    render_tab3()
