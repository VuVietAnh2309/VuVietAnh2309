#!/usr/bin/env python3
"""Vẽ biểu đồ đường cong contribution (theo tuần) ra SVG tĩnh, bản light + dark.

Nguồn dữ liệu:
  - Có GITHUB_TOKEN/GH_TOKEN  -> GraphQL contributionsCollection (chuẩn, ổn định).
  - Không có token            -> đọc trang public github.com/users/<user>/contributions.

Dùng:  python3 scripts/activity_chart.py <user> [out_dir] [weeks]
"""
import json
import os
import re
import sys
import urllib.request
from datetime import date, timedelta

USER = sys.argv[1] if len(sys.argv) > 1 else "VuVietAnh2309"
OUT = sys.argv[2] if len(sys.argv) > 2 else "assets"
WEEKS = int(sys.argv[3]) if len(sys.argv) > 3 else 52


# ---------------------------------------------------------------- data
def fetch_graphql(token):
    q = """query($u:String!){user(login:$u){contributionsCollection{
      contributionCalendar{weeks{contributionDays{date contributionCount}}}}}}"""
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": q, "variables": {"u": USER}}).encode(),
        headers={"Authorization": f"bearer {token}", "User-Agent": "activity-chart"},
    )
    data = json.load(urllib.request.urlopen(req, timeout=30))
    weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
    return {d["date"]: d["contributionCount"] for w in weeks for d in w["contributionDays"]}


def fetch_public():
    req = urllib.request.Request(
        f"https://github.com/users/{USER}/contributions",
        headers={"User-Agent": "activity-chart"},
    )
    html = urllib.request.urlopen(req, timeout=30).read().decode()
    ids = dict(re.findall(r'data-date="([\d-]+)" id="([^"]+)"', html))
    tips = dict(re.findall(r'for="([^"]+)"[^>]*>([^<]*)<', html))
    days = {}
    for d, i in ids.items():
        m = re.match(r"(\d+) contribution", tips.get(i, ""))
        days[d] = int(m.group(1)) if m else 0
    return days


token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
days = fetch_graphql(token) if token else fetch_public()
if not days:
    sys.exit("Không lấy được dữ liệu contribution")

today = max(date.fromisoformat(d) for d in days)
# Gom theo tuần, tuần cuối kết thúc ở "today".
weeks = []
for w in range(WEEKS - 1, -1, -1):
    end = today - timedelta(days=7 * w)
    total = sum(days.get((end - timedelta(days=k)).isoformat(), 0) for k in range(7))
    weeks.append((end, total))

# Stats
total_year = sum(v for d, v in days.items() if date.fromisoformat(d) > today - timedelta(days=365))
streak, cur = 0, today
if days.get(cur.isoformat(), 0) == 0:  # hôm nay chưa commit thì tính tới hôm qua
    cur -= timedelta(days=1)
while days.get(cur.isoformat(), 0) > 0:
    streak += 1
    cur -= timedelta(days=1)
best_end, best_val = max(weeks, key=lambda x: x[1])
last4 = sum(v for _, v in weeks[-4:])
prev = [v for _, v in weeks[:-4]]
avg4_before = (sum(prev) / len(prev) * 4) if prev else 0
growth = f"×{last4 / avg4_before:.1f}" if avg4_before > 0 else "new"


# ---------------------------------------------------------------- svg
W, H = 900, 340
PL, PR, PT, PB = 48, 24, 110, 40  # padding
CW, CH = W - PL - PR, H - PT - PB
vmax = max(1, max(v for _, v in weeks))
nice = next(n for n in (5, 10, 20, 25, 50, 100, 200, 500, 1000, 10**9) if n >= vmax)


def xy(i, v):
    x = PL + CW * i / (len(weeks) - 1)
    y = PT + CH - CH * v / nice
    return x, y


pts = [xy(i, v) for i, (_, v) in enumerate(weeks)]


def smooth(points):
    """Catmull-Rom -> cubic Bezier, kẹp y để đường cong không vọt xuống dưới 0."""
    d = f"M{points[0][0]:.1f},{points[0][1]:.1f}"
    base = PT + CH
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i else points[i]
        p1, p2 = points[i], points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6, min(base, p1[1] + (p2[1] - p0[1]) / 6))
        c2 = (p2[0] - (p3[0] - p1[0]) / 6, min(base, p2[1] - (p3[1] - p1[1]) / 6))
        d += f" C{c1[0]:.1f},{c1[1]:.1f} {c2[0]:.1f},{c2[1]:.1f} {p2[0]:.1f},{p2[1]:.1f}"
    return d


line = smooth(pts)
area = f"{line} L{pts[-1][0]:.1f},{PT + CH} L{pts[0][0]:.1f},{PT + CH} Z"

