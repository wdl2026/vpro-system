import streamlit as st
import pandas as pd

# 1. 战区级黑客 UI
st.set_page_config(page_title="V-PRO INTELLIGENCE HUB", layout="wide")
st.markdown("<style>.main { background-color: #05070a; color: #00ff41; }</style>", unsafe_allow_html=True)

st.title("📡 V-PRO: 全球选品情报与决策中心")

# 2. 集成搜索模块 (情报抓取入口)
with st.sidebar:
    st.header("🔍 实时情报扫描")
    keyword = st.text_input("输入调研关键词 (英文)", value="Heating Pad")
    
    st.write("---")
    # 动态链接：直接调用专业工具的搜索接口
    tt_url = f"https://ads.tiktok.com/business/creativecenter/inspiration/popular/pc/en?period=30&is_new_ontest=1&keyword={keyword}"
    az_url = f"https://www.amazon.com/s?k={keyword}"
    gt_url = f"https://trends.google.com/trends/explore?q={keyword}"
    
    st.markdown(f"👉 [**TikTok 爆量素材库**]({tt_url})")
    st.markdown(f"👉 [**Amazon 市场价格透视**]({az_url})")
    st.markdown(f"👉 [**Google Trends 趋势监控**]({gt_url})")

# 3. 核心决策矩阵 (情报 vs 利润)
st.subheader("⚔️ 情报压测与胜率判定")
c1, c2 = st.columns([1, 2])

with c1:
    st.info("将情报工具中搜索到的数据填入下方")
    p_price = st.number_input("拟售价格 ($)", 29.9)
    p_cost = st.number_input("采购+运费 ($)", 12.0)
    p_cac = st.slider("预估获客成本 (广告费/单)", 5.0, 30.0, 15.0)

with c2:
    # 财务判定逻辑 (Price - Cost - CAC - 15% Fees)
    margin = p_price - p_cost - p_cac - (p_price * 0.15) 
    roi = (margin / (p_cost + p_cac)) * 100 if (p_cost + p_cac) > 0 else 0
    
    st.subheader("📊 实时战损评估")
    col_a, col_b = st.columns(2)
    col_a.metric("单均利润", f"${margin:.2f}")
    col_b.metric("ROI 预判", f"{roi:.1%}")
    
    if roi > 40:
        st.success("✅ **SS级机会**：利润极厚，情报显示值得全力进攻！")
    elif roi > 0:
        st.warning("⚠️ **B级博弈**：利润微薄，必须靠极致素材才能赢。")
    else:
        st.error("🚨 **自杀指令**：情报中的单量全是虚的，该模型下必亏！")
