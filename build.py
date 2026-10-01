import re, json, html
SITE="https://kwhcompare.com"
import datetime
UPDATED="September 2026"; ISO=datetime.date.today().isoformat()
import os, shutil, glob, json
ROOT=os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
shutil.rmtree('site',ignore_errors=True); shutil.copytree('static','site')
src=open('templates/home.html').read()
js=open('static/assets/app.js').read()
rows=re.findall(r'\["(\w\w)","([^"]+)",([\d.]+),(\d+),(-?[\d.]+)\]',js)
S=[dict(code=c,name=n,rate=float(r),bill=int(b),yoy=float(y)) for c,n,r,b,y in rows]
US=18.34
CHOICE={"TX","PA","OH","IL","NY","NJ","MD","MA","CT","DE","ME","NH","RI","DC"}
LIMITED={"MI","VA","CA","OR","NV"}
CS={"NY","NJ","MA","MD","IL","MN","CO","ME","NM","VA","DE","CT","RI","OR","CA","HI","WA","DC"}
REG={"Northeast":"CT DE DC ME MD MA NH NJ NY PA RI VT","West":"AK AZ CA CO HI ID MT NV NM OR UT WA WY",
"Midwest":"IL IN IA KS MI MN MO NE ND OH SD WI","Southeast":"AL FL GA KY MS NC SC TN VA WV","South Central":"AR LA OK TX"}
region={c:r for r,cs in REG.items() for c in cs.split()}
U={"AL":"Alabama Power and local TVA distributors such as Huntsville Utilities","AK":"Chugach Electric, Matanuska Electric and Golden Valley Electric",
"AZ":"APS, Tucson Electric Power and SRP","AR":"Entergy Arkansas, SWEPCO and OG&E","CA":"PG&E, Southern California Edison, SDG&E, LADWP and SMUD",
"CO":"Xcel Energy, Black Hills Energy and Colorado Springs Utilities","CT":"Eversource and United Illuminating","DE":"Delmarva Power and Delaware Electric Cooperative",
"DC":"Pepco","FL":"FPL, Duke Energy Florida, Tampa Electric and JEA","GA":"Georgia Power and the state's electric membership cooperatives",
"HI":"Hawaiian Electric and Kauai Island Utility Cooperative","ID":"Idaho Power, Rocky Mountain Power and Avista","IL":"ComEd and Ameren Illinois",
"IN":"Duke Energy Indiana, AES Indiana, NIPSCO and Indiana Michigan Power","IA":"MidAmerican Energy and Alliant Energy","KS":"Evergy",
"KY":"LG&E and KU, Kentucky Power and Duke Energy Kentucky","LA":"Entergy Louisiana, Cleco and SWEPCO","ME":"Central Maine Power and Versant Power",
"MD":"BGE, Pepco, Delmarva Power and Potomac Edison","MA":"Eversource, National Grid and Unitil","MI":"DTE Energy and Consumers Energy",
"MN":"Xcel Energy, Minnesota Power and Otter Tail Power","MS":"Mississippi Power, Entergy Mississippi and TVA distributors",
"MO":"Ameren Missouri, Evergy and Liberty","MT":"NorthWestern Energy and Montana-Dakota Utilities","NE":"public power districts such as OPPD, NPPD and LES",
"NV":"NV Energy","NH":"Eversource, Unitil and Liberty","NJ":"PSE&G, JCP&L, Atlantic City Electric and Rockland Electric",
"NM":"PNM, El Paso Electric and Xcel Energy","NY":"Con Edison, National Grid, NYSEG, RG&E, Central Hudson, Orange & Rockland and PSEG Long Island",
"NC":"Duke Energy Carolinas, Duke Energy Progress and Dominion Energy","ND":"Xcel Energy, Montana-Dakota Utilities and Otter Tail Power",
"OH":"AEP Ohio, FirstEnergy (Ohio Edison, The Illuminating Company, Toledo Edison), Duke Energy Ohio and AES Ohio","OK":"OG&E and PSO",
"OR":"Portland General Electric and Pacific Power","PA":"PECO, PPL Electric, Duquesne Light and FirstEnergy Pennsylvania",
"RI":"Rhode Island Energy","SC":"Duke Energy, Dominion Energy South Carolina and Santee Cooper","SD":"Black Hills Energy, Xcel Energy and NorthWestern Energy",
"TN":"TVA distributors such as Nashville Electric Service, MLGW, EPB and KUB","TX":"Oncor, CenterPoint Energy, AEP Texas and TNMP in the competitive market, plus city utilities such as Austin Energy and CPS Energy",
"UT":"Rocky Mountain Power","VT":"Green Mountain Power","VA":"Dominion Energy Virginia and Appalachian Power","WA":"Puget Sound Energy, Seattle City Light and Avista",
"WV":"Appalachian Power, Mon Power and Potomac Edison","WI":"We Energies, WPS, Alliant Energy and Xcel Energy","WY":"Rocky Mountain Power, Black Hills Energy and Cheyenne Light, Fuel & Power"}
OFFICIAL={"TX":"Power to Choose, run by the Public Utility Commission of Texas","PA":"PAPowerSwitch, run by the Pennsylvania PUC","OH":"Energy Choice Ohio, run by PUCO",
"IL":"Plug In Illinois, run by the Illinois Commerce Commission","CT":"EnergizeCT's rate board","MA":"Energy Switch Massachusetts"}
slug=lambda n: re.sub(r'[^a-z]+','-',n.lower())
ranked=sorted(S,key=lambda s:s['rate']); 
for i,s in enumerate(ranked): s['rank']=i+1
e=html.escape
andjoin=lambda l: l[0] if len(l)==1 else ", ".join(l[:-1])+" and "+l[-1]

css_link='<link rel="stylesheet" href="/assets/site.css">'
fonts='<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,400..800&display=swap" rel="stylesheet">'
CFG=json.load(open('site.config.json')) if os.path.exists('site.config.json') else {}
AD_CLIENT=(CFG.get('adsense_client') or '').strip()
AD_SLOTS=CFG.get('ad_slots') or {}
AD_PLACEHOLDERS=bool(CFG.get('show_ad_placeholders')) or os.environ.get('AD_PLACEHOLDERS')=='1'
ADS_ON=bool(AD_CLIENT)
ADS=(f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client={AD_CLIENT}" crossorigin="anonymous"></script>' if ADS_ON
     else '<!-- Google AdSense: add your publisher ID in site.config.json to switch ads on -->')
