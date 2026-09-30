const TDU = {
 cnp:{name:"CenterPoint Energy",fixed:4.99,kwh:4.972,prefix:["1008901"],digits:22,phone:"1-800-332-7143",slug:"centerpoint"},
 oncor:{name:"Oncor Electric Delivery",fixed:4.23,kwh:6.013,prefix:["1044372","1017699"],digits:17,phone:"1-888-313-4747",slug:"oncor"},
 aepc:{name:"AEP Texas Central",fixed:3.24,kwh:5.690,prefix:["1003278"],digits:17,phone:"1-877-373-4858",slug:"aep-texas-central"},
 aepn:{name:"AEP Texas North",fixed:3.24,kwh:5.531,prefix:["1020404"],digits:17,phone:"1-877-373-4858",slug:"aep-texas-north"},
 tnmp:{name:"Texas-New Mexico Power (TNMP)",fixed:7.85,kwh:6.467,prefix:["1040051"],digits:17,phone:"1-888-866-7456",slug:"tnmp"}
};
const $ = id => document.getElementById(id);
const money = n => "$" + n.toFixed(2);
const delivery = (t, kwh) => t.fixed + t.kwh / 100 * kwh;

/* ---------- True cost calculator (city pages) ---------- */
const tc = $("tc");
if (tc) {
  const t = TDU[tc.dataset.tdu];
  const f = id => parseFloat($(id).value) || 0;
  function planCost(kwh) {
    const energy = f("tc-energy") / 100 * kwh, base = f("tc-base");
    const credit = kwh >= f("tc-credit-min") && f("tc-credit") > 0 ? f("tc-credit") : 0;
    const del = delivery(t, kwh);
    const total = Math.max(0, energy + base + del - credit);
    return {energy, base, del, credit, total, rate: total / kwh * 100};
  }
  function run() {
    const kwh = Math.max(1, f("tc-kwh"));
    const c = planCost(kwh);
    $("tc-out").innerHTML = `
      <p class="verdict">${money(c.total)} a month, ${c.rate.toFixed(1)}¢ per kWh all-in</p>
      <div class="scroll"><table>
        <tr><td>Energy charge (${f("tc-energy").toFixed(1)}¢ × ${kwh.toLocaleString()} kWh)</td><td class="num">${money(c.energy)}</td></tr>
        <tr><td>Provider base fee</td><td class="num">${money(c.base)}</td></tr>
        <tr><td>${t.name} delivery</td><td class="num">${money(c.del)}</td></tr>
        ${c.credit ? `<tr><td>Bill credit</td><td class="num">−${money(c.credit)}</td></tr>` : ""}
        <tr><td><b>Total</b></td><td class="num"><b>${money(c.total)}</b></td></tr>
      </table></div>
      <p class="sub" style="margin-top:1rem">Same plan at other usage levels, as shown on an Electricity Facts Label:</p>
      <div class="statbox" style="grid-template-columns:repeat(3,1fr)">
        ${[500,1000,2000].map(k => `<div><dt>${k.toLocaleString()} kWh</dt><dd>${planCost(k).rate.toFixed(1)}¢</dd></div>`).join("")}
      </div>
      ${(() => { const a = planCost(999).total, b = planCost(1000).total; return f("tc-credit") > 0 && f("tc-credit-min") === 1000 ? `<p class="disclaimer">Watch the threshold: at 999 kWh this plan costs ${money(a)}, at 1,000 kWh ${money(b)}.</p>` : ""; })()}`;
  }
  tc.querySelectorAll("input").forEach(i => i.addEventListener("input", run));
  run();
}

/* ---------- ESI ID decoder ---------- */
const esiIn = $("esi-in");
if (esiIn) {
  const out = $("esi-out");
  function decode() {
    const d = esiIn.value.replace(/\D/g, "");
    if (!d) { out.innerHTML = ""; return; }
    const key = Object.keys(TDU).find(k => TDU[k].prefix.some(p => d.startsWith(p)));
    if (!key) {
      out.innerHTML = d.length < 7 ? `<p class="status">Keep typing: the first 7 digits identify the utility.</p>`
        : `<p class="status err">This doesn't match a Texas utility prefix. Texas ESI IDs start with 10 and are 17 or 22 digits. If you're outside the competitive market (for example Austin, San Antonio or El Paso), your bill uses a different account number.</p>`;
      return;
    }
    const t = TDU[key];
    const lenOk = d.length === t.digits;
    out.innerHTML = `
      <p class="verdict good">${t.name}</p>
      <p class="sub">${lenOk ? `Valid ${t.digits}-digit ESI ID format.` : `${t.name} ESI IDs have ${t.digits} digits; this one has ${d.length}. Check for a missing or extra digit.`}</p>
      <div class="statbox" style="grid-template-columns:repeat(3,1fr)">
        <div><dt>Delivery at 1,000 kWh</dt><dd>${money(delivery(t,1000))}</dd></div>
        <div><dt>Delivery rate</dt><dd>${t.kwh.toFixed(2)}¢/kWh</dd></div>
        <div><dt>Outages</dt><dd style="font-size:1rem">${t.phone}</dd></div>
      </div>
      <p><a href="/texas/tdu-delivery-charges/#${t.slug}">See ${t.name} delivery charges</a></p>`;
  }
  esiIn.addEventListener("input", decode);
  const cs = $("city-in");
  if (cs) cs.addEventListener("change", () => {
    const [k, url] = cs.value.split("|");
    $("city-out").innerHTML = k ? `<p>Served by <b>${TDU[k].name}</b>. Your ESI ID should start with <b>${TDU[k].prefix.join("</b> or <b>")}</b>. <a href="${url}">See rates in this city</a>.</p>` : "";
  });
}
