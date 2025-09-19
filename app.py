import streamlit as st
import time

# --- 페이지 설정 ---
st.set_page_config(
    page_title="FitFolio - AI 포트폴리오",
    page_icon="✨",
    layout="wide"
)

# --- CSS 파일 로드 함수 (신규 추가) ---
def local_css(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"'{file_name}' 파일을 찾을 수 없습니다. app.py와 동일한 폴더에 있는지 확인해주세요.")

# CSS 파일을 로드합니다.
local_css("styles.css")


# --- 세션 상태(Session State) 초기화 ---
if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'connected_platforms' not in st.session_state:
    st.session_state.connected_platforms = set()
if 'company' not in st.session_state:
    st.session_state.company = ''
if 'job' not in st.session_state:
    st.session_state.job = ''

# --- 더미 데이터 (시뮬레이션용) ---
USER_PROFILE = {
    'skills': ['Python', 'PyTorch', 'TensorFlow', 'LLM', 'On-Device AI', 'React', 'Data Analysis'],
    'projects': [
        {
            'title': '모바일 기기용 이미지 분류 모델 경량화',
            'description': 'TensorFlow Lite를 사용하여 CNN 모델의 크기를 줄이고, 모바일 환경에서의 추론 속도를 30% 개선한 프로젝트입니다.',
        },
        {
            'title': '소셜 미디어 감성 분석 모델',
            'description': 'LSTM 기반의 딥러닝 모델을 사용하여 소셜 미디어 텍스트의 긍정/부정을 분류하는 프로젝트를 진행했습니다.',
        },
    ]
}

# --- 페이지 전환 함수 ---
def change_page(page_name):
    st.session_state.page = page_name

# --- 각 페이지를 그리는 함수들 ---

