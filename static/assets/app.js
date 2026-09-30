const STATES = [
 ["AL","Alabama",16.40,182,2.1],["AK","Alaska",28.21,160,5.0],["AZ","Arizona",15.18,151,-0.3],["AR","Arkansas",14.12,150,5.6],
 ["CA","California",34.74,190,3.4],["CO","Colorado",17.13,121,6.8],["CT","Connecticut",24.32,170,-10.6],["DE","Delaware",19.29,171,6.2],
 ["DC","District of Columbia",24.39,168,7.4],["FL","Florida",15.10,165,-1.6],["GA","Georgia",16.36,171,2.5],["HI","Hawaii",52.72,268,28.7],
 ["ID","Idaho",14.37,136,19.1],["IL","Illinois",19.89,138,8.7],["IN","Indiana",17.51,162,6.3],["IA","Iowa",15.93,149,3.9],
 ["KS","Kansas",15.71,148,4.5],["KY","Kentucky",14.26,152,6.4],["LA","Louisiana",13.49,157,5.9],["ME","Maine",29.59,169,5.2],
 ["MD","Maryland",21.84,168,13.2],["MA","Massachusetts",29.61,172,-2.4],["MI","Michigan",22.99,160,10.4],["MN","Minnesota",17.52,140,2.3],
 ["MS","Mississippi",14.88,167,5.8],["MO","Missouri",16.22,172,1.9],["MT","Montana",15.14,126,2.2],["NE","Nebraska",13.25,131,0.8],
 ["NV","Nevada",13.11,120,6.9],["NH","New Hampshire",27.01,172,14.9],["NJ","New Jersey",24.95,167,0.3],["NM","New Mexico",15.06,108,2.6],
 ["NY","New York",29.49,174,11.1],["NC","North Carolina",14.74,145,10.2],["ND","North Dakota",14.12,150,3.0],["OH","Ohio",19.19,159,9.7],
 ["OK","Oklahoma",14.33,144,5.1],["OR","Oregon",16.32,128,3.3],["PA","Pennsylvania",21.73,165,10.4],["RI","Rhode Island",29.23,167,8.9],
 ["SC","South Carolina",15.55,167,5.1],["SD","South Dakota",15.36,149,8.0],["TN","Tennessee",14.07,158,1.8],["TX","Texas",15.94,173,4.5],
 ["UT","Utah",13.37,96,2.1],["VT","Vermont",24.44,136,6.3],["VA","Virginia",17.22,162,13.1],["WA","Washington",14.91,132,15.0],
 ["WV","West Virginia",15.45,148,-2.3],["WI","Wisconsin",19.56,143,5.6],["WY","Wyoming",15.24,128,2.4]
].map(([code,name,rate,bill,yoy]) => ({code,name,rate,bill,yoy}));
const US_AVG = 18.34;
const CHOICE = new Set(["TX","PA","OH","IL","NY","NJ","MD","MA","CT","DE","ME","NH","RI","DC"]);
const LIMITED = new Set(["MI","VA","CA","OR","NV"]);
const COMMUNITY_SOLAR = new Set(["NY","NJ","MA","MD","IL","MN","CO","ME","NM","VA","DE","CT","RI","OR","CA","HI","WA","DC"]);
const ESI_PREFIX = [
  ["1008901","CenterPoint Energy (Houston area)"],
  ["1044372","Oncor (Dallas–Fort Worth area)"],
  ["1017699","Oncor (East Texas)"],
  ["1003278","AEP Texas Central"],
  ["1020404","AEP Texas North"],
  ["1040051","Texas-New Mexico Power (TNMP)"]
];
const TDU_CODE = {"CenterPoint Energy (Houston area)":"CNP","Oncor (Dallas–Fort Worth area)":"ONC","AEP Texas Central":"AEPC","AEP Texas North":"AEPN","Texas-New Mexico Power (TNMP)":"TNMP","Lubbock Power & Light":"LPL"};
// Approximate residential delivery charges (PUCT rate summary, Aug 2026): fixed $/month + cents/kWh
const TDU = {
  CNP:{name:"CenterPoint Energy", fixed:4.99, kwh:4.97},
  ONC:{name:"Oncor", fixed:4.23, kwh:6.01},
  AEPC:{name:"AEP Texas Central", fixed:3.24, kwh:5.69},
  AEPN:{name:"AEP Texas North", fixed:3.24, kwh:5.53},
  TNMP:{name:"TNMP", fixed:7.85, kwh:6.47}
};
const ENERGY_TYPICAL = 6.8, ENERGY_LOW = 5.0; // cents/kWh, 12-month fixed plans without bill credits, Sept 2026
let currentTdu = document.body.dataset.tdu || null;
const slug = n => n.toLowerCase().replace(/[^a-z]+/g,"-");
const $ = id => document.getElementById(id);
const byCode = Object.fromEntries(STATES.map(s => [s.code, s]));
const fmt$ = n => "$" + n.toLocaleString("en-US", {minimumFractionDigits: 2, maximumFractionDigits: 2});
const fmtC = n => n.toFixed(1) + "¢";

