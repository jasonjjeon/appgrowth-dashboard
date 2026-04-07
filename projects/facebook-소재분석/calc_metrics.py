def safe_div(a, b, pct=False, mult=100):
    if b == 0 or b is None:
        return '-'
    val = a / b
    if pct:
        val = val * mult
        return f'{val:.1f}%'
    return f'{val:,.0f}'

# marketing_reportrow에서 가져온 노출/클릭/비용
cost_data = {
    ('W1', '260226_carousel_workwear_vari_lastpage'): {'imp': 108897, 'clicks': 2311, 'cost': 928710},
    ('W1', '260321_carousel_springoutfits2_45'): {'imp': 100350, 'clicks': 2103, 'cost': 748367},
    ('W1', '260321_carousel_blackandwhite_45'): {'imp': 23724, 'clicks': 561, 'cost': 212984},
    ('W1', '20260219-img-department store brand'): {'imp': 14672, 'clicks': 344, 'cost': 161550},
    ('W1', '260313_carousel_springoutfits'): {'imp': 3556, 'clicks': 158, 'cost': 56731},
    ('W1', '20260226-img-department store brand'): {'imp': 1942, 'clicks': 58, 'cost': 25651},
    ('W1', '260321-carousel_jacket_45'): {'imp': 355, 'clicks': 7, 'cost': 5127},
    ('W1', '260305_img_nike2-deeplink'): {'imp': 108, 'clicks': 2, 'cost': 1346},
    ('W1', '20260226-img-springLook'): {'imp': 42, 'clicks': 1, 'cost': 614},
    ('W1', '260226_img_AImodel-vari'): {'imp': 2, 'clicks': 0, 'cost': 14},
    ('W2', '260226_carousel_workwear_vari_lastpage'): {'imp': 98306, 'clicks': 1951, 'cost': 799230},
    ('W2', '260321_carousel_springoutfits2_45'): {'imp': 89251, 'clicks': 1566, 'cost': 640432},
    ('W2', '260403_img_ston-wappen'): {'imp': 11712, 'clicks': 666, 'cost': 123339},
    ('W2', '260321_carousel_blackandwhite_45'): {'imp': 16465, 'clicks': 332, 'cost': 118050},
    ('W2', '260330_carousel_springwear2_45'): {'imp': 8658, 'clicks': 173, 'cost': 93548},
    ('W2', '260403_img_ston-tshrit'): {'imp': 4483, 'clicks': 135, 'cost': 50758},
    ('W2', '260313_carousel_springoutfits'): {'imp': 2236, 'clicks': 71, 'cost': 30165},
    ('W2', '20260226-img-department store brand'): {'imp': 937, 'clicks': 20, 'cost': 11907},
    ('W2', '260321-carousel_jacket_45'): {'imp': 632, 'clicks': 19, 'cost': 7921},
    ('W2', '20260219-vid-codyLOOK_1'): {'imp': 0, 'clicks': 0, 'cost': 0},
    ('W2', '20260219-img-department store brand'): {'imp': 0, 'clicks': 0, 'cost': 0},
    ('W2', '260305_img_nike2-deeplink'): {'imp': 0, 'clicks': 0, 'cost': 0},
}

# airbridge_raw.events에서 가져온 전환 데이터
conv_data = {
    ('W1', '260226_carousel_workwear_vari_lastpage'): {'installs': 721, 'signup': 174, 'purchase': 40, 'revenue': 2840891, 'first_purchase': 30},
    ('W1', '20260219-img-department store brand'): {'installs': 93, 'signup': 54, 'purchase': 24, 'revenue': 1260960, 'first_purchase': 14},
    ('W1', '260321_carousel_springoutfits2_45'): {'installs': 629, 'signup': 91, 'purchase': 23, 'revenue': 1450626, 'first_purchase': 22},
    ('W1', '260313_carousel_springoutfits'): {'installs': 26, 'signup': 3, 'purchase': 3, 'revenue': 113596, 'first_purchase': 0},
    ('W1', '260321_carousel_blackandwhite_45'): {'installs': 138, 'signup': 29, 'purchase': 2, 'revenue': 163800, 'first_purchase': 2},
    ('W1', '20260226-img-springLook'): {'installs': 0, 'signup': 0, 'purchase': 0, 'revenue': 0, 'first_purchase': 0},
    ('W1', '20260219-vid-codyLOOK_1'): {'installs': 0, 'signup': 0, 'purchase': 0, 'revenue': 0, 'first_purchase': 0},
    ('W1', '260226_img_AImodel-vari'): {'installs': 0, 'signup': 0, 'purchase': 0, 'revenue': 0, 'first_purchase': 0},
    ('W1', '20260226-img-department store brand'): {'installs': 12, 'signup': 5, 'purchase': 0, 'revenue': 0, 'first_purchase': 0},
    ('W1', '260305_img_nike2-deeplink'): {'installs': 0, 'signup': 0, 'purchase': 0, 'revenue': 0, 'first_purchase': 0},
    ('W1', '260321-carousel_jacket_45'): {'installs': 1, 'signup': 1, 'purchase': 0, 'revenue': 0, 'first_purchase': 0},
    ('W2', '260226_carousel_workwear_vari_lastpage'): {'installs': 652, 'signup': 155, 'purchase': 59, 'revenue': 4473639, 'first_purchase': 35},
    ('W2', '260321_carousel_springoutfits2_45'): {'installs': 516, 'signup': 121, 'purchase': 24, 'revenue': 1916412, 'first_purchase': 19},
    ('W2', '20260219-img-department store brand'): {'installs': 0, 'signup': 3, 'purchase': 11, 'revenue': 439331, 'first_purchase': 4},
    ('W2', '260321_carousel_blackandwhite_45'): {'installs': 125, 'signup': 23, 'purchase': 6, 'revenue': 291430, 'first_purchase': 5},
    ('W2', '260330_carousel_springwear2_45'): {'installs': 65, 'signup': 6, 'purchase': 3, 'revenue': 421160, 'first_purchase': 2},
    ('W2', '20260226-img-department store brand'): {'installs': 7, 'signup': 2, 'purchase': 2, 'revenue': 144540, 'first_purchase': 2},
    ('W2', '20260219-vid-codyLOOK_1'): {'installs': 0, 'signup': 0, 'purchase': 1, 'revenue': 64500, 'first_purchase': 1},
    ('W2', '260313_carousel_springoutfits'): {'installs': 9, 'signup': 5, 'purchase': 1, 'revenue': 13900, 'first_purchase': 0},
    ('W2', '260305_img_nike2-deeplink'): {'installs': 0, 'signup': 0, 'purchase': 1, 'revenue': 35910, 'first_purchase': 0},
    ('W2', '260403_img_ston-wappen'): {'installs': 117, 'signup': 18, 'purchase': 0, 'revenue': 0, 'first_purchase': 0},
    ('W2', '260403_img_ston-tshrit'): {'installs': 12, 'signup': 2, 'purchase': 0, 'revenue': 0, 'first_purchase': 0},
    ('W2', '260321-carousel_jacket_45'): {'installs': 3, 'signup': 0, 'purchase': 0, 'revenue': 0, 'first_purchase': 0},
}

