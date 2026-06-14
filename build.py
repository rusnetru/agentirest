#!/usr/bin/env python3
"""Build script: pre-render first 12 skill cards into index.html."""
import json
from pathlib import Path

PRERENDER_COUNT = 12

BASE = Path(__file__).resolve().parent
DIGESTS = BASE / "digests"

# Read index
index = json.loads((DIGESTS / "index.json").read_text(encoding="utf-8"))

# Collect all skills from all issues
all_skills = []
for issue in index["issues"]:
    issue_file = DIGESTS / f"issue-{issue['num']}.json"
    if issue_file.exists():
        data = json.loads(issue_file.read_text(encoding="utf-8"))
        for s in data.get("skills", []):
            s["_issue"] = issue["num"]
            s["_date"] = issue["date"]
            all_skills.append(s)

prerender = all_skills[:PRERENDER_COUNT]

# Read template
template = (BASE / "index.html").read_text(encoding="utf-8")

# Generate card HTML
def card_html(s, i):
    install_block = ""
    if s.get("install"):
        install_block = f"""
      <div class="skill-install">
        <button class="install-toggle" onclick="toggleInstall('{s['_issue']}-{i}')">⚡ Установить</button>
        <div class="install-code" id="install-{s['_issue']}-{i}">{s['install']}</div>
        {f'<div class="usage-note" id="usage-{s["_issue"]}-{i}">💡 {s["usage"]}</div>' if s.get('usage') else ''}
      </div>"""

    return f"""    <div class="skill-item">
      <div class="skill-name">{f'<a href="{s["url"]}" target="_blank">{s["name"]}</a>' if s.get('url') else s['name']}</div>
      <div class="skill-meta">{s.get('source','')} &middot; {s.get('category','')} &middot; <a href="?issue={s['_issue']}" style="color:var(--muted);" onclick="document.getElementById('filter-issue').value='{s['_issue']}';filterSkills();return false;">вып. #{s['_issue']}</a></div>
      <div class="skill-desc">{s.get('desc','')}</div>
      <div class="skill-tags">
        {f'<span class="tag tag-secure">Проверен</span>' if s.get('secure') else ''}
        {f'<span class="tag tag-new">Новое</span>' if s.get('is_new') else ''}
        {f'<span class="tag tag-mcp">MCP</span>' if s.get('is_mcp') else ''}
      </div>{install_block}
    </div>"""

cards = "\n".join(card_html(s, i) for i, s in enumerate(prerender))

# Replace content between SSG markers
import re
pattern = r"(<!-- SSG:CARDS:START -->)\s*(<!-- SSG:CARDS:END -->)"
replacement = f"\\1\n{cards}\n  \\2"
result = re.sub(pattern, replacement, template)

(BASE / "index.html").write_text(result, encoding="utf-8")

print(f"Pre-rendered {len(prerender)} cards (out of {len(all_skills)} total skills from {len(index['issues'])} issues)")
