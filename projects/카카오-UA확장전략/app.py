import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="UA 확장 전략 (카카오·메타·구글)", layout="wide")

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
    .metric-green h1 { color: #22c55e; }
    .metric-blue h1 { color: #3b82f6; }
    .metric-yellow h1 { color: #eab308; }
    .tier-1 { border-left: 4px solid #22c55e; padding-left: 12px; margin-bottom: 8px; }
    .tier-2 { border-left: 4px solid #eab308; padding-left: 12px; margin-bottom: 8px; }
    .tier-3 { border-left: 4px solid #3b82f6; padding-left: 12px; margin-bottom: 8px; }
    .tier-new { border-left: 4px solid #a855f7; padding-left: 12px; margin-bottom: 8px; }
    .section-header {
        background: linear-gradient(90deg, #1e3a5f, transparent);
        padding: 8px 16px; border-radius: 8px; margin: 1.5rem 0 1rem 0;
    }
    .channel-kakao { background: linear-gradient(90deg, #3A1D00, transparent); padding: 8px 16px; border-radius: 8px; margin: 1.5rem 0 1rem 0; }
    .channel-meta { background: linear-gradient(90deg, #1A1D5A, transparent); padding: 8px 16px; border-radius: 8px; margin: 1.5rem 0 1rem 0; }
    .channel-google { background: linear-gradient(90deg, #1A3D1A, transparent); padding: 8px 16px; border-radius: 8px; margin: 1.5rem 0 1rem 0; }
</style>
""", unsafe_allow_html=True)

# ─── 헤더 ───
st.title("UA 확장 전략")
st.caption("기준 기간: 2026.03.09 ~ 04.06 | 보정계수 1.76 | 목표 보정 ROAS 400% (Raw 2.27)")

tab_overview, tab_kakao, tab_meta, tab_google = st.tabs([
    "전체 현황", "카카오 (UA + 앱설치)", "메타 (앱설치-구매)", "구글 (앱설치-구매)"
])

# ═══════════════════════════════════════════════════════════════
# TAB 1: 전체 현황
# ═══════════════════════════════════════════════════════════════
with tab_overview:
    st.markdown('<div class="section-header"><h3>채널별 UA 성과 요약 (3/9~4/6)</h3></div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>카카오 RT (PBTD)</h3><h1>497%</h1><h3>보정 ROAS | 비용 1.13억</h3></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card metric-blue"><h3>카카오 기존 UA</h3><h1>487%</h1><h3>보정 ROAS | 비용 2.10억</h3></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card metric-green"><h3>메타 (전체)</h3><h1>672%</h1><h3>보정 ROAS | 비용 0.54억</h3></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card metric-yellow"><h3>구글 앱설치</h3><h1>683%</h1><h3>보정 ROAS | 비용 0.06억</h3></div>', unsafe_allow_html=True)

    # ─── 채널별 비교 차트 ───
    channel_df = pd.DataFrame({
        "채널": ["카카오 RT\n(PBTD)", "카카오\n기존 UA", "메타\n카탈로그", "메타\n앱구매", "구글\n앱설치"],
        "비용(만)": [11290, 21019, 5461, 900, 636],
        "매출(만)": [31900, 58843, 21681, 3290, 2471],
        "보정ROAS(%)": [497, 487, 672, 600, 683],
        "전환수": [5753, 17785, 3815, 401, 470],
    })

    col_l, col_r = st.columns(2)
    with col_l:
        fig_ch = go.Figure()
        fig_ch.add_trace(go.Bar(x=channel_df["채널"], y=channel_df["비용(만)"], name="비용", marker_color="#ef4444"))
        fig_ch.add_trace(go.Bar(x=channel_df["채널"], y=channel_df["매출(만)"], name="매출", marker_color="#22c55e"))
        fig_ch.update_layout(title="채널별 비용 vs 매출 (4주)", height=380, template="plotly_dark", barmode="group",
                             yaxis_title="만원", legend=dict(orientation="h", y=-0.15))
        st.plotly_chart(fig_ch, use_container_width=True)

    with col_r:
        fig_roas = go.Figure()
        colors = ["#f59e0b", "#3b82f6", "#a855f7", "#a855f7", "#22c55e"]
        fig_roas.add_trace(go.Bar(x=channel_df["채널"], y=channel_df["보정ROAS(%)"],
                                  marker_color=colors, text=channel_df["보정ROAS(%)"].apply(lambda x: f"{x}%"),
                                  textposition="outside"))
        fig_roas.add_hline(y=400, line_dash="dash", line_color="#ef4444", annotation_text="목표 400%")
        fig_roas.update_layout(title="채널별 보정 ROAS", height=380, template="plotly_dark",
                               yaxis_title="보정 ROAS (%)")
        st.plotly_chart(fig_roas, use_container_width=True)

    # ─── 전체 예산 배분안 ───
    st.markdown('<div class="section-header"><h3>UA 확장 예산 배분안 (일예산 기준)</h3></div>', unsafe_allow_html=True)

    budget_all = pd.DataFrame({
        "채널": ["카카오 UA (웹)", "카카오 앱설치-다운", "메타 앱설치-구매", "구글 앱설치-구매"],
        "일예산": ["350만", "150만", "100만 (별도)", "50만 (별도)"],
        "캠페인 유형": ["PBTD UA 기획전 중심", "앱설치 + 인앱구매 최적화", "앱설치-구매 (카탈로그+콘텐츠)", "앱 캠페인 Purchase 최적화"],
        "예상 보정ROAS": ["420~500%", "400~450% (테스트)", "550~700%", "600~700%"],
        "비고": ["기존 유지 + 신규 5개 그룹", "신규 캠페인 셋업 필요", "기존 확장 + 신규 소재", "예산 증액 + 소재 다양화"],
    })
    st.dataframe(budget_all, use_container_width=True, hide_index=True)


# ═══════════════════════════════════════════════════════════════
# TAB 2: 카카오 (UA + 앱설치)
# ═══════════════════════════════════════════════════════════════
with tab_kakao:
    st.markdown('<div class="channel-kakao"><h3>카카오 UA 확장 + 앱설치-다운 캠페인</h3></div>', unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown('<div class="metric-card"><h3>RT 비용 (4주)</h3><h1>1.13억</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card"><h3>RT 보정 ROAS</h3><h1>497%</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>기존 UA 비용</h3><h1>2.10억</h1></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>기존 UA 보정 ROAS</h3><h1>487%</h1></div>', unsafe_allow_html=True)
    with col5:
        st.markdown('<div class="metric-card"><h3>PBTD UA 보정 ROAS</h3><h1>462%</h1></div>', unsafe_allow_html=True)

    # ─── 주간 추이 ───
    weekly_data = pd.DataFrame({
        "주차": ["11주차 (3/9~)", "12주차 (3/16~)", "13주차 (3/23~)", "14주차 (3/30~)"],
        "RT ROAS(보정)": [4.40, 4.65, 5.33, 4.73],
        "UA ROAS(보정)": [5.02, 5.03, 4.88, 4.68],
    })
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(x=weekly_data["주차"], y=weekly_data["RT ROAS(보정)"],
        name="RT 보정 ROAS", mode="lines+markers+text",
        text=[f"{v*100:.0f}%" for v in weekly_data["RT ROAS(보정)"]],
        textposition="top center", line=dict(color="#f59e0b", width=3), marker=dict(size=10)))
    fig_trend.add_trace(go.Scatter(x=weekly_data["주차"], y=weekly_data["UA ROAS(보정)"],
        name="UA 보정 ROAS", mode="lines+markers+text",
        text=[f"{v*100:.0f}%" for v in weekly_data["UA ROAS(보정)"]],
        textposition="bottom center", line=dict(color="#3b82f6", width=3), marker=dict(size=10)))
    fig_trend.add_hline(y=4.0, line_dash="dash", line_color="#ef4444", annotation_text="목표 400%")
    fig_trend.update_layout(title="카카오 주간 보정 ROAS 추이", height=350, template="plotly_dark",
                            legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(fig_trend, use_container_width=True)

    # ═══ 카카오 UA 신규 오픈 광고그룹 ═══
    st.markdown('<div class="section-header"><h3>카카오 UA 신규 오픈 광고그룹 (정확한 광고그룹명)</h3></div>', unsafe_allow_html=True)
    st.markdown("> **선정 기준**: RT 보정 ROAS 400%+ & 전환 검증됨 & 기존 PBTD UA에 미오픈")

    # ─── 1순위 ───
    st.markdown("#### 1순위 - 즉시 오픈 (일예산 250만)")
    tier1 = pd.DataFrame({
        "광고그룹명 (정확)": [
            "male4069-2601_ct_pgacutterbuck-promotion",
            "male3564-2602_ct_benefit-promotion",
            "male3564-2512_ct_now-promotion",
            "male3064-2602_ct_runningshoes-promotion",
            "male3564-2604_ct_hiking-promotion",
        ],
        "캠페인": [
            "bizboard / display",
            "bizboard",
            "bizboard / display",
            "bizboard / display",
            "bizboard",
        ],
        "RT 비용": ["1,450만", "426만", "829만", "768만", "56만"],
        "RT 전환": [965, 213, 509, 439, 36],
        "RT 보정ROAS": ["477%", "557%", "420%", "419%", "454%"],
        "CPC": ["299원", "373원", "316원", "313원", "168원"],
        "제안 일예산": ["80만", "50만", "50만", "40만", "30만"],
        "오픈 근거": [
            "RT 전환 1위(965건), Display CTR 2.93%",
            "ROAS 557% 최상위, 중가 브랜드 전환 용이",
            "전환 509건 볼륨 검증, CPC 적정",
            "시즌 수요(러닝화) + 전환 439건",
            "CPC 168원 최저, 시즌 기획전 활용",
        ],
    })
    st.markdown('<div class="tier-1">', unsafe_allow_html=True)
    st.dataframe(tier1, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── 2순위 ───
    st.markdown("#### 2순위 - 테스트 오픈 (일예산 50만)")
    tier2 = pd.DataFrame({
        "광고그룹명 (정확)": [
            "male3564-2604_ct_warehouserelease-promotion",
            "male3564-2604_ct_shortsleeve-promotion",
            "male3564-2601_ct_highend-promotion",
        ],
        "캠페인": ["bizboard", "bizboard", "bizboard"],
        "RT 비용": ["74만", "50만", "68만"],
        "RT 전환": [45, 19, 19],
        "RT 보정ROAS": ["419%", "304%", "319%"],
        "CPC": ["353원", "459원", "390원"],
        "제안 일예산": ["20만", "15만", "15만"],
        "오픈 근거": [
            "아울렛 감성, 가성비 소구 적합",
            "여름 시즌 선제 테스트",
            "객단가 높아 소액 테스트 후 확장",
        ],
    })
    st.markdown('<div class="tier-2">', unsafe_allow_html=True)
    st.dataframe(tier2, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── 3순위: 기존 PBTD UA 최적화 ───
    st.markdown("#### 3순위 - 기존 PBTD UA 최적화 (일예산 50만)")
    tier3 = pd.DataFrame({
        "광고그룹명 (정확)": [
            "male3064-custom_lecaf_selection-promotion",
            "male3064-custom_ct_highbrand-promotion",
            "male3064-custom_ct_athleredition-promotion",
        ],
        "캠페인": [
            "bizboard_da_pr_pbtd-ua-purchase",
            "bizboard_da_pr_pbtd-ua-purchase",
            "bizboard_da_pr_pbtd-ua-purchase",
        ],
        "현재 비용": ["425만", "98만", "214만"],
        "전환": [376, 7, 17],
        "보정ROAS": ["518%", "785%", "398%"],
        "CPC": ["222원", "133원", "153원"],
        "액션": [
            "예산 확대 → 일 30만 (효율+볼륨 검증)",
            "예산 확대 → 일 10만 (ROAS 최고, 볼륨 테스트)",
            "소재 리프레시 후 유지 → 일 10만",
        ],
    })
    st.markdown('<div class="tier-3">', unsafe_allow_html=True)
    st.dataframe(tier3, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ═══ 카카오 앱설치-다운 캠페인 (신규) ═══
    st.markdown('<div class="section-header"><h3>카카오 앱설치-다운 캠페인 (신규 셋업)</h3></div>', unsafe_allow_html=True)
    st.markdown('<div class="tier-new">', unsafe_allow_html=True)
    st.markdown("""
    **현재 상태**: 카카오에 앱설치 캠페인 없음 → **신규 생성 필요**

    #### 캠페인 셋업 가이드

    | 항목 | 설정값 |
    |------|--------|
    | **캠페인 목표** | 앱 설치 → 인앱 이벤트(구매) 최적화 |
    | **캠페인명 (제안)** | `bizboard_da_pr_pbtd-ua-appinstall-purchase` |
    | **게재 지면** | Bizboard + Display (별도 캠페인) |
    | **일예산** | 150만 (Bizboard 100만 + Display 50만) |
    | **입찰 전략** | 자동 입찰 (인앱 이벤트 최적화) |
    | **타겟** | 남성 30~64세, 앱 미설치자 |

    #### 오픈 광고그룹 (RT 고효율 기획전 기반)

    | 우선순위 | 광고그룹명 (제안) | 참조 RT 광고그룹 | 근거 |
    |---------|-----------------|----------------|------|
    | 1 | `male3064-appinstall_ct_pgacutterbuck-promotion` | male4069-2601_ct_pgacutterbuck-promotion | RT 전환 965건, ROAS 477% |
    | 2 | `male3064-appinstall_lecaf_selection-promotion` | male3055-2508_lecaf_selection-promotion | RT ROAS 653% 최고, UA에서도 검증 |
    | 3 | `male3064-appinstall_ct_benefit-promotion` | male3564-2602_ct_benefit-promotion | RT ROAS 557%, 중가 브랜드 |
    | 4 | `male3064-appinstall_ct_now-promotion` | male3564-2512_ct_now-promotion | RT 전환 509건 볼륨 검증 |
    | 5 | `male3064-appinstall_ct_runningshoes-promotion` | male3064-2602_ct_runningshoes-promotion | 시즌 수요 + RT 439건 |

    #### 운영 전략
    - **1~2주차**: 일예산 50만으로 시작, 학습 기간 확보
    - **3~4주차**: 보정 ROAS 400% 이상 시 일예산 100만으로 증액
    - **5주차~**: 150만까지 확장, 고효율 그룹에 집중
    - **모니터링**: 앱 설치 단가(CPI)와 인앱 구매 전환율 주 1회 체크
    - **소재**: 앱 설치 유도 CTA 포함 소재 별도 제작 필요 ("앱에서 더 싸게")
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── RT 성과 맵 ───
    st.markdown('<div class="section-header"><h3>RT 광고그룹 성과 맵 (비용 vs ROAS)</h3></div>', unsafe_allow_html=True)

    rt_ag = pd.DataFrame({
        "광고그룹": [
            "lecaf_selection", "stoneisland", "pgacutterbuck", "highbrand",
            "cpcompany", "now", "runningshoes", "athleredition",
            "benefit", "product-3570214", "product-4890514", "rowen",
            "hiking", "warehouserelease", "highend", "shortsleeve",
        ],
        "정확한 이름": [
            "male3055-2508_lecaf_selection-promotion",
            "male3564-2601_br_stoneisland-promotion",
            "male4069-2601_ct_pgacutterbuck-promotion",
            "male3564-2601_ct_highbrand-promotion",
            "male3564-2601_br_cpcompany-promotion",
            "male3564-2512_ct_now-promotion",
            "male3064-2602_ct_runningshoes-promotion",
            "male3564-2602_ct_athleredition-promotion",
            "male3564-2602_ct_benefit-promotion",
            "male4064-3570214-product",
            "male3064-4890514-product",
            "male3059-2601_br_sub_rowen-promotion",
            "male3564-2604_ct_hiking-promotion",
            "male3564-2604_ct_warehouserelease-promotion",
            "male3564-2601_ct_highend-promotion",
            "male3564-2604_ct_shortsleeve-promotion",
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
        size="전환수", color="유형", hover_data=["정확한 이름"], text="광고그룹",
        color_discrete_map={"기획전": "#22c55e", "브랜드": "#f59e0b", "상품": "#8b5cf6"},
        size_max=50
    )
    fig_scatter.add_hline(y=400, line_dash="dash", line_color="#ef4444", annotation_text="목표 ROAS 400%")
    fig_scatter.update_traces(textposition="top center", textfont_size=9)
    fig_scatter.update_layout(height=500, template="plotly_dark",
        xaxis_title="4주 비용 (만원)", yaxis_title="보정 ROAS (%)",
        legend=dict(orientation="h", y=-0.12))
    st.plotly_chart(fig_scatter, use_container_width=True)
    st.caption("원 크기 = 전환수 | 빨간 점선 위 = 목표 달성 | 마우스 오버 시 정확한 광고그룹명 확인")


# ═══════════════════════════════════════════════════════════════
# TAB 3: 메타 (앱설치-구매)
# ═══════════════════════════════════════════════════════════════
with tab_meta:
    st.markdown('<div class="channel-meta"><h3>메타 앱설치-구매 캠페인 전략</h3></div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>카탈로그 UA 비용</h3><h1>4,581만</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card metric-green"><h3>카탈로그 보정 ROAS</h3><h1>672%</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>앱구매 비용</h3><h1>902만</h1></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card metric-green"><h3>앱구매 보정 ROAS</h3><h1>600%</h1></div>', unsafe_allow_html=True)

    # ─── 메타 현재 캠페인 성과 ───
    st.markdown('<div class="section-header"><h3>현재 메타 캠페인 성과</h3></div>', unsafe_allow_html=True)

    meta_campaigns = pd.DataFrame({
        "캠페인": [
            "catalog_da_pdp-ua-purchase-utm4",
            "catalog_da_pr-ua-purchase",
            "facebook_da_pr-ua-apppurchase-android-main",
            "facebook_da_pr-ua-apppurchase-android-seeding",
            "facebook_da_pr-ua-apppurchase-android- test",
        ],
        "유형": ["카탈로그 (PDP)", "카탈로그 (기획전)", "앱구매 (메인)", "앱구매 (시딩)", "앱구매 (테스트)"],
        "비용": ["3,161만", "1,344만", "790만", "60만", "52만"],
        "전환": [2585, 770, 401, 9, 18],
        "Raw ROAS": ["4.52", "3.40", "3.41", "0.52", "2.44"],
        "보정 ROAS": ["795%", "598%", "600%", "92%", "429%"],
        "CPC": ["118원", "214원", "415원", "658원", "577원"],
        "판단": ["확대", "확대", "확대", "중단", "유지/관찰"],
    })
    st.dataframe(meta_campaigns, use_container_width=True, hide_index=True)

    # ─── 메타 주간 추이 ───
    meta_weekly = pd.DataFrame({
        "주차": ["11주차", "12주차", "13주차", "14주차"],
        "카탈로그PDP": [3.73, 4.86, 5.27, 4.39],
        "카탈로그기획전": [2.64, 2.79, 3.54, 5.12],
        "앱구매메인": [3.36, 3.85, 2.72, 3.53],
    })
    fig_meta = go.Figure()
    fig_meta.add_trace(go.Scatter(x=meta_weekly["주차"], y=meta_weekly["카탈로그PDP"],
        name="카탈로그 PDP", mode="lines+markers", line=dict(color="#a855f7", width=3)))
    fig_meta.add_trace(go.Scatter(x=meta_weekly["주차"], y=meta_weekly["카탈로그기획전"],
        name="카탈로그 기획전", mode="lines+markers", line=dict(color="#3b82f6", width=3)))
    fig_meta.add_trace(go.Scatter(x=meta_weekly["주차"], y=meta_weekly["앱구매메인"],
        name="앱구매 메인", mode="lines+markers", line=dict(color="#22c55e", width=3)))
    fig_meta.add_hline(y=2.27, line_dash="dash", line_color="#ef4444", annotation_text="마지노 Raw 2.27")
    fig_meta.update_layout(title="메타 캠페인별 Raw ROAS 주간 추이", height=380, template="plotly_dark",
                           yaxis_title="Raw ROAS", legend=dict(orientation="h", y=-0.15))
    st.plotly_chart(fig_meta, use_container_width=True)

    # ─── 메타 광고그룹 성과 ───
    st.markdown('<div class="section-header"><h3>메타 광고그룹별 성과 (상위)</h3></div>', unsafe_allow_html=True)

    meta_ag = pd.DataFrame({
        "광고그룹명 (정확)": [
            "male3554-all_product_catalog-product-incremental2",
            "male3064-apppurchase_contents-promotion-main",
            "male3064-2603_focus_fahrenheit_outlet-promotion",
            "male3064-sel_ct_first-promotion",
            "male3064-sel_ct_firstgolf-promotion",
            "male3064-sel_br_hazzys-promotion",
            "male3064-sel_br_maestro-promotion",
            "male3064-2603_br_ilcorso-promotion",
        ],
        "캠페인": [
            "catalog_da_pdp-ua-purchase-utm4",
            "facebook_da_pr-ua-apppurchase-android-main",
            "catalog_da_pr-ua-purchase",
            "catalog_da_pr-ua-purchase",
            "catalog_da_pr-ua-purchase",
            "catalog_da_pr-ua-purchase",
            "catalog_da_pr-ua-purchase",
            "catalog_da_pr-ua-purchase",
        ],
        "비용": ["3,161만", "790만", "300만", "280만", "264만", "193만", "104만", "36만"],
        "전환": [2585, 401, 147, 200, 156, 128, 63, 24],
        "보정ROAS": ["795%", "600%", "525%", "663%", "641%", "678%", "609%", "649%"],
        "CPC": ["118원", "415원", "276원", "122원", "144원", "236원", "338원", "397원"],
    })
    st.dataframe(meta_ag, use_container_width=True, hide_index=True)

    # ─── 메타 확장 전략 ───
    st.markdown('<div class="section-header"><h3>메타 앱설치-구매 확장 전략</h3></div>', unsafe_allow_html=True)
    st.markdown("""
    #### 현재 상황
    - **카탈로그 PDP** (보정 795%): 최고 효율, CPC 118원으로 볼륨 확장 여지 큼
    - **앱구매 메인** (보정 600%): 안정적이나 CPC 415원으로 높은 편
    - **시딩 캠페인** (보정 92%): 효율 나쁨 → 중단 권장

    #### 확장 방향

    | 액션 | 캠페인 | 상세 |
    |------|--------|------|
    | **예산 확대** | catalog_da_pdp-ua-purchase-utm4 | 일 45만 → 70만, CPC 118원이라 볼륨 충분 |
    | **예산 확대** | facebook_da_pr-ua-apppurchase-android-main | 일 30만 → 50만, 앱구매 직접 최적화 |
    | **신규 오픈** | 카탈로그 기획전 신규 그룹 | hazzys, maestro 등 고효율 브랜드 확장 |
    | **중단** | facebook_da_pr-ua-apppurchase-android-seeding | ROAS 92%, 비용 낭비 |
    | **소재 전략** | 전체 | 카카오와 동일 기획전 소재 활용 (크로스채널) |

    #### 신규 광고그룹 제안

    | 광고그룹명 (제안) | 근거 |
    |-----------------|------|
    | `male3064-sel_br_elcanto-promotion` | 카카오 UA에서 ROAS 602% 검증 |
    | `male3064-sel_ct_pgacutterbuck-promotion` | 카카오 RT 전환 1위 상품 |
    | `male3064-2603_ct_benefit-promotion` | 카카오 RT ROAS 557% 기획전 |
    | `male3064-sel_ct_runningshoes-promotion` | 시즌 수요 + 카카오 검증 |
    """)


# ═══════════════════════════════════════════════════════════════
# TAB 4: 구글 (앱설치-구매)
# ═══════════════════════════════════════════════════════════════
with tab_google:
    st.markdown('<div class="channel-google"><h3>구글 앱설치-구매 캠페인 전략</h3></div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown('<div class="metric-card"><h3>비용 (2주)</h3><h1>636만</h1></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="metric-card metric-green"><h3>보정 ROAS</h3><h1>683%</h1></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="metric-card"><h3>전환</h3><h1>470건</h1></div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="metric-card"><h3>CPC</h3><h1>421원</h1></div>', unsafe_allow_html=True)

    # ─── 구글 현재 캠페인 ───
    st.markdown('<div class="section-header"><h3>현재 구글 캠페인 성과</h3></div>', unsafe_allow_html=True)

    google_camp = pd.DataFrame({
        "캠페인": [
            "App promotion-AppInstall-ua-Purchase",
            "App promotion-AppInstall-ua-Install",
        ],
        "광고그룹명 (정확)": [
            "Ad group 20260206 pre-contents-purchase",
            "Ad group 20260206 pre-contents-install",
        ],
        "비용": ["636만", "0원 (전환만)"],
        "전환": [470, 4],
        "Raw ROAS": ["3.88", "-"],
        "보정 ROAS": ["683%", "-"],
        "CPC": ["421원", "-"],
        "상태": ["운영 중 (3/26~)", "학습 전/미집행"],
    })
    st.dataframe(google_camp, use_container_width=True, hide_index=True)

    # ─── 구글 주간 추이 ───
    google_weekly = pd.DataFrame({
        "주차": ["13주차 (3/23~)", "14주차 (3/30~)"],
        "비용(만)": [217, 386],
        "전환": [148, 285],
        "Raw ROAS": [3.24, 4.13],
        "보정ROAS(%)": [570, 727],
    })

    col_gl, col_gr = st.columns(2)
    with col_gl:
        fig_gw = go.Figure()
        fig_gw.add_trace(go.Bar(x=google_weekly["주차"], y=google_weekly["비용(만)"],
            name="비용(만)", marker_color="#22c55e"))
        fig_gw.add_trace(go.Scatter(x=google_weekly["주차"], y=google_weekly["보정ROAS(%)"],
            name="보정 ROAS(%)", yaxis="y2", mode="lines+markers+text",
            text=[f"{v}%" for v in google_weekly["보정ROAS(%)"]],
            textposition="top center", line=dict(color="#eab308", width=3), marker=dict(size=12)))
        fig_gw.update_layout(
            title="구글 앱설치 주간 추이", height=380, template="plotly_dark",
            yaxis=dict(title="비용 (만원)"),
            yaxis2=dict(title="보정 ROAS (%)", overlaying="y", side="right"),
            legend=dict(orientation="h", y=-0.15)
        )
        st.plotly_chart(fig_gw, use_container_width=True)

    with col_gr:
        st.markdown("""
        #### 핵심 포인트
        - **2주 만에 ROAS 570% → 727%로 급상승** (학습 효과)
        - 전환수도 148건 → 285건으로 **약 2배 증가**
        - 비용 대비 효율이 전 채널 중 가장 높음
        - **결론: 가장 빠르게 스케일업 가능한 채널**
        """)

    # ─── 구글 확장 전략 ───
    st.markdown('<div class="section-header"><h3>구글 앱설치-구매 확장 전략</h3></div>', unsafe_allow_html=True)

    st.markdown("""
    #### 현재 상황
    - 3/26부터 운영 시작, 아직 **2주차**지만 ROAS가 빠르게 개선 중
    - 광고그룹 1개만 운영 중 → 확장 여지가 매우 큼
    - 구글 앱 캠페인 특성상 머신러닝 학습이 핵심 (소재/타겟 자동 최적화)

    #### 확장 계획

    | 단계 | 기간 | 일예산 | 목표 |
    |------|------|--------|------|
    | **현재** | 3/26~ (2주차) | ~46만 | 학습 안정화 |
    | **1단계** | 4월 2주차 | 80만 | ROAS 유지하며 볼륨 확대 |
    | **2단계** | 4월 3주차 | 120만 | 전환수 일 40건+ 목표 |
    | **3단계** | 4월 4주차~ | 150만 | 안정화 후 최대 확장 |

    #### 추가 캠페인/광고그룹 제안

    | 캠페인 유형 | 설명 | 예상 효과 |
    |------------|------|----------|
    | **Purchase 최적화 (현재)** | 기존 캠페인 예산 확대 | ROAS 600%+ 유지하며 볼륨 확대 |
    | **tROAS 캠페인 (신규)** | 목표 ROAS 설정 (350%) | 구글 ML이 ROAS 기준 자동 최적화 |
    | **카탈로그 기반 (신규)** | 상품 피드 연동 | 메타 카탈로그처럼 자동 소재 생성 |

    #### 소재 전략
    - 구글 앱 캠페인은 **텍스트 + 이미지 + 영상** 조합으로 자동 생성
    - 카카오/메타에서 검증된 **기획전 이미지** 그대로 활용
    - 앱 스토어 스크린샷 최적화 병행 (전환율 영향)

    #### 주의사항
    - 구글 앱 캠페인은 예산을 **급격히 올리면 학습이 리셋**됨 → 20~30%씩 점진 증액
    - 최소 50건/주 전환 데이터가 쌓여야 학습 안정화
    - Install 캠페인은 전환 없이 비용만 소진 → **Purchase 캠페인에 집중**
    """)


# ═══════════════════════════════════════════════════════════════
# 하단 요약
# ═══════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
#### 전체 실행 타임라인

| 주차 | 카카오 UA | 카카오 앱설치 | 메타 | 구글 |
|------|----------|------------|------|------|
| **1주차** (4/7~) | 1순위 5개 오픈 | 캠페인 셋업 | 예산 확대 | 예산 80만 증액 |
| **2주차** (4/14~) | 성과 확인, 2순위 오픈 | 소액 테스트 시작 | 신규 그룹 오픈 | 예산 120만 |
| **3주차** (4/21~) | 전체 리뷰, 비효율 축소 | 학습 확인, 증액 | 크로스채널 소재 테스트 | 예산 150만 |
| **4주차** (4/28~) | 안정화, 월간 리포트 | 150만 목표 도달 | 안정화 | tROAS 캠페인 테스트 |
""")
st.caption("마지막 업데이트: 2026-04-07 | 데이터 출처: Redash DATA_DB marketing_cost")
