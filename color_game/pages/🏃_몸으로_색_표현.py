# pages/5_🏃_몸으로_색_표현.py
import random
import streamlit as st

st.title("🏃 몸으로 색 표현 (난이도 3단계)")

BASE = [
    {"name": "빨강", "hex": "#FF0000", "emoji": "🙋", "action": "손 들기"},
    {"name": "파랑", "hex": "#0000FF", "emoji": "🤸", "action": "점프"},
    {"name": "노랑", "hex": "#FFD700", "emoji": "👏", "action": "손바닥 치기"},
]
EXTRA = [
    {"name": "분홍", "hex": "#FF4FB3", "emoji": "✌", "action": "브이"},
    {"name": "검정", "hex": "#111111", "emoji": "🐘", "action": "빙글빙글"},
]

def palette(level: str):
    return BASE + EXTRA if level == "어려움" else BASE

def circle_svg(color_hex: str, size: int) -> str:
    r = size * 0.40
    cx = cy = size / 2
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
      <rect width="{size}" height="{size}" fill="white"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="{color_hex}" />
    </svg>
    """

def show_circle(color_hex: str, size: int):
    st.markdown(circle_svg(color_hex, size), unsafe_allow_html=True)

def show_circle_center(color_hex: str, size: int):
    st.markdown(
        f'<div style="width:100%; display:flex; justify-content:center;">{circle_svg(color_hex, size)}</div>',
        unsafe_allow_html=True
    )

def pick_count(level: str) -> int:
    if level == "쉬움":
        return 1
    if level == "중간":
        return random.choices([1, 2, 3], weights=[50, 40, 10], k=1)[0]

    # ✅ 어려움 확률 설정
    # 1개: 40%, 2개: 30%, 3개: 20%, 4개: 6%, 5개: 4%
    return random.choices([1, 2, 3, 4, 5], weights=[40, 30, 20, 6, 4], k=1)[0]

def make_round(level: str):
    colors = palette(level)
    k = pick_count(level)
    if k <= len(colors):
        return random.sample(colors, k=k)
    return [random.choice(colors) for _ in range(k)]

# state
if "body_level" not in st.session_state:
    st.session_state.body_level = "쉬움"
if "body_round" not in st.session_state:
    st.session_state.body_round = make_round(st.session_state.body_level)

# 난이도 선택(상단만)
level = st.radio(
    "난이도", ["쉬움", "중간", "어려움"],
    horizontal=True,
    index=["쉬움", "중간", "어려움"].index(st.session_state.body_level)
)

if st.session_state.body_level != level:
    st.session_state.body_level = level
    st.session_state.body_round = make_round(level)

# -----------------------------
# 메인: 문제 영역 (제목 옆에 작은 버튼)
# -----------------------------
st.divider()

h1, h2 = st.columns([5, 1])
with h1:
    st.markdown("## 🎯 지금 나오는 색을 몸으로 표현해요!")
with h2:
    st.write("")  # 높이 맞춤
    if st.button("다음 ▶"):
        st.session_state.body_round = make_round(level)
        st.rerun()

round_items = st.session_state.body_round
k = len(round_items)

# 동그라미 크기(개수 많아지면 자동으로 줄이기)
if k == 1:
    Q_SIZE = 520 if level == "어려움" else 440
elif k == 2:
    Q_SIZE = 420
elif k == 3:
    Q_SIZE = 360
elif k == 4:
    Q_SIZE = 300
else:  # k == 5
    Q_SIZE = 270

# 문제 동그라미 배치
if k == 1:
    show_circle_center(round_items[0]["hex"], size=Q_SIZE)

elif k == 2:
    spacerL, c1, c2, spacerR = st.columns([1, 2, 2, 1])
    with c1:
        show_circle(round_items[0]["hex"], size=Q_SIZE)
    with c2:
        show_circle(round_items[1]["hex"], size=Q_SIZE)

elif k == 3:
    spacerL, c1, c2, c3, spacerR = st.columns([1, 2, 2, 2, 1])
    with c1:
        show_circle(round_items[0]["hex"], size=Q_SIZE)
    with c2:
        show_circle(round_items[1]["hex"], size=Q_SIZE)
    with c3:
        show_circle(round_items[2]["hex"], size=Q_SIZE)

elif k == 4:
    spacerL, c1, c2, c3, c4, spacerR = st.columns([1, 2, 2, 2, 2, 1])
    with c1:
        show_circle(round_items[0]["hex"], size=Q_SIZE)
    with c2:
        show_circle(round_items[1]["hex"], size=Q_SIZE)
    with c3:
        show_circle(round_items[2]["hex"], size=Q_SIZE)
    with c4:
        show_circle(round_items[3]["hex"], size=Q_SIZE)

else:  # k == 5
    spacerL, c1, c2, c3, c4, c5, spacerR = st.columns([1, 2, 2, 2, 2, 2, 1])
    with c1:
        show_circle(round_items[0]["hex"], size=Q_SIZE)
    with c2:
        show_circle(round_items[1]["hex"], size=Q_SIZE)
    with c3:
        show_circle(round_items[2]["hex"], size=Q_SIZE)
    with c4:
        show_circle(round_items[3]["hex"], size=Q_SIZE)
    with c5:
        show_circle(round_items[4]["hex"], size=Q_SIZE)

# -----------------------------
# 서브: 동작 규칙(접어서 보기)
# -----------------------------
st.divider()
with st.expander("👀 동작 규칙 보기 (필요할 때만 펼치기)", expanded=False):
    items = palette(level)
    RULE_CIRCLE = 70
    RULE_EMOJI = 44
    RULE_TEXT = 20

    cols = st.columns(len(items))
    for i, it in enumerate(items):
        with cols[i]:
            show_circle(it["hex"], size=RULE_CIRCLE)
            st.markdown(
                f"""
                <div style="text-align:center;">
                  <div style="font-size:{RULE_EMOJI}px; line-height:1.0;">{it['emoji']}</div>
                  <div style="font-size:{RULE_TEXT}px; font-weight:900;">{it['name']}</div>
                  <div style="font-size:{RULE_TEXT}px; font-weight:900;">{it['action']}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