/* ---------- State select + remembered inputs ---------- */
const sel = $("state");
sel.innerHTML = '<option value="">Select your state</option>' + STATES.map(s => `<option value="${s.code}">${s.name}</option>`).join("");
try {
  const saved = JSON.parse(localStorage.getItem("kwhc-last") || "null");
  if (saved && !document.body.dataset.state) { sel.value = saved.state || ""; $("kwh").value = saved.kwh || ""; $("total").value = saved.total || ""; }
} catch (e) {}

if (document.body.dataset.state) sel.value = document.body.dataset.state;

/* ---------- Tabs ---------- */
const tabs = [["tab-manual","p-manual"],["tab-bill","p-bill"]];
function showTab(id) {
  tabs.forEach(([t,p]) => { const on = t === id; $(t).setAttribute("aria-selected", on); $(p).hidden = !on; });
}
tabs.forEach(([t]) => $(t).addEventListener("click", () => showTab(t)));

/* ---------- ESI ID detection ---------- */
function detectEsi(raw) {
  const d = (raw || "").replace(/\D/g, "");
  if (!d) return null;
  if (d.length !== 17 && d.length !== 22) return {valid:false, digits:d};
  const hit = ESI_PREFIX.find(([p]) => d.startsWith(p));
  return {valid:true, digits:d, tdu: hit ? hit[1] : null};
}
$("esi").addEventListener("input", e => {
  const r = detectEsi(e.target.value), note = $("esi-note");
  if (!r) { note.textContent = ""; return; }
  if (!r.valid) { note.textContent = r.digits.length > 5 ? "Texas ESI IDs have 17 or 22 digits. Account numbers from other states are fine too." : ""; return; }
  note.textContent = r.tdu ? `Texas ESI ID detected: served by ${r.tdu}.` : "Texas ESI ID detected.";
  if (r.tdu) currentTdu = TDU_CODE[r.tdu] || currentTdu;
  if (!sel.value) sel.value = "TX";
});

