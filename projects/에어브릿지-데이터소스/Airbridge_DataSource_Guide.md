# Redash 에어브릿지(Airbridge) 데이터 소스 완전 가이드

## 요약: 에어브릿지 데이터는 어디에?

| 데이터소스 ID | 이름 | 데이터베이스 | 용도 | 우선순위 |
|-------------|------|-----------|------|---------|
| **8** | BigQuery | `airbridge_raw.events` | 캠페인/어트리뷰션 원본 데이터 | ⭐⭐ 심화분석 |
| **2** | AWS Athena | `airbridge_raw_parquet_0.airbridge_touchpoints_csv` | 터치포인트 집계 | ⭐⭐ 채널분석 |
| **7** | DATA_DB (MySQL) | `marketing_cost` | 채널별 ROAS (가장 자주 쓰임) | ⭐⭐⭐ 일상업무 |
| **7** | DATA_DB (MySQL) | `daily_products_cvr` | 상품별 전환율 | ⭐⭐ 상품분석 |
| **7** | DATA_DB (MySQL) | `promotion_result` | 기획전 성과 | ⭐⭐ 기획전분석 |
| **1** | Athler (MySQL) | `marketing_report*` | 광고 성과 원본 | ⭐ 레거시 |

---

## 1. BigQuery 데이터 소스 (ID: 8) - 에어브릿지 원본

### 📊 airbridge_raw.events
**통합 이벤트 테이블 (app + web 통합)**

```
데이터소스: BigQuery (ID: 8)
스키마: airbridge_raw
테이블명: events
행 수: 수십억 건 (2년 이상 누적)
갱신: 실시간 (매시간)
```

#### 핵심 컬럼 (54개 성과지표)

**1) 채널/캠페인 정보**
- `channel` - 광고 채널명 (예: google, naver, kakao, meta)
- `channel_type` - 채널 타입 (organic, paid)
- `campaign` - 캠페인명
- `campaign_id` - 캠페인 ID
- `campaign_short_id` - 단축 캠페인 ID
- `ad_group` - 광고그룹명
- `ad_group_id` - 광고그룹 ID
- `ad_creative` - 광고소재명
- `ad_creative_id` - 광고소재 ID

**2) 성과 지표**
- `assist_clicks` - 보조 클릭 (클릭 없이 노출만)
- `assist_impressions` - 노출 횟수
- `click_id` - 클릭 ID
- `contribution_margin_revenue` - 기여도 매출
- `is_revenue_event` - 매출 이벤트 여부
- `is_revenue` - 수익성 있는 이벤트
- `total_revenue` - 총 매출
- `event_value` - 이벤트 값
- `event_value_original` - 원화 이벤트 값

**3) 제품 정보**
- `product_id` - 상품 ID
- `product_name` - 상품명
- `product_category_id` - 상품 카테고리 ID
- `product_category_name` - 상품 카테고리명
- `product_price` - 상품 가격
- `product_quantity` - 구매 수량
- `product_list` - 상품 목록

**4) 이벤트 정보**
- `event_name` - 이벤트 이름 (예: install, sign_up, purchase)
- `event_category` - 이벤트 카테고리
- `event_action` - 이벤트 액션
- `event_label` - 이벤트 레이블
- `target_event_category` - 타겟 이벤트 카테고리
- `transaction_id` - 거래 ID
- `transaction_type` - 거래 타입

**5) 시간 정보**
- `event_timestamp` - 이벤트 발생 타임스탬프
- `event_date` - 이벤트 발생 날짜
- `event_datetime` - 이벤트 발생 일시
- `system_install_timestamp` - 시스템 설치 시간
- `install_begin_timestamp` - 설치 시작 시간

**6) 기타**
- `device_type` - 디바이스 타입 (mobile, desktop)
- `device_model` - 디바이스 모델
- `device_identifier` - 디바이스 ID
- `user_id` - 사용자 ID
- `user_email` - 사용자 이메일 (해시값)
- `conversion_fraud_tag` - 사기 태그

#### 사용 예시

```sql
-- 채널별 일일 ROAS 계산
SELECT 
  event_date,
  channel,
  campaign,
  COUNT(CASE WHEN is_revenue_event THEN 1 END) as conversions,
  SUM(total_revenue) as revenue,
  COUNT(DISTINCT user_id) as unique_users
FROM `airbridge_raw.events`
WHERE event_date >= '2025-03-01'
  AND event_name IN ('purchase', 'install')
GROUP BY event_date, channel, campaign
LIMIT 1000;
```

