
import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 核心工业配置
st.set_page_config(page_title="V-PRO ERP ULTIMATE", layout="wide")

# 2. 注入专业视觉样式
st.markdown("""
    <style>
    .main { background-color: #0b0e14; color: #e0e0e0; }
    .stMetric { background-color: #161b22; border-radius: 10px; padding: 15px; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# 3. 侧边栏控制
with st.sidebar:
    st.title("🎛️ 运营决策中心")
    platform = st.selectbox("核心渠道", ["TikTok Shop", "Amazon FBA", "Temu", "Shopify"])
    st.divider()
    u_cost = st.number_input("采购成本 ($)", value=12.5)
    ship = st.number_input("物流费用 ($)", value=8.0)
    price = st.number_input("拟售价格 ($)", value=45.0)
    cac = st.number_input("广告成本 (CAC)", value=15.0)
    st.divider()
    stock = st.number_input("当前库存", value=500)
    d_sales = st.number_input("日均销量", value=20)
    lead_time = st.slider("补货周期 (天)", 7, 60, 25)

# 4. 逻辑计算
fees = {"TikTok Shop": 0.08, "Amazon FBA": 0.15, "Temu": 0.05, "Shopify": 0.03}
f_amt = price * fees[platform]
net = price - u_cost - ship - cac - f_amt
roi = net / (u_cost + ship + cac) if (u_cost + ship + cac) > 0 else 0
days = stock / d_sales if d_sales > 0 else 999
reorder = "🚨 立即补货" if days <= lead_time else "✅ 库存充足"

# 5. 主看板
st.title(f"📊 V-PRO ERP | {platform} 看板")
c1, c2, c3, c4 = st.columns(4)
c1.metric("单均净利", f"${net:.2f}")
c2.metric("ROI", f"{roi:.1%}")
c3.metric("库存支撑", f"{days:.1f} 天")
c4.metric("补货决策", reorder)

st.divider()
col_l, col_r = st.columns([2, 1])
with col_l:
    st.subheader("📈 成本结构拆解")
    df = pd.DataFrame({"项": ["成本", "物流", "佣金", "广告", "利润"], "值": [u_cost, ship, f_amt, cac, max(0, net)]})
    st.plotly_chart(px.bar(df, x="项", y="值", color="项", text_auto=True), use_container_width=True)
with col_r:
    st.subheader("⚖️ 盈亏平衡点分析")
    be = u_cost + ship + cac + f_amt
    st.write(f"保本价: **${be:.2f}**")
    st.progress(min(max(price/(be*1.5), 0.0), 1.0), text="价格健康度")