AD_LOADER=('<script>document.querySelectorAll("ins.adsbygoogle").forEach(function(i){if(i.offsetWidth>0&&!i.dataset.adsbygoogleStatus){(window.adsbygoogle=window.adsbygoogle||[]).push({});}});</script>' if ADS_ON else '')
header=src.split('<header class="site">')[1].split('</header>')[0]
header=header.replace('<a href="#faq">FAQ</a>','<a href="/esi-id-lookup/">ESI ID lookup</a>\n      <a href="#faq">FAQ</a>')
header=header.replace('<a href="#read-bill">Read your bill</a>','<a href="#texas">Texas</a>\n      <a href="#esi">ESI ID lookup</a>\n      <a href="#blog">Guides</a>')
header='<header class="site">'+header.replace('href="#top"','href="/"').replace('href="#rates"','href="/#rates"').replace('href="#choice"','href="/#choice"').replace('href="#texas"','href="/electricity-rates/texas/"').replace('href="#esi"','href="/esi-id-lookup/"').replace('href="#blog"','href="/blog/"').replace('href="#faq"','href="/#faq"')+'</header>'
footer=f'''<footer>
  <div class="wrap cols">
    <div><strong class="logo" style="font-size:1rem">kWhCompare</strong><p style="max-width:44ch">Independent electricity rate comparisons for U.S. households. Estimates are for guidance only and aren't offers from any provider.</p></div>
    <div><p><a href="/#rates">Rates by state</a><br><a href="/electricity-rates/texas/">Texas rates</a><br><a href="/electricity-rates/pennsylvania/">Pennsylvania rates</a><br><a href="/electricity-rates/ohio/">Ohio rates</a></p></div>
    <div><p><a href="/blog/">Guides</a><br><a href="/blog/why-is-my-electric-bill-so-high/">Why is my bill so high?</a><br><a href="/blog/what-is-a-good-price-per-kwh/">Good price per kWh</a></p></div>
    <div><p><a href="/about/">About</a><br><a href="/methodology/">Methodology</a><br><a href="/privacy/">Privacy policy</a><br><a href="/terms/">Terms of use</a><br><a href="/contact/">Contact</a></p></div>
  </div>
  <div class="wrap"><p>© 2026 kWhCompare. Rate data: U.S. Energy Information Administration.</p></div>
</footer>'''
tool=src.split('<div class="tool" id="compare">')[1].split('<div id="results" hidden aria-live="polite"></div>')[0]
tool='<div class="tool" id="compare">'+tool+'<div id="results" hidden aria-live="polite"></div>\n    </div>'
def ad(n=1, kind="display", wrap=True):
    """One ad unit. Nothing is rendered until AdSense is configured (or placeholders are on for previews)."""
    if not (ADS_ON or AD_PLACEHOLDERS): return ""
    if ADS_ON:
        slot=AD_SLOTS.get(kind) or AD_SLOTS.get("display") or ""
        if not slot: return ""
        if kind=="in_article":
            unit=f'<ins class="adsbygoogle" style="display:block;text-align:center" data-ad-layout="in-article" data-ad-format="fluid" data-ad-client="{AD_CLIENT}" data-ad-slot="{slot}"></ins>'
        elif kind=="sidebar":
            unit=f'<ins class="adsbygoogle" style="display:block" data-ad-client="{AD_CLIENT}" data-ad-slot="{slot}" data-ad-format="vertical"></ins>'
        else:
            unit=f'<ins class="adsbygoogle" style="display:block" data-ad-client="{AD_CLIENT}" data-ad-slot="{slot}" data-ad-format="auto" data-full-width-responsive="true"></ins>'
    else:
        unit='<div class="ad-ph">Ad space</div>'
    box=f'<aside class="ad ad-{kind.replace("_","-")}" aria-label="Advertisement"><span class="ad-label">Advertisement</span>{unit}</aside>'
    return f'<div class="wrap">{box}</div>' if wrap else box
import design as D
ALL_ARTS=D.load_articles()
header=D.make_header()
footer=D.make_footer(ALL_ARTS)

def head(title,desc,path,ld,extra=""):
    return f'''<!DOCTYPE html>
<html lang="en-US">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:type" content="website"><meta property="og:locale" content="en_US"><meta property="og:site_name" content="kWhCompare">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{SITE}{path}">
<meta name="twitter:card" content="summary">
<meta name="theme-color" content="#14302b">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⚡</text></svg>">
{ADS}
{fonts}
{css_link}
<script type="application/ld+json">{json.dumps(ld)}</script>
{extra}</head>'''

def crumbs(items):
    return {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":i+1,"name":n,"item":SITE+p} for i,(n,p) in enumerate(items)]}

def state_page(s):
    c,n=s['code'],s['name']; path=f"/electricity-rates/{slug(n)}/"
    kwh=round(s['bill']/s['rate']*100)
    vs=(s['rate']-US)/US*100
    vs_txt=f"{abs(vs):.0f}% {'above' if vs>0 else 'below'} the national average of {US}¢"
    rk=s['rank']; rk_txt=f"{rk}{'th' if 10<rk%100<14 else {1:'st',2:'nd',3:'rd'}.get(rk%10,'th')}"
    trend=f"up {s['yoy']:.1f}%" if s['yoy']>0 else f"down {abs(s['yoy']):.1f}%"
    reg=region[c]; peers=[x for x in S if region[x['code']]==reg and x['code']!=c]
    peers_sorted=sorted(peers,key=lambda x:x['rate'])
    cheaper=[x for x in peers_sorted if x['rate']<s['rate']]
    if c=="TX":
        market=f"""<h2>Can you choose your electricity provider in Texas?</h2>
<p>Yes, and in most of the state you have to. Homes served by Oncor, CenterPoint Energy, AEP Texas and TNMP pick a retail electric provider, while the utility keeps delivering power and handling outages. Cities with their own utilities, such as Austin Energy and San Antonio's CPS Energy, are not part of the competitive market.</p>
<p>Your 17- or 22-digit ESI ID on the bill identifies your meter and utility. Texas plans are advertised at 500, 1,000 and 2,000 kWh, so compare the price at your real usage, and watch for bill credits that only apply above a certain usage. When your contract ends, many providers roll you onto a pricier month-to-month rate. You can cross-check offers on {OFFICIAL[c]}.</p>"""
    elif c in CHOICE:
        market=f"""<h2>Can you choose your electricity provider in {n}?</h2>
<p>Yes. {n} has retail electricity choice. Your local utility keeps delivering power and handling outages, but you can buy the electricity itself from a competitive supplier. That supply charge is usually more than half of an all-in bill, so it's where switching pays off.</p>
<p>If you've never shopped, you're likely on your utility's default rate, often shown on the bill as the "price to compare." Before switching, check whether the rate is fixed or variable, the contract length, any monthly fee and the early cancellation fee.{f' You can cross-check offers on {OFFICIAL[c]}.' if c in OFFICIAL else ''}</p>"""
    elif c in LIMITED:
        market=f"""<h2>Can you choose your electricity provider in {n}?</h2>
<p>Only in a limited way. {n} allows retail choice for some customers or through capped programs, so most households stay with {U[c]}. Your biggest levers are the rate plans your utility offers, community solar where available, and cutting usage.</p>"""
    else:
        market=f"""<h2>Can you choose your electricity provider in {n}?</h2>
<p>No. {n} is a regulated market: {U[c]} both deliver and sell your power, and rates are set by the state utility commission. You can't switch supplier, but you can change how you pay, for example with a time-of-use plan, budget billing or efficiency upgrades.</p>"""
    tips=[]
    if c in CHOICE: tips.append("<li><strong>Compare fixed-rate supply plans.</strong> Households on the default rate often save 10–20% on the supply portion.</li>")
    tips.append("<li><strong>Ask your utility about time-of-use pricing.</strong> Shifting laundry, dishwashing and EV charging to off-peak hours can cut 5–15%.</li>")
    if c in CS: tips.append(f"<li><strong>Look at community solar.</strong> {n} has community solar programs that credit your bill for a share of a local solar farm, often 5–15% savings with no rooftop panels.</li>")
    tips.append("<li><strong>Tackle heating and cooling first.</strong> A smart thermostat and sealed air leaks usually save more than any other single change.</li>")
    tips.append("<li><strong>Check for assistance programs.</strong> LIHEAP and utility discount programs can lower bills for eligible households.</li>")
    faq=[(f"What is the average electricity rate in {n}?",f"The average residential rate in {n} is {s['rate']:.2f} cents per kWh as of {UPDATED}, {vs_txt}."),
         (f"What is the average electric bill in {n}?",f"About ${s['bill']} per month, based on average use of roughly {kwh:,} kWh."),
         (f"Can I switch electricity providers in {n}?",("Yes. "+n+" has retail electricity choice, so you can pick a competitive supplier while your utility keeps delivering power.") if c in CHOICE else ("Only in a limited way; most households stay with their utility." if c in LIMITED else f"No. {n} is regulated, so your utility sells and delivers your power.")),
         (f"Who are the main electric utilities in {n}?",f"The main utilities in {n} are {U[c]}.")]
    ld={"@context":"https://schema.org","@graph":[crumbs([("Home","/"),("Electricity rates","/#rates"),(n,path)]),
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}]}
    title=f"{n} Electricity Rates ({UPDATED}): {s['rate']:.2f}¢/kWh Average | kWhCompare"
    desc=f"{n} residential electricity averages {s['rate']:.2f}¢/kWh ({UPDATED}), {trend} in a year. Check your bill against the {n} average and see ways to pay less."
    links=" ".join(f'<li><a href="/electricity-rates/{slug(x["name"])}/">{x["name"]} {x["rate"]:.1f}¢</a></li>' for x in peers_sorted)
    return path, head(title,desc,path,ld)+f'''
<body data-state="{c}">
{header}
<main>
<div class="wrap crumbs"><a href="/">Home</a> / <a href="/#rates">Electricity rates</a> / {n}</div>
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>Electricity rates in {n}</h1>
      <p class="lede">Homes in {n} pay an average of {s['rate']:.2f}¢ per kWh, {vs_txt}. Enter your bill to see where you stand.</p>
      <dl class="facts">
        <div><dt>{n} average</dt><dd>{s['rate']:.2f}¢/kWh</dd></div>
        <div><dt>Avg monthly bill</dt><dd>${s['bill']}</dd></div>
        <div><dt>Past 12 months</dt><dd>{'+' if s['yoy']>0 else ''}{s['yoy']:.1f}%</dd></div>
      </dl>
      {D.figure("texas" if c=="TX" else "power-lines","hero-photo")}
    </div>
    {tool}
  </div>
</section>
<section class="content">
  <div class="wrap prose">
    <h2>How {n} electricity prices compare</h2>
    <p>{n} ranks <strong>{rk_txt} cheapest of 51</strong> (50 states plus D.C.) for residential electricity. At {s['rate']:.2f}¢/kWh, it sits {vs_txt}, and prices are {trend} over the past year.</p>
    <p>The typical {n} household uses about <strong>{kwh:,} kWh a month</strong> and pays around <strong>${s['bill']}</strong>. {"Among " + reg + " states, " + andjoin([x['name'] for x in cheaper[:3]]) + (" have" if len(cheaper[:3])>1 else " has") + " lower rates." if cheaper else f"{n} has the lowest rate in the {reg} region."}</p>
    <dl class="statbox">
      <div><dt>Rate</dt><dd>{s['rate']:.2f}¢</dd></div>
      <div><dt>vs U.S.</dt><dd>{'+' if vs>0 else '−'}{abs(vs):.0f}%</dd></div>
      <div><dt>Avg usage</dt><dd>{kwh:,} kWh</dd></div>
      <div><dt>National rank</dt><dd>{rk_txt}</dd></div>
    </dl>
    <p>To find your own rate, divide your total bill by the kWh you used. If you paid ${s['bill']} for {kwh:,} kWh, you're right at the {n} average.</p>
  </div>
</section>
{ad(1)}
<section class="content">
  <div class="wrap two-col">
    <div class="prose">{market}
      <h2>Main electric utilities in {n}</h2>
      <p>Most {n} homes are served by {U[c]}. Your utility's name and account number are near the top of your bill.</p>
    </div>
    <div class="prose">
      <h2>How to lower your electric bill in {n}</h2>
      <ul>{''.join(tips)}</ul>
    </div>
  </div>
</section>
{ad(2)}
<section class="content">
  <div class="wrap">
    <h2>{n} electricity FAQ</h2>
    {''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in faq)}
  </div>
</section>
<section class="content">
  <div class="wrap">
    <h2>Compare other {reg} states</h2>
    <ul class="state-links">{links}</ul>
    <p class="disclaimer">Averages are EIA residential revenue divided by kWh sold, {UPDATED}. Your rate depends on your utility, plan and season. <a href="/#rates">See all 50 states</a>.</p>
  </div>
</section>
</main>
{footer}
<script src="/assets/app.js" defer></script>
</body>
</html>'''

