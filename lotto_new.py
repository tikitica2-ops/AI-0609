import streamlit as st
import random
from datetime import datetime
import os
from dotenv import load_dotenv

# 1. .env 파일에서 API Key 및 환경변수 로드
load_dotenv()
API_KEY = os.getenv("APIkey")

# 세션 상태 초기화
if 'lotto_sets' not in st.session_state:
    st.session_state.lotto_sets = None
    st.session_state.generated_time = None

# 2. 페이지 설정 및 애니메이션 포함 커스텀 CSS
st.set_page_config(page_title="프리미엄 로또 생성기", page_icon="🎰", layout="centered")

st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E1E24;
        margin-bottom: 2rem;
    }
    .time-text {
        text-align: center;
        color: #666666;
        font-size: 0.9rem;
        margin-bottom: 2rem;
    }
    
    /* 로또 공 디자인 */
    .lotto-ball {
        display: inline-block;
        width: 45px;
        height: 45px;
        line-height: 45px;
        text-align: center;
        border-radius: 50%;
        font-weight: bold;
        font-size: 1.1rem;
        color: white;
        margin: 0 5px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .ball-1 { background: radial-gradient(circle at 30% 30%, #ffbe0b, #fb5607); }
    .ball-2 { background: radial-gradient(circle at 30% 30%, #00b4d8, #0077b6); }
    .ball-3 { background: radial-gradient(circle at 30% 30%, #ff006e, #c70039); }
    .ball-4 { background: radial-gradient(circle at 30% 30%, #a2a2a2, #4a4a4a); }
    .ball-5 { background: radial-gradient(circle at 30% 30%, #38b000, #007200); }
    
    .set-label {
        font-weight: bold;
        margin: 0 15px;
        color: #495057;
        min-width: 50px;
    }

    /* ─── 슬라이딩 애니메이션 정의 ─── */
    @keyframes slideFromLeft {
        0% {
            transform: translateX(-100%);
            opacity: 0;
        }
        100% {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideFromRight {
        0% {
            transform: translateX(100%);
            opacity: 0;
        }
        100% {
            transform: translateX(0);
            opacity: 1;
        }
    }

    /* 공통 컨테이너: 화면 전체 너비를 활용하되 넘치는 애니메이션은 숨김 */
    .motion-wrapper {
        overflow: hidden;
        padding: 5px 0;
    }

    /* 왼쪽 -> 오른쪽 슬라이딩 바 */
    .slide-left-to-right {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 12px;
        margin-bottom: 15px;
        border-left: 5px solid #0077b6;
        
        /* 애니메이션 적용: 0.8초 동안 부드럽게(ease-out) 진행 */
        animation: slideFromLeft 0.8s ease-out forwards;
    }

    /* 오른쪽 -> 왼쪽 슬라이딩 바 */
    .slide-right-to-left {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        padding: 15px;
        background-color: #f1f3f5;
        border-radius: 12px;
        margin-bottom: 15px;
        border-right: 5px solid #ff006e;
        
        /* 애니메이션 적용: 0.8초 동안 부드럽게(ease-out) 진행 */
        animation: slideFromRight 0.8s ease-out forwards;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 로직 및 UI 구현
st.markdown("<div class='main-title'>🎰 PREMIUM LOTTO GENERATOR</div>", unsafe_allow_html=True)

def generate_lotto():
    sets = []
    for _ in range(5):
        numbers = sorted(random.sample(range(1, 46), 6))
        sets.append(numbers)
    st.session_state.lotto_sets = sets
    st.session_state.generated_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    if st.button("✨ 행운의 번호 추첨하기 ✨", use_container_width=True):
        generate_lotto()

st.markdown("---")

# 번호 출력 섹션
if st.session_state.lotto_sets:
    st.markdown(f"<div class='time-text'>🕒 생성 시간: {st.session_state.generated_time}</div>", unsafe_allow_html=True)
    
    for i, lotto_set in enumerate(st.session_state.lotto_sets):
        set_num = i + 1
        # 홀수 세트는 왼쪽에서 슬라이딩(정렬도 왼쪽), 짝수 세트는 오른쪽에서 슬라이딩(정렬도 오른쪽)
        is_left_direction = (set_num % 2 != 0)
        
        # 공 HTML 생성
        balls_html = ""
        for num in lotto_set:
            if num <= 10: ball_class = "ball-1"
            elif num <= 20: ball_class = "ball-2"
            elif num <= 30: ball_class = "ball-3"
            elif num <= 40: ball_class = "ball-4"
            else: ball_class = "ball-5"
            balls_html += f"<span class='lotto-ball {ball_class}'>{num}</span>"
            
        # 방향에 따른 슬라이딩 컨테이너 구성
        if is_left_direction:
            html_content = f"""
            <div class='motion-wrapper'>
                <div class='slide-left-to-right'>
                    <span class='set-label'>SET {set_num}</span>
                    <div>{balls_html}</div>
                </div>
            </div>
            """
        else:
            html_content = f"""
            <div class='motion-wrapper'>
                <div class='slide-right-to-left'>
                    <div>{balls_html}</div>
                    <span class='set-label' style='text-align: right;'>SET {set_num}</span>
                </div>
            </div>
            """
            
        st.markdown(html_content, unsafe_allow_html=True)
else:
    st.info("버튼을 누르면 좌우에서 부드럽게 슬라이딩되는 애니메이션과 함께 로또 번호가 등장합니다.")