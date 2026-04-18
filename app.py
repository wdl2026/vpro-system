import streamlit as st
import pandas as pd

# 1. 战区级 UI 布局
st.set_page_config(page_title="V-PRO INTELLIGENCE HUB", layout="wide")
st.markdown("<style>.main { background-color: #05070a; color: #00ff41; }</style>", unsafe_allow_html=True)

st.title("📡 V-PRO: 全球选品情报与决策中心")

# 2. 情报抓取模块 (这就是你要的“入口”)
with st.sidebar:
    st.header("🔍 实时情报入口")
    keyword = st.text_input("输入调研关键词", value="Home Decor")
    
    st.write("---")
    st.write("👉 [TikTok 官方爆量素材库](https://ads.tiktok.com/business/creativecenter/inspiration/popular/pc/en)")
    st.write("👉 [Amazon 市场热度透视](https://www.amazon.com/s?k=" + keyword + ")")
    st.write("👉 [Google Trends 趋势监控](https://trends.google.com/trends/explore?q=" + keyword + ")")

# 3. 核心决策矩阵 (把搜到的数据变现)
st.subheader("⚔️ 情报压测与胜率判定")
c1, c2 = st.columns([1, 2])

with c1:
    st.info("从情报工具中抓取数据填入")
    p_price = st.number_input("拟售价格 ($)", 29.9)
    p_cost = st.number_input("进货+运费 ($)", 12.0)
    p_cac = st.slider("预估获客成本 (CAC)", 5.0, 30.0, 15.0)

with c2:
    # 工业级费率计算 (含平台佣金/损耗)
    margin = p_price - p_cost - p_cac - (p_price * 0.15) 
    roi = (margin / (p_cost + p_cac)) * 100 if (p_cost + p_cac) > 0 else 0
    
    st.subheader("📊 实时战损评估")
    col_a, col_b = st.columns(2)
    col_a.metric("单均利润", f"${margin:.2f}")
    col_b.metric("ROI 预判", f"{roi:.1%}")
    
    if roi > 40: st.success("✅ **SS级机会**：情报显示该品类利润厚，建议立刻从 PiPiADS 扒素材开测！")
    elif roi > 0: st.warning("⚠️ **B级博弈**：利润微薄，除非你有独家素材，否则容易给平台打工。")
    else: st.error("🚨 **自杀指令**：模型显示亏损，情报中看到的单量全是虚的，别进！")

# 4. 竞品对比实验室
st.divider()
st.subheader("📈 市场竞品胜率排位")
battle_data = pd.DataFrame([
    {"品类": "方案 A (高价品牌)", "售价": 49.9, "胜率": 85},
    {"品类": "方案 B (低价跑量)", "售价": 19.9, "胜率": 22},
])
st.bar_chart(battle_data, x="品类", y="胜率")
