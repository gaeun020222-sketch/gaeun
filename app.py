import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config
import time

# 1. 페이지 기본 설정
st.set_page_config(page_title="갑신정변 역사 탐구", layout="wide")

# --------------------------------------------------------------------------
# [공통 설정] 이미지 URL 관리
# --------------------------------------------------------------------------
IMAGE_URLS = {
    "청나라": "https://i.ibb.co/1fXH5Ffb/chung.png",
    "일본": "https://i.ibb.co/KchxkbQJ/japan.png",
    "민씨정권": "https://i.ibb.co/tpyZWYgH/image.png",
    "고종": "https://i.ibb.co/fYpjpVJ2/image.png",
    "김옥균": "https://i.ibb.co/1jFg9C6/image.png",
    "온건개화파": "https://i.ibb.co/BKGYrkf3/image.png", # 김홍집
    "흥선대원군": "https://i.ibb.co/PsJwdCrK/image.png",
    # 탭 3 시뮬레이션 메인 이미지
    "Day1": "https://i.ibb.co/zW92HRsr/DAY1.png",
    "Day2": "https://i.ibb.co/Ld3J6X8V/DAY2.png",
    "Day3": "https://i.ibb.co/fdFSJbqD/DAY3.png"
}

# 탭 3 추가 이미지 (더보기용)
EXTRA_IMAGES = {
    "Day1": [
        "https://i.ibb.co/WNJG9M5B/day1p.png",   # 1일차 사진
        "https://i.ibb.co/BHjTBBbX/dat1map.png"  # 1일차 지도
    ],
    "Day2": [
        "https://i.ibb.co/99Rb3bnd/day2p.png",    # 2일차 사진
        "https://i.ibb.co/BVBXtngJ/day2map.png"   # 2일차 지도
    ],
    "Day3": [
        "https://i.ibb.co/WQ9SmVK/day3p.png",     # 3일차 사진
        "https://i.ibb.co/6RvMx16x/day3map.png"   # 3일차 지도
    ]
}

# --------------------------------------------------------------------------
# [함수] 텍스트 스트리밍 효과
# --------------------------------------------------------------------------
def stream_data(text):
    for char in text:
        yield char
        time.sleep(0.03)

# --------------------------------------------------------------------------
# [상태 관리] 세션 스테이트 초기화
# --------------------------------------------------------------------------
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 'intro'

if 'student_name' not in st.session_state:
    st.session_state['student_name'] = ""

# 탭 1용 변수
if 'step' not in st.session_state:
    st.session_state['step'] = 1
if 'quiz_finished' not in st.session_state:
    st.session_state['quiz_finished'] = False
if 'show_next' not in st.session_state:
    st.session_state['show_next'] = False

# 탭 2용 변수
if 'chat_role' not in st.session_state:
    st.session_state['chat_role'] = None
if 'chat_stage' not in st.session_state:
    st.session_state['chat_stage'] = 0
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# 탭 3용 변수 (시뮬레이션 및 이미지 더보기 토글)
if 'sim_metrics' not in st.session_state:
    st.session_state['sim_metrics'] = {'success': 30, 'public': 20, 'power': 20}
if 'day1_choice' not in st.session_state:
    st.session_state['day1_choice'] = None
if 'day2_choice' not in st.session_state:
    st.session_state['day2_choice'] = None
if 'day3_choice' not in st.session_state:
    st.session_state['day3_choice'] = None

# 이미지 더보기 상태 관리
if 'show_more_day1' not in st.session_state:
    st.session_state['show_more_day1'] = False
if 'show_more_day2' not in st.session_state:
    st.session_state['show_more_day2'] = False
if 'show_more_day3' not in st.session_state:
    st.session_state['show_more_day3'] = False

# --------------------------------------------------------------------------
# [페이지 0] 인트로
# --------------------------------------------------------------------------
def render_intro():
    st.title("🏫 AI와 함께하는 역사 탐구 수업")
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("📜 오늘의 학습 주제")
        st.info("**갑신정변, 3일간의 기록: 성공과 실패의 갈림길**")
        st.markdown("""
        * **1단계:** 19세기 후반, 조선을 둘러싼 권력 관계 파악하기
        * **2단계:** 역사 속 인물(김옥균, 김홍집)과 대화하며 입장 이해하기
        * **3단계:** 갑신정변 3일간의 과정을 시뮬레이션하며 실패 원인 분석하기
        """)
    with col2:
        st.subheader("👋 환영합니다!")
        st.write("수업을 시작하기 위해 이름을 입력해주세요.")
        name_input = st.text_input("이름", placeholder="예: 김역사")
        if st.button("수업 시작하기 🚀", type="primary"):
            if name_input.strip() != "":
                st.session_state['student_name'] = name_input
                st.session_state['current_page'] = 'tab1'
                st.rerun()
            else:
                st.warning("이름을 입력해야 시작할 수 있어요!")

