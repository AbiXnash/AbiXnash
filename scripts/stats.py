"""Generate assets/stats.svg from public GitHub data. Needs GITHUB_TOKEN."""
import json, os, urllib.request
from xml.sax.saxutils import escape
from card import W, card

LOGIN = "AbiXnash"
SKIP = {"Jupyter Notebook", "HTML", "CSS", "Makefile", "Dockerfile", "Shell"}
QUERY = """query($login:String!){ user(login:$login){
  contributionsCollection{ contributionCalendar{ totalContributions } }
  repositories(ownerAffiliations:OWNER,isFork:false,privacy:PUBLIC,first:100){
    totalCount nodes{ stargazerCount languages(first:10){ edges{ size node{ name } } } } } } }"""

req = urllib.request.Request(
    "https://api.github.com/graphql",
    data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
    headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "User-Agent": "profile-stats"},
)
user = json.load(urllib.request.urlopen(req))["data"]["user"]
repos = user["repositories"]
contribs = user["contributionsCollection"]["contributionCalendar"]["totalContributions"]
stars = sum(r["stargazerCount"] for r in repos["nodes"])

langs = {}
for r in repos["nodes"]:
    for e in r["languages"]["edges"]:
        n = e["node"]["name"]
        if n not in SKIP:
            langs[n] = langs.get(n, 0) + e["size"]
top = sorted(langs.items(), key=lambda kv: -kv[1])[:5]
total = sum(s for _, s in top) or 1

light = ["#0071e3", "#4b9bf0", "#86bdf6", "#b7d7fa", "#dcebfc"]
dark = ["#2f81f7", "#1f6feb", "#1958b7", "#16447f", "#122d52"]
css = "".join(f".l{i}{{fill:{c}}}" for i, c in enumerate(light))
css += "@media (prefers-color-scheme: dark){" + "".join(f".l{i}{{fill:{c}}}" for i, c in enumerate(dark)) + "}"

nums = [(f"{contribs:,}", "contributions, past year"), (str(repos["totalCount"]), "public repos"), (str(stars), "stars")]
col = (W - 48) / 3
parts = []
for i, (v, label) in enumerate(nums):
    x = 24 + i * col + (20 if i else 0)
    if i:
        parts.append(f'  <line class="rule" x1="{24 + i * col}" y1="58" x2="{24 + i * col}" y2="104"/>')
    parts.append(f'  <text x="{x}" y="86" font-size="28" font-weight="700">{v}</text>')
    parts.append(f'  <text x="{x}" y="104" font-size="11" class="muted">{label}</text>')

parts.append(f'  <line class="rule" x1="24" y1="126" x2="{W - 24}" y2="126"/>')
parts.append(f'  <text x="24" y="152" font-size="11" class="muted" letter-spacing="1.5">LANGUAGES</text>')
parts.append(f'  <clipPath id="bar"><rect x="24" y="164" width="{W - 48}" height="8" rx="4"/></clipPath>')
seg, x = [], 24.0
for i, (name, size) in enumerate(top):
    w = (W - 48) * size / total
    seg.append(f'<rect class="l{i}" x="{x:.1f}" y="164" width="{w + 0.5:.1f}" height="8"/>')
    x += w
parts.append('  <g clip-path="url(#bar)">' + "".join(seg) + "</g>")
lx = 24
for i, (name, size) in enumerate(top):
    t = f"{name.lower()} {round(100 * size / total)}%"
    parts.append(f'  <circle class="l{i}" cx="{lx + 4}" cy="194" r="4"/>')
    parts.append(f'  <text x="{lx + 14}" y="198" font-size="12">{escape(t)}</text>')
    lx += 14 + 7.3 * len(t) + 16

label = f"GitHub stats: {contribs} contributions in the past year, {repos['totalCount']} public repos, {stars} stars. Top languages: " + ", ".join(n for n, _ in top)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "stats.svg")
open(out, "w").write(card(222, "github", "\n".join(parts), label, css))
print("wrote assets/stats.svg:", contribs, "contribs,", repos["totalCount"], "repos,", top)