def simple(path,title,desc,body):
    ld={"@context":"https://schema.org","@graph":[crumbs([("Home","/"),(title,path)])]}
    return head(f"{title} | kWhCompare",desc,path,ld)+f'''
<body>
{header}
<main><div class="wrap crumbs"><a href="/">Home</a> / {title}</div>
<section class="content" style="border:0"><div class="wrap prose"><h1 style="font-size:clamp(2rem,4vw,2.8rem)">{title}</h1>{body}</div></section></main>
{footer}
</body></html>'''

import os
import hashlib
def _ver(f):
    return hashlib.md5(open(f,'rb').read()).hexdigest()[:10]
ASSET_V={a:_ver('static/assets/'+a) for a in ('site.css','app.js','tx.js')}
def write(path,content):
    for a,v in ASSET_V.items():
        content=content.replace(f'/assets/{a}"',f'/assets/{a}?v={v}"')
    if AD_LOADER and '</body>' in content: content=content.replace('</body>',AD_LOADER+'\n</body>',1)
    p='site'+path+('index.html' if path.endswith('/') else '')
    os.makedirs(os.path.dirname(p),exist_ok=True); open(p,'w').write(content)

paths=["/"]
for s in S:
    p,c=state_page(s); write(p,c); paths.append(p)

# Home page from the original, with external assets
home=src
home=re.sub(r'<style>.*?</style>',css_link,home,flags=re.S)
home=re.sub(r'<script>\s*const STATES.*?</script>','<script src="/assets/app.js" defer></script>',home,flags=re.S)
home=re.sub(r'<section class="content" id="states">.*?</section>\n','',home,flags=re.S)
home=home.replace('https://kwhcompare.netlify.app',SITE).replace('https://www.kwhcompare.com',SITE)
home=home.replace('https://www.kwhcompare.com',SITE)
home=home.replace('<meta name="theme-color" content="#14302b">','<meta name="theme-color" content="#14302b">\n<link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>⚡</text></svg>">')
home=re.sub(r'<footer>.*?</footer>',footer,home,flags=re.S)
allstates=" ".join(f'<li><a href="/electricity-rates/{slug(s["name"])}/">{s["name"]}</a></li>' for s in S)
home=home.replace('<section class="content" id="how">',f'<section class="content" id="states"><div class="wrap"><h2>Electricity rates in your state</h2><ul class="state-links">{allstates}</ul></div></section>\n<section class="content" id="how">')
write("/",home)

