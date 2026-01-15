# app.py
import random
import streamlit as st

st.set_page_config(page_title="색과 모양으로 놀기 + 순서 지키기", layout="wide")

# -----------------------------
# Shared constants / helpers
# -----------------------------
RAINBOW_COLORS = [
    "#FF0000",  # red
    "#0000FF",
    "#FFD700",
    "#008000",
    "#8B4513"


]
BLACK = "#111111"

def render_svg(svg: str):
    st.markdown(
        f'<div style="display:flex;justify-content:center;align-items:center;">{svg}</div>',
        unsafe_allow_html=True,
    )

def big_center_text(text: str):
    st.markdown(
        f"""
        <div style="text-align:center;font-size:40px;font-weight:800;margin-top:10px;margin-bottom:10px;">
          {text}
        </div>
        """,
        unsafe_allow_html=True,
    )

def instruction_box(lines):
    st.info("\n".join([f"- {x}" for x in lines]))

# -----------------------------
# SVG shapes
# -----------------------------
def svg_circle(color: str, size: int = 360) -> str:
    r = size * 0.32
    cx = cy = size / 2
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
      <rect width="{size}" height="{size}" fill="white"/>
      <circle cx="{cx}" cy="{cy}" r="{r}" fill="{color}" />
    </svg>
    """

def svg_square(color: str, size: int = 360) -> str:
    s = size * 0.62
    x = y = (size - s) / 2
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
      <rect width="{size}" height="{size}" fill="white"/>
      <rect x="{x}" y="{y}" width="{s}" height="{s}" fill="{color}" rx="14"/>
    </svg>
    """

def svg_triangle(color: str, size: int = 360) -> str:
    pad = size * 0.18
    x1, y1 = size/2, pad
    x2, y2 = size - pad, size - pad
    x3, y3 = pad, size - pad
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
      <rect width="{size}" height="{size}" fill="white"/>
      <polygon points="{x1},{y1} {x2},{y2} {x3},{y3}" fill="{color}" />
    </svg>
    """

def svg_star(color: str, size: int = 360) -> str:
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <rect width="100" height="100" fill="white"/>
      <path d="M50 7 L61 38 L94 38 L66 57 L76 90 L50 71 L24 90 L34 57 L6 38 L39 38 Z"
            fill="{color}"/>
    </svg>
    """