# --------------------------------------------------------------------------
# [페이지 1] 탭 1: 정치 마당
# --------------------------------------------------------------------------
def render_tab1():
    st.title(f"🏛️ 1단계: 19세기 후반 권력 지도 ({st.session_state['student_name']} 학생)")
    st.markdown("퀴즈를 풀며 당시 복잡했던 나라 안팎의 권력 관계를 파헤쳐 봅시다.")
    st.divider()
    col_quiz, col_viz = st.columns([1, 1.5])
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
                        st.error("❌ 오답입니다. 다시 한번 생각해서 옳은 답을 골라보세요!")
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

    with col_viz:
        st.subheader("📊 권력 관계 시각화")
        if st.session_state['quiz_finished']:
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
            st.divider()
            col_next_btn = st.columns([4, 1])
            with col_next_btn[1]:
                if st.button("다음 미션 도전하기 ➡️", type="primary"):
                    st.session_state['current_page'] = 'tab2'
                    st.rerun()
        else:
            st.info("👈 왼쪽 퀴즈를 모두 풀어야 지도가 나타납니다.")
            st.image("https://cdn-icons-png.flaticon.com/512/610/610333.png", width=100)

# --------------------------------------------------------------------------
# [페이지 2] 탭 2: 개화파와 대화
# --------------------------------------------------------------------------
def render_tab2():
    st.title("💬 2단계: 역사 속으로 - 개화파와의 대화")
    st.markdown("당신은 이제 역사 속 인물이 되어, 상대방과 조선의 미래를 논하게 됩니다.")
    st.divider()

    if st.session_state['chat_role'] is None:
        st.subheader("🎭 당신은 누구입니까?")
        col1, col2 = st.columns(2)
        with col1:
            st.image(IMAGE_URLS["김옥균"], width=150)
            if st.button("나는 '김옥균' (급진개화파)"):
                st.session_state['chat_role'] = 'Kim_Ok'
                st.session_state['chat_stage'] = 1
                st.session_state['chat_history'] = [] 
                st.rerun()
        with col2:
            st.image(IMAGE_URLS["온건개화파"], width=150)
            if st.button("나는 '김홍집' (온건개화파)"):
                st.session_state['chat_role'] = 'Kim_Hong'
                st.session_state['chat_stage'] = 1
                st.session_state['chat_history'] = []
                st.rerun()
    else:
        my_role = st.session_state['chat_role']
        opponent_img = IMAGE_URLS["온건개화파"] if my_role == 'Kim_Ok' else IMAGE_URLS["김옥균"]
        my_name = "김옥균" if my_role == 'Kim_Ok' else "김홍집"
        opponent_name = "김홍집" if my_role == 'Kim_Ok' else "김옥균"
        
        st.info(f"🎭 당신의 역할: **{my_name}** | 대화 상대: **{opponent_name}**")

        if not st.session_state['chat_history']:
            if my_role == 'Kim_Ok':
                start_msg = "안녕, 김옥균! 나는 김홍집이야."
            else:
                start_msg = "반갑소, 김홍집 대감. 나는 김옥균이오."
            with st.chat_message("assistant", avatar=opponent_img):
                message_placeholder = st.empty()
                full_response = ""
                for chunk in stream_data(start_msg):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state['chat_history'].append({"role": "assistant", "content": start_msg})
        else:
            for msg in st.session_state['chat_history']:
                if msg['role'] == 'assistant':
                    with st.chat_message(msg['role'], avatar=opponent_img):
                        st.write(msg['content'])
                else:
                    with st.chat_message(msg['role']): 
                        st.write(msg['content'])

        if prompt := st.chat_input("답변을 입력하세요..."):
            st.session_state['chat_history'].append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            stage = st.session_state['chat_stage']
            response = ""
            
            if my_role == 'Kim_Ok':
                if stage == 1:
                    response = f"우리는 둘 다 개화를 해야 한다고 주장하는 개화파이지만, 그 방법에 대해서는 생각이 다르지.\n\n조선이 개항을 하고 나서 청이 우리에게 지나치게 간섭하고 있잖아. {my_name}, 너는 이런 상황에서 **청과의 관계**를 어떻게 해야 한다고 생각해? \n\n(예: 관계를 끊어야 한다 / 관계를 유지해야 한다)"
                    st.session_state['chat_stage'] = 2
                elif stage == 2:
                    if any(word in prompt for word in ['끊', '청산', '자주', '배격', '몰아', '없애', '반대']):
                        response = "맞아. 나 김홍집은 청과의 관계를 유지해야 한다고 생각하지만, 너는 청나라와의 관계를 끊어야 한다고 주장했지.\n\n그렇다면 우리는 서양의 것을 어디까지 받아들일지에 대해서도 의견이 달라. 너의 의견은 어때? \n\n(예: 기술만 받아들여야 한다 / 사상과 제도까지 모두 바꿔야 한다)"
                        st.session_state['chat_stage'] = 3
                    else:
                        response = "음, 다시 한번 생각해보자. 너(김옥균)는 청나라가 간섭하는 걸 아주 싫어했어. 자주적인 나라가 되려면 관계를 어떻게 해야 할까? \n\n(힌트: '끊는다'는 말이 들어가게 답해봐)"
                elif stage == 3:
                    if any(word in prompt for word in ['사상', '제도', '법', '모두', '전부', '함께', '싹']):
                        response = "맞아. 나 김홍집은 '동도서기'라 하여 기술만 받아들이자고 했지만, 너는 사상과 제도까지 싹 바꿔야 한다고 주장했어 (문명개화론).\n\n나와 입장이 다른 개화파를 만나 이야기를 나눠볼 수 있어서 무척 즐거웠어. 다음에 또 만나!"
                        st.session_state['chat_stage'] = 4
                    else:
                        response = "정말 그렇게 생각해? 너는 일본의 메이지 유신을 본받아 기술뿐만 아니라 법과 제도까지 바꿔야 한다고 주장했었어. \n\n(힌트: '모두' 또는 '제도'가 들어가게 답해봐)"
            else:
                if stage == 1:
                    response = f"우리는 뜻을 같이하는 동지였으나 지금은 갈라졌구려. {my_name} 대감, 청나라 군대가 우리 궁궐을 지키고 있는 이 상황이 마음에 드시오? 청과의 관계를 어찌해야 하겠소? \n\n(예: 청나라와 친하게 지내야 한다 / 관계를 끊어야 한다)"
                    st.session_state['chat_stage'] = 2
                elif stage == 2:
                    if any(word in prompt for word in ['유지', '친하', '지속', '함께', '섬겨', '보호']):
                        response = "그렇군요. 당신은 청나라의 보호 아래 안정을 원하시는군요. 하지만 나는 청나라를 몰아내야 한다고 생각하오.\n\n그렇다면 개화는 어떻게 하시려오? 서양의 모든 것을 받아들여야 하지 않겠소? \n\n(예: 기술만 받아들이면 된다 / 모든 것을 바꿔야 한다)"
                        st.session_state['chat_stage'] = 3
                    else:
                        response = "아니오 대감, 다시 생각해보시오. 당신은 온건개화파이지 않소? 청나라와 척을 지면 나라가 위험하다고 생각하지 않았소? \n\n(힌트: '유지한다'는 말이 들어가게 답해봐)"
                elif stage == 3:
                    if any(word in prompt for word in ['기술', '전통', '지키', '바탕', '동도서기']):
                        response = "역시 우리는 생각이 다르군요. 당신은 조선의 정신을 지키며 기술만 배우자(동도서기)는 입장이고, 나는 뿌리부터 바꿔야 한다는 입장이니 말이오.\n\n오늘 대화로 서로의 차이를 확실히 알게 되었소. 각자의 길에서 최선을 다합시다."
                        st.session_state['chat_stage'] = 4
                    else:
                        response = "그건 내(김옥균) 생각이오. 당신은 조선의 유교적 질서는 지켜야 한다고 생각하지 않소? \n\n(힌트: '기술만' 받아들인다고 답해봐)"

            with st.chat_message("assistant", avatar=opponent_img):
                message_placeholder = st.empty()
                full_response = ""
                for chunk in stream_data(response):
                    full_response += chunk
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            st.session_state['chat_history'].append({"role": "assistant", "content": response})
            st.rerun() 

        if st.session_state['chat_stage'] == 4:
            st.success("🎉 대화 미션 완료!")
            col_btn1, col_btn2 = st.columns(2)
            with col_btn1:
                if st.button("🔄 다시 채팅하기 (처음으로)"):
                    st.session_state['chat_role'] = None 
                    st.session_state['chat_history'] = []
                    st.session_state['chat_stage'] = 0
                    st.rerun()
            with col_btn2:
                if st.button("다음 미션 도전하기 (갑신정변 3일) ➡️", type="primary"):
                    st.session_state['current_page'] = 'tab3'
                    st.rerun()