priv="""<p>Last updated September 25, 2026.</p>
<h2>What we collect</h2><p>Numbers you type into the comparison tool (state, kWh, bill amount, ESI ID) are processed in your browser. Your last entries may be remembered in your browser's local storage so you don't have to retype them; you can clear this in your browser settings. We don't ask for your name, email or address.</p>
<h2>Your bill numbers</h2><p>The numbers you enter in our calculators are processed in your browser and never sent to us. We don't ask for or store your bill.</p>
<h2>Advertising and cookies</h2><p>We use Google AdSense to show ads. Google and its partners use cookies to serve ads based on your prior visits to this and other websites. You can opt out of personalized advertising at Google's Ads Settings (adssettings.google.com) or at aboutads.info. Third-party vendors may also use cookies in line with their own policies.</p>
<h2>Analytics</h2><p>We may use privacy-friendly analytics to count visits and improve pages. This data is aggregated and not used to identify you.</p>
<h2>Affiliate links</h2><p>Some links to electricity plans may be affiliate links. If you sign up through one, we may earn a commission at no cost to you. This never changes the rate you're offered.</p>
<h2>Your rights</h2><p>California residents have rights under the CCPA, including the right to know and delete personal information. Because we don't collect personal information directly, most requests can be handled by clearing your browser's cookies and storage. Contact us with any questions.</p>
<h2>Children</h2><p>This site isn't directed at children under 13 and we don't knowingly collect their information.</p>"""
terms="""<p>Last updated September 25, 2026.</p>
<p>kWhCompare provides general information and estimates about U.S. electricity prices. Savings figures are estimates based on public average data and the numbers you enter; they aren't quotes, offers or advice from any electricity provider.</p>
<p>Always read a plan's electricity facts label, terms of service and cancellation terms before switching. We aren't responsible for decisions made using this site.</p>
<p>Rate data comes from the U.S. Energy Information Administration and may be revised. Content may change without notice.</p>"""
about="""<p>kWhCompare helps U.S. households answer a simple question: am I paying too much for electricity?</p>
<p>We turn public data from the U.S. Energy Information Administration into plain-language rate comparisons for every state, and our free bill analyzer shows how your all-in rate compares with your state's average.</p>
<p>We're independent. We don't sell electricity, and the estimates on this site aren't offers from any provider. Some plan links may be affiliate links, which help keep the site free.</p>
<h2>Editorial standards</h2><p>Every figure on this site comes from a public, official source: the U.S. Energy Information Administration for state rates and bills, and the Public Utility Commission of Texas for Texas delivery charges and customer rules. Guides are written and reviewed by the kWhCompare editorial team, dated, and updated when the underlying data changes. Advertisers and partners have no say over what we publish or how plans are ranked.</p>
<p>Found an error? Tell us at <strong>hello@kwhcompare.com</strong> and we'll correct it. Read more about <a href="/methodology/">our data and methodology</a>.</p>"""
contact="""<p>Questions, corrections or partnership inquiries: <strong>hello@kwhcompare.com</strong></p><p>We read every message and usually reply within two business days.</p>"""
METH="""<p>Last updated September 29, 2026.</p>
<h2>State electricity rates</h2><p>State averages are residential revenue divided by residential kWh sold, from U.S. Energy Information Administration data for mid-2026. They include generation, delivery, fees and taxes. Average bills are the typical monthly residential bill in each state. National rank orders all 50 states plus Washington, D.C., from cheapest to most expensive.</p>
<h2>Bill analyzer</h2><p>Your all-in rate is your total bill divided by kWh used. We compare it with your state average. In deregulated states, savings estimates assume the supply portion is roughly 55–60% of an all-in bill and that competitive fixed-rate plans typically undercut default supply prices by 10–20%. In regulated states we estimate savings from time-of-use rates, community solar and efficiency. All results are estimates, not offers.</p>
<h2>Texas delivery charges and plan calculator</h2><p>Texas delivery (TDU) charges come from the Public Utility Commission of Texas residential rate summary and are updated after the scheduled March 1 and September 1 changes. The plan calculator adds the energy charge, base fee and delivery charges, subtracts any bill credit you enter, and divides by usage, the same way an Electricity Facts Label calculates average prices.</p>
<h2>ESI ID decoder</h2><p>The decoder matches the first seven digits of an ESI ID to the published prefixes of Texas transmission and distribution utilities. It runs in your browser; we don't store what you enter.</p>
<h2>Guides</h2><p>Guides are based on official sources listed at the end of each article, including the EIA, the U.S. Department of Energy and PUCT rules. Worked examples show every assumption so you can repeat the math with your own numbers.</p>"""
for p,t,d,b in [("/methodology/","Methodology and data sources","How kWhCompare calculates electricity rates, savings estimates and Texas plan costs.",METH),("/privacy/","Privacy policy","How kWhCompare handles your data, cookies and advertising.",priv),
                ("/terms/","Terms of use","Terms of use for kWhCompare.",terms),
                ("/about/","About kWhCompare","Who we are and where our electricity rate data comes from.",about),
                ("/contact/","Contact","Contact kWhCompare.",contact)]:
    write(p,simple(p,t,d,b)); paths.append(p)

exec(open('tx.py').read())
open('site/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+
  "\n".join(f'  <url><loc>{SITE}{p}</loc><lastmod>{ISO}</lastmod></url>' for p in paths)+'\n</urlset>\n')