def svg_heart(color: str, size: int = 360) -> str:
    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
      <rect width="100" height="100" fill="white"/>
      <path d="M50 84
               C20 64, 8 48, 12 34
               C16 20, 30 16, 40 26
               C45 31, 48 36, 50 39
               C52 36, 55 31, 60 26
               C70 16, 84 20, 88 34
               C92 48, 80 64, 50 84 Z"
            fill="{color}"/>
    </svg>
    """

SHAPES = [
    ("동그라미", svg_circle),
    ("네모", svg_square),
    ("세모", svg_triangle),
    ("별", svg_star),
    ("하트", svg_heart),
]

# -----------------------------
# Pattern game (rules)
# -----------------------------
TOKEN_A = ("빨강", "#FF3B30")
TOKEN_B = ("파랑", "#007AFF")
TOKEN_C = ("노랑", "#FFCC00")
TOKEN_D = ("초록", "#34C759")
TOKEN_E = ("갈색", "#8B5A2B")

EASY_TOKENS = [TOKEN_A, TOKEN_B]
HARD_TOKENS = [TOKEN_A, TOKEN_B, TOKEN_C, TOKEN_D, TOKEN_E]

# -----------------------------
# 규칙 생성
# -----------------------------
def make_rule(difficulty="easy"):
    easy_rules = [
        ("AB 반복", [TOKEN_A, TOKEN_B]),
        ("AABB 반복", [TOKEN_A, TOKEN_A, TOKEN_B, TOKEN_B]),
        ("AAB 반복", [TOKEN_A, TOKEN_A, TOKEN_B]),
    ]

    hard_rules = [
        # 5색 반복
        ("ABCDE 반복", [TOKEN_A, TOKEN_B, TOKEN_C, TOKEN_D, TOKEN_E]),
        ("EDCBA 반복", [TOKEN_E, TOKEN_D, TOKEN_C, TOKEN_B, TOKEN_A]),

        # 덩어리 규칙 (색 많아짐)
        ("AABBCCDDEE", [
            TOKEN_A, TOKEN_A,
            TOKEN_B, TOKEN_B,
            TOKEN_C, TOKEN_C,
            TOKEN_D, TOKEN_D,
            TOKEN_E, TOKEN_E,
        ]),

        # 대칭 규칙
        ("ABCDEDCBA", [
            TOKEN_A, TOKEN_B, TOKEN_C, TOKEN_D, TOKEN_E,
            TOKEN_D, TOKEN_C, TOKEN_B,
        ]),

        # 5색 교차
        ("ABCED 반복", [TOKEN_A, TOKEN_B, TOKEN_C, TOKEN_E, TOKEN_D]),
    ]

    if difficulty == "easy":
        return random.choice(easy_rules)
    else:
        return random.choice(hard_rules)

# -----------------------------
def build_sequence(pattern, length):
    return [pattern[i % len(pattern)] for i in range(length)]

# -----------------------------
def make_pattern_quiz(num_q=8, difficulty="easy"):
    quizzes = []
    token_pool = EASY_TOKENS if difficulty == "easy" else HARD_TOKENS

    for _ in range(num_q):
        rule_name, pattern = make_rule(difficulty)

        start_len = random.randint(4, 5) if difficulty == "easy" else random.randint(6, 9)

        seq = build_sequence(pattern, start_len)
        correct_next = pattern[start_len % len(pattern)]

        wrong_candidates = [t for t in token_pool if t != correct_next]
        wrong_next = random.choice(wrong_candidates)

        if random.random() < 0.5:
            left, right = correct_next, wrong_next
            answer = "왼쪽"
        else:
            left, right = wrong_next, correct_next
            answer = "오른쪽"

        quizzes.append({
            "rule_name": rule_name,
            "sequence": seq,
            "left": left,
            "right": right,
            "answer": answer,
        })

    return quizzes


def token_svg(token_color: str, token_label: str, size: int = 180) -> str:
    # Colored circle token with label
    r = size * 0.38
    cx = cy = size / 2
    text_y = size * 0.92

    return f"""
    <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" xmlns="http://www.w3.org/2000/svg">
      <rect width="{size}" height="{size}" fill="white"/>
      <circle cx="{cx}" cy="{cy*0.85}" r="{r}" fill="{token_color}"/>
      <text x="{cx}" y="{text_y}" text-anchor="middle" font-size="{int(size*0.14)}"
            font-family="sans-serif" fill="#111">{token_label}</text>
    </svg>
    """

# =============================
# 공용 색 토큰 (말로 구분 가능한 색만)
# =============================
TOKEN_RED    = ("빨강", "#FF0000")
TOKEN_BLUE   = ("파랑", "#0000FF")
TOKEN_YELLOW = ("노랑", "#FFD700")
TOKEN_GREEN  = ("초록", "#008000")
TOKEN_BROWN  = ("갈색", "#8B4513")

# -----------------------------
# Session defaults (shared)
# -----------------------------
if "color_idx" not in st.session_state:
    st.session_state.color_idx = random.randrange(len(RAINBOW_COLORS))

if "shape_idx" not in st.session_state:
    st.session_state.shape_idx = random.randrange(len(SHAPES))

if "pattern_quizzes" not in st.session_state:
    st.session_state.pattern_quizzes = make_pattern_quiz(num_q=6)

if "pattern_q_idx" not in st.session_state:
    st.session_state.pattern_q_idx = 0

if "show_answers" not in st.session_state:
    st.session_state.show_answers = False

# -----------------------------
# Home page
# -----------------------------
st.title("🎨 색과 모양으로 놀기 + 🎲 순서 지키기 게임")
st.write(
    """
초등 1~2학년 학생들이 **정답 입력 없이** 말과 몸으로 참여하는 수업용 웹앱입니다.  
왼쪽 사이드바에서 페이지를 골라 진행하세요.
"""
)

st.markdown("### 이 웹앱 구성")
st.markdown(
    """
- 🎨 랜덤 색 동그라미 (색 맞추기)
- ⚫ 검정색 랜덤 모양 (모양 맞추기)
- 🔴🔵 순서 지키기 (AB 규칙)
- 🧩 규칙 찾기 (왼쪽/오른쪽 선택, 마지막에 정답표)
- 🏃 몸으로 색 표현 (색-행동 규칙 반응)
"""
)

with st.sidebar:
    st.header("교사용 설정(공통)")
    st.session_state.show_answers = st.toggle("정답표 보기(규칙찾기)", value=st.session_state.show_answers)
    if st.button("🔄 규칙 찾기 문제 새로 만들기"):
        st.session_state.pattern_quizzes = make_pattern_quiz(num_q=6)
        st.session_state.pattern_q_idx = 0
        st.toast("새 문제 세트를 만들었어요!")
