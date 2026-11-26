"""Refresh the auto-generated "Latest" block in README.md.

Writes between <!-- LATEST:START --> and <!-- LATEST:END -->:
  * latest fusion-metrics release (GitHub Releases) and how long ago it shipped
  * PyPI downloads over the last month (pypistats.org)
  * metrics shipped and how many remain on the metric-port roadmap
  * most recent release published in any other public repo of the user

Stdlib only. Any source that fails is skipped, so the block never breaks the README.

    GITHUB_TOKEN=... python3 scripts/latest.py VuVietAnh2309 README.md
"""
import datetime as dt
import json
import os
import re
import sys
import urllib.request

USER = sys.argv[1] if len(sys.argv) > 1 else "VuVietAnh2309"
README = sys.argv[2] if len(sys.argv) > 2 else "README.md"
PKG_REPO = "fusion-metrics"
BASE_METRICS = 18  # metrics shipped in fusion-metrics v1.0; each closed metric-port issue adds one
START, END = "<!-- LATEST:START -->", "<!-- LATEST:END -->"
NOW = dt.datetime.now(dt.timezone.utc)


def get(url, gh=True):
    req = urllib.request.Request(url, headers={"User-Agent": "profile-readme-latest"})
    if gh:
        req.add_header("Accept", "application/vnd.github+json")
        if os.environ.get("GITHUB_TOKEN"):
            req.add_header("Authorization", f"Bearer {os.environ['GITHUB_TOKEN']}")
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def ago(iso):
    d = (NOW.date() - dt.datetime.fromisoformat(iso.replace("Z", "+00:00")).date()).days
    if d <= 0:
        return "today"
    if d == 1:
        return "yesterday"
    if d < 31:
        return f"{d} days ago"
    if d < 365:
        m = d // 30
        return f"{m} month{'s' * (m > 1)} ago"
    y = d // 365
    return f"{y} year{'s' * (y > 1)} ago"


def human(n):
    return f"{n / 1000:.1f}k" if n >= 1000 else str(n)


def safe(fn):
    try:
        return fn()
    except Exception as e:  # noqa: BLE001 - one bad source must not break the rest
        print(f"skip {fn.__name__}: {e}", file=sys.stderr)
        return None


def release():
    r = get(f"https://api.github.com/repos/{USER}/{PKG_REPO}/releases/latest")
    return (f"📦 [`{PKG_REPO}` **{r['tag_name']}**]({r['html_url']}) released {ago(r['published_at'])}")


def downloads():
    n = get(f"https://pypistats.org/api/packages/{PKG_REPO}/recent", gh=False)["data"]["last_month"]
    return f"📈 **{human(n)}** PyPI downloads in the last 30 days"


def roadmap():
    items = get(f"https://api.github.com/search/issues?q=repo:{USER}/{PKG_REPO}+label:metric-port&per_page=100")["items"]
    done = sum(i["state"] == "closed" for i in items)
    todo = len(items) - done
    url = f"https://github.com/{USER}/{PKG_REPO}/issues?q=is%3Aopen+label%3Ametric-port"
    line = f"🧭 **{BASE_METRICS + done}** metrics shipped"
    return line + (f" · **{todo}** more on the [roadmap]({url})" if todo else " · roadmap complete")


def other_release():
    repos = get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner&sort=pushed")
    best = None
    for repo in repos:
        if repo["fork"] or repo["private"] or repo["name"] in (PKG_REPO, USER):
            continue
        try:
            r = get(f"https://api.github.com/repos/{USER}/{repo['name']}/releases/latest")
        except Exception:  # noqa: BLE001 - repo without releases
            continue
        if not best or r["published_at"] > best[1]["published_at"]:
            best = (repo["name"], r)
    if not best:
        return None
    name, r = best
    return f"🏷️ [`{name}` {r['tag_name']}]({r['html_url']}) released {ago(r['published_at'])}"


lines = [x for x in (safe(release), safe(downloads), safe(roadmap), safe(other_release)) if x]
stamp = NOW.strftime("%d %b %Y")
block = "\n".join([START, "", *[f"- {x}" for x in lines], "",
                   f"<sub>Auto-updated daily by GitHub Actions · last run {stamp}</sub>", END])

text = open(README, encoding="utf-8").read()
if START not in text or END not in text:
    sys.exit(f"markers {START} / {END} not found in {README}")
new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S)
if new != text:
    open(README, "w", encoding="utf-8").write(new)
print(block)
