"""PBTD 카카오모먼트 주간 분석 → HTML 보고서 생성"""
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ──────────────────────────────────────────────
# 데이터 (app.py와 동일)
# ──────────────────────────────────────────────
RAW = {
    "캠페인": [
        "bizboard-retarget", "bizboard-retarget",
        "bizboard-ua", "bizboard-ua",
        "display-retarget", "display-retarget",
        "kakao 합계", "kakao 합계",
    ],
    "주차": ["W1", "W2", "W1", "W2", "W1", "W2", "W1", "W2"],
    "Impressions": [8_909_505, 11_116_000, 1_618_645, 2_892_869, 1_494_490, 850_437, 12_022_640, 14_859_306],
    "Clicks": [61_178, 65_497, 11_900, 12_653, 26_972, 15_252, 100_050, 93_402],
    "비용": [21_690_419, 23_643_311, 2_394_221, 2_719_175, 10_444_799, 5_334_921, 34_529_439, 31_697_407],
    "회원가입": [7, 16, 251, 427, 5, 3, 263, 446],
    "구매완료": [1_127, 1_449, 107, 214, 509, 295, 1_743, 1_958],
    "구매액": [66_387_990, 63_758_221, 4_914_681, 7_037_535, 31_049_160, 14_185_722, 102_351_831, 84_981_478],
    "구매유저(App)": [744, 931, 29, 47, 351, 203, 1_124, 1_181],
    "구매유저(Web)": [277, 396, 74, 162, 106, 64, 457, 622],
}

df = pd.DataFrame(RAW)
df["구매유저 합계"] = df["구매유저(App)"] + df["구매유저(Web)"]

W2_DB_COST = 31_697_407
W2_AIRBRIDGE_COST = 32_374_233
W2_RATIO = W2_AIRBRIDGE_COST / W2_DB_COST
df.loc[df["주차"] == "W2", "비용"] = (df.loc[df["주차"] == "W2", "비용"] * W2_RATIO).round(0).astype(int)
df.loc[(df["주차"] == "W2") & (df["캠페인"] == "kakao 합계"), "비용"] = W2_AIRBRIDGE_COST

ROAS_FACTOR = 1.763
df["CTR"] = df["Clicks"] / df["Impressions"] * 100
df["CPC"] = df["비용"] / df["Clicks"]
df["가입 CVR"] = df["회원가입"] / df["Clicks"] * 100
df["구매 CVR"] = df["구매완료"] / df["Clicks"] * 100
df["구매 CPA"] = df["비용"] / df["구매완료"]
df["ROAS"] = df["구매액"] / df["비용"] * ROAS_FACTOR * 100
df["ARPPU"] = df["구매액"] / df["구매유저 합계"]

CAMPAIGNS = ["bizboard-retarget", "bizboard-ua", "display-retarget"]
COLORS = {"bizboard-retarget": "#FAE100", "bizboard-ua": "#3C1E1E", "display-retarget": "#FF6B35"}
MARGIN = dict(t=50, b=40, l=10, r=10)

# ──────────────────────────────────────────────
# KPI 계산
# ──────────────────────────────────────────────
w1 = df[(df["캠페인"] == "kakao 합계") & (df["주차"] == "W1")].iloc[0]
w2 = df[(df["캠페인"] == "kakao 합계") & (df["주차"] == "W2")].iloc[0]

def pct_change(v1, v2):
    if v1 == 0: return "N/A"
    return f"{(v2 - v1) / v1 * 100:+.1f}%"

kpis = [
    ("비용", f"{w2['비용']:,.0f}원", pct_change(w1["비용"], w2["비용"])),
    ("구매완료", f"{w2['구매완료']:,.0f}건", pct_change(w1["구매완료"], w2["구매완료"])),
    ("구매액", f"{w2['구매액']:,.0f}원", pct_change(w1["구매액"], w2["구매액"])),
    ("ROAS", f"{w2['ROAS']:.2f}%", pct_change(w1["ROAS"], w2["ROAS"])),
    ("구매 CPA", f"{w2['구매 CPA']:,.0f}원", pct_change(w1["구매 CPA"], w2["구매 CPA"])),
    ("ARPPU", f"{w2['ARPPU']:,.0f}원", pct_change(w1["ARPPU"], w2["ARPPU"])),
]

# ──────────────────────────────────────────────
# 차트 생성
# ──────────────────────────────────────────────
charts_html = []

