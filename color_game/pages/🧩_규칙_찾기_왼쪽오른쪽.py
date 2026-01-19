# pages/4_🧩_규칙_찾기_왼쪽오른쪽.py
import time
import streamlit as st
import app

st.title("🧩 규칙 찾기 (왼쪽/오른쪽)")

app.instruction_box([
    "화면의 색 순서를 보고 ‘다음은 무엇일지’ 예측해요.",
    "정답은 화면 가운데에 ‘딩!’ 하고 크게 떠요.",
    "다음 문제를 누르면 정답이 잠깐 뜬 뒤 자동으로 넘어가요.",
])

# -----------------------------
# 세션 초기화
# -----------------------------
if "pattern_quizzes" not in st.session_state:
    st.session_state.pattern_quizzes = app.make_pattern_quiz(num_q=8)

if "pattern_q_idx" not in st.session_state:
    st.session_state.pattern_q_idx = 0

quizzes = st.session_state.pattern_quizzes
q_idx = st.session_state.pattern_q_idx

# -----------------------------
# 유틸: 정답 텍스트
# -----------------------------
def answer_text(q) -> str:
    ans = str(q.get("answer", ""))
    u = ans.upper()
    if u.startswith("L") or "왼" in ans:
        return "왼쪽"
    return "오른쪽"

# -----------------------------
# ✅ 딩! 오버레이 (z축)
# -----------------------------
def show_answer_overlay(text: str, duration: float = 1.2):
    # "딩!" 느낌: 🔔 + 팝/바운스 애니메이션 + 살짝 반짝
    st.markdown(
        f"""
        <style>
          @keyframes pop {{
            0%   {{ transform: scale(0.85); opacity: 0; }}
            45%  {{ transform: scale(1.05); opacity: 1; }}
            70%  {{ transform: scale(0.98); opacity: 1; }}
            100% {{ transform: scale(1.0);  opacity: 1; }}
          }}
          @keyframes bell {{
            0% {{ transform: rotate(0deg); }}
            20% {{ transform: rotate(-12deg); }}
            40% {{ transform: rotate(12deg); }}
            60% {{ transform: rotate(-10deg); }}
            80% {{ transform: rotate(10deg); }}
            100% {{ transform: rotate(0deg); }}
          }}
          .ans-overlay {{
            position: fixed;
            inset: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            pointer-events: none;
            z-index: 99999;
          }}
          .ans-card {{
            background: rgba(0,0,0,0.58);
            color: #ffffff;
            padding: 26px 70px;
            border-radius: 26px;
            font-weight: 1000;
            letter-spacing: 4px;
            box-shadow: 0 24px 70px rgba(0,0,0,0.35);
            animation: pop 220ms ease-out;
            display: flex;
            align-items: center;
            gap: 22px;
          }}
          .ans-bell {{
            font-size: 92px;
            line-height: 1;
            animation: bell 420ms ease-in-out;
          }}
          .ans-text {{
            font-size: 120px;
            line-height: 1;
          }}
        </style>

        <div class="ans-overlay">
          <div class="ans-card">
            <div class="ans-bell">🔔</div>
            <div class="ans-text">{text}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    time.sleep(duration)

# -----------------------------
# 끝났을 때
# -----------------------------
if q_idx >= len(quizzes):
    st.success("문제를 모두 풀었어요! 🎉")
    if st.button("🔁 새 문제 세트 만들기", use_container_width=True):
        st.session_state.pattern_quizzes = app.make_pattern_quiz(num_q=8)
        st.session_state.pattern_q_idx = 0
        st.rerun()
    st.stop()

# -----------------------------
# 현재 문제 렌더
# -----------------------------
q = quizzes[q_idx]
st.markdown(f"### Q{q_idx+1}")

# 시퀀스 보여주기
seq = q["sequence"]
cols = st.columns(min(10, len(seq)))
for i, tok in enumerate(seq[:10]):
    label, color = tok[0], tok[1]
    with cols[i]:
        app.render_svg(app.token_svg(color, label, size=150))

st.markdown("#### 다음은 무엇일까요?")
cL, cR = st.columns(2)
left_tok, right_tok = q["left"], q["right"]

with cL:
    app.render_svg(app.token_svg(left_tok[1], left_tok[0], size=240))
    st.markdown("<div style='text-align:center;font-size:22px;font-weight:900;'>왼쪽</div>", unsafe_allow_html=True)

with cR:
    app.render_svg(app.token_svg(right_tok[1], right_tok[0], size=240))
    st.markdown("<div style='text-align:center;font-size:22px;font-weight:900;'>오른쪽</div>", unsafe_allow_html=True)

st.divider()

# -----------------------------
# 버튼: 이전 / 정답보기 / 다음문제
# -----------------------------
b_prev, b_reveal, b_next = st.columns([1, 1, 1])

with b_prev:
    if st.button("⬅️ 이전", use_container_width=True) and q_idx > 0:
        st.session_state.pattern_q_idx -= 1
        st.rerun()

with b_reveal:
    if st.button("✅ 정답 보기", use_container_width=True):
        show_answer_overlay(answer_text(q), duration=1.2)
        st.rerun()

with b_next:
    if st.button("➡️ 다음 문제", use_container_width=True):
        # ✅ 로직 유지: 정답 잠깐(1~2초) → 다음 문제로
        show_answer_overlay(answer_text(q), duration=1.2)
        st.session_state.pattern_q_idx += 1
        st.rerun()