---

### 📊 airbridge_backfill.app_events_raw & airbridge_backfill.web_events_raw

**앱/웹 이벤트 백필 데이터**

```
데이터소스: BigQuery (ID: 8)
구조: airbridge_raw.events와 동일 (214개 컬럼)
앱 테이블: airbridge_backfill.app_events_raw
웹 테이블: airbridge_backfill.web_events_raw
용도: 이전 데이터나 특정 플랫폼 분석
```

특징:
- `airbridge_raw.events`보다 더 상세한 원본 데이터
- 앱과 웹을 분리한 테이블
- 더 많은 컬럼 (214개)을 포함

---

## 2. AWS Athena 데이터 소스 (ID: 2) - 터치포인트

### 📊 airbridge_raw_parquet_0.airbridge_touchpoints_csv

**일별 터치포인트 집계 데이터 (최적화된 포맷)**

```
데이터소스: AWS Athena (ID: 2)
스키마: airbridge_raw_parquet_0
테이블명: airbridge_touchpoints_csv
포맷: Parquet (압축, 속도 최적화)
갱신: 일일 (자정 기준)
행 수: 수백만 건
```

#### 핵심 컬럼

**1) 광고채널**
- `channel` - 광고 채널
- `campaign` - 캠페인명
- `campaign_id` - 캠페인 ID
- `ad_group` - 광고그룹
- `ad_creative` - 광고소재
- `ad_creative_id` - 광고소재 ID

**2) 성과지표 (노출, 클릭, 비용, 전환)**
- `impressions` / `impression_count` - 노출 수
- `clicks` / `click_count` - 클릭 수
- `cost` - 광고비
- `conversion_count` - 전환 수
- `contribution_margin` - 기여도
- `contribution_margin_revenue` - 기여도 매출

**3) 매출**
- `revenue` - 총 매출
- `total_revenue` - 누적 매출
- `product_price` - 상품 가격
- `product_quantity` - 구매량

**4) 사용자/제품**
- `user_id` - 사용자 ID
- `user_email` - 사용자 이메일
- `device_type` - 디바이스 타입
- `product_id` - 상품 ID
- `product_name` - 상품명
- `product_category` - 상품 카테고리

**5) 이벤트**
- `event_name` - 이벤트 이름
- `event_value` - 이벤트 값
- `is_revenue_event` - 수익 이벤트 여부

---

## 3. MySQL 가공 테이블 (ID: 7) - 데이터 마트 ⭐⭐⭐ 추천

**가장 많이 사용하는 테이블들**

### 📊 marketing_cost (최우선)
**채널별 일별 광고비 및 성과**

```sql
데이터소스: DATA_DB (ID: 7)
테이블명: marketing_cost
행 수: 약 10만 건 (3년 누적)
갱신: 매일 자정
주기: 일별 (report_date)
```

| 컬럼명 | 설명 | 예시 |
|-------|------|------|
| `report_date` | 보고 날짜 | 2025-04-01 |
| `channel` | 광고 채널 | google, naver, kakao, meta |
| `campaign` | 캠페인명 | Spring-Sale-2025 |
| `ad_group` | 광고그룹 | Brand-Search |
| `impressions` | 노출 수 | 50000 |
| `clicks` | 클릭 수 | 2500 |
| `cost` | 광고비 (원) | 500000 |
| `revenue` | 매출 (원) | 2000000 |
| `order_complete` | 주문 완료 수 | 150 |
| `roas` | ROAS (매출/비용) | 4.0 |

**자주 쓰는 쿼리:**
```sql
-- 채널별 이번 달 ROAS
SELECT channel, SUM(cost) as total_cost, SUM(revenue) as total_revenue,
       ROUND(SUM(revenue)/SUM(cost), 2) as roas
FROM marketing_cost
WHERE report_date >= DATE_FORMAT(CURDATE(), '%Y-%m-01')
GROUP BY channel
ORDER BY roas DESC
LIMIT 100;
```

---

### 📊 daily_products_cvr
**상품별 일별 노출, 클릭, 전환율**

```
데이터소스: DATA_DB (ID: 7)
테이블명: daily_products_cvr
주요 컬럼: date, product_id, impressions, clicks, orders, cvr
갱신: 매일
```

