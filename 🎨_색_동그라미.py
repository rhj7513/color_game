# pages/1_🎨_색_동그라미.py
import random
import streamlit as st
import app  # 공용 함수/상수 사용

st.title("🎨 랜덤 색 동그라미 (색 맞추기)")
app.instruction_box([
    "동그라미가 나오면 아이들이 색 이름을 크게 말해요.",
    "정답 입력은 없어요. 말로만 참여해요.",
])

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if st.button("다음 색 동그라미 ▶️", use_container_width=True):
        st.session_state.color_idx = random.randrange(len(app.RAINBOW_COLORS))

    color = app.RAINBOW_COLORS[st.session_state.color_idx]
    app.render_svg(app.svg_circle(color=color, size=440))
