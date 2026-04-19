import streamlit as st
import pandas as pd
import numpy as np
import requests
from pytrends.request import TrendReq

st.set_page_config(page_title="V-PRO REAL SYSTEM", layout="wide")

# =========================================================
# 🔍 1. 搜索入口
# =========================================================
st.sidebar.header("🔍 产品搜索")

user_input = st.sidebar.text_input("输入关键词（英文）", "dog bed")
search_btn = st.sidebar.button("🚀 搜索市场")

# =========================================================
# ⚙️ 参数控制（商业级）
# =========================================================
st.sidebar.header("⚙️ 商业参数")

fee_rate = st.sidebar.slider("平台抽成", 0.05, 0.3, 0.15)
cost_rate = st.sidebar.slider("成本比例", 0.1, 0.6, 0.3)
min_profit = st.sidebar.slider("最低利润过滤", 0, 20, 5)
min_prob = st.sidebar.slider("最低胜率过滤", 0.3, 0.9, 0.6)

# =========================================================
# 📦 2. 关键词扩展（找品核心）
# =========================================================
def expand_keywords(base):
    suffix = [
        "portable", "smart", "automatic",
        "kit", "tool", "pro", "mini"
    ]
    return list(set([base] + [f"{base} {s}" for s in suffix]))

# =========================================================
# 🛒 3. 市场数据（eBay）
# =========================================================
def get_market(keyword):

    url = "https://svcs.ebay.com/services/search/FindingService/v1"

    params = {
        "OPERATION-NAME": "findItemsByKeywords",
        "SERVICE-VERSION": "1.0.0",
        "RESPONSE-DATA-FORMAT": "JSON",
        "keywords": keyword,
        "GLOBAL-ID": "EBAY-AU",
        "paginationInput.entriesPerPage": 20
    }

    try:
        r = requests.get(url, params=params, timeout=10)
        data = r.json()

        items = data["findItemsByKeywordsResponse"][0]["searchResult"][0].get("item", [])

        prices = [
            float(i["sellingStatus"][0]["currentPrice"][0]["__value__"])
            for i in items
        ]

        if not prices:
            return None

        return {
            "price": np.median(prices),
            "competition": len(prices),
            "price_std": np.std(prices)
        }

    except:
        return None

# =========================================================
# 📈 4. 趋势动能
# =========================================================
def get_trend(keyword):

    try:
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], timeframe='today 3-m')
        data = pytrends.interest_over_time()

        if data.empty:
            return 0.0

        s = data[keyword]

        recent = s[-30:].mean()
        older = s[:-30].mean()

        if older == 0:
            return 0

        return (recent - older) / (older + 1e-5)

    except:
        return 0.0

# =========================================================
# 💰 5. 利润模型
# =========================================================
def profit(price):
    shipping = 10 if price < 50 else 18
    return price - shipping - price * fee_rate - price * cost_rate

# =========================================================
# 🧠 6. 概率模型（稳定版）
# =========================================================
def probability(momentum, profit_val, competition):

    comp = 1 / (competition + 1)

    raw = (
        momentum * 0.45 +
        profit_val * 0.35 +
        comp * 0.20
    )

    return 1 / (1 + np.exp(-raw))

# =========================================================
# 🎯 7. 决策系统（强过滤版）
# =========================================================
def decision(p, profit_val):

    if p > 0.75 and profit_val > 10:
        return "🔥 ALL IN"
    elif p > 0.65 and profit_val > 5:
        return "🚀 SCALE"
    else:
        return "❌ DROP"

# =========================================================
# 🧠 主程序
# =========================================================
st.title("🧠 V-PRO REAL（搜索版选品系统）")

if search_btn:

    base_keywords = [k.strip() for k in user_input.split(",")]

    candidates = []
    for k in base_keywords:
        candidates.extend(expand_keywords(k))

    results = []

    progress = st.progress(0)

    for i, c in enumerate(candidates):

        market = get_market(c)
        if not market:
            continue

        trend = get_trend(c)
        p_val = profit(market["price"])
        prob = probability(trend, p_val, market["competition"])

        # 🔥 强过滤（关键）
        if p_val < min_profit:
            continue

        if prob < min_prob:
            continue

        results.append({
            "product": c,
            "price": round(market["price"], 2),
            "profit": round(p_val, 2),
            "trend": round(trend, 2),
            "competition": market["competition"],
            "probability": round(prob, 2),
            "decision": decision(prob, p_val)
        })

        progress.progress((i + 1) / len(candidates))

    if len(results) == 0:
        st.warning("❌ 没筛出可做产品（建议换关键词）")
    else:
        df = pd.DataFrame(results).sort_values("probability", ascending=False)

        st.subheader("🔥 可执行产品（已过滤）")
        st.dataframe(df, use_container_width=True)

        st.subheader("🏆 TOP 3（直接干）")
        st.dataframe(df.head(3), use_container_width=True)