/* ---------- Comparison engine ---------- */
function compare({state, kwh, total}) {
  const s = byCode[state];
  const rate = total / kwh * 100; // cents per kWh, all-in
  const diff = (rate - s.rate) / s.rate;
  const opts = [];
  const cost = r => r / 100 * kwh;

  const tdu = state === "TX" && currentTdu && TDU[currentTdu];
  if (tdu) {
    const deliv = tdu.fixed + tdu.kwh / 100 * kwh;
    const allIn = e => (deliv + e / 100 * kwh) / kwh * 100;
    opts.push({t:"Low-cost 12-month fixed plan", d:`Among the cheapest plans without bill credits in ${tdu.name} territory. Includes ${fmt$(deliv)} of regulated delivery charges.`, r:allIn(ENERGY_LOW), cta:"See low-cost fixed plans"});
    opts.push({t:"Typical 12-month fixed plan", d:"A mid-market fixed rate with no usage-based bill credits, so your price stays the same in winter and summer.", r:allIn(ENERGY_TYPICAL), cta:"See 12-month plans"});
    opts.push({t:"24-month fixed plan", d:"Slightly higher rate, but locks your price through two Texas summers.", r:allIn(ENERGY_TYPICAL + 0.5), cta:"See 24-month plans"});
  } else if (CHOICE.has(state)) {
    // Supply is ~55–60% of an all-in bill; competitive fixed plans typically undercut default supply by 10–20%.
    const fixed = Math.min(rate * (1 - 0.58 * 0.15), s.rate * 0.95);
    opts.push({t:"12-month fixed-rate plan", d:"Locks your supply price for a year. Compare cancellation fees before you sign.", r:fixed, cta:"See fixed-rate plans"});
    opts.push({t:"100% renewable fixed plan", d:"Same price protection, backed by renewable energy certificates.", r:fixed * 1.04, cta:"See green plans"});
    opts.push({t:"Free nights / time-of-use plan", d:"Best if you can move about a third of your use (laundry, EV charging) to off-peak hours.", r:fixed * 0.94, cta:"See time-of-use plans"});
  } else {
    opts.push({t:"Your utility's time-of-use rate", d:"Cheaper off-peak pricing. Savings assume you shift about a third of your usage.", r:rate * 0.92, cta:"Check your utility's rate options"});
    if (COMMUNITY_SOLAR.has(state)) opts.push({t:"Community solar subscription", d:"Bill credits from a local solar farm, no panels or upfront cost.", r:rate * 0.9, cta:"Find community solar near you"});
    opts.push({t:"Efficiency upgrades", d:"Smart thermostat, LED lighting and draft sealing typically trim 5–10% of usage.", r:rate * 0.93, cta:"See efficiency tips"});
  }
  opts.forEach(o => { o.cost = cost(o.r); o.save = Math.max(0, total - o.cost); });
  opts.sort((a,b) => a.cost - b.cost);
  return {s, rate, diff, opts};
}

function pinPos(v, lo, hi) { return Math.max(3, Math.min(97, (v - lo) / (hi - lo) * 100)); }

