"""
Writes the next article in content/queue.json with the Claude API,
validates it against SEO and quality rules, and saves it to content/articles/.

Usage:  ANTHROPIC_API_KEY=... python3 scripts/write_article.py
Exit code 0 = article written, 2 = queue empty, 1 = failed validation.
"""
import datetime, glob, json, os, re, sys, urllib.request, urllib.error

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-5")
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
TODAY = os.environ.get("ARTICLE_DATE", datetime.date.today().isoformat())

# ---------------------------------------------------------------- context
def site_catalog():
    """Existing URLs and titles, from the last build."""
    os.system(f"{sys.executable} build.py > /dev/null")
    pages = {}
    for f in glob.glob("site/**/index.html", recursive=True):
        path = "/" + os.path.relpath(os.path.dirname(f), "site").replace("\\", "/") + "/"
        path = "/" if path == "/./" else path
        t = re.search(r"<title>(.*?)</title>", open(f, encoding="utf-8").read())
        pages[path] = re.sub(r"\s*\|\s*kWhCompare$", "", t.group(1)) if t else path
    return pages

def fact_pack():
    js = open("static/assets/app.js", encoding="utf-8").read()
    rows = re.findall(r'\["(\w\w)","([^"]+)",([\d.]+),(\d+),(-?[\d.]+)\]', js)
    states = {n: {"rate_cents_kwh": float(r), "avg_monthly_bill_usd": int(b), "one_year_change_pct": float(y)} for c, n, r, b, y in rows}
    from tx import TDU
    tdu = {t["name"]: {"fixed_usd_month": t["fixed"], "cents_per_kwh": t["kwh"],
                       "delivery_at_1000_kwh_usd": round(t["fixed"] + t["kwh"] * 10, 2), "outage_phone": t["phone"]} for t in TDU.values()}
    return {
        "as_of": "Mid-2026 (EIA) and late summer 2026 (PUCT). Today's date: " + TODAY,
        "us_average_residential_rate_cents_kwh": 18.34,
        "texas_average_rate_cents_kwh": 15.94,
        "residential_rates_by_state": states,
        "texas_tdu_delivery_charges": tdu,
        "deregulated_states": ["Texas", "Pennsylvania", "Ohio", "Illinois", "New York", "New Jersey", "Maryland", "Massachusetts",
                               "Connecticut", "Delaware", "Maine", "New Hampshire", "Rhode Island", "District of Columbia"],
        "limited_choice_states": ["Michigan", "Virginia", "California", "Oregon", "Nevada"],
        "texas_rules": {
            "switch_without_fee": "Within 14 days before a fixed contract expires, or when moving with proof of new address",
            "rescission": "3 federal business days after signing",
            "deposit_cap": "Greater of 1/5 of estimated annual billing or two estimated monthly bills (PUCT §25.478)",
            "deposit_waivers": "Age 65+ not delinquent; certified family violence victims; satisfactory payment history letter",
            "tdu_rate_updates": "March 1 and September 1",
            "wholesale_indexed_residential_plans": "Banned after Winter Storm Uri (2021)",
            "efl": "Every plan publishes an Electricity Facts Label with average prices at 500, 1,000 and 2,000 kWh",
        },
    }

STYLE = """You are the senior writer and SEO editor at kWhCompare.com, an independent U.S. electricity rate comparison site.
You write for American homeowners and renters who want to understand and lower their electric bill.

VOICE
- Clear, confident, friendly and specific, like a knowledgeable friend, never salesy.
- U.S. English, second person ("you"), short paragraphs (1-3 sentences), plain words.
- Never use: "in today's world", "delve", "navigate", "landscape", "crucial", "unlock", "game-changer", "it's important to note",
  "in conclusion", "whether you're", "look no further", "ever-changing". No emojis. No exclamation marks.

SEO
- The article must satisfy the search intent of the target keyword better than anything else on page one.
- The lede answers the question directly in 40-60 words (featured-snippet style) and includes the keyword naturally.
- 5-8 <h2> sections with descriptive, keyword-rich headings; <h3> where useful. Never an <h1> in the body.
- Use the keyword and close variants naturally; no keyword stuffing.
- Include at least one worked example with real arithmetic, shown step by step, using the FACT PACK when relevant.
- Include one comparison <table> when it genuinely helps (wrap it in <div class="scroll">...</div>).
- Link to 3-6 relevant pages from the INTERNAL PAGES list only, with descriptive anchor text. No external links.
- End with a practical "what to do next" section.

ACCURACY (critical)
- Only use statistics from the FACT PACK or widely established facts (for example DOE thermostat guidance, basic physics).
- If a figure isn't in the FACT PACK and you're not certain it's well established, describe it qualitatively or as a typical range with "about/typically".
- Never invent studies, surveys, quotes, company names, prices of specific providers or legal rules.
- Texas rules must match the FACT PACK exactly.

FORMAT
Return ONLY one JSON object, no markdown fences, with these keys:
{
 "slug": "lowercase-hyphenated-url-slug (3-8 words, contains the keyword)",
 "title": "SEO title, 45-65 characters, keyword near the start, may include (2026)",
 "h1": "On-page headline in sentence case",
 "desc": "Meta description, 140-160 characters, includes keyword and a reason to click",
 "lede": "40-70 word opening paragraph (plain text, <strong> allowed)",
 "body": "Article HTML, 1,200-1,800 words, allowed tags only: h2 h3 p ul ol li strong em a table thead tbody tr th td div(class=scroll)",
 "faq": [["question", "answer in 1-3 sentences"], ... 4 items, questions people actually search],
 "sources": ["Organization, document or dataset (domain)", ... 1-4 official sources you relied on],
 "tool": ["CTA button text (2-5 words)", "One-line CTA description", "/internal/path/"]
}"""

