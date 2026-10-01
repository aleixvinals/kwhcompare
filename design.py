# Design v2: image library, icons, header/footer, cards
import os, json, glob, re

IMG = {  # key: (alt text, accent hue for fallback, icon). Photos (webp/jpg/png) override the SVG illustrations.
 "hero":        ("Illustration of a suburban home at dusk with warm lights on inside", 160, "house"),
 "power-lines": ("Illustration of electric transmission towers and power lines at sunset", 30, "tower"),
 "meter":       ("Illustration of an electric meter mounted on the outside wall of a house", 200, "meter"),
 "thermostat":  ("Illustration of a smart thermostat on a living room wall", 15, "thermo"),
 "ev-charging": ("Illustration of an electric car plugged into a home charger in a garage", 190, "car"),
 "solar":       ("Illustration of solar panels on a residential roof under a blue sky", 45, "sun"),
 "bill":        ("Illustration of an electric bill and a calculator on a desk", 140, "receipt"),
 "texas":       ("Illustration of a Texas city skyline at sunset", 25, "star"),
 "moving":      ("Illustration of moving boxes stacked in a bright new home", 35, "box"),
 "ac-unit":     ("Illustration of outdoor air conditioner units beside a house", 195, "fan"),
 "lightbulb":   ("Illustration of an LED light bulb glowing in a dark room", 50, "bulb"),
}
ICON = {
 "house":   '<path d="M3 11l9-7 9 7v9a1 1 0 0 1-1 1h-5v-6H9v6H4a1 1 0 0 1-1-1z"/>',
 "tower":   '<path d="M12 2l-5 20M12 2l5 20M8 9h8M6.5 15h11M9 6h6"/>',
 "meter":   '<circle cx="12" cy="12" r="9"/><path d="M12 12l4-4M8 16h8"/>',
 "thermo":  '<path d="M10 14V5a2 2 0 0 1 4 0v9a4 4 0 1 1-4 0z"/><path d="M12 9v6"/>',
 "car":     '<path d="M3 16v-4l2-5h10l3 5h3v4h-2M3 16h2m12 0H9"/><circle cx="7" cy="16" r="2"/><circle cx="17" cy="16" r="2"/>',
 "sun":     '<circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M5 19l2-2M17 7l2-2"/>',
 "receipt": '<path d="M6 2h12v20l-3-2-3 2-3-2-3 2z"/><path d="M9 7h6M9 11h6M9 15h4"/>',
 "star":    '<path d="M12 2l3 7h7l-5.5 4.5L18.5 21 12 16.5 5.5 21l2-7.5L2 9h7z"/>',
 "box":     '<path d="M3 7l9-4 9 4v10l-9 4-9-4z"/><path d="M3 7l9 4 9-4M12 11v10"/>',
 "fan":     '<circle cx="12" cy="12" r="2"/><path d="M12 10c0-4 1-7 4-7s2 5-2 8M14 12c4 0 7 1 7 4s-5 2-8-2M12 14c0 4-1 7-4 7s-2-5 2-8M10 12c-4 0-7-1-7-4s5-2 8 2"/>',
 "bulb":    '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
 "calc":    '<rect x="5" y="2" width="14" height="20" rx="2"/><path d="M8 6h8M8 11h2M14 11h2M8 15h2M14 15h2M8 19h2M14 19h2"/>',
 "map":     '<path d="M9 3L3 6v15l6-3 6 3 6-3V3l-6 3z"/><path d="M9 3v15M15 6v15"/>',
 "bolt":    '<path d="M13 2L4 14h7l-1 8 9-12h-7z"/>',
 "shield":  '<path d="M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
 "lock":    '<rect x="4" y="10" width="16" height="11" rx="2"/><path d="M8 10V7a4 4 0 0 1 8 0v3"/>',
 "doc":     '<path d="M6 2h9l5 5v15H6z"/><path d="M14 2v6h6M9 13h8M9 17h8"/>',
 "scale":   '<path d="M12 3v18M5 21h14M6 7h12M6 7l-3 7a3 3 0 0 0 6 0zM18 7l-3 7a3 3 0 0 0 6 0z"/>',
}
def icon(name, size=24):
    return f'<svg class="ico" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICON[name]}</svg>'

def img_file(key):
    for ext in ("webp", "jpg", "jpeg", "png", "svg"):
        if os.path.exists(f"static/img/{key}.{ext}"): return f"/img/{key}.{ext}"
    return None

def figure(key, cls="", eager=False):
    alt, hue, ic = IMG[key]
    f = img_file(key)
    if f:
        load = 'fetchpriority="high"' if eager else 'loading="lazy"'
        return f'<figure class="ph {cls}"><img src="{f}" alt="{alt}" {load} decoding="async"></figure>'
    return (f'<figure class="ph ph-fallback {cls}" role="img" aria-label="{alt}" style="--h:{hue}">'
            f'{icon(ic, 56)}</figure>')