open('site/robots.txt','w').write(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n")
open('site/ads.txt','w').write(f"google.com, {AD_CLIENT.replace('ca-','')}, DIRECT, f08c47fec0942fa0\n" if ADS_ON else "# Add your AdSense publisher ID in site.config.json and this file fills itself in.\n")
open('site/404.html','w').write(simple("/404/","Page not found","Page not found.",'<p>That page doesn\'t exist. <a href="/">Compare your electricity rate</a> or <a href="/#rates">browse rates by state</a>.</p>').replace('index, follow','noindex'))
print(len(paths),"pages")

# ================= TEXAS: cities, ESI ID tool, TDU charges =================
from tx import TDU, CLIMATE, CITIES
tx=[s for s in S if s['code']=='TX'][0]
deliv=lambda t,k: t['fixed']+t['kwh']/100*k
TDU_SLUG={"cnp":"centerpoint","oncor":"oncor","aepc":"aep-texas-central","aepn":"aep-texas-north","tnmp":"tnmp"}
txjs='<script src="/assets/tx.js" defer></script>'
city_url=lambda c: f"/electricity-rates/texas/{slug(c)}/"
def tdu_table(hl=None):
    rows=""
    for k,t in sorted(TDU.items(),key=lambda kv:deliv(kv[1],1000)):
        st=' style="background:var(--field)"' if k==hl else ""
        nm="<b>%s</b>"%t["name"] if k==hl else t["name"]
        rows+='<tr%s><td id="%s">%s</td><td class="num">$%.2f</td><td class="num">%.2f¢</td><td class="num">$%.2f</td><td class="num">$%.2f</td><td class="num">$%.2f</td></tr>'%(st,TDU_SLUG[k],nm,t["fixed"],t["kwh"],deliv(t,500),deliv(t,1000),deliv(t,2000))
    return '<div class="scroll"><table><thead><tr><th>Utility (TDU)</th><th class="num">Monthly fixed</th><th class="num">Per kWh</th><th class="num">500 kWh</th><th class="num">1,000 kWh</th><th class="num">2,000 kWh</th></tr></thead><tbody>'+rows+'</tbody></table></div>'

def city_page(city,k,clim):
    t=TDU[k]; path=city_url(city); d1=deliv(t,1000)
    cheapest=min(TDU.values(),key=lambda x:deliv(x,1000)); dear=max(TDU.values(),key=lambda x:deliv(x,1000))
    rank=sorted(TDU,key=lambda x:deliv(TDU[x],1000)).index(k)+1
    peers=[c for c,kk,_ in CITIES if kk==k and c!=city]
    cl_name,cl_txt=CLIMATE[clim]
    share=d1/(tx['rate']/100*1000)*100
    faq=[(f"Who delivers electricity in {city}, Texas?",f"{t['name']} owns the power lines in {city} and delivers your electricity, whichever retail provider you choose. Report outages to {t['short']} at {t['phone']}."),
         (f"Can I choose my electricity provider in {city}?",f"Yes. {city} is in the competitive Texas market, so you pick a retail electric provider while {t['short']} keeps delivering power."),
         (f"How much are delivery charges in {city}?",f"About ${d1:.2f} a month at 1,000 kWh: a ${t['fixed']:.2f} fixed charge plus about {t['kwh']:.2f}¢ per kWh. Every provider passes this through at cost."),
         (f"What's a good electricity rate in {city}?",f"Compare the all-in price per kWh at your real usage, including {t['short']} delivery. The Texas average is {tx['rate']:.2f}¢/kWh all-in, so a fixed plan below that at your usage is a good deal.")]
    ld={"@context":"https://schema.org","@graph":[crumbs([("Home","/"),("Texas","/electricity-rates/texas/"),(city,path)]),
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faq]}]}
    title=f"{city}, TX Electricity Rates & Plans ({UPDATED}) | kWhCompare"
    desc=f"Compare electricity plans in {city}, Texas. {t['short']} delivery costs about ${d1:.0f}/month at 1,000 kWh. Calculate any plan's true all-in price before you switch."
    links=" ".join(f'<li><a href="{city_url(c)}">{c}</a></li>' for c in peers) or "<li>—</li>"
    return path, head(title,desc,path,ld)+f'''
<body>
{header}
<main>
<div class="wrap crumbs"><a href="/">Home</a> / <a href="/electricity-rates/texas/">Texas</a> / {city}</div>
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>Electricity rates in {city}, Texas</h1>
      <p class="lede">{city} is in the competitive Texas market: you choose your provider, and {t['short']} delivers the power. Use the calculator to see what any plan really costs at your usage.</p>
      <dl class="facts">
        <div><dt>Utility</dt><dd>{t['short']}</dd></div>
        <div><dt>Delivery, 1,000 kWh</dt><dd>${d1:.2f}</dd></div>
        <div><dt>Texas average</dt><dd>{tx['rate']:.2f}¢</dd></div>
      </dl>
      {D.figure("texas","hero-photo")}
    </div>
    <div class="tool" id="tc" data-tdu="{k}">
      <div class="panel">
        <p style="margin:0 0 1rem;font-weight:700">What will a plan really cost in {city}?</p>
        <div class="grid2">
          <div class="field"><label for="tc-kwh">Your monthly usage <span class="hint">(kWh)</span></label><input id="tc-kwh" type="number" inputmode="numeric" value="1000" min="1"></div>
          <div class="field"><label for="tc-energy">Plan energy charge <span class="hint">(¢/kWh)</span></label><input id="tc-energy" type="number" inputmode="decimal" value="9.5" step="0.1" min="0"></div>
          <div class="field"><label for="tc-base">Provider base fee <span class="hint">($/mo)</span></label><input id="tc-base" type="number" inputmode="decimal" value="0" step="0.01" min="0"></div>
          <div class="field"><label for="tc-credit">Bill credit <span class="hint">($, if any)</span></label><input id="tc-credit" type="number" inputmode="decimal" value="0" step="1" min="0"></div>
        </div>
        <div class="field"><label for="tc-credit-min">Credit applies at or above <span class="hint">(kWh)</span></label><input id="tc-credit-min" type="number" inputmode="numeric" value="1000" min="0"></div>
        <p class="hint" style="margin:0">Find the energy charge, base fee and bill credit on the plan's Electricity Facts Label (EFL).</p>
      </div>
      <div id="tc-out" style="border-top:1px solid var(--line);padding:1.25rem" aria-live="polite"></div>
    </div>
  </div>
</section>
<section class="content">
  <div class="wrap two-col">
    <div class="prose">
      <h2>Delivery charges in {city}</h2>
      <p>{t['name']} serves {t['area']}. Its delivery charge is about <strong>${t['fixed']:.2f} a month plus {t['kwh']:.2f}¢ per kWh</strong>, roughly <strong>${d1:.2f} at 1,000 kWh</strong>. That's about {share:.0f}% of a bill at the Texas average rate, and it's identical whichever provider you pick.</p>
      <p>Of Texas's five main delivery utilities, {t['short']} is the {["cheapest","second cheapest","middle","second most expensive","most expensive"][rank-1]} at 1,000 kWh. {"A home in "+city+" pays about $"+f"{d1-cheapest['fixed']-cheapest['kwh']*10:.2f}"+" more a month in delivery than the same home in the CenterPoint area." if t is not cheapest else "That gives "+city+" households a head start: the same plan costs less here than in Oncor or TNMP territory."}</p>
      <p>Providers can't mark delivery up, and it changes on March 1 and September 1 each year when the Public Utility Commission of Texas approves new rates.</p>
    </div>
    <div class="prose">
      <h2>Energy use in {cl_name}</h2>
      <p>{cl_txt}</p>
      <h2>Power outages in {city}</h2>
      <p>Your provider doesn't fix outages; {t['short']} does. Report outages to {t['short']} at <strong>{t['phone']}</strong>, whichever company sends your bill.</p>
    </div>
  </div>
</section>
{ad(1)}
<section class="content">
  <div class="wrap">
    <h2>How {city} delivery compares with the rest of Texas</h2>
    {tdu_table(k)}
    <p class="disclaimer">Approximate residential delivery charges from the Public Utility Commission of Texas rate summary, late summer 2026. Always check the current figures on a plan's EFL.</p>
  </div>
</section>
<section class="content">
  <div class="wrap two-col">
    <div class="prose">
      <h2>How to choose a plan in {city}</h2>
      <p><strong>Compare at your real usage.</strong> Plans are advertised at 1,000 kWh, but if your summer bills show 2,000 kWh, that's the price that matters.</p>
      <p><strong>Be careful with bill credits.</strong> A plan that's cheap at exactly 1,000 kWh can be expensive at 999 kWh or 1,500 kWh. Use the calculator above to check.</p>
      <p><strong>Prefer fixed rates.</strong> Variable plans can jump during heat waves and freezes. Check the contract length and early termination fee too.</p>
      <p><strong>Mark your contract end date.</strong> When a fixed plan ends, most providers move you to a pricier month-to-month rate.</p>
    </div>
    <div class="prose">
      <h2>Find your ESI ID</h2>
      <p>Your ESI ID identifies your meter. In {t['short']} territory it's {t['digits']} digits and starts with <strong>{" or ".join(t['prefix'])}</strong>. It's printed on your bill near your service address.</p>
      <p><a href="/esi-id-lookup/">Decode your ESI ID</a> or <a href="/#compare">check your current bill</a> against the Texas average.</p>
    </div>
  </div>
</section>
{ad(2)}
<section class="content">
  <div class="wrap">
    <h2>{city} electricity FAQ</h2>
    {''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in faq)}
  </div>
</section>
<section class="content">
  <div class="wrap">
    <h2>Other {t['short']} cities</h2>
    <ul class="state-links">{links}</ul>
    <p class="disclaimer"><a href="/electricity-rates/texas/">All Texas cities and rates</a></p>
  </div>
</section>
</main>
{footer}
{txjs}
</body>
</html>'''

for c,k,cl in CITIES:
    p,h=city_page(c,k,cl); write(p,h); paths.append(p)

# ESI ID lookup page
esi_path="/esi-id-lookup/"
esi_faq=[("What is an ESI ID?","An Electric Service Identifier is the unique number for your electric meter in the competitive Texas market. Providers need it to switch you or start service."),
 ("How many digits is an ESI ID?","17 digits for Oncor, AEP Texas and TNMP, and 22 digits for CenterPoint Energy."),
 ("Where can I find my ESI ID?","On your electric bill near the service address, in your provider's online account, or by asking your provider or utility with your service address."),
 ("Does my ESI ID change if I switch providers?","No. The ESI ID belongs to the meter at your address, so it stays the same whichever provider you choose.")]
ld={"@context":"https://schema.org","@graph":[crumbs([("Home","/"),("ESI ID lookup",esi_path)]),
  {"@type":"WebApplication","name":"Texas ESI ID Decoder","url":SITE+esi_path,"applicationCategory":"UtilitiesApplication","operatingSystem":"Any","offers":{"@type":"Offer","price":"0","priceCurrency":"USD"}},
  {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in esi_faq]}]}
