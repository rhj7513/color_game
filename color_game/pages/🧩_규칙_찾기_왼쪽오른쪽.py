# pages/4_🧩_규칙_찾기_왼쪽오른쪽.py
import streamlit as st
import app

st.title("🧩 규칙 찾기 (왼쪽/오른쪽)")
app.instruction_box([
    "화면의 색 순서를 보고 ‘다음은 무엇일지’ 예측해요.",
    "아이들은 종이에 Q1=왼쪽 / Q1=오른쪽처럼 적어요.",
    "모든 문제를 다 낸 뒤, '정답 보기' 버튼을 눌러 정답을 확인해요.",
])

# ✅ session_state 초기화(필수)
if "pattern_quizzes" not in st.session_state:
    st.session_state.pattern_quizzes = app.make_pattern_quiz(num_q=8, difficulty="hard")
if "pattern_q_idx" not in st.session_state:
    st.session_state.pattern_q_idx = 0
if "reveal_answers" not in st.session_state:
    st.session_state.reveal_answers = False

quizzes = st.session_state.pattern_quizzes
q_idx = st.session_state.pattern_q_idx

# def render_split_answers(quizzes):
#     left_list, right_list = [], []
#     for i, q in enumerate(quizzes, start=1):
#         (left_list if q["answer"] == "왼쪽" else right_list).append(f"Q{i}")

#     st.subheader("✅ 정답 모아보기")
#     cL, cR = st.columns(2)
#     with cL:
#         st.markdown("### ⬅ LEFT (왼쪽)")
#         st.write(" / ".join(left_list) if left_list else "없음")
#     with cR:
#         st.markdown("### RIGHT (오른쪽) ➡")
#         st.write(" / ".join(right_list) if right_list else "없음")

#     st.divider()
#     st.markdown("### 🔎 문항별 정답")
#     for i, q in enumerate(quizzes, start=1):
#         st.write(f"Q{i}. {q['answer']}")

def render_split_answers(quizzes):
    st.subheader("✅ 정답 + 문제 다시 보기")

    for i, q in enumerate(quizzes, start=1):
        st.markdown(f"### Q{i}")

        # 문제(색 순서) 다시 보여주기
        seq = q["sequence"]
        cols = st.columns(len(seq))
        for idx, tok in enumerate(seq):
            label, color = tok[0], tok[1]
            with cols[idx]:
                app.render_svg(app.token_svg(color, label, size=110))

        # 정답 표시
        answer = q["answer"]
        st.success(f"정답: {answer}")

        st.divider()


# -----------------------------
# main
# -----------------------------
if q_idx >= len(quizzes):
    st.success("문제를 모두 냈어요!")

    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("✅ 정답 보기", use_container_width=True):
            st.session_state.reveal_answers = True

    if st.session_state.reveal_answers:
        render_split_answers(quizzes)

    st.divider()
    if st.button("🔄 새 문제 세트(어려움)", use_container_width=True):
        st.session_state.pattern_quizzes = app.make_pattern_quiz(
            num_q=6,
            difficulty="easy"
        )
        st.session_state.pattern_quizzes = app.make_pattern_quiz(
            num_q=8,
            difficulty="hard"
        )
        # st.session_state.pattern_quizzes = app.make_pattern_quiz(num_q=8, difficulty="hard")
        st.session_state.pattern_q_idx = 0
        st.session_state.reveal_answers = False
        st.toast("더 어려운 새 문제 세트를 만들었어요!")
        st.rerun()

else:
    q = quizzes[q_idx]
    st.markdown(f"### Q{q_idx+1}")

    seq = q["sequence"]
    cols = st.columns(min(10, len(seq)))
    for i, tok in enumerate(seq[:10]):
        label, color = tok[0], tok[1]
        with cols[i]:
            app.render_svg(app.token_svg(color, label, size=150))

    st.markdown("#### 다음은 무엇일까요?")

    left_tok, right_tok = q["left"], q["right"]
    cL, cR = st.columns(2)
    with cL:
        app.render_svg(app.token_svg(left_tok[1], left_tok[0], size=230))
        st.markdown("<div style='text-align:center;font-size:22px;font-weight:900;'>왼쪽</div>",
                    unsafe_allow_html=True)
    with cR:
        app.render_svg(app.token_svg(right_tok[1], right_tok[0], size=230))
        st.markdown("<div style='text-align:center;font-size:22px;font-weight:900;'>오른쪽</div>",
                    unsafe_allow_html=True)

    nav1, nav2 = st.columns(2)
    with nav1:
        if st.button("⬅️ 이전", use_container_width=True) and q_idx > 0:
            st.session_state.pattern_q_idx -= 1
            st.rerun()
    with nav2:
        if st.button("➡️ 다음", use_container_width=True):
            st.session_state.pattern_q_idx += 1
            st.rerun()