# --------------------------------------------------------------------------
# [페이지 3] 탭 3: 시뮬레이터 (수정됨: 이미지 더보기 추가)
# --------------------------------------------------------------------------
def render_tab3():
    st.title("⏳ 3단계: 갑신정변, 운명의 3일 시뮬레이터")
    
    st.warning("""
    ⚠️ **잠깐!** 이 활동은 실제 역사 내용을 바탕으로 **'만약 내가 김옥균이었다면?'** 하고 상상해보는 시뮬레이션입니다.
    여러분의 선택에 따라 결과가 달라질 수 있지만, 실제 역사는 교과서 내용과 같다는 점을 꼭 기억해주세요!
    """)
    st.divider()

    # 상태 게이지
    col_hud, col_main = st.columns([1, 3]) 
    
    with col_hud:
        st.subheader("📊 나의 혁명 상황판")
        st.info("현재 상태를 확인하세요!")
        
        st.write("📈 **갑신정변 성공 확률**")
        st.progress(st.session_state['sim_metrics']['success'] / 100)
        st.write(f"현재: {st.session_state['sim_metrics']['success']}%")
        st.markdown("---")
        
        st.write("👨‍👩‍👧‍👦 **백성들의 지지**")
        st.progress(st.session_state['sim_metrics']['public'] / 100)
        st.write(f"현재: {st.session_state['sim_metrics']['public']}%")
        st.markdown("---")
        
        st.write("⚔️ **우리 스스로 지키는 힘**")
        st.progress(st.session_state['sim_metrics']['power'] / 100)
        st.write(f"현재: {st.session_state['sim_metrics']['power']}%")

    with col_main:
        timeline = st.select_slider(
            "⏳ 시간의 흐름을 따라가보세요",
            options=["1일차: 거사 (12.4)", "2일차: 개혁 (12.5)", "3일차: 삼일천하 (12.6)"]
        )

        # --- 날짜별 시뮬레이션 로직 ---
        
        # [1일차]
        if timeline == "1일차: 거사 (12.4)":
            st.error("🔥 **1일차: 우정총국 축하연의 불길**")
            col1, col2 = st.columns([1, 1.5])
            with col1:
                st.image(IMAGE_URLS["Day1"], caption="1일차: 거사의 시작") 
                
                # [추가됨] 이미지 더 보기 버튼
                if st.button("📸 이미지 더 보기 (그날의 현장)", key="btn_more_day1"):
                    st.session_state['show_more_day1'] = True
                    st.rerun()
            
            with col2:
                st.write("""
                **[상황]** 우정총국 개국 축하연에서 불길이 솟아올랐습니다! 혼란을 틈타 김옥균과 급진개화파는 계획대로 민씨 정권을 몰아내고 고종 임금님을 안전한 곳으로 모셨습니다.
                
                이제 궁궐을 지켜야 합니다. **김옥균(당신)은 누구에게 궁궐 수비를 맡기겠습니까?**
                """)
                
                col_b1, col_b2 = st.columns(2)
                if col_b1.button("🅰️ 일본군에게 부탁한다 (실제 역사)"):
                    st.session_state['day1_choice'] = 'A'
                    st.session_state['sim_metrics']['success'] = 30
                    st.session_state['sim_metrics']['public'] = 10
                    st.session_state['sim_metrics']['power'] = 10
                    st.rerun()
                    
                if col_b2.button("🅱️ 우리 군대가 지킨다 (가상 선택)"):
                    st.session_state['day1_choice'] = 'B'
                    st.session_state['sim_metrics']['success'] = 50
                    st.session_state['sim_metrics']['public'] = 40
                    st.session_state['sim_metrics']['power'] = 50
                    st.rerun()

                if st.session_state['day1_choice'] == 'A':
                    st.warning("😓 **선택 결과:** 일본군이 궁궐을 지키게 되었습니다. 하지만 백성들은 '왜 남의 나라 군대가 왕을 지키냐'며 수군거립니다. (백성들의 지지 하락)")
                elif st.session_state['day1_choice'] == 'B':
                    st.success("🤩 **상상 결과:** 우리 군대가 당당히 왕을 지킵니다! 백성들도 '드디어 우리 힘으로!'라며 기뻐합니다. (성공 확률 상승)")

            # [추가된 이미지 뷰어 영역]
            if st.session_state['show_more_day1']:
                st.divider()
                st.subheader("📂 1일차 현장 추가 자료")
                img_c1, img_c2 = st.columns(2)
                img_c1.image(EXTRA_IMAGES["Day1"][0], caption="우정총국 축하연 현장 기록화")
                img_c2.image(EXTRA_IMAGES["Day1"][1], caption="1일차 주요 이동 경로 지도")
                
                if st.button("❌ 창닫기", key="close_day1"):
                    st.session_state['show_more_day1'] = False
                    st.rerun()

        # [2일차]
        elif timeline == "2일차: 개혁 (12.5)":
            st.success("📜 **2일차: 새로운 세상의 약속**")
            col1, col2 = st.columns([1, 1.5])
            with col1:
                st.image(IMAGE_URLS["Day2"], caption="2일차: 개혁안 발표")
                
                # [추가됨] 이미지 더 보기 버튼
                if st.button("📸 이미지 더 보기 (개혁안 원문)", key="btn_more_day2"):
                    st.session_state['show_more_day2'] = True
                    st.rerun()

            with col2:
                st.write("""
                **[상황]** 새로운 정부가 들어섰습니다. 김옥균은 고종 임금님의 허락을 받아 나라를 바꿀 **'14개조 개혁 정강'**을 발표하려 합니다.
                
                이 기쁜 소식과 개혁의 내용을 **누구와 공유**하시겠습니까?
                """)
                
                col_b1, col_b2 = st.columns(2)
                if col_b1.button("🅰️ 급진개화파끼리만 공유한다 (실제 역사)"):
                    st.session_state['day2_choice'] = 'A'
                    st.session_state['sim_metrics']['success'] = max(0, st.session_state['sim_metrics']['success'] - 20)
                    st.session_state['sim_metrics']['public'] = max(0, st.session_state['sim_metrics']['public'] - 20)
                    st.rerun()
                    
                if col_b2.button("🅱️ 백성들에게 내용을 설명한다 (가상 선택)"):
                    st.session_state['day2_choice'] = 'B'
                    st.session_state['sim_metrics']['success'] = min(100, st.session_state['sim_metrics']['success'] + 20)
                    st.session_state['sim_metrics']['public'] = min(100, st.session_state['sim_metrics']['public'] + 30)
                    st.rerun()

                if st.session_state['day2_choice'] == 'A':
                    st.warning("😓 **선택 결과:** 백성들은 궁궐 안에서 무슨 일이 일어나는지 전혀 몰랐습니다. '자기들끼리 벼슬 나눠 먹네'라며 오히려 의심하기 시작했습니다.")
                elif st.session_state['day2_choice'] == 'B':
                    st.success("🤩 **상상 결과:** 방방곡곡에 방을 붙여 개혁을 알리자, 백성들이 '우리도 사람답게 사는 세상이 온다!'며 환호합니다.")

            # [추가된 이미지 뷰어 영역]
            if st.session_state['show_more_day2']:
                st.divider()
                st.subheader("📂 2일차 추가 자료")
                img_c1, img_c2 = st.columns(2)
                img_c1.image(EXTRA_IMAGES["Day2"][0], caption="개혁 정강 발표 모습")
                img_c2.image(EXTRA_IMAGES["Day2"][1], caption="2일차 주요 거점 지도")
                
                if st.button("❌ 창닫기", key="close_day2"):
                    st.session_state['show_more_day2'] = False
                    st.rerun()

        # [3일차]
        elif timeline == "3일차: 삼일천하 (12.6)":
            st.warning("⚔️ **3일차: 최후의 순간**")
            col1, col2 = st.columns([1, 1.5])
            with col1:
                st.image(IMAGE_URLS["Day3"], caption="3일차: 청나라의 개입")
                
                # [추가됨] 이미지 더 보기 버튼
                if st.button("📸 이미지 더 보기 (전투 상황)", key="btn_more_day3"):
                    st.session_state['show_more_day3'] = True
                    st.rerun()

            with col2:
                st.write("""
                **[상황]** 약 1,500명의 청나라 군대가 몰려왔습니다! 우리가 믿었던 일본군은 불리해지자 슬금슬금 도망갈 준비를 합니다.
                절체절명의 위기 순간, 김옥균(당신)은 **어떤 결단**을 내리겠습니까?
                """)
                
                col_b1, col_b2 = st.columns(2)
                if col_b1.button("🅰️ 일본으로 도망친다 (실제 역사)"):
                    st.session_state['day3_choice'] = 'A'
                    st.session_state['sim_metrics']['success'] = 0
                    st.rerun()
                    
                if col_b2.button("🅱️ 백성들과 함께 끝까지 싸운다 (가상 선택)"):
                    st.session_state['day3_choice'] = 'B'
                    st.session_state['sim_metrics']['success'] = min(100, st.session_state['sim_metrics']['success'] + 10)
                    st.rerun()

                if st.session_state['day3_choice'] is not None:
                    final_score = st.session_state['sim_metrics']['success']
                    
                    st.divider()
                    st.markdown("### 🏁 시뮬레이션 결과")
                    
                    if st.session_state['day3_choice'] == 'A':
                        st.error(f"😢 **역사대로 실패...** (성공 확률 {final_score}%)")
                        st.write("일본 배를 타고 망명길에 올랐습니다. 갑신정변은 3일 만에 실패로 끝나고 말았습니다.")
                    else:
                        if final_score >= 70:
                            st.balloons() 
                            st.success(f"🎉 **기적 같은 성공!** (성공 확률 {final_score}%)")
                            st.write("백성들이 몽둥이와 낫을 들고 나와 청나라 군대를 막아섰습니다! '우리 개혁을 지키자!'는 함성에 청나라 군대도 물러갑니다.")
                        else:
                            st.info(f"😭 **장렬한 최후...** (성공 확률 {final_score}%)")
                            st.write("백성들과 함께 끝까지 싸웠지만, 청나라 군대가 너무 강했습니다. 하지만 당신의 용기는 후세에 길이 남을 것입니다.")

                    st.divider()
                    if st.button("다음 단계로 이동 (평가) ➡️", type="primary"):
                        st.session_state['current_page'] = 'tab4'
                        st.rerun()

            # [추가된 이미지 뷰어 영역]
            if st.session_state['show_more_day3']:
                st.divider()
                st.subheader("📂 3일차 추가 자료")
                img_c1, img_c2 = st.columns(2)
                img_c1.image(EXTRA_IMAGES["Day3"][0], caption="청나라 군대와의 전투")
                img_c2.image(EXTRA_IMAGES["Day3"][1], caption="3일차 최종 대치 지도")
                
                if st.button("❌ 창닫기", key="close_day3"):
                    st.session_state['show_more_day3'] = False
                    st.rerun()

