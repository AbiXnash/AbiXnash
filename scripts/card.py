"""Shared card frame for the profile SVGs (light + dark)."""

W = 560
FONT = 'ui-monospace, SFMono-Regular, Menlo, Consolas, monospace'
CSS = f"""
  text {{ font-family: {FONT}; fill: #1d1d1f; }}
  .muted {{ fill: #6e6e73; }}
  .card {{ fill: #ffffff; stroke: #d2d2d7; }}
  .rule {{ stroke: #e5e5ea; }}
  .chip {{ fill: #eef4fd; }} .chip-t {{ fill: #0062c4; }}
  @media (prefers-color-scheme: dark) {{
    text {{ fill: #f5f5f7; }}
    .muted {{ fill: #8e8e93; }}
    .card {{ fill: #0d1117; stroke: #30363d; }}
    .rule {{ stroke: #30363d; }}
    .chip {{ fill: #132b4a; }} .chip-t {{ fill: #58a6ff; }}
  }}
"""


def card(h, title, body, label, extra_css=""):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{label}">
  <style>{CSS}{extra_css}</style>
  <rect class="card" x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="14"/>
  <text x="24" y="38" font-size="11" class="muted" letter-spacing="1.5">{title.upper()}</text>
{body}
</svg>
'''
