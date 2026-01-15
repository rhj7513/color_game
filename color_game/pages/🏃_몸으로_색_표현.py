# pages/5_🏃_몸으로_색_표현.py
import random
import streamlit as st
import app

st.title("🏃 몸으로 색 표현하기")
app.instruction_box([
   "색이 나오면 말하지 말고 몸으로만 반응해요.",
    "🔴 빨강: 손 들기",
    "🔵 파랑: 점프",
    "🟨 노랑: 손바닥 치기 (짝!)",
])

st.markdown(
    """
    <div style="font-size:26px;line-height:1.8;">
    🔴 <b>빨강</b> → 🙋 손 들기<br/>
    🔵 <b>파랑</b> → 🤸 점프<br/>
    🟨 <b>노랑</b> → 👏 손바닥 치기
    </div>
    """,
    unsafe_allow_html=True
)

# only 3 colors for action rule
ACTION_COLORS = [
    ("빨강", "#FF3B30"),
    ("파랑", "#007AFF"),
    ("노랑", "#FFCC00"),
]

if "action_color" not in st.session_state:
    st.session_state.action_color = random.choice(ACTION_COLORS)

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if st.button("다음 색 ▶️", use_container_width=True):
        st.session_state.action_color = random.choice(ACTION_COLORS)

    name, color = st.session_state.action_color
    app.render_svg(app.svg_circle(color=color, size=440))
    st.markdown(
        f"<div style='text-align:center;font-size:34px;font-weight:900;margin-top:8px;'>{name}</div>",
        unsafe_allow_html=True
    )