opts="".join(f'<option value="{k}|{city_url(c)}">{c}</option>' for c,k,_ in sorted(CITIES))
prefix_rows="".join(f'<tr><td>{t["name"]}</td><td>{" or ".join(t["prefix"])}</td><td class="num">{t["digits"]}</td><td>{t["phone"]}</td></tr>' for t in TDU.values())
esi=head("Texas ESI ID Lookup: Find & Decode Your ESI ID (2026) | kWhCompare",
 "Decode any Texas ESI ID instantly: see your utility (Oncor, CenterPoint, AEP, TNMP), delivery charges and outage number. Learn where to find your ESI ID.",esi_path,ld)+f'''
<body>
{header}
<main>
<div class="wrap crumbs"><a href="/">Home</a> / ESI ID lookup</div>
<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>Texas ESI ID lookup</h1>
      <p class="lede">Type your ESI ID to see which utility serves your home, what it charges for delivery and who to call in an outage.</p>
      <p class="hint">We decode the number in your browser and don't store it.</p>
      {D.figure("meter","hero-photo")}
    </div>
    <div class="tool">
      <div class="panel">
        <div class="field"><label for="esi-in">Your ESI ID <span class="hint">(17 or 22 digits)</span></label>
        <input id="esi-in" type="text" inputmode="numeric" autocomplete="off" placeholder="e.g. 10443720000000000"></div>
        <div id="esi-out" aria-live="polite"></div>
        <p class="or">Don't have it handy?</p>
        <div class="field"><label for="city-in">Find your utility by city</label>
        <select id="city-in"><option value="">Choose your city</option>{opts}</select></div>
        <div id="city-out" aria-live="polite"></div>
      </div>
    </div>
  </div>
</section>
<section class="content">
  <div class="wrap two-col">
    <div class="prose">
      <h2>Where to find your ESI ID</h2>
      <p><strong>On your electric bill.</strong> Look near your service address for "ESI ID," "ESID" or "Electric Service Identifier."</p>
      <p><strong>In your provider's app or website.</strong> Most providers list it in account details or on each bill PDF.</p>
      <p><strong>From your provider or utility.</strong> Moving into a new home? Any retail provider can find the ESI ID from your service address when you sign up.</p>
      <p>Outside the competitive market, in cities like Austin, San Antonio, El Paso and most co-op areas, there's no ESI ID to shop with: your city utility or co-op is your only provider.</p>
    </div>
    <div class="prose">
      <h2>How to read an ESI ID</h2>
      <p>The first seven digits identify the utility that owns your meter. The rest identify the meter itself. That's why providers ask for it: it tells them which delivery charges apply to your address.</p>
      <p>Your ESI ID never changes when you switch providers. It belongs to the meter, not to you.</p>
    </div>
  </div>
</section>
{ad(1)}
<section class="content">
  <div class="wrap">
    <h2>ESI ID prefixes by utility</h2>
    <div class="scroll"><table><thead><tr><th>Utility</th><th>Starts with</th><th class="num">Digits</th><th>Outages</th></tr></thead><tbody>{prefix_rows}</tbody></table></div>
  </div>
</section>
<section class="content">
  <div class="wrap">
    <h2>ESI ID FAQ</h2>
    {''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in esi_faq)}
  </div>
</section>
{ad(2)}
</main>
{footer}
{txjs}
</body>
</html>'''
write(esi_path,esi); paths.append(esi_path)

# TDU delivery charges page
tdu_path="/texas/tdu-delivery-charges/"
cities_by={k:[c for c,kk,_ in CITIES if kk==k] for k in TDU}
tdu_sections=""
for k,t in TDU.items():
    cl=", ".join('<a href="%s">%s</a>'%(city_url(c),c) for c in cities_by[k])
    tdu_sections+='<div class="prose" style="margin-bottom:1.5rem"><h3 style="margin:0 0 .3rem">%s</h3><p style="margin:0">Serves %s. Outages: %s. Cities: %s.</p></div>'%(t["name"],t["area"],t["phone"],cl)
tfaq=[("What are TDU delivery charges?","Fees your local transmission and distribution utility charges to deliver power to your home. They're set by the Public Utility Commission of Texas and are the same with every provider."),
      ("When do Texas delivery charges change?","Scheduled updates happen on March 1 and September 1 each year, and utilities can also change rates after a rate case."),
      ("Which Texas utility has the lowest delivery charges?",f"At 1,000 kWh, {min(TDU.values(),key=lambda x:deliv(x,1000))['name']} is currently the cheapest and {max(TDU.values(),key=lambda x:deliv(x,1000))['name']} the most expensive.")]
ld={"@context":"https://schema.org","@graph":[crumbs([("Home","/"),("Texas","/electricity-rates/texas/"),("TDU delivery charges",tdu_path)]),
  {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in tfaq]}]}
tdu=head("Texas TDU Delivery Charges (2026): Oncor, CenterPoint, AEP, TNMP | kWhCompare",
 "Current Texas TDU delivery charges compared: fixed monthly fee, per-kWh rate and monthly cost at 500, 1,000 and 2,000 kWh for Oncor, CenterPoint, AEP Texas and TNMP.",tdu_path,ld)+f'''
<body>
{header}
<main>
<div class="wrap crumbs"><a href="/">Home</a> / <a href="/electricity-rates/texas/">Texas</a> / TDU delivery charges</div>
<section class="content" style="border:0">
  <div class="wrap">
    <h1 style="font-size:clamp(2rem,4.5vw,3rem)">Texas TDU delivery charges</h1>
    <div class="prose"><p class="lede" style="max-width:60ch">Every Texas electricity bill includes a delivery charge from the utility that owns the local power lines. It's set by the state, it's the same with every provider, and it depends only on your address.</p></div>
    {tdu_table()}
    <p class="disclaimer">Approximate residential charges from the Public Utility Commission of Texas rate summary, late summer 2026. Lubbock Power & Light also serves part of the competitive market and isn't shown.</p>
  </div>
</section>
{ad(1)}
<section class="content">
  <div class="wrap">
    <h2>Which utility serves your city</h2>
    {tdu_sections}
    <p><a href="/esi-id-lookup/">Not sure? Decode your ESI ID</a></p>
  </div>
</section>
<section class="content">
  <div class="wrap">
    <h2>Delivery charges FAQ</h2>
    {''.join(f'<details><summary>{e(q)}</summary><p>{e(a)}</p></details>' for q,a in tfaq)}
  </div>
</section>
</main>
{footer}
</body>
</html>'''
write(tdu_path,tdu); paths.append(tdu_path)

# Add Texas city hub section to the Texas state page
tp='site/electricity-rates/texas/index.html'; th=open(tp).read()
hub_lists=""
for k in TDU:
    hub_lists+='<h3 style="margin:1.2rem 0 .5rem;font-size:1rem">%s</h3><ul class="state-links">%s</ul>'%(TDU[k]["name"],"".join('<li><a href="%s">%s</a></li>'%(city_url(c),c) for c in cities_by[k]))
hub=f'''<section class="content" id="texas-cities">
  <div class="wrap">
    <h2>Electricity rates in Texas cities</h2>
    <p class="prose">Delivery charges depend on which utility serves your city. Pick your city to calculate a plan's true cost, or <a href="/esi-id-lookup/">decode your ESI ID</a> and <a href="/texas/tdu-delivery-charges/">compare delivery charges</a>.</p>
    {hub_lists}
  </div>
</section>
'''
th=th.replace('<section class="content">\n  <div class="wrap">\n    <h2>Texas electricity FAQ</h2>',hub+'<section class="content">\n  <div class="wrap">\n    <h2>Texas electricity FAQ</h2>')
open(tp,'w').write(th)

# Home: link Texas tools
hp='site/index.html'; hh=open(hp).read()
hh=hh.replace('<section class="content" id="how">','''<section class="content" id="texas"><div class="wrap two-col"><div class="prose"><h2>Shopping for power in Texas?</h2><p>Most Texans pick their own provider. Find your city to see your delivery charges and calculate a plan's true all-in price, or decode your ESI ID to see which utility serves you.</p></div><div><ul class="state-links"><li><a href="/esi-id-lookup/">ESI ID lookup</a></li><li><a href="/texas/tdu-delivery-charges/">TDU delivery charges</a></li><li><a href="/electricity-rates/texas/houston/">Houston</a></li><li><a href="/electricity-rates/texas/dallas/">Dallas</a></li><li><a href="/electricity-rates/texas/fort-worth/">Fort Worth</a></li><li><a href="/electricity-rates/texas/corpus-christi/">Corpus Christi</a></li><li><a href="/electricity-rates/texas/#texas-cities">All Texas cities</a></li></ul></div></div></section>
<section class="content" id="how">''',1)
open(hp,'w').write(hh)

