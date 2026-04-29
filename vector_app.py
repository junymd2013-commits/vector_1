import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import math

st.set_page_config(page_title="ベクトルの内積と角度", layout="wide")

st.title("ベクトルの内積と角度を調べよう（Streamlit版）")

# --------------------------------
# 入力欄（左右2カラム）
# --------------------------------
col1, col2 = st.columns(2)

with col1:
    st.subheader("ベクトル a の成分")
    ax = st.text_input("a_x", "5")
    ay = st.text_input("a_y", "3")

with col2:
    st.subheader("ベクトル b の成分")
    bx = st.text_input("b_x", "-4")
    by = st.text_input("b_y", "6")

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
    fig, axp = plt.subplots(figsize=(6, 6))

    axp.set_xlim(-10, 10)
    axp.set_ylim(-10, 10)
    axp.set_xticks(np.arange(-10, 11, 1))
    axp.set_yticks(np.arange(-10, 11, 1))
    axp.grid(True, alpha=0.3)

    axp.axhline(0, color="black", linewidth=1)
    axp.axvline(0, color="black", linewidth=1)

    # ベクトル a
    axp.arrow(0, 0, a[0], a[1], head_width=0.3, color="blue", length_includes_head=True)
    axp.text(a[0] + 0.3, a[1] + 0.3, "a", fontsize=14, color="blue")

    # ベクトル b
    axp.arrow(0, 0, b[0], b[1], head_width=0.3, color="red", length_includes_head=True)
    axp.text(b[0] + 0.3, b[1] + 0.3, "b", fontsize=14, color="red")

    st.pyplot(fig)

    # --------------------------------
    # 内積・角度計算
    # --------------------------------
    dot = np.dot(a, b)
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)

    st.subheader("計算結果")

    st.write(f"**内積：{dot:.2f}**")
    st.write(f"**|a| = {norm_a:.2f}**,  **|b| = {norm_b:.2f}**")

    if norm_a == 0 or norm_b == 0:
        st.warning("角度：定義できません（どちらかがゼロベクトル）")
        st.stop()

    cos_theta = dot / (norm_a * norm_b)
    cos_theta = np.clip(cos_theta, -1, 1)
    theta = np.degrees(np.arccos(cos_theta))

    st.write(f"**角度：{theta:.2f}°**")

    # --------------------------------
    # 鋭角・鈍角・直角の判定
    # --------------------------------
    if dot > 0:
        st.success("内積 > 0（鋭角）")
    elif dot < 0:
        st.error("内積 < 0（鈍角）")
    else:
        st.info("内積 = 0（直角）")