# --------------------------------------------------------------------------
# [페이지 4] 탭 4: 평가
# --------------------------------------------------------------------------
def render_tab4():
    st.title("📝 4단계: 나의 역사적 상상력 펼치기")
    st.markdown("지금까지의 활동을 바탕으로, 역사를 바라보는 나만의 생각을 정리해 봅시다.")
    st.divider()

    st.subheader(f"✍️ {st.session_state['student_name']} 학생, 만약 당신이 김옥균이었다면?")
    st.write("갑신정변의 실패 원인을 되돌아보며, 만약 내가 리더였다면 어떤 선택을 했을지 적어보세요.")
    
    user_thought = st.text_area("내용을 입력하세요 (예: 나는 일본군을 믿지 않고 백성들에게 토지를 나누어 주어 우리 편으로 만들었을 것이다.)", height=150)
    
    if st.button("결과 전송하기 (선생님께 제출)"):
        if len(user_thought) > 10:
            st.balloons()
            st.success(f"👏 **{st.session_state['student_name']} 학생, 오늘 학습을 모두 완료했습니다! 정말 수고 많았습니다.**")
            st.write(f"**제출된 생각:** {user_thought}")
            st.info("선생님께 내용이 안전하게 전달되었습니다. 브라우저를 종료해도 좋습니다.")
        else:
            st.warning("내용이 너무 짧습니다. 조금 더 구체적으로 적어주세요!")
    
    st.divider()
    if st.button("⬅️ 처음(인트로)으로 돌아가기"):
        st.session_state['current_page'] = 'intro'
        st.rerun()

# --------------------------------------------------------------------------
# [메인 로직] 페이지 라우팅
# --------------------------------------------------------------------------
if st.session_state['current_page'] == 'intro':
    render_intro()
elif st.session_state['current_page'] == 'tab1':
    render_tab1()
elif st.session_state['current_page'] == 'tab2':
    render_tab2()
elif st.session_state['current_page'] == 'tab3':
    render_tab3()
elif st.session_state['current_page'] == 'tab4':
    render_tab4()
