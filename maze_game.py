import streamlit as st
import random
import time

# 페이지 설정
st.set_page_config(
    page_title="🐻 곰돌이 푸의 꿀 찾기 게임",
    page_icon="🐻",
    layout="wide"
)

# CSS 스타일 추가
st.markdown("""
<style>
.game-container {
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 500px;
    background: linear-gradient(135deg, #87CEEB 0%, #98FB98 100%);
    border-radius: 15px;
    padding: 20px;
    margin: 20px 0;
}

.game-container:focus {
    outline: none;
}

.maze {
    display: grid;
    gap: 2px;
    background-color: #2c3e50;
    padding: 10px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

.cell {
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    border-radius: 3px;
    transition: all 0.3s ease;
}

.wall {
    background-color: #34495e;
}

.path {
    background-color: #ecf0f1;
}

.player {
    background-color: #f39c12;
    border-radius: 50%;
    animation: bounce 1s infinite;
}

.honey {
    background-color: #f1c40f;
    animation: sparkle 2s infinite;
}

.goal {
    background-color: #e74c3c;
    border-radius: 50%;
}

@keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
        transform: translateY(0);
    }
    40% {
        transform: translateY(-3px);
    }
    60% {
        transform: translateY(-1px);
    }
}

@keyframes sparkle {
    0%, 100% {
        transform: scale(1);
        opacity: 1;
    }
    50% {
        transform: scale(1.1);
        opacity: 0.8;
    }
}

@keyframes balloon-celebration {
    0% {
        transform: translateY(0px) scale(0);
        opacity: 0;
    }
    50% {
        transform: translateY(-100px) scale(1);
        opacity: 1;
    }
    100% {
        transform: translateY(-200px) scale(1.2);
        opacity: 0;
    }
}

.celebration-balloon {
    position: absolute;
    font-size: 2rem;
    animation: balloon-celebration 3s ease-out forwards;
    z-index: 1000;
}

.controls {
    display: flex;
    justify-content: center;
    gap: 10px;
    margin: 20px 0;
}

.control-btn {
    padding: 10px 15px;
    font-size: 1.2rem;
    border: none;
    border-radius: 8px;
    background-color: #3498db;
    color: white;
    cursor: pointer;
    transition: background-color 0.3s;
}

.control-btn:hover {
    background-color: #2980b9;
}

.stats {
    background-color: #f8f9fa;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 4px solid #3498db;
}

.success-message {
    background-color: #d4edda;
    color: #155724;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 4px solid #28a745;
    animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
    from {
        transform: translateX(-100%);
        opacity: 0;
    }
    to {
        transform: translateX(0);
        opacity: 1;
    }
}

.keyboard-hint {
    background-color: #e8f4fd;
    padding: 15px;
    border-radius: 10px;
    margin: 10px 0;
    border-left: 4px solid #3498db;
    text-align: center;
}

.keyboard-hint h4 {
    margin: 0 0 10px 0;
    color: #2c3e50;
}

.keyboard-hint p {
    margin: 5px 0;
    color: #34495e;
}
</style>

<script>
// 키보드 이벤트 핸들러
document.addEventListener('keydown', function(event) {
    const key = event.key;
    
    // 방향키나 WASD 키 처리
    if (key === 'ArrowUp' || key === 'w' || key === 'W') {
        event.preventDefault();
        updateGameInput('up');
    } else if (key === 'ArrowDown' || key === 's' || key === 'S') {
        event.preventDefault();
        updateGameInput('down');
    } else if (key === 'ArrowLeft' || key === 'a' || key === 'A') {
        event.preventDefault();
        updateGameInput('left');
    } else if (key === 'ArrowRight' || key === 'd' || key === 'D') {
        event.preventDefault();
        updateGameInput('right');
    }
});

function updateGameInput(direction) {
    // Streamlit의 text_input 값을 업데이트
    const inputElement = document.querySelector('input[data-testid="textInput"]');
    if (inputElement) {
        inputElement.value = direction;
        inputElement.dispatchEvent(new Event('input', { bubbles: true }));
    }
}
</script>
""", unsafe_allow_html=True)