def add_chart(fig, height=400):
    max_y = max((v for t in fig.data for v in (t.y if hasattr(t, "y") and t.y is not None else []) if isinstance(v, (int, float))), default=0)
    fig.update_layout(margin=MARGIN, height=height)
    if max_y > 0:
        fig.update_yaxes(range=[0, max_y * 1.2])
    charts_html.append(fig.to_html(full_html=False, include_plotlyjs=False))

# 1. CTR
fig = go.Figure()
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=c, x=d["주차"], y=d["CTR"], marker_color=COLORS[c],
                         text=[f"{v:.2f}%" for v in d["CTR"]], textposition="outside"))
fig.update_layout(title="CTR (클릭률)", yaxis_title="%", barmode="group")
add_chart(fig)

# 2. CPC
fig = go.Figure()
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=c, x=d["주차"], y=d["CPC"], marker_color=COLORS[c],
                         text=[f"{v:,.0f}원" for v in d["CPC"]], textposition="outside"))
fig.update_layout(title="CPC (클릭당 비용)", yaxis_title="원", barmode="group")
add_chart(fig)

# 3. 구매 CVR
fig = go.Figure()
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=c, x=d["주차"], y=d["구매 CVR"], marker_color=COLORS[c],
                         text=[f"{v:.2f}%" for v in d["구매 CVR"]], textposition="outside"))
fig.update_layout(title="구매 CVR (구매완료 / Clicks)", yaxis_title="%", barmode="group")
add_chart(fig)

# 4. 구매 CPA
fig = go.Figure()
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=c, x=d["주차"], y=d["구매 CPA"], marker_color=COLORS[c],
                         text=[f"{v:,.0f}원" for v in d["구매 CPA"]], textposition="outside"))
fig.update_layout(title="구매 CPA (비용 / 구매완료)", yaxis_title="원", barmode="group")
add_chart(fig)

# 5. ROAS
fig = go.Figure()
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=c, x=d["주차"], y=d["ROAS"], marker_color=COLORS[c],
                         text=[f"{v:.0f}%" for v in d["ROAS"]], textposition="outside"))
fig.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="손익분기 100%")
fig.update_layout(title="ROAS (에어브릿지 ROAS × 1.763)", yaxis_title="%", barmode="group")
add_chart(fig)

# 6. ARPPU
fig = go.Figure()
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=c, x=d["주차"], y=d["ARPPU"], marker_color=COLORS[c],
                         text=[f"{v:,.0f}원" for v in d["ARPPU"]], textposition="outside"))
fig.update_layout(title="ARPPU (구매액 / 구매유저수)", yaxis_title="원", barmode="group")
add_chart(fig)

# 7. 구매액 vs 비용
fig = make_subplots(specs=[[{"secondary_y": True}]])
for c in CAMPAIGNS:
    d = df[df["캠페인"] == c]
    fig.add_trace(go.Bar(name=f"{c} 구매액", x=[f"{c}<br>{w}" for w in d["주차"]],
                         y=d["구매액"].values, marker_color=COLORS[c], opacity=0.8), secondary_y=False)
    fig.add_trace(go.Scatter(name=f"{c} 비용", x=[f"{c}<br>{w}" for w in d["주차"]],
                             y=d["비용"].values, mode="markers+lines",
                             marker=dict(size=10, color=COLORS[c]), line=dict(dash="dot")), secondary_y=True)
fig.update_layout(title="캠페인별 구매액(막대) vs 비용(점선)", barmode="group", margin=MARGIN, height=450)
fig.update_yaxes(title_text="구매액 (원)", secondary_y=False)
fig.update_yaxes(title_text="비용 (원)", secondary_y=True)
charts_html.append(fig.to_html(full_html=False, include_plotlyjs=False))

# ──────────────────────────────────────────────
# 데이터 테이블 생성
# ──────────────────────────────────────────────
table_df = df[["캠페인", "주차", "Impressions", "Clicks", "비용", "구매완료", "구매액",
               "CTR", "CPC", "구매 CVR", "구매 CPA", "ROAS", "ARPPU"]].copy()