ALLOWED = {"h2", "h3", "p", "ul", "ol", "li", "strong", "em", "a", "table", "thead", "tbody", "tr", "th", "td", "div", "br"}
BANNED = ["in today's world", "delve", "game-changer", "it's important to note", "in conclusion", "look no further", "ever-changing", "unlock"]

def words(html):
    return len(re.sub(r"<[^>]+>", " ", html).split())

def validate(a, pages, existing_slugs, keyword):
    errs = []
    for k in ["slug", "title", "h1", "desc", "lede", "body", "faq", "sources", "tool"]:
        if not a.get(k): errs.append(f"missing {k}")
    if errs: return errs
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+){2,9}", a["slug"]): errs.append("slug format")
    if a["slug"] in existing_slugs: errs.append("slug already exists; choose a different angle and slug")
    if not 40 <= len(a["title"]) <= 70: errs.append(f"title length {len(a['title'])} (need 45-65)")
    if not 120 <= len(a["desc"]) <= 165: errs.append(f"desc length {len(a['desc'])} (need 140-160)")
    n = words(a["body"])
    if not 1100 <= n <= 2200: errs.append(f"body is {n} words (need 1,200-1,800)")
    if len(re.findall(r"<h2>", a["body"])) < 4: errs.append("need at least 5 <h2> sections")
    tags = {t.lower() for t in re.findall(r"</?\s*([a-zA-Z0-9]+)", a["body"])}
    bad = tags - ALLOWED
    if bad: errs.append(f"disallowed tags: {sorted(bad)}")
    if re.search(r"<div(?![^>]*class=\"scroll\")", a["body"]): errs.append("div only allowed as <div class=\"scroll\">")
    if re.search(r"\son\w+=|javascript:|<script|style=", a["body"], re.I): errs.append("no scripts, event handlers or inline styles")
    links = re.findall(r'href="([^"]+)"', a["body"])
    ext = [l for l in links if not l.startswith("/")]
    if ext: errs.append(f"external links not allowed: {ext}")
    broken = [l for l in links if l.startswith("/") and l.split("#")[0] not in pages]
    if broken: errs.append(f"links to pages that don't exist: {broken}")
    if len(set(links)) < 3: errs.append("need at least 3 internal links")
    if not (3 <= len(a["faq"]) <= 6) or not all(isinstance(x, list) and len(x) == 2 for x in a["faq"]): errs.append("faq must be 4 [q,a] pairs")
    tool = a["tool"]
    if not (isinstance(tool, list) and len(tool) == 3 and tool[2].split("#")[0] in pages): errs.append("tool must be [text, description, existing internal path]")
    low = (a["body"] + a["lede"]).lower()
    used = [b for b in BANNED if b in low]
    if used: errs.append(f"banned phrases used: {used}")
    kw = keyword.lower().split()
    if sum(w in (a["title"] + " " + a["lede"]).lower() for w in kw) < max(1, len(kw) - 1): errs.append("keyword missing from title/lede")
    return errs

def call_claude(messages):
    body = json.dumps({"model": MODEL, "max_tokens": 12000, "system": STYLE, "messages": messages}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=body, headers={
        "x-api-key": API_KEY, "anthropic-version": "2023-06-01", "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        sys.exit(f"API error {e.code}: {e.read().decode()[:500]}")
    return "".join(b.get("text", "") for b in data["content"] if b["type"] == "text")

def parse(text):
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    start, end = text.find("{"), text.rfind("}")
    return json.loads(text[start:end + 1])

def main():
    if not API_KEY: sys.exit("ANTHROPIC_API_KEY is not set")
    queue = json.load(open("content/queue.json", encoding="utf-8"))
    item = next((q for q in queue if q.get("status") == "pending"), None)
    if not item:
        print("Queue is empty. Add topics to content/queue.json."); sys.exit(2)
    pages = site_catalog()
    existing = {p.strip("/").split("/")[-1] for p in pages if p.startswith("/blog/")}
    brief = f"""TARGET KEYWORD: {item['keyword']}
WORKING TITLE: {item.get('title', '')}
ANGLE AND MUST-COVER POINTS: {item.get('angle', '')}
READER: {item.get('reader', 'U.S. households who want to understand and lower their electric bill')}

INTERNAL PAGES (path: title). Link only to these:
{chr(10).join(f'{p}: {t}' for p, t in sorted(pages.items()))}

FACT PACK (use these figures exactly):
{json.dumps(fact_pack(), indent=1)}

Write the article now. Return only the JSON object."""
    messages = [{"role": "user", "content": brief}]
    for attempt in range(3):
        raw = call_claude(messages)
        try:
            art = parse(raw)
            errs = validate(art, pages, existing, item["keyword"])
        except Exception as e:
            art, errs = None, [f"invalid JSON: {e}"]
        if not errs: break
        print(f"Attempt {attempt + 1} failed checks: {errs}")
        messages += [{"role": "assistant", "content": raw},
                     {"role": "user", "content": "Fix these problems and return the complete corrected JSON only:\n- " + "\n- ".join(errs)}]
    else:
        sys.exit("Article failed quality checks after 3 attempts; nothing published.")

    art["date"] = TODAY
    art["keyword"] = item["keyword"]
    out = f"content/articles/{TODAY}-{art['slug']}.json"
    json.dump(art, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    item["status"] = "done"; item["published"] = TODAY; item["slug"] = art["slug"]
    json.dump(queue, open("content/queue.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"Wrote {out} ({words(art['body'])} words): {art['title']}")
    with open(os.environ.get("GITHUB_OUTPUT", os.devnull), "a") as gh:
        gh.write(f"title={art['title']}\nslug={art['slug']}\n")

if __name__ == "__main__":
    main()
