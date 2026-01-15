# pages/6_🎯_글자와_색_헷갈리기.py
import random
import streamlit as st
import app

st.title("🎯 글자와 색 혼합 게임")
app.instruction_box([
    "글자를 읽지 말고, 글자의 '색깔'만 말해요.",
    "예) 글자: 파랑 / 색: 빨강 → 정답은 '빨강'",
    "정답 입력은 없어요. 말이나 몸으로만 표현해요.",
])

# -----------------------------
# 사용할 색 토큰 (명확한 색만)
# -----------------------------
TOKENS = [
    app.TOKEN_RED,
    app.TOKEN_BLUE,
    app.TOKEN_YELLOW,
    app.TOKEN_GREEN,
    app.TOKEN_BROWN,
]

# -----------------------------
# session state
# -----------------------------
if "stroop_item" not in st.session_state:
    st.session_state.stroop_item = None
if "show_answer" not in st.session_state:
    st.session_state.show_answer = False

# -----------------------------
# 문제 생성
# -----------------------------
def make_stroop_question():
    word_token = random.choice(TOKENS)   # 글자 내용
    color_token = random.choice(TOKENS)  # 글자 색

    # 항상 다르게 (어려운 문제)
    while color_token == word_token:
        color_token = random.choice(TOKENS)

    return {
        "word": word_token[0],      # 글자
        "color_name": color_token[0],  # 정답
        "color_hex": color_token[1],
    }

# 처음 로드 시 문제 생성
if st.session_state.stroop_item is None:
    st.session_state.stroop_item = make_stroop_question()

q = st.session_state.stroop_item

# -----------------------------
# 문제 화면
# -----------------------------
st.markdown(
    f"""
    <div style="
        text-align:center;
        font-size:96px;
        font-weight:900;
        margin:30px 0;
        color:{q['color_hex']};
    ">
        {q['word']}
    </div>
    <div style="text-align:center;font-size:22px;font-weight:700;">
        👉 말해야 하는 것은 <b>글자의 색깔</b>이에요
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 버튼 영역
# -----------------------------
st.divider()
c1, c2, c3 = st.columns(3)

with c1:
    if st.button("다음 문제 ▶", use_container_width=True):
        st.session_state.stroop_item = make_stroop_question()
        st.session_state.show_answer = False
        st.rerun()

with c2:
    if st.button("정답 보기(교사용)", use_container_width=True):
        st.session_state.show_answer = True

with c3:
    if st.button("정답 숨기기", use_container_width=True):
        st.session_state.show_answer = False

# -----------------------------
# 정답 표시
# -----------------------------
if st.session_state.show_answer:
    st.success(f"정답: {q['color_name']}")
