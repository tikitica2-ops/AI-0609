import streamlit as st
import openai
import os
from dotenv import load_dotenv

# 1. .env 파일에 저장된 환경 변수 불러오기
load_dotenv()

# 시스템 환경 변수에서 OpenAI API Key 추출
openai_api_key = os.getenv("OPENAI_API_KEY")

# 2. 웹 페이지 기본 설정 및 타이틀
st.set_page_config(
    page_title="코린이 탈출기! 파이썬 코드 리뷰 & 디버거",
    page_icon="🐍",
    layout="wide"
)

st.title("🐍 비전공자를 위한 파이썬 코드 리뷰어 & 디버깅 툴")
st.caption("어려운 개발 용어는 가라! 내가 작성한 코드를 초보자의 눈높이에서 쉽게 설명하고 고쳐줍니다.")

# 3. 사이드바: 가이드라인만 표시 (API 입력창 제거)
with st.sidebar:
    st.header("⚙️ 설정 및 안내")
    
    if openai_api_key:
        st.success("✅ .env 파일에서 API Key를 성공적으로 불러왔습니다.")
    else:
        st.error("❌ .env 파일에서 OPENAI_API_KEY를 찾을 수 없습니다. 파일이나 가상환경을 확인해주세요.")
    
    st.divider()
    st.markdown("""
    ### 💡 사용 방법
    1. 오른쪽 입력창에 분석하고 싶은 **파이썬 코드**를 붙여넣습니다.
    2. **'코드 분석 시작하기'** 버튼을 누르면 AI의 친절한 설명이 시작됩니다!
    """)

# 4. 메인 화면 구성 (2개의 칸으로 분할)
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("💻 나의 파이썬 코드 입력")
    sample_code = '''def welcome(name)
    print("안녕하세요 " + name + "님!")
    
# 숫자가 짝수인지 홀수인지 구별하는 코드인데 에러가 나요
num = 7
if num % 2 = 0:
    print("짝수입니다")
else
    print("홀수입니다")'''
    
    user_code = st.text_area(
        "리뷰하거나 디버깅할 코드를 여기에 붙여넣으세요:",
        value=sample_code,
        height=400
    )
    
    analyze_btn = st.button("🚀 코드 분석 시작하기", use_container_width=True)

# 5. 분석 로직 수행 및 결과 출력
with col2:
    st.subheader("🤖 AI 코린이 매니저의 진단 결과")
    
    if analyze_btn:
        if not openai_api_key:
            st.error("⚠️ API Key가 설정되지 않아 분석을 진행할 수 없습니다. .env 파일을 확인해 주세요.")
        elif not user_code.strip():
            st.warning("⚠️ 분석할 코드를 입력해주세요!")
        else:
            with st.spinner("AI가 코드를 꼼꼼하게 읽고 있습니다. 잠시만 기다려주세요..."):
                try:
                    # OpenAI 클라이언트 초기화 (가져온 API Key 사용)
                    client = openai.OpenAI(api_key=openai_api_key)
                    
                    # 비전공자 맞춤형 프롬프트 설정
                    system_prompt = (
                        "당신은 프로그래밍을 처음 배우는 비전공자(코린이)를 위한 친절한 파이썬 선생님입니다.\n"
                        "답변할 때는 아래의 규칙을 반드시 지켜주세요:\n"
                        "1. 어려운 IT/개발 전문 용어는 사용하지 않거나, 사용할 경우 일상적인 비유(예: 요리 레시피, 서랍장 등)를 들어 설명하세요.\n"
                        "2. 출력 형식은 명확하게 다음 3가지 섹션으로 나누어 작성하세요:\n\n"
                        "### 📝 1. 이 코드는 어떤 코드인가요? (한 줄 요약 및 상세 설명)\n"
                        "- 코드가 궁극적으로 무엇을 하려는 기능인지 일상 언어로 설명하고, 코드의 흐름을 단계별(1단계, 2단계...)로 쉽게 풀어써 주세요.\n\n"
                        "### 🔍 2. 에러 및 수정 필요 부분 (원인과 해결책)\n"
                        "- 문법 오류(SyntaxError)나 논리적 오류가 있다면, 에러가 난 정확한 줄(Line) 번호나 코드 조각을 언급하세요.\n"
                        "- 왜 에러가 났는지 '원인'을 비전공자 눈높이에서 설명하고, 어떻게 고쳐야 하는지 '해결책'을 상세히 코멘트하세요. (에러가 없다면 칭찬과 함께 패스하세요)\n\n"
                        "### 💡 3. 올바르게 수정된 전체 코드\n"
                        "- 완벽하게 작동하는 전체 코드를 마크다운 코드 블록(```python ... ```)으로 제공하세요. 각 코드 라인마다 `#` 주석을 활용하여 '이 줄이 왜 필요한지' 아주 상세한 다큐먼트(설명)를 한글로 달아주세요."
                    )
                    
                    user_prompt = f"내가 작성한 코드:\n```python\n{user_code}\n```\n\n이 코드를 분석해서 리뷰와 디버깅 결과를 알려줘."
                    
                    # API 호출
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=0.3
                    )
                    
                    # 결과 출력
                    result_text = response.choices[0].message.content
                    st.markdown(result_text)
                    st.success("✨ 분석이 완료되었습니다!")
                    
                except Exception as e:
                    st.error(f"❌ 에러가 발생했습니다: {str(e)}")
    else:
        st.info("👈 왼쪽에서 '코드 분석 시작하기' - 버튼을 누르면 이 자리에 결과가 나타납니다.")