def hero_bg():
    f = img_file("hero")
    return f' style="--hero:url({f})"' if f else ""

# Article category + image, works for hand-written and automated articles
RULES = [
 (r"\bev\b|electric car|charg", "EV", "ev-charging"),
 (r"solar", "Solar", "solar"),
 (r"summer|air condition|\bac\b", "Savings", "ac-unit"),
 (r"winter|heater|thermostat|heat pump", "Savings", "thermostat"),
 (r"deposit|moving|move|set up|setup|prepaid", "Moving", "moving"),
 (r"kwh|kilowatt|refrigerator|appliance|pool", "Basics", "lightbulb"),
 (r"going up|rising|prices up|increase", "Analysis", "power-lines"),
 (r"average.*texas|texas.*average|electric-bill-texas", "Texas", "texas"),
 (r"bill|price|rate|budget|fee|switch|facts label|efl|plan", "Bills & plans", "bill"),
 (r"texas|houston|dallas|ercot", "Texas", "texas"),
]
def art_meta(a):
    text = " ".join([a.get("slug",""), a.get("title",""), a.get("keyword","")]).lower()
    for pat, cat, im in RULES:
        if re.search(pat, text): return cat, im
    return "Guide", "power-lines"

def load_articles():
    from blog2 import ARTICLES
    arts = list(ARTICLES)
    for f in sorted(glob.glob("content/articles/*.json")):
        a = json.load(open(f, encoding="utf-8"))
        a["faq"] = [tuple(x) for x in a["faq"]]; a["tool"] = tuple(a["tool"])
        a.setdefault("script", ""); a.setdefault("sources", [])
        if not any(x["slug"] == a["slug"] for x in arts): arts.append(a)
    return sorted(arts, key=lambda a: a["date"], reverse=True)

def cap(s): return s[0].upper() + s[1:]

def guide_card(a, eager=False):
    cat, im = art_meta(a)
    return (f'<a class="gcard" href="/blog/{a["slug"]}/">{figure(im, "gcard-img", eager)}'
            f'<div class="gcard-body"><span class="kicker">{cat}</span><h3>{cap(a["h1"])}</h3>'
            f'<p>{a["desc"]}</p></div></a>')

TRUSTBAR = ('<div class="trustbar"><div class="wrap"><span>' + icon("bolt",14) + 'Free, no sign-up</span>'
            '<span>' + icon("lock",14) + 'Your numbers stay in your browser</span>'
            '<span>' + icon("shield",14) + 'Rates updated September 2026</span></div></div>')

def make_header():
    return TRUSTBAR + '''<header class="site">
  <div class="wrap">
    <a class="logo" href="/" aria-label="kWhCompare home"><span class="logo-mark" aria-hidden="true">⚡</span>kWhCompare</a>
    <nav class="top" aria-label="Main">
      <a href="/#tools">Tools</a>
      <a href="/#rates">Rates by state</a>
      <a href="/electricity-rates/texas/">Texas</a>
      <a href="/blog/">Guides</a>
      <a href="/methodology/">How we calculate</a>
    </nav>
  </div>
</header>'''

def make_footer(arts):
    g = "".join(f'<li><a href="/blog/{a["slug"]}/">{cap(a["h1"])}</a></li>' for a in arts[:5])
    return f'''<footer class="site-foot">
  <div class="wrap foot-grid">
    <div class="foot-brand"><a class="logo" href="/"><span class="logo-mark" aria-hidden="true">⚡</span>kWhCompare</a>
      <p>Independent electricity rate comparisons for U.S. households, built on official data.</p></div>
    <div><h3>Tools</h3><ul>
      <li><a href="/#compare">Electric bill analyzer</a></li>
      <li><a href="/#rates">Electricity rates by state</a></li>
      <li><a href="/electricity-rates/texas/#texas-cities">Texas plan calculator</a></li>
      <li><a href="/esi-id-lookup/">ESI ID lookup</a></li>
      <li><a href="/texas/tdu-delivery-charges/">TDU delivery charges</a></li></ul></div>
    <div><h3>Guides</h3><ul>{g}<li><a href="/blog/">All guides →</a></li></ul></div>
    <div><h3>Company</h3><ul>
      <li><a href="/about/">About</a></li><li><a href="/methodology/">How we calculate</a></li><li><a href="/contact/">Contact</a></li></ul>
      <h3>Legal</h3><ul><li><a href="/privacy/">Privacy policy</a></li><li><a href="/terms/">Terms of use</a></li></ul></div>
  </div>
  <div class="wrap foot-legal"><p>Results are estimates for educational purposes and aren't financial advice or offers from any provider. Your utility bill is the final word on what you owe. Rate data: U.S. Energy Information Administration and Public Utility Commission of Texas. © 2026 kWhCompare.</p></div>
</footer>'''
