#!/usr/bin/env python3
"""Build script: pre-render skill cards, update stats, generate news.json."""
import json, re
from pathlib import Path

PRERENDER_COUNT = 12
NEWS_MAX = 10
BASE = Path(__file__).resolve().parent
DIGESTS = BASE / "digests"

# --- Read index ---
index = json.loads((DIGESTS / "index.json").read_text(encoding="utf-8"))

# --- Collect all skills ---
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
total_skills = len(all_skills)
total_issues = len(index["issues"])

# --- Read template ---
template = (BASE / "index.html").read_text(encoding="utf-8")

# --- Update stats ---
stats_html = f'Всего в архиве: <strong>{total_skills}</strong> навыков из <strong>{total_issues}</strong> выпусков'
template = re.sub(
    r"<!--BUILD:STATS-->.*<!--/BUILD:STATS-->",
    f"<!--BUILD:STATS-->{stats_html}<!--/BUILD:STATS-->",
    template
)

# --- Generate card HTML ---
def card_html(s, i):
    name_html = s["name"]
    if s.get("url"):
        name_html = f'<a href="{s["url"]}" target="_blank">{s["name"]}</a>'

    parts = [
        f'    <div class="skill-item">',
        f'      <div class="skill-name">{name_html}</div>',
        f'      <div class="skill-meta">{s.get("source","")} &middot; {s.get("category","")} &middot; <a href="?issue={s["_issue"]}" style="color:var(--muted);" onclick="document.getElementById(\'filter-issue\').value=\'{s["_issue"]}\';filterSkills();return false;">вып. #{s["_issue"]}</a></div>',
        f'      <div class="skill-desc">{s.get("desc","")}</div>',
        f'      <div class="skill-tags">',
    ]
    if s.get("secure"):
        parts.append('        <span class="tag tag-secure">Проверен</span>')
    if s.get("is_new"):
        parts.append('        <span class="tag tag-new">Новое</span>')
    if s.get("is_mcp"):
        parts.append('        <span class="tag tag-mcp">MCP</span>')
    parts.append('      </div>')

    if s.get("install"):
        parts.append(f'      <div class="skill-install">')
        parts.append(f'        <button class="install-toggle" onclick="toggleInstall(\'{s["_issue"]}-{i}\')">⚡ Установить</button>')
        parts.append(f'        <div class="install-code" id="install-{s["_issue"]}-{i}">{s["install"]}</div>')
        if s.get("usage"):
            parts.append(f'        <div class="usage-note" id="usage-{s["_issue"]}-{i}">💡 {s["usage"]}</div>')
        parts.append(f'      </div>')

    parts.append(f'    </div>')
    return "\n".join(parts)

cards = "\n".join(card_html(s, i) for i, s in enumerate(prerender))
template = re.sub(
    r"<!--BUILD:CARDS-->.*<!--/BUILD:CARDS-->",
    f"<!--BUILD:CARDS-->\n{cards}\n  <!--/BUILD:CARDS-->",
    template,
    flags=re.DOTALL
)

# --- Write index.html ---
(BASE / "index.html").write_text(template, encoding="utf-8")
print(f"Pre-rendered {len(prerender)} cards (out of {total_skills} skills from {total_issues} issues)")

# --- Generate news.json ---
news_entries = []
for issue in reversed(index["issues"]):
    issue_file = DIGESTS / f"issue-{issue['num']}.json"
    if not issue_file.exists():
        continue

    data = json.loads(issue_file.read_text(encoding="utf-8"))
    skills = data.get("skills", [])
    if not skills:
        continue

    categories = list(dict.fromkeys(s.get("category", "Other") for s in skills))[:3]
    top_skills = [s["name"] for s in skills[:3]]
    skill_preview = ", ".join(top_skills)

    news_entries.append({
        "date": issue["date"],
        "title": f"Выпуск #{issue['num']}: {', '.join(categories)}",
        "summary": f"{len(skills)} навыков: {skill_preview}",
        "issue": issue["num"],
        "type": "digest",
    })

news_entries = news_entries[:NEWS_MAX]

# Static announcements at top
news_entries.insert(0, {
    "date": "2026-06-15",
    "title": "Открыт приём навыков от сообщества",
    "summary": "Предложите навык через GitHub Issues — AI-агент рассмотрит и включит в дайджест.",
    "url": "https://github.com/rusnetru/agentirest/issues/new?template=skill-suggestion.yml",
    "type": "announcement",
})

news_json = {"news": news_entries}
(BASE / "news.json").write_text(
    json.dumps(news_json, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8"
)
print(f"Generated news.json with {len(news_entries)} entries")