| 컬럼명 | 설명 |
|-------|------|
| `date` | 분석 날짜 |
| `product_id` | 상품 ID |
| `product_name` | 상품명 |
| `impressions` | 노출 수 |
| `clicks` | 클릭 수 |
| `orders` | 주문 수 |
| `cvr` | 전환율 (%) |

---

### 📊 promotion_result
**기획전별 성과**

```
데이터소스: DATA_DB (ID: 7)
테이블명: promotion_result
주요 컬럼: page_name, unique_landing, unique_users, total_conversions, total_sales
```

| 컬럼명 | 설명 |
|-------|------|
| `page_name` | 기획전명 |
| `unique_landing` | 착지 수 |
| `unique_users` | 유니크 유저 |
| `total_conversions` | 총 전환 수 |
| `total_sales` | 총 매출 |
| `gmv_per_view` | 조회당 GMV |
| `impress_to_click` | 노출→클릭 전환율 |
| `click_to_order` | 클릭→구매 전환율 |

---

## 4. MySQL 원본 테이블 (ID: 1) - 레거시

### 📊 marketing_report & marketing_reportrow
**에어브릿지에서 수집한 원본 광고 성과**

```
데이터소스: Athler (ID: 1)
marketing_report: 요약 (channels × campaigns)
marketing_reportrow: 상세 (일별 세부)
```

| 컬럼명 | 설명 |
|-------|------|
| `event_date` | 성과 날짜 |
| `channel` | 광고 채널 |
| `campaign` | 캠페인 |
| `clicks_channel` | 채널 클릭 수 |
| `cost_channel` | 채널 비용 |
| `impressions_channel` | 채널 노출 수 |
| `app_web_revenue` | 앱/웹 매출 |
| `web_order_complete_users` | 주문 완료 유저 |

**⚠️ 참고:** DATA_DB의 `marketing_cost`를 사용하는 것이 더 효율적입니다.

---

## 5. AWS Athena의 다른 에어브릿지 테이블

### raw_csv 디렉토리 (CSV 원본)
- `raw_csv.airbridge_events_csv` - 웹 이벤트 CSV
- `raw_csv.airbridge_events_csv_app` - 앱 이벤트 CSV
- `raw_csv.airbridge_events_parquet` - 웹 이벤트 Parquet
- `raw_csv.airbridge_events_parquet_app` - 앱 이벤트 Parquet

### raw_csv.airbridge_touchpoints_csv_daily_web
**웹 터치포인트 일별 데이터**

---

## 데이터소스 선택 가이드

### 💡 "채널별 ROAS를 보고 싶어요"
→ **DATA_DB > marketing_cost** (ID: 7) ✅ 가장 빠름

```sql
SELECT report_date, channel, roas, revenue, cost
FROM marketing_cost
WHERE report_date >= '2025-03-01'
LIMIT 100;
```

### 💡 "구글 광고 캠페인별 상세 성과를 알고 싶어요"
→ **BigQuery > airbridge_raw.events** (ID: 8)

```sql
SELECT event_date, campaign, ad_group,
       COUNT(*) as events,
       SUM(total_revenue) as revenue,
       COUNT(DISTINCT user_id) as users
FROM `airbridge_raw.events`
WHERE channel = 'google' AND event_date >= '2025-03-01'
GROUP BY event_date, campaign, ad_group
LIMIT 1000;
```

### 💡 "어떤 상품이 가장 많이 클릭되나요?"
→ **DATA_DB > daily_products_cvr** (ID: 7)

```sql
SELECT date, product_id, product_name, 
       SUM(clicks) as total_clicks, 
       SUM(impressions) as total_impressions,
       AVG(cvr) as avg_cvr
FROM daily_products_cvr
WHERE date >= '2025-03-01'
GROUP BY product_id, product_name
ORDER BY total_clicks DESC
LIMIT 100;
```

### 💡 "기획전 성과가 좋은가요?"
→ **DATA_DB > promotion_result** (ID: 7)

```sql
SELECT page_name, unique_landing, total_conversions,
       total_sales, gmv_per_view
FROM promotion_result
WHERE created_at >= '2025-03-01'
ORDER BY total_sales DESC
LIMIT 100;
```