table_df["Impressions"] = table_df["Impressions"].apply(lambda x: f"{x:,.0f}")
table_df["Clicks"] = table_df["Clicks"].apply(lambda x: f"{x:,.0f}")
table_df["비용"] = table_df["비용"].apply(lambda x: f"{x:,.0f}원")
table_df["구매완료"] = table_df["구매완료"].apply(lambda x: f"{x:,.0f}")
table_df["구매액"] = table_df["구매액"].apply(lambda x: f"{x:,.0f}원")
table_df["CTR"] = table_df["CTR"].apply(lambda x: f"{x:.2f}%")
table_df["CPC"] = table_df["CPC"].apply(lambda x: f"{x:,.0f}원")
table_df["구매 CVR"] = table_df["구매 CVR"].apply(lambda x: f"{x:.2f}%")
table_df["구매 CPA"] = table_df["구매 CPA"].apply(lambda x: f"{x:,.0f}원")
table_df["ROAS"] = table_df["ROAS"].apply(lambda x: f"{x:.2f}%")
table_df["ARPPU"] = table_df["ARPPU"].apply(lambda x: f"{x:,.0f}원")

# 증감률 테이블
change_rows = []
metrics = ["Impressions", "Clicks", "비용", "구매완료", "구매액", "구매 CVR", "구매 CPA", "ROAS", "ARPPU"]
orig = df.copy()
for camp in CAMPAIGNS + ["kakao 합계"]:
    row = {"캠페인": camp}
    cd = orig[orig["캠페인"] == camp]
    r1, r2 = cd[cd["주차"] == "W1"].iloc[0], cd[cd["주차"] == "W2"].iloc[0]
    for m in metrics:
        v1, v2 = r1[m], r2[m]
        row[m] = f"{(v2-v1)/v1*100:+.1f}%" if v1 != 0 else "N/A"
    change_rows.append(row)
change_df = pd.DataFrame(change_rows)

# ──────────────────────────────────────────────
# HTML 생성
# ──────────────────────────────────────────────
kpi_cards = ""
for label, value, delta in kpis:
    color = "#22c55e" if delta.startswith("+") else "#ef4444" if delta.startswith("-") else "#6b7280"
    # CPA, 비용은 감소가 좋음 → 색상 반전
    if label in ("구매 CPA", "비용") and delta.startswith("-"):
        color = "#22c55e"
    elif label in ("구매 CPA", "비용") and delta.startswith("+"):
        color = "#ef4444"
    kpi_cards += f"""
    <div class="kpi-card">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-delta" style="color:{color}">{delta}</div>
    </div>"""

