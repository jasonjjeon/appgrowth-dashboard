import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import date

REDASH_URL = "http://52.79.76.239"
REDASH_API_KEY = "jdfeLA7zhMRizlsTPz0TYF8f8Uy68P0aON3nyaBx"
DATA_SOURCE_ID = 7  # DATA_DB (mysql)

st.set_page_config(
    page_title="카카오 광고그룹 ROAS 대시보드",
    page_icon="📊",
    layout="wide"
)

st.title("📊 카카오 광고그룹 ROAS 대시보드")
st.caption(f"기준일: {date.today().strftime('%Y-%m-%d')} | 채널: Kakao | 자동 새로고침: 1시간")

SQL = """
SELECT
    ad_group,
    campaign,
    SUM(CASE WHEN report_date >= DATE_SUB(CURDATE(), INTERVAL 1 DAY)  THEN cost ELSE 0 END) AS cost_1d,
    SUM(CASE WHEN report_date >= DATE_SUB(CURDATE(), INTERVAL 1 DAY)  THEN revenue ELSE 0 END) AS revenue_1d,
    ROUND(
        SUM(CASE WHEN report_date >= DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN revenue ELSE 0 END) /
        NULLIF(SUM(CASE WHEN report_date >= DATE_SUB(CURDATE(), INTERVAL 1 DAY) THEN cost ELSE 0 END), 0), 2
    ) AS roas_1d,
    SUM(CASE WHEN report_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)  THEN cost ELSE 0 END) AS cost_7d,
    SUM(CASE WHEN report_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)  THEN revenue ELSE 0 END) AS revenue_7d,
    ROUND(
        SUM(CASE WHEN report_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) THEN revenue ELSE 0 END) /
        NULLIF(SUM(CASE WHEN report_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY) THEN cost ELSE 0 END), 0), 2
    ) AS roas_7d,
    SUM(CASE WHEN report_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN cost ELSE 0 END) AS cost_30d,
    SUM(CASE WHEN report_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN revenue ELSE 0 END) AS revenue_30d,
    ROUND(
        SUM(CASE WHEN report_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN revenue ELSE 0 END) /
        NULLIF(SUM(CASE WHEN report_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY) THEN cost ELSE 0 END), 0), 2
    ) AS roas_30d
FROM marketing_cost
WHERE channel = 'kakao'
  AND report_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
GROUP BY ad_group, campaign
HAVING cost_30d > 0
ORDER BY COALESCE(roas_7d, 0) DESC
"""

@st.cache_data(ttl=3600)
def load_data():
    resp = requests.post(
        f"{REDASH_URL}/api/query_results",
        headers={"Authorization": f"Key {REDASH_API_KEY}"},
        json={"data_source_id": DATA_SOURCE_ID, "query": SQL, "max_age": 3600},
        timeout=60
    )
    resp.raise_for_status()
    data = resp.json()
    rows = data["query_result"]["data"]["rows"]
    return pd.DataFrame(rows)

with st.spinner("데이터 불러오는 중..."):
    try:
        df = load_data()
    except Exception as e:
        st.error(f"데이터 로드 실패: {e}")
        st.stop()

for col in ["cost_1d", "revenue_1d", "roas_1d", "cost_7d", "revenue_7d", "roas_7d", "cost_30d", "revenue_30d", "roas_30d"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 캠페인 필터
campaigns = ["전체"] + sorted(df["campaign"].dropna().unique().tolist())
selected = st.selectbox("캠페인 필터", campaigns)
filtered = df if selected == "전체" else df[df["campaign"] == selected]

# 요약 지표
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("광고그룹 수", f"{len(filtered):,}개")
with c2:
    v = filtered[filtered["cost_1d"] > 0]["roas_1d"].mean()
    st.metric("평균 ROAS (1일)", f"{v:.2f}" if pd.notna(v) else "-")
with c3:
    v = filtered[filtered["cost_7d"] > 0]["roas_7d"].mean()
    st.metric("평균 ROAS (7일)", f"{v:.2f}" if pd.notna(v) else "-")
with c4:
    v = filtered[filtered["cost_30d"] > 0]["roas_30d"].mean()
    st.metric("평균 ROAS (30일)", f"{v:.2f}" if pd.notna(v) else "-")

st.divider()

# 상위 20개 ROAS 비교 차트
st.subheader("ROAS 비교 — 상위 20개 광고그룹 (7일 기준)")
top20 = filtered[filtered["cost_7d"] > 0].nlargest(20, "roas_7d").copy()
top20["label"] = top20["ad_group"].str[:38]

fig = go.Figure()
fig.add_trace(go.Bar(name="1일 ROAS",  x=top20["label"], y=top20["roas_1d"],  marker_color="#FFD700"))
fig.add_trace(go.Bar(name="7일 ROAS",  x=top20["label"], y=top20["roas_7d"],  marker_color="#FF6B00"))
fig.add_trace(go.Bar(name="30일 ROAS", x=top20["label"], y=top20["roas_30d"], marker_color="#8B3A00"))
fig.update_layout(
    barmode="group",
    xaxis_tickangle=-40,
    height=460,
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
    margin=dict(b=130),
    yaxis_title="ROAS",
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# 상세 테이블
st.subheader("전체 광고그룹 상세 성과표")

def fmt_won(v):
    return f"₩{int(v):,}" if pd.notna(v) and v > 0 else "-"

def fmt_roas(v):
    return f"{v:.2f}" if pd.notna(v) else "-"

table = filtered[[
    "ad_group", "campaign",
    "cost_1d", "revenue_1d", "roas_1d",
    "cost_7d", "revenue_7d", "roas_7d",
    "cost_30d", "revenue_30d", "roas_30d",
]].copy()

table.columns = [
    "광고그룹", "캠페인",
    "광고비(1일)", "매출(1일)", "ROAS(1일)",
    "광고비(7일)", "매출(7일)", "ROAS(7일)",
    "광고비(30일)", "매출(30일)", "ROAS(30일)",
]

for c in ["광고비(1일)", "매출(1일)", "광고비(7일)", "매출(7일)", "광고비(30일)", "매출(30일)"]:
    table[c] = table[c].apply(fmt_won)
for c in ["ROAS(1일)", "ROAS(7일)", "ROAS(30일)"]:
    table[c] = table[c].apply(fmt_roas)

def highlight_roas(val):
    try:
        v = float(val)
        if v >= 5:   return "color: #00AA00; font-weight: bold"
        elif v >= 3: return "color: #FF8800"
        else:        return "color: #CC0000"
    except:
        return ""

styled = table.style.applymap(highlight_roas, subset=["ROAS(1일)", "ROAS(7일)", "ROAS(30일)"])
st.dataframe(styled, use_container_width=True, height=520)
st.caption("ROAS 색상: 🟢 5 이상 우수 | 🟠 3~5 보통 | 🔴 3 미만 개선 필요")