THEMES = {
    "light": dict(bg="#ffffff", border="#d0d7de", text="#1f2328", muted="#656d76", grid="#eaeef2"),
    "dark": dict(bg="#0d1117", border="#30363d", text="#e6edf3", muted="#8b949e", grid="#21262d"),
}


def render(t):
    c = THEMES[t]
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
             f'font-family="-apple-system,BlinkMacSystemFont,Segoe UI,Helvetica,Arial,sans-serif">')
    o.append(f"""<defs>
  <linearGradient id="stroke" x1="0" x2="1" y1="0" y2="0">
    <stop offset="0" stop-color="#00d2ff"/><stop offset=".55" stop-color="#a855f7"/><stop offset="1" stop-color="#00f5a0"/>
  </linearGradient>
  <linearGradient id="fill" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="#a855f7" stop-opacity=".35"/><stop offset="1" stop-color="#00d2ff" stop-opacity="0"/>
  </linearGradient>
  <style>
    .draw{{stroke-dasharray:3000;stroke-dashoffset:3000;animation:d 2.4s ease-out forwards}}
    .fade{{opacity:0;animation:f 1s ease-out 1.6s forwards}}
    @keyframes d{{to{{stroke-dashoffset:0}}}} @keyframes f{{to{{opacity:1}}}}
  </style>
</defs>""")
    o.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="12" fill="{c["bg"]}" stroke="{c["border"]}"/>')

    # Header
    o.append(f'<text x="{PL - 16}" y="40" font-size="18" font-weight="600" fill="{c["text"]}">Contribution activity</text>')
    o.append(f'<text x="{PL - 16}" y="60" font-size="12" fill="{c["muted"]}">Weekly contributions · last {WEEKS} weeks</text>')
    stats = [(f"{total_year}", "contributions / year"), (f"{streak} days", "current streak"),
             (f"{best_val}", "best week"), (growth, "last 4 weeks vs. avg")]
    sx = W - PR
    for val, lab in reversed(stats):
        o.append(f'<text x="{sx}" y="42" text-anchor="end" font-size="18" font-weight="700" fill="url(#stroke)">{val}</text>')
        o.append(f'<text x="{sx}" y="60" text-anchor="end" font-size="11" fill="{c["muted"]}">{lab}</text>')
        sx -= 135

    # Grid + y labels
    for k in range(5):
        v = nice * k / 4
        y = PT + CH - CH * k / 4
        dash = "" if k == 0 else 'stroke-dasharray="3 4"'
        o.append(f'<line x1="{PL}" x2="{W - PR}" y1="{y:.1f}" y2="{y:.1f}" stroke="{c["grid"]}" {dash}/>')
        o.append(f'<text x="{PL - 8}" y="{y + 4:.1f}" text-anchor="end" font-size="10" fill="{c["muted"]}">{v:g}</text>')

    # Month labels
    seen, last_x = None, -999
    for i, (d, _) in enumerate(weeks):
        if d.month != seen and i < len(weeks) - 2:
            seen = d.month
            x, _ = xy(i, 0)
            if x - last_x < 40:  # tháng lẻ ở mép trái quá sát nhau thì bỏ
                continue
            last_x = x
            o.append(f'<text x="{x:.1f}" y="{H - 16}" text-anchor="middle" font-size="10" '
                     f'fill="{c["muted"]}">{d.strftime("%b")}</text>')

    # Curve
    o.append(f'<path class="fade" d="{area}" fill="url(#fill)"/>')
    o.append(f'<path class="draw" d="{line}" fill="none" stroke="url(#stroke)" stroke-width="3" '
             f'stroke-linecap="round" stroke-linejoin="round"/>')

    # Peak + latest markers
    bi = max(range(len(weeks)), key=lambda i: weeks[i][1])
    for i, label in ((bi, f"peak {weeks[bi][1]}"), (len(weeks) - 1, f"now {weeks[-1][1]}")):
        x, y = pts[i]
        if i == len(weeks) - 1 and i != bi:  # điểm cuối: nhãn nằm bên trái, dưới đường
            tx, ty, anchor = x - 10, y + 18, "end"
        else:
            tx, ty, anchor = x, y - 12, ("end" if x > W - 120 else "middle")
        o.append(f'<g class="fade"><circle cx="{x:.1f}" cy="{y:.1f}" r="5" fill="{c["bg"]}" stroke="#a855f7" stroke-width="2.5"/>'
                 f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}" font-size="11" font-weight="600" '
                 f'fill="{c["text"]}">{label}</text></g>')
        if i == bi and bi == len(weeks) - 1:
            break
    o.append("</svg>")
    return "\n".join(o)


os.makedirs(OUT, exist_ok=True)
for t, name in (("light", "activity.svg"), ("dark", "activity-dark.svg")):
    with open(os.path.join(OUT, name), "w") as f:
        f.write(render(t))
print(f"weeks={len(weeks)} max={vmax} total_year={total_year} streak={streak} growth={growth}")
