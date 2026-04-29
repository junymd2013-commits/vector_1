import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
import math

st.set_page_config(page_title="ベクトルの内積と角度", layout="centered")

st.markdown("<h2 style='text-align:center;'>ベクトルの内積と角度を調べよう（Streamlit版）</h2>", unsafe_allow_html=True)

# --------------------------------
# 入力欄
# --------------------------------
st.subheader("ベクトルの成分を入力してください")

colA, colB = st.columns(2)

with colA:
    st.markdown("### ベクトル a")
    ax = st.text_input("a_x", "5", max_chars=6)
    ay = st.text_input("a_y", "3", max_chars=6)

with colB:
    st.markdown("### ベクトル b")
    bx = st.text_input("b_x", "-4", max_chars=6)
    by = st.text_input("b_y", "6", max_chars=6)

st.info("分数：1/2、平方根：sqrt(3) のように入力できます。")

# --------------------------------
# 安全な eval
# --------------------------------
def safe_eval(expr):
    safe_dict = {"sqrt": math.sqrt}
    return float(eval(expr, {"__builtins__": None}, safe_dict))

# --------------------------------
# 計算ボタン
# --------------------------------
if st.button("計算する"):
    try:
        ax_val = safe_eval(ax)
        ay_val = safe_eval(ay)
        bx_val = safe_eval(bx)
        by_val = safe_eval(by)
    except:
        st.error("入力が正しくありません。")
        st.stop()

    a = np.array([ax_val, ay_val])
    b = np.array([bx_val, by_val])

    # --------------------------------
    # グラフ描画
    # --------------------------------
    fig, axp = plt.subplots(figsize=(5, 5))

    axp.set_xlim(-10, 10)
    axp.set_ylim(-10, 10)
    axp.set_xticks(np.arange(-10, 11, 2))
    axp.set_yticks(np.arange(-10, 11, 2))
    axp.grid(True, alpha=0.3)

    axp.axhline(0, color="black", linewidth=1)
    axp.axvline(0, color="black", linewidth=1)

    # ベクトル a
    axp.arrow(0, 0, a[0], a[1], head_width=0.3, color="blue", length_includes_head=True)
    axp.text(a[0] + 0.3, a[1] + 0.3, "a", fontsize=14, color="blue")

    # ベクトル b
    axp.arrow(0, 0, b[0], b[1], head_width=0.3, color="red", length_includes_head=True)
    axp.text(b[0] + 0.3, b[1] + 0.3, "b", fontsize=14, color="red")

    # --------------------------------
    # 内積・角度計算
    # --------------------------------
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    if norm_a != 0 and norm_b != 0:
        # 内積から求めた角度（常に 0〜180°）
        cos_theta = dot / (norm_a * norm_b)
        cos_theta = np.clip(cos_theta, -1, 1)
        theta = np.degrees(np.arccos(cos_theta))  # ← これが正しい角度

        # --------------------------------
        # 角度の向きだけ atan2 で判定
        # --------------------------------
        angle_a = math.atan2(a[1], a[0])
        angle_b = math.atan2(b[1], b[0])

        # 向き（符号）だけ使う
        delta_raw = angle_b - angle_a
        direction = 1 if delta_raw >= 0 else -1

        # 扇形の開始角度（度）
        theta1 = math.degrees(angle_a)

        # 扇形の終了角度（度）
        theta2 = theta1 + direction * theta

        # 扇形の半径
        r = min(norm_a, norm_b) * 0.6

        wedge = Wedge(
            center=(0, 0),
            r=r,
            theta1=theta1,
            theta2=theta2,
            facecolor="green",
            alpha=0.25,
            edgecolor="green"
        )
        axp.add_patch(wedge)

    st.pyplot(fig)

    # --------------------------------
    # 結果表示
    # --------------------------------
    st.subheader("計算結果")

    st.write(f"**内積：{dot:.2f}**")
    st.write(f"**|a| = {norm_a:.2f}**,  **|b| = {norm_b:.2f}**")

    if norm_a == 0 or norm_b == 0:
        st.warning("角度：定義できません（どちらかがゼロベクトル）")
        st.stop()

    st.write(f"**角度：{theta:.2f}°**")

    if dot > 0:
        st.success("内積 > 0（鋭角）")
    elif dot < 0:
        st.error("内積 < 0（鈍角）")
    else:
        st.info("内積 = 0（直角）")
