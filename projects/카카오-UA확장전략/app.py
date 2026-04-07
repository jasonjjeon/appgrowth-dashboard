import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="카카오 UA 확장 전략", layout="wide")

# ─── 커스텀 스타일 ───
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; }
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        padding: 1.2rem; border-radius: 12px; text-align: center;
        border: 1px solid #0f3460; margin-bottom: 0.5rem;
    }
    .metric-card h3 { color: #94a3b8; font-size: 0.85rem; margin: 0; }
    .metric-card h1 { color: #e2e8f0; font-size: 1.8rem; margin: 0.3rem 0 0 0; }
    .tier-1 { border-left: 4px solid #22c55e; padding-left: 12px; margin-bottom: 8px; }
    .tier-2 { border-left: 4px solid #eab308; padding-left: 12px; margin-bottom: 8px; }
    .tier-3 { border-left: 4px solid #ef4444; padding-left: 12px; margin-bottom: 8px; }
    .section-header {
        background: linear-gradient(90deg, #1e3a5f, transparent);
        padding: 8px 16px; border-radius: 8px; margin: 1.5rem 0 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ─── 헤더 ───
st.title("카카오 UA 확장 전략")
st.caption("기준 기간: 2026.03.09 ~ 04.06 | 보정계수 1.76 | 목표 ROAS 400%")

# ═══════════════════════════════════════════
# 1. 현재 현황 요약
# ═══════════════════════════════════════════
st.markdown('<div class="section-header"><h3>현재 카카오 리타게팅 현황 (PBTD 2개 캠페인)</h3></div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown('<div class="metric-card"><h3>총 비용 (4주)</h3><h1>1.13억</h1></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card"><h3>총 매출 (4주)</h3><h1>3.19억</h1></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card"><h3>보정 ROAS</h3><h1>497%</h1></div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card"><h3>평균 CPC</h3><h1>375원</h1></div>', unsafe_allow_html=True)
with col5:
    st.markdown('<div class="metric-card"><h3>총 전환</h3><h1>5,753건</h1></div>', unsafe_allow_html=True)

# ─── 주간 추이 차트 ───
weekly_data = pd.DataFrame({
    "주차": ["11주차\n(3/9~)", "12주차\n(3/16~)", "13주차\n(3/23~)", "14주차\n(3/30~)"],
    "RT 비용(만)": [2935, 2244, 3214, 2898],
    "RT ROAS(raw)": [2.50, 2.64, 3.03, 2.69],
    "RT ROAS(보정)": [4.40, 4.65, 5.33, 4.73],
    "UA 비용(만)": [5471, 6278, 5115, 3705],
    "UA ROAS(raw)": [2.85, 2.86, 2.77, 2.66],
    "UA ROAS(보정)": [5.02, 5.03, 4.88, 4.68],
})

col_left, col_right = st.columns(2)
with col_left:
    fig_roas = go.Figure()
    fig_roas.add_trace(go.Scatter(
        x=weekly_data["주차"], y=weekly_data["RT ROAS(보정)"],
        name="RT 보정 ROAS", mode="lines+markers+text",
        text=[f"{v:.0%}" for v in weekly_data["RT ROAS(보정)"]],
        textposition="top center", line=dict(color="#22c55e", width=3),
        marker=dict(size=10)
    ))
    fig_roas.add_trace(go.Scatter(
        x=weekly_data["주차"], y=weekly_data["UA ROAS(보정)"],
        name="UA 보정 ROAS", mode="lines+markers+text",
        text=[f"{v:.0%}" for v in weekly_data["UA ROAS(보정)"]],
        textposition="bottom center", line=dict(color="#3b82f6", width=3),
        marker=dict(size=10)
    ))
    fig_roas.add_hline(y=4.0, line_dash="dash", line_color="#ef4444",
                       annotation_text="목표 ROAS 400%")
    fig_roas.update_layout(
        title="주간 보정 ROAS 추이 (RT vs UA)", height=380,
        yaxis_title="보정 ROAS", template="plotly_dark",
        legend=dict(orientation="h", y=-0.15)
    )
    st.plotly_chart(fig_roas, use_container_width=True)

with col_right:
    fig_cost = go.Figure()
    fig_cost.add_trace(go.Bar(
        x=weekly_data["주차"], y=weekly_data["RT 비용(만)"],
        name="RT 비용", marker_color="#22c55e"
    ))
    fig_cost.add_trace(go.Bar(
        x=weekly_data["주차"], y=weekly_data["UA 비용(만)"],
        name="UA 비용", marker_color="#3b82f6"
    ))
    fig_cost.update_layout(
        title="주간 비용 추이 (RT vs UA)", height=380,
        yaxis_title="비용 (만원)", barmode="group", template="plotly_dark",
        legend=dict(orientation="h", y=-0.15)
    )
    st.plotly_chart(fig_cost, use_container_width=True)


# ═══════════════════════════════════════════
# 2. 신규 오픈 광고그룹 우선순위
# ═══════════════════════════════════════════
st.markdown('<div class="section-header"><h3>신규 오픈 광고그룹 우선순위</h3></div>', unsafe_allow_html=True)

st.markdown("""
> **선정 기준**: RT에서 보정 ROAS 400% 이상이면서 UA에 아직 없거나 볼륨이 작은 광고그룹
> **일예산 500만 기준** 배분 (기존 UA 유지 + 신규 확장)
""")

# ─── Tier 1: 즉시 오픈 ───
tier1_data = pd.DataFrame({
    "광고그룹": [
        "PGA커터벅 (male4069)",
        "베네핏 기획전 (male3564)",
        "NOW 기획전 (male3564)",
        "러닝화 기획전 (male3064)",
        "하이킹 기획전 (male3564)",
    ],
    "RT 보정ROAS": ["477%", "557%", "420%", "419%", "454%"],
    "RT 전환수": [965, 213, 509, 439, 36],
    "CPC": ["299원", "373원", "316원", "313원", "168원"],
    "UA 상태": ["미오픈", "미오픈", "미오픈", "미오픈", "미오픈"],
    "제안 일예산": ["100만", "80만", "80만", "60만", "30만"],
    "오픈 이유": [
        "RT 전환 1위(965건), Display CTR 2.93%로 UA 전환 기대",
        "RT ROAS 557%로 높은 효율, 중가 브랜드라 UA 전환 용이",
        "RT 전환 509건으로 볼륨 검증됨, CPC 316원 적정",
        "러닝화 수요 시즌, RT 전환 439건 검증",
        "CPC 168원 최저, 시즌 기획전으로 신규 유입에 적합",
    ]
})

st.markdown("#### 1순위 - 즉시 오픈 (일예산 350만)")
st.markdown('<div class="tier-1">', unsafe_allow_html=True)
st.dataframe(tier1_data, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Tier 2: 테스트 오픈 ───
tier2_data = pd.DataFrame({
    "광고그룹": [
        "창고방출 기획전 (male3564)",
        "반팔 기획전 (male3564)",
        "하이엔드 기획전 (male3564)",
    ],
    "RT 보정ROAS": ["419%", "304%", "319%"],
    "RT 전환수": [45, 19, 19],
    "CPC": ["353원", "459원", "390원"],
    "UA 상태": ["미오픈", "미오픈", "미오픈"],
    "제안 일예산": ["30만", "20만", "20만"],
    "오픈 이유": [
        "아울렛 감성으로 신규 유저 가성비 소구 가능",
        "여름 시즌 대비 선제 오픈, 볼륨 테스트",
        "객단가 높아 ROAS 확보 용이하나 전환수 적어 테스트 필요",
    ]
})

st.markdown("#### 2순위 - 테스트 오픈 (일예산 70만)")
st.markdown('<div class="tier-2">', unsafe_allow_html=True)
st.dataframe(tier2_data, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)

# ─── Tier 3: 기존 UA 최적화 ───
tier3_data = pd.DataFrame({
    "광고그룹": [
        "르까프 셀렉션 (PBTD UA)",
        "하이브랜드 (male3064, PBTD UA)",
        "애슬레에디션 (PBTD UA)",
    ],
    "현재 UA ROAS(보정)": ["518%", "785%", "398%"],
    "현재 전환수": [376, 7, 17],
    "CPC": ["222원", "133원", "153원"],
    "액션": [
        "예산 확대 (일 80만 → 120만) - 효율+볼륨 모두 검증됨",
        "예산 확대 (일 30만 → 60만) - ROAS 최고, 볼륨 확대 필요",
        "소재 리프레시 후 유지 - ROAS 마지노 근접",
    ],
})

st.markdown("#### 3순위 - 기존 UA 최적화 (일예산 80만)")
st.markdown('<div class="tier-3">', unsafe_allow_html=True)
st.dataframe(tier3_data, use_container_width=True, hide_index=True)
st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════
# 3. 예산 배분 요약
# ═══════════════════════════════════════════
st.markdown('<div class="section-header"><h3>일예산 500만 배분안</h3></div>', unsafe_allow_html=True)

col_pie, col_detail = st.columns([1, 1.5])

with col_pie:
    budget_df = pd.DataFrame({
        "구분": ["1순위 신규 오픈", "2순위 테스트", "3순위 기존 최적화"],
        "일예산(만)": [350, 70, 80],
        "색상": ["#22c55e", "#eab308", "#3b82f6"]
    })
    fig_pie = px.pie(
        budget_df, values="일예산(만)", names="구분",
        color_discrete_sequence=["#22c55e", "#eab308", "#3b82f6"],
        hole=0.4
    )
    fig_pie.update_layout(
        title="일예산 배분 비중", height=350, template="plotly_dark",
        legend=dict(orientation="h", y=-0.1)
    )
    fig_pie.update_traces(textinfo="label+value+percent", texttemplate="%{label}<br>%{value}만원<br>(%{percent})")
    st.plotly_chart(fig_pie, use_container_width=True)

with col_detail:
    st.markdown("""
    | 구분 | 광고그룹 수 | 일예산 | 예상 ROAS(보정) |
    |------|-----------|--------|----------------|
    | **1순위 신규** | 5개 | 350만 | 420~500% |
    | **2순위 테스트** | 3개 | 70만 | 300~420% |
    | **3순위 최적화** | 3개 | 80만 | 450~700% |
    | **합계** | **11개** | **500만** | **목표 400%+** |

    ---
    **단계적 실행 계획:**
    - **1주차**: 1순위 5개 오픈 (일예산 각 50만~100만)
    - **2주차**: 성과 확인 후 2순위 3개 추가 오픈
    - **3주차**: 전체 성과 리뷰, 저효율 그룹 축소 → 고효율 그룹 확대
    - **4주차**: 안정화 및 월간 리포트
    """)


# ═══════════════════════════════════════════
# 4. RT 광고그룹 전체 성과 맵
# ═══════════════════════════════════════════
st.markdown('<div class="section-header"><h3>RT 광고그룹 성과 맵 (비용 vs ROAS)</h3></div>', unsafe_allow_html=True)

# 리타게팅 광고그룹 데이터
rt_ag = pd.DataFrame({
    "광고그룹": [
        "르까프 셀렉션", "스톤아일랜드", "PGA커터벅", "하이브랜드",
        "CP컴퍼니", "NOW기획전", "러닝화", "애슬레에디션",
        "베네핏", "상품3570214", "상품4890514", "로웬",
        "하이킹", "창고방출", "하이엔드", "반팔",
    ],
    "비용(만)": [935, 1720, 1450, 819, 1252, 829, 768, 538, 426, 641, 413, 205, 56, 74, 68, 50],
    "보정ROAS(%)": [653, 487, 477, 639, 429, 420, 419, 508, 557, 418, 503, 353, 454, 419, 319, 304],
    "전환수": [1020, 397, 965, 223, 312, 509, 439, 149, 213, 275, 375, 78, 36, 45, 19, 19],
    "유형": [
        "기획전", "브랜드", "기획전", "기획전",
        "브랜드", "기획전", "기획전", "기획전",
        "기획전", "상품", "상품", "브랜드",
        "기획전", "기획전", "기획전", "기획전",
    ]
})

fig_scatter = px.scatter(
    rt_ag, x="비용(만)", y="보정ROAS(%)",
    size="전환수", color="유형", text="광고그룹",
    color_discrete_map={"기획전": "#22c55e", "브랜드": "#f59e0b", "상품": "#8b5cf6"},
    size_max=50
)
fig_scatter.add_hline(y=400, line_dash="dash", line_color="#ef4444",
                      annotation_text="목표 ROAS 400%")
fig_scatter.update_traces(textposition="top center", textfont_size=10)
fig_scatter.update_layout(
    height=500, template="plotly_dark",
    xaxis_title="4주 비용 (만원)", yaxis_title="보정 ROAS (%)",
    legend=dict(orientation="h", y=-0.12)
)
st.plotly_chart(fig_scatter, use_container_width=True)
st.caption("원 크기 = 전환수 | 빨간 점선 위 = 목표 달성 | 기획전(초록)이 UA 확장 우선 대상")


# ═══════════════════════════════════════════
# 5. 핵심 인사이트 & 주의사항
# ═══════════════════════════════════════════
st.markdown('<div class="section-header"><h3>핵심 인사이트 & 주의사항</h3></div>', unsafe_allow_html=True)

col_ins, col_warn = st.columns(2)
with col_ins:
    st.markdown("""
    #### 핵심 인사이트
    - **기획전 > 단일상품**: 기획전 광고그룹이 상품 단위보다 ROAS, 전환수 모두 우위
    - **가성비 > 프리미엄**: 르까프/PGA커터벅 등 중가 브랜드가 UA에서 전환율 높음
    - **Display CTR 3배**: Bizboard 대비 Display의 CTR이 3배 높아 효율적 소재 운영 가능
    - **CPC 하락 추세**: RT CPC가 421원 → 281원으로 하락 중 (학습 효과)
    - **남성 30~64세 집중**: 타겟이 명확하여 UA 확장 시에도 동일 타겟 유지 권장
    """)

with col_warn:
    st.markdown("""
    #### 주의사항
    - **오디언스 겹침**: 기존 UA 캠페인과 신규 PBTD UA 간 타겟 중복 주의 (제외 설정 필수)
    - **프리미엄 브랜드**: 스톤아일랜드/CP컴퍼니는 UA 효율 낮음 → RT에만 유지
    - **ROAS 마지노**: Raw ROAS 2.27 (보정 400%) 이하 시 즉시 예산 축소
    - **UA ROAS 하락 추세**: 기존 UA가 주간 하락 중 (502% → 468%) → 소재 리프레시 필요
    - **단계적 확장**: 일예산 한 번에 500만 X → 200만부터 주 단위 증가
    """)

st.markdown("---")
st.caption("마지막 업데이트: 2026-04-07 | 데이터 출처: Redash DATA_DB marketing_cost")