all_keys = sorted(
    set(list(cost_data.keys()) + list(conv_data.keys())),
    key=lambda x: (x[0], -conv_data.get(x, {}).get('purchase', 0), -conv_data.get(x, {}).get('revenue', 0))
)

rows = []
for key in all_keys:
    w, creative = key
    c = cost_data.get(key, {'imp': 0, 'clicks': 0, 'cost': 0})
    v = conv_data.get(key, {'installs': 0, 'signup': 0, 'purchase': 0, 'revenue': 0, 'first_purchase': 0})

    imp = c['imp']
    clicks = c['clicks']
    cost = c['cost']
    installs = v['installs']
    signup = v['signup']
    purchase = v['purchase']
    revenue = v['revenue']
    first_p = v['first_purchase']

    ctr = safe_div(clicks, imp, pct=True)
    cpc = safe_div(cost, clicks)
    cpi = safe_div(cost, installs)
    cvr_signup = safe_div(signup, clicks, pct=True)
    cpa_signup = safe_div(cost, signup)
    cvr_purchase = safe_div(purchase, clicks, pct=True)
    cpa_purchase = safe_div(cost, purchase)
    roas = safe_div(revenue, cost, pct=True, mult=100)
    arppu = safe_div(revenue, purchase)

    rows.append({
        'week': w,
        'creative': creative,
        'imp': imp, 'clicks': clicks, 'ctr': ctr,
        'cost': cost, 'cpc': cpc,
        'installs': installs, 'cpi': cpi,
        'signup': signup, 'cvr_signup': cvr_signup, 'cpa_signup': cpa_signup,
        'purchase': purchase, 'cvr_purchase': cvr_purchase, 'cpa_purchase': cpa_purchase,
        'revenue': revenue, 'roas': roas, 'arppu': arppu,
        'first_purchase': first_p
    })

# 출력
header = ['주차', '소재명', '노출', '클릭', 'CTR', '비용', 'CPC', '설치', 'CPI', '가입', 'CVR(가입)', 'CPA(가입)', '구매', 'CVR(구매)', 'CPA(구매)', '구매액', 'ROAS', 'ARPPU', '첫구매']
print('\t'.join(header))

for r in rows:
    line = [
        r['week'],
        r['creative'],
        str(r['imp']),
        str(r['clicks']),
        str(r['ctr']),
        str(r['cost']),
        str(r['cpc']),
        str(r['installs']),
        str(r['cpi']),
        str(r['signup']),
        str(r['cvr_signup']),
        str(r['cpa_signup']),
        str(r['purchase']),
        str(r['cvr_purchase']),
        str(r['cpa_purchase']),
        str(r['revenue']),
        str(r['roas']),
        str(r['arppu']),
        str(r['first_purchase'])
    ]
    print('\t'.join(line))

# 주차별 합계
print()
print("=== 주차별 합계 ===")
for week in ['W1', 'W2']:
    wkeys = [k for k in all_keys if k[0] == week]
    total_imp = sum(cost_data.get(k, {}).get('imp', 0) for k in wkeys)
    total_clicks = sum(cost_data.get(k, {}).get('clicks', 0) for k in wkeys)
    total_cost = sum(cost_data.get(k, {}).get('cost', 0) for k in wkeys)
    total_installs = sum(conv_data.get(k, {}).get('installs', 0) for k in wkeys)
    total_signup = sum(conv_data.get(k, {}).get('signup', 0) for k in wkeys)
    total_purchase = sum(conv_data.get(k, {}).get('purchase', 0) for k in wkeys)
    total_revenue = sum(conv_data.get(k, {}).get('revenue', 0) for k in wkeys)
    total_first_p = sum(conv_data.get(k, {}).get('first_purchase', 0) for k in wkeys)

    print(f"{week}: 노출 {total_imp:,} | 클릭 {total_clicks:,} | CTR {safe_div(total_clicks, total_imp, pct=True)} | 비용 {total_cost:,}원 | CPC {safe_div(total_cost, total_clicks)} | 설치 {total_installs:,} | CPI {safe_div(total_cost, total_installs)} | 가입 {total_signup:,} | 구매 {total_purchase:,} | 구매액 {total_revenue:,}원 | ROAS {safe_div(total_revenue, total_cost, pct=True, mult=100)} | 첫구매 {total_first_p:,}")