open('site/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+
  "\n".join(f'  <url><loc>{SITE}{p}</loc><lastmod>{ISO}</lastmod></url>' for p in paths)+'\n</urlset>\n')
print("total pages:",len(paths))

# ================= BLOG =================
from blog2 import ARTICLES
for f in sorted(glob.glob('content/articles/*.json')):
    a=json.load(open(f))
    a['faq']=[tuple(x) for x in a['faq']]; a['tool']=tuple(a['tool'])
    a.setdefault('script',''); a.setdefault('sources',[])
    if not any(x['slug']==a['slug'] for x in ARTICLES): ARTICLES.append(a)
ARTICLES=sorted(ARTICLES,key=lambda a:a['date'],reverse=True)
def st_table(rows):
    return '<div class="scroll"><table><thead><tr><th>State</th><th class="num">¢/kWh</th><th class="num">Avg bill</th></tr></thead><tbody>'+"".join(
        '<tr><td><a href="/electricity-rates/%s/">%s</a></td><td class="num">%.2f</td><td class="num">$%d</td></tr>'%(slug(s['name']),s['name'],s['rate'],s['bill']) for s in rows)+'</tbody></table></div>'
tables='<div class="two-col"><div><h3>5 cheapest</h3>'+st_table(ranked[:5])+'</div><div><h3>5 most expensive</h3>'+st_table(ranked[::-1][:5])+'</div></div>'
MONTHS=["January","February","March","April","May","June","July","August","September","October","November","December"]
def nice(d): y,m,dd=d.split('-'); return f"{MONTHS[int(m)-1]} {int(dd)}, {y}"
import re as _re
def words(h): return len(_re.sub(r'<[^>]+>',' ',h).split())
for a in ARTICLES:
    a['body']=a['body'].replace('{STATE_TABLES}',tables)
    a['mins']=max(3,round(words(a['body'])/220))
for a in ARTICLES:
    path=f"/blog/{a['slug']}/"
    ld={"@context":"https://schema.org","@graph":[crumbs([("Home","/"),("Guides","/blog/"),(a['h1'],path)]),
        {"@type":"Article","headline":a['title'],"description":a['desc'],"datePublished":a['date'],"dateModified":a['date'],
         "author":{"@type":"Organization","name":"kWhCompare Editorial Team","url":SITE+"/about/"},
         "publisher":{"@type":"Organization","name":"kWhCompare","url":SITE+"/"},"mainEntityOfPage":SITE+path,"inLanguage":"en-US"},
        {"@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":ans}} for q,ans in a['faq']]}]}
    # split body after the first h2 section to place a mid-article ad
    parts=a['body'].split('<h2>'); mid=len(parts)//2+1
    body='<h2>'.join(parts[:mid])+ad(2,"in_article",False)+'<h2>'+'<h2>'.join(parts[mid:]) if len(parts)>4 else a['body']
    others=[o for o in ARTICLES if o is not a]
    tname,tdesc,turl=a['tool']
    html_=head(a['title']+" | kWhCompare",a['desc'],path,ld,'<meta property="article:published_time" content="%s">\n'%a['date']).replace('<meta property="og:type" content="website">','<meta property="og:type" content="article">')+f'''
<body>
{header}
<main>
<div class="wrap crumbs"><a href="/">Home</a> / <a href="/blog/">Guides</a> / {e(a['h1'])}</div>
<div class="wrap article-layout">
<article class="content prose" style="border:0">
    <span class="kicker">{D.art_meta(a)[0]}</span>
    <h1 style="font-size:clamp(2rem,4.8vw,3.1rem)">{e(a['h1'][0].upper()+a['h1'][1:])}</h1>
    <p class="hint" style="margin:0 0 1.2rem">By the kWhCompare Editorial Team · Updated {nice(a['date'])} · {a['mins']} min read</p>
    <p class="lede" style="max-width:62ch">{a['lede']}</p>
    {D.figure(D.art_meta(a)[1],"article-photo",True)}
    {ad(1,"in_article",False)}
    {body}
    <div class="bill-anatomy" style="margin:2rem 0;display:flex;flex-wrap:wrap;gap:1rem;align-items:center;justify-content:space-between">
      <div><strong>{tname}</strong><br><span class="hint">{tdesc}</span></div>
      <a class="btn meter" style="width:auto;text-decoration:none" href="{turl}">{tname} →</a>
    </div>
    <h2>Frequently asked questions</h2>
    {''.join(f'<details><summary>{e(q)}</summary><p>{e(ans)}</p></details>' for q,ans in a['faq'])}
    <h2 style="font-size:1.2rem;margin-top:2rem">Sources</h2>
    <ul class="hint">{''.join(f'<li>{e(s)}</li>' for s in a['sources'])}</ul>
    <p class="hint">Figures are checked against these sources when each guide is updated. See <a href="/methodology/">how we research and calculate</a>. This guide is for general information and isn't financial advice.</p>
    {ad(3,"display",False)}
</article>
<aside class="sidebar" aria-label="Related tools">
  <div class="sidebar-sticky">
    <div class="side-card"><span class="kicker">Free tool</span><strong>Are you overpaying?</strong><p>Compare your rate with your state's average in 30 seconds.</p><a class="btn meter" href="/#compare">Check my bill</a></div>
    <div class="side-card side-links"><strong>Popular tools</strong><ul><li><a href="/#rates">Rates by state</a></li><li><a href="/electricity-rates/texas/#texas-cities">Texas plan calculator</a></li><li><a href="/esi-id-lookup/">ESI ID lookup</a></li><li><a href="/texas/tdu-delivery-charges/">TDU delivery charges</a></li></ul></div>
    {ad(4,"sidebar",False)}
  </div>
</aside>
</div>
<section class="content">
  <div class="wrap">
    <h2>More guides</h2>
    <ul class="state-links">{"".join(f'<li><a href="/blog/{o["slug"]}/">{e(o["h1"][0].upper()+o["h1"][1:])}</a></li>' for o in others)}</ul>
  </div>
</section>
</main>
{footer}
{a['script']}
</body>
</html>'''
    write(path,html_); paths.append(path)

# Blog index
bp="/blog/"
ld={"@context":"https://schema.org","@graph":[crumbs([("Home","/"),("Guides",bp)]),
    {"@type":"CollectionPage","name":"Electricity guides","url":SITE+bp,
     "hasPart":[{"@type":"Article","headline":a['title'],"url":f"{SITE}/blog/{a['slug']}/"} for a in ARTICLES]}]}
cards="".join(D.guide_card(a,i<2) for i,a in enumerate(ARTICLES))
blog_idx=head("Electricity Guides: Bills, Rates & Switching Plans | kWhCompare",
 "Plain-English guides to lowering your electric bill: why bills rise, how to read an EFL, fixed vs variable rates and when to switch providers.",bp,ld)+f'''
<body>
{header}
<main>
<div class="wrap crumbs"><a href="/">Home</a> / Guides</div>
<section class="content" style="border:0">
  <div class="wrap">
    <h1 style="font-size:clamp(2rem,4.8vw,3.1rem)">Electricity guides</h1>
    <p class="lede">Plain-English answers to the questions behind every electric bill.</p>
    <div class="gcard-grid">{cards}</div>
  </div>
</section>
{ad(1)}
</main>
{footer}
</body>
</html>'''
write(bp,blog_idx); paths.append(bp)