def show_landing_page():
    st.markdown("""
    <div class="landing-container">
        <h1 class="hero-title">당신의 커리어, AI가 맞춤 설계합니다.</h1>
        <p class="hero-description" style="color: #6b7280;">FitFolio는 흩어진 당신의 경험을 모아 지원하는 기업에 맞춰 포트폴리오를 자동으로 재구성해주는 가장 스마트한 방법입니다.</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2.1, 1.5, 1.9])
    with col2:
        if st.button("내 포트폴리오 만들기", type="primary"):
            change_page('connect')
            st.rerun()

def show_connect_page():
    st.markdown('<h2 class="text-center" style="font-size: 2rem;">1. 데이터 연동하기</h2>', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True) 

    platforms = {
        "github": {"name": "GitHub", "desc": "프로젝트와 코드를 가져옵니다.", "icon": "https://simpleicons.org/icons/github.svg"},
        "linkedin": {"name": "LinkedIn", "desc": "경력과 학력을 가져옵니다.", "icon": "https://simpleicons.org/icons/linkedin.svg"},
        "tistory": {"name": "블로그 (Tistory)", "desc": "작성한 글과 전문성을 가져옵니다.", "icon": "https://simpleicons.org/icons/tistory.svg"},
        "behance": {"name": "Behance", "desc": "디자인 작업물을 가져옵니다.", "icon": "https://simpleicons.org/icons/behance.svg"},
    }
    
    cols = st.columns(4) 
    
    for col, (key, val) in zip(cols, platforms.items()):
        with col:
            is_connected = key in st.session_state.connected_platforms
            button_text = "연동 완료 ✔" if is_connected else "연동하기"
            
            st.markdown(f"""
            <div class="card" style="text-align: center; height: 100%;">
                <img src="{val['icon']}" style="width: 40px; height: 40px; margin: 0 auto 1rem auto;">
                <div style="flex-grow: 1;">
                    <h3 style="font-size: 1.2rem; margin-bottom: 0.2rem; margin-top: 0;">{val['name']}</h3>
                    <p style="color: var(--subtext-color); font-size: 0.9rem; margin-bottom: 1.5rem;">{val['desc']}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            if st.button(button_text, key=key, disabled=is_connected):
                st.session_state.connected_platforms.add(key)
                st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([2, 1.5, 2])
    with col2:
        is_ready = len(st.session_state.connected_platforms) > 0
        if st.button("다음 단계로", disabled=not is_ready, type="primary"):
            change_page('input')
            st.rerun()


def show_input_page():
    st.markdown('<h2 class="text-center" style="font-size: 2rem;">2. 포트폴리오 맞춤화</h2>', unsafe_allow_html=True)
    st.markdown('<div style="margin-bottom: 2rem;"></div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        with st.container(border=True):
            company = st.text_input("지원 회사명", placeholder="예: SK 하이닉스")
            job = st.text_input("지원 직무", placeholder="예: 설비/설계")
            
            st.markdown('<div style="margin-top: 1rem;"></div>', unsafe_allow_html=True)
            
            btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
            with btn_col2:
                if st.button("AI 맞춤 포트폴리오 생성", type="primary"):
                    if not company or not job:
                        st.warning("회사명과 직무를 모두 입력해주세요.")
                    else:
                        st.session_state.company = company
                        st.session_state.job = job
                        change_page('analysis')
                        st.rerun()

def show_analysis_page():
    st.markdown('<h2 class="text-center">AI가 회원님의 데이터를 분석하고 있습니다.</h2>', unsafe_allow_html=True)
    
    messages = [
        f"'{st.session_state.company}'의 최신 기술 동향을 분석 중입니다...",
        "채용 공고의 핵심 요구 역량을 추출하고 있습니다...",
        f"'{st.session_state.job}' 직무와 회원님의 경험 데이터 매칭 중...",
        "프로젝트 설명을 AI가 재구성하는 중...",
        "맞춤 포트폴리오 생성 완료!"
    ]
    
    progress_bar = st.progress(0, text=messages[0])

    for i, message in enumerate(messages):
        progress_value = (i + 1) / len(messages)
        progress_bar.progress(progress_value, text=message)
        time.sleep(1.5)
    
    change_page('result')
    st.rerun()


def show_result_page():
    # <<<--- 이 함수 전체를 새 디자인에 맞게 재작성했습니다 --- #
    
    # 헤더
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 3rem;">
        <h1 class="hero-title" style="font-size: 3rem; margin-bottom: 1rem;">
            {st.session_state.company} 맞춤 포트폴리오
        </h1>
        <p class="hero-description" style="font-size: 1.1rem; color: #6b7280; max-width: 100%;">
            FitFolio의 AI가 '{st.session_state.job}' 직무에 맞춰 재구성한 결과입니다.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # AI 분석 요약 카드
    st.markdown(f"""
    <div class="card analysis-card">
        <div class="card-title">
            <span style="font-size: 1.5rem;">💡</span> AI 분석 요약
        </div>
        <div class="card-content">
            <p class="card-description">
                FitFolio AI가 분석한 '{st.session_state.company} {st.session_state.job}' 직무의 핵심은 
                <span class="highlight">'LLM 경량화'</span>와 
                <span class="highlight">'온디바이스 AI'</span> 경험입니다. 
                회원님의 경험을 이 키워드에 맞춰 강조하고 재구성했습니다.
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 핵심 역량 카드
    st.markdown("""
    <div class="card">
        <div class="card-title">
             <span style="font-size: 1.5rem;">🎯</span> 핵심 역량 (Skills)
        </div>
    """, unsafe_allow_html=True)
    
    required_skills = ['On-Device AI', 'LLM', 'PyTorch']
    for skill in USER_PROFILE['skills']:
        is_highlighted = skill in required_skills
        # highlighted-skill 클래스는 아래 CSS 파일에 추가했습니다.
        st.markdown(f"""
        <div class="skill-item-new {'highlighted-skill' if is_highlighted else ''}">
            {skill}
        </div>
        """, unsafe_allow_html=True)

    # 프로젝트 재구성 카드
    st.markdown("""
    <div class="card" style="margin-top: 2rem;">
         <div class="card-title">
             <span style="font-size: 1.5rem;">🚀</span> 프로젝트 재구성 (Projects)
        </div>
    """, unsafe_allow_html=True)

    for project in USER_PROFILE['projects']:
        st.markdown(f"""
        <div class="experience-item">
            <div class="experience-info">
                <span class="experience-status">✅</span>
                <span class="experience-title">{project['title']}</span>
            </div>
        </div>
        <div class="profile-content" style="border-radius: 0.5rem; margin-bottom: 1rem;">
            <p><b>[기존 설명]</b> {project['description']}</p>
            <p style="margin-top: 0.5rem;"><b>[✨ AI Rewrite]</b> '{st.session_state.company}'가 최근 집중하고 있는 <strong>'온디바이스 AI'</strong> 전략에 맞춰, <strong>TensorFlow Lite 기반 모델 경량화</strong> 경험을 강조했습니다. 이를 통해 제한된 하드웨어 환경에서의 효율적인 AI 모델 배포 및 운영 능력을 어필할 수 있습니다.</p>
        </div>
        """, unsafe_allow_html=True)


    # 처음으로 돌아가기 버튼
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 1.5, 2])
    with col2:
        if st.button("처음으로 돌아가기", type="primary"):
            st.session_state.page = 'landing'
            st.session_state.connected_platforms = set()
            st.rerun()

# --- 메인 로직 ---
if st.session_state.page == 'landing':
    show_landing_page()
elif st.session_state.page == 'connect':
    show_connect_page()
elif st.session_state.page == 'input':
    show_input_page()
elif st.session_state.page == 'analysis':
    show_analysis_page()
elif st.session_state.page == 'result':
    show_result_page()