### 💡 "설치 수, 가입 수, 구매 수의 어트리뷰션을 보고 싶어요"
→ **BigQuery > airbridge_backfill.app_events_raw** (ID: 8)

```sql
SELECT event_date, event_name, channel, campaign,
       COUNT(DISTINCT user_id) as unique_users,
       COUNT(*) as total_events,
       SUM(total_revenue) as revenue
FROM `airbridge_backfill.app_events_raw`
WHERE event_date >= '2025-03-01'
  AND event_name IN ('install', 'sign_up', 'purchase')
GROUP BY event_date, event_name, channel, campaign
LIMIT 1000;
```

---

## 성과지표 정의

### ROAS (Return on Ad Spend)
```
ROAS = 광고로부터의 매출 / 광고비
예: 100만원 광고비 → 400만원 매출 = ROAS 4.0
```

### CVR (Conversion Rate)
```
CVR = 전환 수 / 클릭 수 × 100%
예: 100 클릭 중 5건 구매 = CVR 5%
```

### CTR (Click Through Rate)
```
CTR = 클릭 수 / 노출 수 × 100%
예: 10,000 노출 중 500 클릭 = CTR 5%
```

### CPC (Cost Per Click)
```
CPC = 광고비 / 클릭 수
예: 100만원 광고비 / 1,000 클릭 = CPC 1,000원
```

### AOV (Average Order Value)
```
AOV = 총 매출 / 주문 수
예: 1,000만원 매출 / 100주문 = AOV 100,000원
```

---

## 데이터 최신도

| 데이터소스 | 갱신 주기 | 지연시간 | 정확도 |
|----------|---------|--------|------|
| DATA_DB (7) | 매일 | 1-2시간 | ⭐⭐⭐⭐⭐ 높음 |
| BigQuery (8) | 매시간 | 30분-1시간 | ⭐⭐⭐⭐ 높음 |
| AWS Athena (2) | 일일 | 1-2시간 | ⭐⭐⭐ 중간 |
| Athler MySQL (1) | 매시간 | 1-2시간 | ⭐⭐⭐ 중간 |

---

## 자주 묻는 질문

**Q. 광고비와 매출을 한눈에 보려면?**
A. `marketing_cost` (ID: 7)를 사용하세요. 가장 빠르고 정확합니다.

**Q. 캠페인별 ROI를 정확히 계산하려면?**
A. `airbridge_raw.events` (ID: 8)를 사용해 이벤트 단위로 계산하세요.

**Q. 어제 성과를 오늘 아침에 보려면?**
A. `marketing_cost` (ID: 7)를 사용하세요. 자정 이후 갱신됩니다.

**Q. 앱 설치와 웹 구매를 따로 분석하려면?**
A. `airbridge_backfill.app_events_raw`와 `airbridge_backfill.web_events_raw` (ID: 8)를 분리해서 사용하세요.

**Q. 어느 테이블에 광고비가 없나요?**
A. AWS Athena의 Parquet 테이블들입니다. 터치포인트 데이터만 있고, 광고비는 별도로 가져와야 합니다.

---

## 리대시 대시보드 추천 구성

### 1. 일일 광고 성과 대시보드
- 기본: `marketing_cost` (ID: 7)
- 추가: `daily_products_cvr` (ID: 7)

### 2. 캠페인별 심화 분석
- 기본: `airbridge_raw.events` (ID: 8)
- JOIN: 상품 정보, 브랜드 정보

### 3. 기획전 성과
- 기본: `promotion_result` (ID: 7)

### 4. 채널 현황
- 기본: `marketing_cost` (ID: 7)
- 시계열 분석으로 추이 확인

---

## 최종 요약

| 쓰임새 | 추천 데이터소스 | 테이블 | 속도 |
|--------|-------------|-------|------|
| **일상 리포팅** | DATA_DB (7) | marketing_cost | 매우 빠름 |
| **상품 분석** | DATA_DB (7) | daily_products_cvr | 매우 빠름 |
| **기획전 분석** | DATA_DB (7) | promotion_result | 매우 빠름 |
| **채널별 상세** | BigQuery (8) | airbridge_raw.events | 빠름 |
| **어트리뷰션** | BigQuery (8) | airbridge_backfill.* | 중간 |
| **터치포인트** | AWS Athena (2) | airbridge_touchpoints | 중간 |

---

**마지막 업데이트:** 2026-04-07
**작성자:** Data Analyst