function render(input) {
  const {s, rate, diff, opts} = compare(input);
  const out = $("results");
  const pct = Math.round(Math.abs(diff) * 100);
  let cls = "good", head;
  if (diff > 0.05) { cls = "bad"; head = `You pay ${pct}% more than the ${s.name} average.`; }
  else if (diff < -0.05) head = `You pay ${pct}% less than the ${s.name} average.`;
  else { cls = ""; head = `You pay about the ${s.name} average.`; }
  const best = opts[0];
  const yearly = best.save * 12;
  const lo = Math.min(rate, s.rate, US_AVG) * 0.7, hi = Math.max(rate, s.rate, US_AVG) * 1.25;
  const market = CHOICE.has(s.code) ? `${s.name} lets you choose your supplier, so switching plans is your biggest lever.`
    : LIMITED.has(s.code) ? `${s.name} has limited retail choice, so most savings come from rate options and solar.`
    : `${s.name} is regulated, so you keep your utility but can still change how you pay.`;

  out.innerHTML = `
    <p class="verdict ${cls}">${head}</p>
    <p class="sub">Your all-in rate is <b>${fmtC(rate)}/kWh</b> vs ${fmtC(s.rate)} in ${s.name} and ${fmtC(US_AVG)} nationally. ${market}</p>
    <div class="gauge" role="img" aria-label="Your rate ${fmtC(rate)} compared with state average ${fmtC(s.rate)} and U.S. average ${fmtC(US_AVG)}">
      <div class="gauge-track"></div>
      <div class="pin" style="left:${pinPos(s.rate,lo,hi)}%"><b>${s.code}</b> ${fmtC(s.rate)}</div>
      <div class="pin you" style="left:${pinPos(rate,lo,hi)}%"><b>You ${fmtC(rate)}</b></div>
    </div>
    ${yearly > 5 ? `<p class="sub" style="color:var(--ink)">Best option below could save about <b>${fmt$(yearly)}/year</b>.</p>` : ""}
    <div class="options">
      ${opts.map(o => `
        <div class="opt">
          <h3>${o.t}</h3>
          <p>${o.d}</p>
          <div class="amt"><strong>${fmt$(o.cost)}/mo</strong><span>${o.save > 0.5 ? "save " + fmt$(o.save) : "similar cost"}</span></div>
          <a class="go" href="#" data-partner="${s.code}-${o.t.toLowerCase().replace(/[^a-z]+/g,'-')}">${o.cta}</a>
        </div>`).join("")}
    </div>
    <p class="disclaimer">Estimates based on ${Math.round(input.kwh).toLocaleString()} kWh and ${fmt$(input.total)}. Actual prices depend on your utility zone, plan terms and taxes.</p>`;
  out.hidden = false;
  out.scrollIntoView({behavior: matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth", block: "nearest"});
}

$("run").addEventListener("click", () => {
  const state = sel.value, kwh = parseFloat($("kwh").value), total = parseFloat($("total").value);
  const missing = !state ? sel : !(kwh > 0) ? $("kwh") : !(total > 0) ? $("total") : null;
  if (missing) { missing.focus(); missing.reportValidity?.(); $("results").hidden = false; $("results").innerHTML = `<p class="status err">Add your ${missing === sel ? "state" : missing.id === "kwh" ? "kWh used" : "total bill amount"} to compare.</p>`; return; }
  try { localStorage.setItem("kwhc-last", JSON.stringify({state, kwh, total})); } catch (e) {}
  render({state, kwh, total});
});

/* ---------- Bill reading ---------- */
function parseBillText(txt) {
  const t = txt.replace(/,/g, "");
  const out = {};
  const k = t.match(/(\d{2,5}(?:\.\d+)?)\s*kwh/i) || t.match(/kwh[^\d]{0,30}(\d{2,5}(?:\.\d+)?)/i);
  if (k) out.kwh = parseFloat(k[1]);
  const a = t.match(/(?:total (?:amount )?due|amount due|total due|total charges|balance due|please pay)[^\d$]{0,30}\$?\s*(\d+\.\d{2})/i);
  if (a) out.total = parseFloat(a[1]);
  const esi = t.match(/\b(\d{17}(?:\d{5})?)\b/);
  if (esi) out.esi = esi[1];
  const st = STATES.find(s => new RegExp("\\b" + s.name + "\\b", "i").test(t)) ||
             STATES.find(s => new RegExp(",\\s*" + s.code + "\\s+\\d{5}").test(t));
  if (st) out.state = st.code;
  return out;
}

function applyBill(d, source) {
  const st = $("bill-status");
  if (d.state && byCode[d.state]) sel.value = d.state;
  if (d.kwh) $("kwh").value = d.kwh;
  if (d.total) $("total").value = d.total;
  if (d.esi) { $("esi").value = d.esi; $("esi").dispatchEvent(new Event("input")); }
  const found = [d.kwh && "kWh used", d.total && "amount due", d.state && "state", d.esi && "ESI ID", d.utility && "utility"].filter(Boolean);
  if (d.kwh && d.total && sel.value) {
    st.className = "status"; st.textContent = `Read ${found.join(", ")} from your ${source}${d.utility ? " (" + d.utility + ")" : ""}.`;
    render({state: sel.value, kwh: d.kwh, total: d.total});
  } else {
    st.className = "status err";
    st.textContent = found.length ? `Found ${found.join(", ")}. Add the rest in "Enter my numbers" to finish.` : "Couldn't find kWh or amount due. Enter them in \"Enter my numbers\".";
    if (found.length) setTimeout(() => showTab("tab-manual"), 1400);
  }
}

let photo = null, sample = null;
const drop = $("drop"), fileIn = $("file");
drop.addEventListener("click", () => fileIn.click());
drop.addEventListener("keydown", e => { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); fileIn.click(); } });
["dragover","dragenter"].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.add("over"); }));
["dragleave","drop"].forEach(ev => drop.addEventListener(ev, e => { e.preventDefault(); drop.classList.remove("over"); }));
drop.addEventListener("drop", e => { if (e.dataTransfer.files[0]) setPhoto(e.dataTransfer.files[0]); });
fileIn.addEventListener("change", () => { if (fileIn.files[0]) setPhoto(fileIn.files[0]); });
function setPhoto(f) {
  photo = f;
  drop.querySelector("strong").textContent = f.name;
  drop.querySelector(".hint").textContent = "Ready. Press \"Read my bill\".";
}

