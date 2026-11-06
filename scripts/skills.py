"""Generate assets/skills.svg. Edit GROUPS to change the stack."""
import os
from card import W, card

GROUPS = [
    ("languages", ["java", "go", "typescript", "sql", "lua"]),
    ("frameworks", ["spring boot", "gin", "echo", "next.js", "astro"]),
    ("tools", ["docker", "cloudflare", "git", "linux", "neovim"]),
]
CH, PAD, GAP, X0 = 7.8, 12, 8, 136

parts, y = [], 60
for name, items in GROUPS:
    parts.append(f'  <text x="24" y="{y + 17}" font-size="12" class="muted">{name}</text>')
    x = X0
    for it in items:
        w = round(len(it) * CH + PAD * 2)
        parts.append(f'  <rect class="chip" x="{x}" y="{y}" width="{w}" height="26" rx="13"/>')
        parts.append(f'  <text class="chip-t" x="{x + w / 2}" y="{y + 17}" font-size="13" text-anchor="middle">{it}</text>')
        x += w + GAP
    assert x <= W - 24, f"{name} row overflows"
    y += 38

label = "stack. " + ". ".join(f"{n}: {', '.join(i)}" for n, i in GROUPS)
out = os.path.join(os.path.dirname(__file__), "..", "assets", "skills.svg")
open(out, "w").write(card(y + 14, "stack", "\n".join(parts), label))
print("wrote assets/skills.svg")