html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PBTD 카카오모먼트 주간 분석</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ font-family: -apple-system, 'Pretendard', 'Noto Sans KR', sans-serif; background: #f8f9fa; color: #191919; padding: 24px; max-width: 1400px; margin: 0 auto; }}
    h1 {{ font-size: 28px; margin-bottom: 4px; }}
    .subtitle {{ color: #6b7280; font-size: 14px; margin-bottom: 24px; }}
    .kpi-row {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: 16px; margin-bottom: 32px; }}
    .kpi-card {{ background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    .kpi-label {{ font-size: 13px; color: #6b7280; margin-bottom: 4px; }}
    .kpi-value {{ font-size: 22px; font-weight: 700; }}
    .kpi-delta {{ font-size: 14px; font-weight: 600; margin-top: 4px; }}
    .section {{ margin-bottom: 40px; }}
    .section h2 {{ font-size: 20px; margin-bottom: 16px; border-bottom: 2px solid #FAE100; padding-bottom: 8px; }}
    .chart-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }}
    .chart-box {{ background: white; border-radius: 12px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    .chart-full {{ background: white; border-radius: 12px; padding: 16px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 24px; }}
    table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
    th {{ background: #1f2937; color: white; padding: 10px 8px; text-align: right; white-space: nowrap; }}
    th:first-child, th:nth-child(2) {{ text-align: left; }}
    td {{ padding: 8px; border-bottom: 1px solid #e5e7eb; text-align: right; white-space: nowrap; }}
    td:first-child, td:nth-child(2) {{ text-align: left; font-weight: 600; }}
    tr:hover {{ background: #f3f4f6; }}
    tr.total {{ background: #fef3c7; font-weight: 700; }}
    .insight-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin-bottom: 24px; }}
    .insight-box {{ background: white; border-radius: 12px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    .insight-box h3 {{ font-size: 16px; margin-bottom: 12px; }}
    .insight-box ul {{ padding-left: 20px; line-height: 1.8; font-size: 14px; }}
    .action-box {{ background: #fffbeb; border: 1px solid #fbbf24; border-radius: 12px; padding: 20px; }}
    .action-box h3 {{ font-size: 16px; margin-bottom: 12px; }}
    .action-box ol {{ padding-left: 20px; line-height: 2; font-size: 14px; }}
    .footer {{ text-align: center; color: #9ca3af; font-size: 12px; margin-top: 40px; padding-top: 20px; border-top: 1px solid #e5e7eb; }}
    @media (max-width: 768px) {{
        .kpi-row {{ grid-template-columns: repeat(3, 1fr); }}
        .chart-grid, .insight-grid {{ grid-template-columns: 1fr; }}
    }}
</style>
</head>
<body>

<h1>📊 PBTD 카카오모먼트 주간 분석</h1>
<p class="subtitle">W1 (3/23~3/29) vs W2 (3/30~4/5) | ROAS = 에어브릿지 ROAS × 1.763 (보정계수)</p>

<!-- KPI -->
<div class="section">
    <h2>핵심 KPI (kakao 합계, W2 기준)</h2>
    <div class="kpi-row">{kpi_cards}</div>
</div>

<!-- 유입 -->
<div class="section">
    <h2>📈 유입 지표</h2>
    <div class="chart-grid">
        <div class="chart-box">{charts_html[0]}</div>
        <div class="chart-box">{charts_html[1]}</div>
    </div>
</div>

<!-- 구매 -->
<div class="section">
    <h2>💰 구매 지표</h2>
    <div class="chart-grid">
        <div class="chart-box">{charts_html[2]}</div>
        <div class="chart-box">{charts_html[3]}</div>
    </div>
    <div class="chart-grid">
        <div class="chart-box">{charts_html[4]}</div>
        <div class="chart-box">{charts_html[5]}</div>
    </div>
    <div class="chart-full">{charts_html[6]}</div>
</div>

<!-- 데이터 테이블 -->
<div class="section">
    <h2>📋 캠페인별 데이터</h2>
    <div class="chart-full" style="overflow-x:auto;">
        {table_df.to_html(index=False, classes="", border=0).replace('<tr>', '<tr class="total">' if False else '<tr>').replace("kakao 합계", '<strong>kakao 합계</strong>')}
    </div>
</div>

<div class="section">
    <h2>📊 W1 → W2 증감률</h2>
    <div class="chart-full" style="overflow-x:auto;">
        {change_df.to_html(index=False, classes="", border=0).replace("kakao 합계", '<strong>kakao 합계</strong>')}
    </div>
</div>

<!-- 인사이트 -->
<div class="section">
    <h2>💡 핵심 인사이트</h2>
    <div class="insight-grid">
        <div class="insight-box">
            <h3>✅ 긍정적 변화</h3>
            <ul>
                <li><strong>구매 CVR</strong> 1.74% → 2.10% (+20.7%) 전환 효율 개선</li>
                <li><strong>구매 CPA</strong> 비용 기준 하락, 효율 개선</li>
                <li><strong>bizboard-ua</strong> 구매 +100%, ROAS 성장세</li>
                <li><strong>lecaf_selection</strong> (ua) 가입 393건, 가장 효율적</li>
            </ul>
        </div>
        <div class="insight-box">
            <h3>⚠️ 주의 필요</h3>
            <ul>
                <li><strong>display-retarget 전반 급감</strong>: 노출 -43%, 구매액 -54%</li>
                <li><strong>ROAS 하락</strong>: 522.59% → 462.78% (-11.4%)</li>
                <li><strong>ARPPU 전반 하락</strong>: 객단가 감소 추세</li>
                <li><strong>bizboard-retarget</strong>: 구매↑ but 구매액↓</li>
            </ul>
        </div>
    </div>
    <div class="action-box">
        <h3>📌 다음 액션 제안</h3>
        <ol>
            <li><strong>display-retarget</strong> 예산/소재 변경 이력 확인 → 급감 원인 파악</li>
            <li><strong>bizboard-ua lecaf_selection</strong> 예산 증액 검토 → 가입 효율 우수</li>
            <li><strong>ARPPU 하락 원인</strong> → 구매 상품 카테고리/할인율 변화 추가 분석</li>
            <li>W2 신규 광고그룹 (ct_hiking, ct_shortsleeve, ct_warehouserelease) 초기 성과 모니터링</li>
        </ol>
    </div>
</div>

<div class="footer">
    PBTD 카카오모먼트 주간 분석 | 데이터 기준: 에어브릿지 | 생성일: 2026-04-07
</div>

</body>
</html>"""

output_path = "/Users/jeon/workspace/projects/카카오-주간분석/2026-04-07_PBTD_카카오모먼트_주간분석.html"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"생성 완료: {output_path}")
