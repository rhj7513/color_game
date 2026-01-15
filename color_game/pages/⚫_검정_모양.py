# pages/2_⚫_검정_모양.py
import random
import streamlit as st
import app

st.title("⚫ 검정색 랜덤 모양 (모양 맞추기)")
app.instruction_box([
    "색은 검정색으로 통일!",
    "모양 이름을 말해요: 동그라미/세모/네모/별/하트",
])

c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    if st.button("다음 모양 ▶️", use_container_width=True):
        st.session_state.shape_idx = random.randrange(len(app.SHAPES))

    shape_name, shape_fn = app.SHAPES[st.session_state.shape_idx]
    app.render_svg(shape_fn(color=app.BLACK, size=440))
    # st.caption(f"교사용 힌트: 현재 모양 = {shape_name}")