# Home: guides section
hh=open('site/index.html').read()
glist="".join(f'<li><a href="/blog/{a["slug"]}/">{e(a["h1"][0].upper()+a["h1"][1:])}</a></li>' for a in ARTICLES)
hh=hh.replace('<section class="content" id="faq">',f'<section class="content" id="guides"><div class="wrap"><h2>Guides</h2><ul class="state-links">{glist}</ul></div></section>\n<section class="content" id="faq">',1)
open('site/index.html','w').write(hh)

open('site/sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+
  "\n".join(f'  <url><loc>{SITE}{p}</loc><lastmod>{ISO}</lastmod></url>' for p in paths)+'\n</urlset>\n')
print("with blog:",len(paths))

# ================= HOME v2 =================
def sec(id_):
    m=re.search(r'<section class="content" id="%s">.*?</section>'%id_,src,flags=re.S); return m.group(0) if m else ""
h_head=src.split('<body>')[0]
h_head=re.sub(r'<style>.*?</style>',css_link,h_head,flags=re.S)
h_head=re.sub(r'<!-- Google AdSense:.*?-->\s*','',h_head,flags=re.S).replace('</head>',ADS+'\n</head>',1)
h_head=h_head.replace('https://kwhcompare.netlify.app',SITE).replace('https://www.kwhcompare.com',SITE)
if 'rel="icon"' not in h_head:
    h_head=h_head.replace('<meta name="theme-color" content="#14302b">','<meta name="theme-color" content="#14302b">\n<link rel="icon" href="data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' viewBox=\'0 0 100 100\'><text y=\'.9em\' font-size=\'90\'>⚡</text></svg>">')
TOOLS=[("calc","Electric bill analyzer","Is your rate above your state's average? Find out in 30 seconds.","/#compare"),
 ("map","Electricity rates by state","Average price, bill and 12-month change for all 50 states.","/#rates"),
 ("receipt","Texas plan cost calculator","The real price of any plan at your usage, including delivery.","/electricity-rates/texas/#texas-cities"),
 ("meter","ESI ID lookup","Decode your Texas ESI ID: utility, delivery charges, outage line.","/esi-id-lookup/"),
 ("tower","TDU delivery charges","What Oncor, CenterPoint, AEP and TNMP charge to deliver power.","/texas/tdu-delivery-charges/"),
 ("car","EV charging cost calculator","What charging at home costs versus gas, by state.","/blog/cost-to-charge-electric-car-at-home/")]
tool_cards="".join(f'<a class="tcard" href="{u}"><span class="tcard-ico">{D.icon(i)}</span><span><strong>{t}</strong><span>{d}</span></span></a>' for i,t,d,u in TOOLS)
risers=sorted(S,key=lambda s:-s['yoy'])[:6]; mx=risers[0]['yoy']
bars="".join(f'''<a href="/electricity-rates/{slug(s['name'])}/"><text x="0" y="{i*40+24}" class="bl">{s['name']}</text>
<rect x="150" y="{i*40+9}" width="{s['yoy']/mx*330:.0f}" height="20" rx="4" class="bar-r"/>
<text x="{150+s['yoy']/mx*330+8:.0f}" y="{i*40+24}" class="bv">+{s['yoy']:.1f}%</text></a>''' for i,s in enumerate(risers))
chart=f'<svg viewBox="0 0 540 {len(risers)*40}" class="chart" role="img" aria-label="States with the biggest 12-month electricity price increases: '+", ".join(f"{s['name']} {s['yoy']:.1f}%" for s in risers)+f'">{bars}</svg>'
tx_links="".join(f'<li><a href="{u}">{t}</a></li>' for t,u in [("Houston","/electricity-rates/texas/houston/"),("Dallas","/electricity-rates/texas/dallas/"),("Fort Worth","/electricity-rates/texas/fort-worth/"),("Corpus Christi","/electricity-rates/texas/corpus-christi/"),("Midland","/electricity-rates/texas/midland/"),("All 37 cities","/electricity-rates/texas/#texas-cities")])
TRUST=[("doc","Official sources","Every rate comes from the U.S. EIA or the Public Utility Commission of Texas, with the date shown."),
 ("calc","Math in the open","Our methodology page shows exactly how every estimate is calculated."),
 ("lock","Nothing stored","The numbers you type are calculated on your device and never sent to us."),
 ("scale","No paid rankings","Providers and advertisers can't change our results or what we write.")]
trust="".join(f'<div class="trust-item"><span class="tcard-ico">{D.icon(i)}</span><h3>{t}</h3><p>{d}</p></div>' for i,t,d in TRUST)
guides="".join(D.guide_card(a) for a in ALL_ARTS[:6])
home2=h_head+f'''<body>
{header}
<main id="top">
<section class="hero-band"{D.hero_bg()}>
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <span class="kicker light">Free electric bill analyzer</span>
      <h1>Are you overpaying for electricity?</h1>
      <p class="lede">Type in two numbers from your bill. We compare your rate with your state's average and show cheaper ways to pay for the same power.</p>
      <ul class="checks">
        <li><strong>Official data.</strong> Rates from the U.S. EIA and the Texas PUC.</li>
        <li><strong>Private by design.</strong> Your numbers never leave your browser.</li>
        <li><strong>Independent.</strong> No provider pays for placement.</li>
      </ul>
      <dl class="facts">
        <div><dt>U.S. average</dt><dd>{US:.2f}¢/kWh</dd></div>
        <div><dt>Cheapest state</dt><dd>{ranked[0]['name']} {ranked[0]['rate']:.1f}¢</dd></div>
        <div><dt>Priciest state</dt><dd>{ranked[-1]['name']} {ranked[-1]['rate']:.1f}¢</dd></div>
      </dl>
    </div>
    {tool}
  </div>
</section>
<section class="content" id="tools">
  <div class="wrap">
    <h2>Free electricity tools</h2>
    <p class="sub">No sign-up, no email, no sales calls.</p>
    <div class="tcard-grid">{tool_cards}</div>
  </div>
</section>
{ad(1)}
<section class="content data-band">
  <div class="wrap data-grid">
    <div>
      <span class="kicker">Latest data · {UPDATED}</span>
      <p class="big-stat">{US:.2f}¢</p>
      <h2>Electricity prices keep climbing</h2>
      <p>The average U.S. home now pays {US:.2f}¢ per kWh, about 5% more than a year ago. In {risers[0]['name']} prices rose {risers[0]['yoy']:.0f}%. <a href="/blog/what-is-a-good-price-per-kwh/">Is your rate a good price?</a></p>
    </div>
    <figure class="chart-fig">{chart}<figcaption>States with the biggest 12-month increases in residential electricity prices. Source: U.S. Energy Information Administration.</figcaption></figure>
  </div>
</section>
<section class="content" id="guides">
  <div class="wrap">
    <div class="sec-head"><h2>Guides</h2><a href="/blog/">All guides →</a></div>
    <div class="gcard-grid">{guides}</div>
  </div>
</section>
<section class="content" id="texas">
  <div class="wrap feature">
    {D.figure("texas","feature-photo")}
    <div class="prose">
      <span class="kicker">Texas</span>
      <h2>Shopping for power in Texas?</h2>
      <p>Most Texans choose their own provider, and the cheapest-looking plan often isn't. Pick your city to see your delivery charges and the true all-in price of any plan at your real usage.</p>
      <ul class="state-links">{tx_links}</ul>
    </div>
  </div>
</section>
{ad(2)}
{sec("rates")}
<section class="content" id="trust">
  <div class="wrap">
    <h2>Why you can trust these numbers</h2>
    <div class="trust-grid">{trust}</div>
  </div>
</section>
{sec("choice")}
{sec("read-bill")}
{ad(3)}
{sec("faq")}
</main>
{footer}
<script src="/assets/app.js" defer></script>
</body>
</html>'''
write("/",home2)
print("home v2 written")