# 미로 생성 함수
def generate_maze(width, height, difficulty):
    """난이도에 따라 미로를 생성합니다"""
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    # 시작점과 끝점 설정
    start_x, start_y = 1, 1
    end_x, end_y = width-2, height-2
    
    # 미로 생성 (DFS 알고리즘 사용)
    stack = [(start_x, start_y)]
    maze[start_y][start_x] = 0
    
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    
    while stack:
        current_x, current_y = stack[-1]
        neighbors = []
        
        for dx, dy in directions:
            nx, ny = current_x + dx, current_y + dy
            if (0 < nx < width-1 and 0 < ny < height-1 and 
                maze[ny][nx] == 1):
                neighbors.append((nx, ny))
        
        if neighbors:
            next_x, next_y = random.choice(neighbors)
            maze[next_y][next_x] = 0
            maze[current_y + (next_y - current_y) // 2][current_x + (next_x - current_x) // 2] = 0
            stack.append((next_x, next_y))
        else:
            stack.pop()
    
    # 난이도에 따라 추가 경로 생성
    if difficulty == "하":
        # 쉬운 난이도: 더 많은 경로
        for _ in range(width * height // 8):
            x, y = random.randint(1, width-2), random.randint(1, height-2)
            if maze[y][x] == 1:
                maze[y][x] = 0
    elif difficulty == "상":
        # 어려운 난이도: 더 적은 경로
        for _ in range(width * height // 20):
            x, y = random.randint(1, width-2), random.randint(1, height-2)
            if maze[y][x] == 0:
                maze[y][x] = 1
    
    return maze, (start_x, start_y), (end_x, end_y)

# 키보드 입력 처리 함수
def handle_keyboard_input(key):
    """키보드 입력을 처리하여 캐릭터를 이동시킵니다"""
    if st.session_state.game_state['game_won']:
        return
    
    x, y = st.session_state.game_state['player_pos']
    maze = st.session_state.game_state['maze']
    
    new_x, new_y = x, y
    
    if key == 'up' and y > 0 and maze[y-1][x] == 0:
        new_y = y - 1
    elif key == 'down' and y < len(maze)-1 and maze[y+1][x] == 0:
        new_y = y + 1
    elif key == 'left' and x > 0 and maze[y][x-1] == 0:
        new_x = x - 1
    elif key == 'right' and x < len(maze[0])-1 and maze[y][x+1] == 0:
        new_x = x + 1
    
    # 위치가 변경되었으면 업데이트
    if (new_x, new_y) != (x, y):
        st.session_state.game_state['player_pos'] = (new_x, new_y)
        st.session_state.game_state['moves'] += 1
        st.rerun()

# 세션 상태 초기화
if 'game_state' not in st.session_state:
    st.session_state.game_state = {
        'maze': None,
        'player_pos': (1, 1),
        'goal_pos': (1, 1),
        'difficulty': '중',
        'maze_size': (15, 15),
        'moves': 0,
        'game_won': False,
        'celebration_balloons': []
    }

# 키보드 입력 처리
if 'last_key' not in st.session_state:
    st.session_state.last_key = None

# 키보드 입력 감지
key_input = st.text_input("키보드 입력 (방향키 사용)", value="", key="keyboard_input", help="이 입력창을 클릭한 후 방향키를 사용하세요")

# 제목
st.title("🐻 곰돌이 푸의 꿀 찾기 게임")
st.markdown("방향키를 사용해서 곰돌이 푸를 움직여 꿀을 찾아보세요!")

# 사이드바 설정
with st.sidebar:
    st.header("🎮 게임 설정")
    
    # 난이도 선택
    difficulty = st.selectbox(
        "난이도 선택",
        ["하", "중", "상"],
        index=["하", "중", "상"].index(st.session_state.game_state['difficulty'])
    )
    
    # 미로 크기 설정
    if difficulty == "하":
        maze_size = (11, 11)
    elif difficulty == "중":
        maze_size = (15, 15)
    else:  # 상
        maze_size = (19, 19)
    
    st.session_state.game_state['difficulty'] = difficulty
    st.session_state.game_state['maze_size'] = maze_size
    
    # 새 게임 버튼
    if st.button("🔄 새 게임", type="primary", use_container_width=True):
        maze, start_pos, goal_pos = generate_maze(maze_size[0], maze_size[1], difficulty)
        st.session_state.game_state.update({
            'maze': maze,
            'player_pos': start_pos,
            'goal_pos': goal_pos,
            'moves': 0,
            'game_won': False,
            'celebration_balloons': []
        })
        st.rerun()
    
    # 통계 표시
    st.markdown("---")
    st.markdown("### 📊 게임 통계")
    st.metric("이동 횟수", st.session_state.game_state['moves'])
    st.metric("난이도", difficulty)
    st.metric("미로 크기", f"{maze_size[0]}×{maze_size[1]}")

# 게임이 시작되지 않았으면 새 게임 시작
if st.session_state.game_state['maze'] is None:
    maze, start_pos, goal_pos = generate_maze(maze_size[0], maze_size[1], difficulty)
    st.session_state.game_state.update({
        'maze': maze,
        'player_pos': start_pos,
        'goal_pos': goal_pos,
        'moves': 0,
        'game_won': False,
        'celebration_balloons': []
    })

# 게임 승리 메시지
if st.session_state.game_state['game_won']:
    st.markdown("""
    <div class="success-message">
        <h3>🎉 축하합니다! 꿀을 찾았어요!</h3>
        <p>곰돌이 푸가 꿀을 성공적으로 찾았습니다!</p>
    </div>
    """, unsafe_allow_html=True)

# 키보드 조작 안내
st.markdown("""
<div class="keyboard-hint">
    <h4>🎮 키보드 조작 방법</h4>
    <p><strong>↑</strong> 위로 이동</p>
    <p><strong>↓</strong> 아래로 이동</p>
    <p><strong>←</strong> 왼쪽으로 이동</p>
    <p><strong>→</strong> 오른쪽으로 이동</p>
    <p><em>위의 입력창을 클릭한 후 방향키를 사용하세요!</em></p>
</div>
""", unsafe_allow_html=True)

# 키보드 입력 처리
if key_input:
    # 입력된 키에 따라 이동 처리
    if key_input.lower() in ['w', 'up', 'arrowup']:
        handle_keyboard_input('up')
    elif key_input.lower() in ['s', 'down', 'arrowdown']:
        handle_keyboard_input('down')
    elif key_input.lower() in ['a', 'left', 'arrowleft']:
        handle_keyboard_input('left')
    elif key_input.lower() in ['d', 'right', 'arrowright']:
        handle_keyboard_input('right')
    
    # 입력창 초기화
    st.session_state.keyboard_input = ""

# 게임 승리 체크
player_pos = st.session_state.game_state['player_pos']
goal_pos = st.session_state.game_state['goal_pos']

if player_pos == goal_pos and not st.session_state.game_state['game_won']:
    st.session_state.game_state['game_won'] = True
    # 축하 풍선 효과
    for i in range(5):
        st.session_state.game_state['celebration_balloons'].append({
            'id': i,
            'timestamp': time.time()
        })
    st.rerun()

# 미로 렌더링
maze = st.session_state.game_state['maze']
player_pos = st.session_state.game_state['player_pos']
goal_pos = st.session_state.game_state['goal_pos']

# 미로 HTML 생성
maze_html = '<div class="game-container"><div class="maze" style="grid-template-columns: repeat(' + str(len(maze[0])) + ', 30px);">'

for y in range(len(maze)):
    for x in range(len(maze[0])):
        if (x, y) == player_pos:
            maze_html += '<div class="cell player">🐻</div>'
        elif (x, y) == goal_pos:
            maze_html += '<div class="cell goal">🍯</div>'
        elif maze[y][x] == 1:
            maze_html += '<div class="cell wall"></div>'
        else:
            maze_html += '<div class="cell path"></div>'

maze_html += '</div></div>'

# 축하 풍선 효과
if st.session_state.game_state['celebration_balloons']:
    current_time = time.time()
    for balloon in st.session_state.game_state['celebration_balloons']:
        if current_time - balloon['timestamp'] < 3:
            maze_html += f'''
            <div class="celebration-balloon" style="left: {random.randint(100, 400)}px; top: {400 + random.randint(0, 50)}px;">
                🎈
            </div>
            '''
    
    # 오래된 풍선 제거
    st.session_state.game_state['celebration_balloons'] = [
        b for b in st.session_state.game_state['celebration_balloons'] 
        if current_time - b['timestamp'] < 3
    ]

st.markdown(maze_html, unsafe_allow_html=True)

# 게임 설명
st.markdown("---")
st.markdown("""
### 🎮 게임 방법
1. **키보드 방향키**를 사용해서 곰돌이 푸(🐻)를 움직이세요
2. **꿀(🍯)**을 찾으면 게임에서 승리합니다!
3. **새 게임** 버튼으로 새로운 미로를 생성할 수 있습니다
4. **난이도**를 선택해서 게임의 난이도를 조절할 수 있습니다

### 🎯 난이도별 특징
- **하**: 작은 미로, 많은 경로
- **중**: 중간 크기 미로, 적당한 경로
- **상**: 큰 미로, 적은 경로

### ✨ 특징
- 매번 새로운 미로가 생성됩니다
- 곰돌이 푸가 바운스 애니메이션으로 움직입니다
- 꿀을 찾으면 축하 풍선이 날아갑니다
- 이동 횟수를 추적합니다
- 키보드 방향키로 직관적인 조작이 가능합니다
""")

# 자동 새로고침 (축하 풍선 애니메이션을 위해)
if st.session_state.game_state['celebration_balloons']:
    time.sleep(0.1)
    st.rerun()
