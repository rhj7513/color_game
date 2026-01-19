# pages/2_⚫_검정모양_연습.py
import random
import math
import streamlit as st

st.title("⚫ 검정 모양 연습 (버튼 1개)")

st.markdown("""
- 버튼을 누르면 **문제(도형)**가 나와요.  
- 다시 누르면 **정답(도형 이름)**이 **도형 자리에서 크게** 보여요.  
- 또 누르면 **다음 문제**로 넘어가요.
""")

# -----------------------------
# 설정
# -----------------------------
SHAPES = ["circle", "triangle", "square", "star", "heart"]
SHAPE_KO = {
    "circle": "동그라미",
    "triangle": "세모",
    "square": "네모",
    "star": "별",
    "heart": "하트",
}

SIZE = 560  # ✅ 더 크게 (원하면 620까지 올려도 됨)
COLOR = "#111"

# -----------------------------
# state
# -----------------------------
if "shape_current" not in st.session_state:
    st.session_state.shape_current = random.choice(SHAPES)

# 단계: question -> answer -> next question ...
if "shape_phase" not in st.session_state:
    st.session_state.shape_phase = "question"

def pick_new_shape():
    candidates = [s for s in SHAPES if s != st.session_state.shape_current]
    st.session_state.shape_current = random.choice(candidates) if candidates else random.choice(SHAPES)

# -----------------------------
# SVG helpers (예쁜 도형)
# -----------------------------
def _star_points(cx, cy, outer_r, inner_r, num_points=5):
    pts = []
    angle0 = -math.pi / 2  # 위쪽부터
    step = math.pi / num_points
    for i in range(num_points * 2):
        r = outer_r if i % 2 == 0 else inner_r
        a = angle0 + i * step
        x = cx + r * math.cos(a)
        y = cy + r * math.sin(a)
        pts.append((x, y))
    return " ".join([f"{x:.1f},{y:.1f}" for x, y in pts])

def shape_svg(shape: str, size: int = 560, color: str = "#111") -> str:
    w = h = size
    cx = cy = size / 2

    if shape == "circle":
        r = size * 0.30
        return f"""
        <svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
          <rect width="{w}" height="{h}" fill="white"/>
          <circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}"/>
        </svg>
        """

    if shape == "square":
        s = size * 0.62
        x = cx - s / 2
        y = cy - s / 2
        rx = size * 0.04  # 살짝 둥글게(더 예쁨)
        return f"""
        <svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
          <rect width="{w}" height="{h}" fill="white"/>
          <rect x="{x}" y="{y}" width="{s}" height="{s}" rx="{rx}" fill="{color}"/>
        </svg>
        """

    if shape == "triangle":
        top = (cx, size * 0.14)
        left = (size * 0.20, size * 0.84)
        right = (size * 0.80, size * 0.84)
        return f"""
        <svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
          <rect width="{w}" height="{h}" fill="white"/>
          <polygon points="{top[0]},{top[1]} {left[0]},{left[1]} {right[0]},{right[1]}" fill="{color}"/>
        </svg>
        """

    if shape == "star":
        outer_r = size * 0.30
        inner_r = size * 0.13
        pts = _star_points(cx, cy, outer_r, inner_r, 5)
        return f"""
        <svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
          <rect width="{w}" height="{h}" fill="white"/>
          <polygon points="{pts}" fill="{color}"/>
        </svg>
        """

    if shape == "heart":
        # 예쁜 하트: 좌우 대칭 + 부드러운 곡선
        s = size
        return f"""
        <svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">
          <rect width="{w}" height="{h}" fill="white"/>
          <path d="
            M {s*0.50} {s*0.83}
            C {s*0.20} {s*0.62}, {s*0.10} {s*0.42}, {s*0.22} {s*0.30}
            C {s*0.34} {s*0.18}, {s*0.48} {s*0.22}, {s*0.50} {s*0.34}
            C {s*0.52} {s*0.22}, {s*0.66} {s*0.18}, {s*0.78} {s*0.30}
            C {s*0.90} {s*0.42}, {s*0.80} {s*0.62}, {s*0.50} {s*0.83}
            Z
          " fill="{color}"/>
        </svg>
        """

    return ""

# -----------------------------
# 중앙 정렬 렌더 (핵심)
# -----------------------------
def render_center(html: str):
    st.markdown(
        f"""
        <div style="width:100%; display:flex; justify-content:center; align-items:center;">
          {html}
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# 표시 영역
# -----------------------------
current_shape = st.session_state.shape_current

if st.session_state.shape_phase == "question":
    st.markdown("### ❓ 이 모양은 뭐예요?")
    render_center(shape_svg(current_shape, size=SIZE, color=COLOR))
    button_label = "✅ 정답 보기"

else:
    # ✅ 도형이 있던 '자리'에 큰 글씨로 정답 보여주기
    name = SHAPE_KO[current_shape]
    render_center(
        f"""
        <div style="
            width:{SIZE}px; height:{SIZE}px;
            display:flex; align-items:center; justify-content:center;
            font-size:96px; font-weight:900;
            border-radius:16px;
            ">
            {name}
        </div>
        """
    )
    button_label = "➡️ 다음 문제"

# -----------------------------
# 버튼 1개 상호작용
# -----------------------------
if st.button(button_label, use_container_width=True):
    if st.session_state.shape_phase == "question":
        st.session_state.shape_phase = "answer"
    else:
        pick_new_shape()
        st.session_state.shape_phase = "question"
    st.rerun()
