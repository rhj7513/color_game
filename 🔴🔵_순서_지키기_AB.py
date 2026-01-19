# pages/3_🔴🔵_순서_지키기_AB.py
import streamlit as st
import random
import app

st.title("🔴🔵 순서 지키기 (쉬움: AB 규칙)")
app.instruction_box([
    "규칙은 항상 있어요(랜덤X).",
    "연습 3문제에서 규칙이 조금씩 달라져요.",
    "아이들은 ‘다음은 무엇일까?’를 말로 예측해요.",
])

# -----------------------------
# init
# -----------------------------
if "seq_practice_idx" not in st.session_state:
    st.session_state.seq_practice_idx = 0  # 0~2

# 3 practice patterns (규칙이 다름)
PRACTICES = [
    {
        "title": "Practice 1: AB (2 colors alternating)",
        "pattern": [app.TOKEN_A, app.TOKEN_B],
        "length": 8,
        "question": "👉 다음은 빨강일까? 파랑일까?",
    },
    {
        "title": "Practice 2: ABC (3 colors repeating)",
        "pattern": [app.TOKEN_A, app.TOKEN_B, app.TOKEN_C],
        "length": 9,
        "question": "👉 다음은 빨강/파랑/노랑 중 뭐가 올까?",
    },
    {
        "title": "Practice 3: AABB (chunk rule)",
        "pattern": [app.TOKEN_A, app.TOKEN_A, app.TOKEN_B, app.TOKEN_B],
        "length": 10,
        "question": "👉 다음은 빨강일까? 파랑일까? (덩어리 규칙!)",
    },
]

p = PRACTICES[st.session_state.seq_practice_idx]
st.markdown(f"### {p['title']}")
st.caption(f"연습 {st.session_state.seq_practice_idx + 1} / 3")

# -----------------------------
# build sequence
# -----------------------------
seq = app.build_sequence(p["pattern"], p["length"])

# show sequence tokens
cols = st.columns(min(10, len(seq)))
for i, tok in enumerate(seq[:10]):
    label, color = tok[0], tok[1]
    with cols[i]:
        app.render_svg(app.token_svg(color, label, size=150))

st.markdown("#### 질문")
st.write(p["question"])

# -----------------------------
# optional: show next choices (Left/Right style) - no input
# -----------------------------
st.divider()
st.markdown("#### (선택) 다음 후보 두 개 중 하나 고르기: 왼쪽 vs 오른쪽")

correct_next = p["pattern"][p["length"] % len(p["pattern"])]
token_pool = [app.TOKEN_A, app.TOKEN_B, app.TOKEN_C]
wrong_candidates = [t for t in token_pool if t != correct_next]
wrong_next = random.choice(wrong_candidates)

if random.random() < 0.5:
    left_tok, right_tok = correct_next, wrong_next
else:
    left_tok, right_tok = wrong_next, correct_next

cL, cR = st.columns(2)
with cL:
    app.render_svg(app.token_svg(left_tok[1], left_tok[0], size=230))
    st.markdown("<div style='text-align:center;font-size:22px;font-weight:900;'>왼쪽</div>",
                unsafe_allow_html=True)
with cR:
    app.render_svg(app.token_svg(right_tok[1], right_tok[0], size=230))
    st.markdown("<div style='text-align:center;font-size:22px;font-weight:900;'>오른쪽</div>",
                unsafe_allow_html=True)

# -----------------------------
# navigation
# -----------------------------
st.divider()
n1, n2, n3 = st.columns([1, 1, 1])

with n1:
    if st.button("⬅️ 이전", use_container_width=True) and st.session_state.seq_practice_idx > 0:
        st.session_state.seq_practice_idx -= 1
        st.rerun()

with n2:
    if st.button("🔁 처음(연습1)", use_container_width=True):
        st.session_state.seq_practice_idx = 0
        st.rerun()

with n3:
    if st.button("➡️ 다음", use_container_width=True):
        if st.session_state.seq_practice_idx < 2:
            st.session_state.seq_practice_idx += 1
            st.rerun()
        else:
            st.success("연습 3문제 끝! 이제 ‘규칙 찾기(왼쪽/오른쪽)’로 넘어가면 돼요.")