// Photo reading needs an AI backend. Inside Claude it uses the viewer's Claude; on your own site, swap in your API endpoint.
(async () => {
  $("photo-area").hidden = true;
  try {
    if (!window.claude?.use) return;
    sample = await window.claude.use("sample");
    if (!sample) return;
    const lim = await sample.limits().catch(() => null);
    if (lim?.images) { fileIn.accept = lim.images.mediaTypes.join(","); $("photo-area").hidden = false; }
  } catch (e) {}
})();

$("read").addEventListener("click", async () => {
  const st = $("bill-status"), btn = $("read");
  const txt = $("billtext").value.trim();
  if (!photo && !txt) { st.className = "status err"; st.textContent = "Add a bill photo or paste the bill text first."; return; }

  if (photo && sample) {
    btn.disabled = true; st.className = "status"; st.textContent = "Reading your bill…";
    try {
      const d = await sample.json(
        `The image is a U.S. residential electric bill. Extract these fields and reply with only one JSON object, no prose:
{"utility": string|null, "state": two-letter US state code|null, "kwh": number|null (energy used this billing period), "total": number|null (total amount due in USD), "supply_rate_cents": number|null, "esi": string|null (Texas ESI ID digits or account number)}
Use null for anything not visible. Numbers without units or commas.`,
        {images: photo, modelTier: "default"});
      applyBill(d || {}, "bill photo");
    } catch (e) {
      st.className = "status err";
      st.textContent = e.code === "not_granted" ? "Photo reading was declined. Paste the bill text instead." :
        e.code === "rate_limited" ? "Too many requests right now. Try again in a minute." :
        e.code === "image_rejected" ? "That image couldn't be read. Try a clearer photo or a screenshot." :
        "Couldn't read the photo. Paste the bill text or enter your numbers.";
    } finally { btn.disabled = false; }
    return;
  }
  applyBill(parseBillText(txt), "bill text");
});

/* ---------- Rate table ---------- */
if (document.getElementById("rate-table")) {
let sortKey = "rate", sortDir = 1;
const maxRate = Math.max(...STATES.map(s => s.rate));
function drawTable() {
  const q = $("filter").value.trim().toLowerCase();
  const rows = STATES.filter(s => !q || s.name.toLowerCase().includes(q) || s.code.toLowerCase() === q)
    .sort((a,b) => (a[sortKey] > b[sortKey] ? 1 : a[sortKey] < b[sortKey] ? -1 : 0) * sortDir);
  document.querySelector("#rate-table tbody").innerHTML = rows.map(s => `
    <tr>
      <td><a href="/electricity-rates/${slug(s.name)}/">${s.name}</a></td>
      <td class="num"><span class="bar" style="width:${Math.round(s.rate / maxRate * 70)}px" aria-hidden="true"></span>${s.rate.toFixed(2)}</td>
      <td class="num">$${s.bill}</td>
      <td class="num">${s.yoy > 0 ? "+" : ""}${s.yoy.toFixed(1)}%</td>
      <td>${CHOICE.has(s.code) ? '<span class="tag choice">Choice</span>' : LIMITED.has(s.code) ? '<span class="tag">Limited</span>' : '<span class="tag">Regulated</span>'}</td>
    </tr>`).join("") || `<tr><td colspan="5">No state matches "${q.replace(/[<>&]/g,"")}".</td></tr>`;
}
document.querySelectorAll("th button").forEach(b => b.addEventListener("click", () => {
  const k = b.dataset.sort; sortDir = sortKey === k ? -sortDir : 1; sortKey = k; drawTable();
}));
$("filter").addEventListener("input", drawTable);
drawTable();
}

/* Partner links: replace href with your affiliate URLs per state/plan type */
document.addEventListener("click", e => { const a = e.target.closest("a.go"); if (a && a.getAttribute("href") === "#") e.preventDefault(); });
