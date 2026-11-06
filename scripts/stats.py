"""Generate assets/stats.svg from public GitHub data. Needs GITHUB_TOKEN."""
import json, os, urllib.request
from xml.sax.saxutils import escape

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

W = 560
light = ["#0071e3", "#4b9bf0", "#86bdf6", "#b7d7fa", "#dcebfc"]
dark = ["#2997ff", "#1a6fd1", "#16529a", "#133c6e", "#102a4b"]

nums = [(f"{contribs:,}", "contributions, past year"), (str(repos["totalCount"]), "public repos"), (str(stars), "stars")]
parts = []
for i, (v, label) in enumerate(nums):
    x = i * 190
    parts.append(f'<text x="{x}" y="62" font-size="24" font-weight="700">{v}</text>')
    parts.append(f'<text x="{x}" y="82" font-size="12" class="muted">{label}</text>')

x = 0.0
for i, (name, size) in enumerate(top):
    w = W * size / total
    parts.append(f'<rect class="l{i}" x="{x:.1f}" y="108" width="{w:.1f}" height="10"/>')
    x += w
lx = 0
for i, (name, size) in enumerate(top):
    label = f"{name.lower()} {round(100 * size / total)}%"
    parts.append(f'<rect class="l{i}" x="{lx}" y="134" width="10" height="10" rx="2"/>')
    parts.append(f'<text x="{lx + 16}" y="143" font-size="12">{escape(label)}</text>')
    lx += 16 + 8 * len(label) + 18

css = "".join(f".l{i}{{fill:{c}}}" for i, c in enumerate(light))
css_dark = "".join(f".l{i}{{fill:{c}}}" for i, c in enumerate(dark))
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="156" viewBox="0 0 {W} 156" role="img" aria-label="GitHub stats: {contribs} contributions in the past year, {repos['totalCount']} public repos, {stars} stars.">
  <defs><clipPath id="bar"><rect x="0" y="108" width="{W}" height="10" rx="5"/></clipPath></defs>
  <style>
    text {{ font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; fill: #1d1d1f; }}
    .muted {{ fill: #6e6e73; }} {css}
    @media (prefers-color-scheme: dark) {{ text {{ fill: #f5f5f7; }} .muted {{ fill: #86868b; }} {css_dark} }}
  </style>
  <text x="0" y="22" font-size="17" font-weight="700">github</text>
  {parts[0]}{parts[1]}{parts[2]}{parts[3]}{parts[4]}{parts[5]}
  <g clip-path="url(#bar)">{"".join(p for p in parts[6:6 + len(top)])}</g>
  {"".join(parts[6 + len(top):])}
</svg>
'''
open(os.path.join(os.path.dirname(__file__), "..", "assets", "stats.svg"), "w").write(svg)
print("wrote assets/stats.svg:", contribs, "contribs,", repos["totalCount"], "repos,", top)
