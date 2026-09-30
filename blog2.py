from blog import ARTICLES, art, TDU, dl
# ---------- shared numbers ----------
US=18.34; TXR=15.94; GAS=4.48
KWH_MI=0.30; LOSS=1.10; EFF=KWH_MI*LOSS   # kWh from the wall per mile
MI=1000; EVK=MI*EFF
def ev_cost(rate): return EVK*rate/100
gas_cost=MI/30*GAS
EV_ROWS=[("Texas",15.94),("Florida",15.10),("U.S. average",18.34),("New York",29.49),("California",34.74),("Hawaii",52.72)]
ev_table='<div class="scroll"><table><thead><tr><th>Where you charge</th><th class="num">Rate</th><th class="num">1,000 miles</th><th class="num">Per mile</th></tr></thead><tbody>'+"".join(
 f'<tr><td>{n}</td><td class="num">{r:.1f}¢</td><td class="num">${ev_cost(r):.0f}</td><td class="num">{ev_cost(r)/MI*100:.1f}¢</td></tr>' for n,r in EV_ROWS)+\
 f'<tr><td><b>Gas car, 30 mpg</b></td><td class="num">${GAS:.2f}/gal</td><td class="num"><b>${gas_cost:.0f}</b></td><td class="num">{gas_cost/MI*100:.1f}¢</td></tr></tbody></table></div>'

EV_TOOL='''<div class="tool" id="evc" style="margin:1.5rem 0">
<div class="panel"><p style="margin:0 0 1rem;font-weight:700">Your EV charging cost</p>
<div class="grid2">
<div class="field"><label for="ev-mi">Miles per month</label><input id="ev-mi" type="number" value="1000" min="0" inputmode="numeric"></div>
<div class="field"><label for="ev-rate">Your electricity rate <span class="hint">(¢/kWh)</span></label><input id="ev-rate" type="number" value="18.3" step="0.1" min="0" inputmode="decimal"></div>
<div class="field"><label for="ev-eff">EV efficiency <span class="hint">(kWh per 100 mi)</span></label><input id="ev-eff" type="number" value="30" min="10" inputmode="numeric"></div>
<div class="field"><label for="ev-gas">Gas price <span class="hint">($/gal)</span></label><input id="ev-gas" type="number" value="4.48" step="0.01" min="0" inputmode="decimal"></div>
</div>
<div class="field"><label for="ev-mpg">Gas car you'd otherwise drive <span class="hint">(mpg)</span></label><input id="ev-mpg" type="number" value="30" min="1" inputmode="numeric"></div>
</div><div id="ev-out" style="border-top:1px solid var(--line);padding:1.25rem" aria-live="polite"></div></div>'''
EV_JS='''<script>
(function(){const v=id=>parseFloat(document.getElementById(id).value)||0;
function run(){const mi=v("ev-mi"),kwh=mi*v("ev-eff")/100*1.1,ev=kwh*v("ev-rate")/100,gas=v("ev-mpg")?mi/v("ev-mpg")*v("ev-gas"):0,save=gas-ev;
document.getElementById("ev-out").innerHTML=`<p class="verdict ${save>0?"good":"bad"}">$${ev.toFixed(0)} a month to charge at home</p>
<p class="sub">About ${Math.round(kwh).toLocaleString()} kWh, including roughly 10% charging losses. The same miles in a gas car cost about $${gas.toFixed(0)}, so you ${save>0?"save":"pay an extra"} <b>$${Math.abs(save).toFixed(0)} a month</b>, or $${Math.abs(save*12).toFixed(0)} a year.</p>`}
document.querySelectorAll("#evc input").forEach(i=>i.addEventListener("input",run));run();})();
</script>'''

art("cost-to-charge-electric-car-at-home",
"How Much Does It Cost to Charge an EV at Home? (2026 Calculator)",
"How much does it cost to charge an EV at home?",
f"Charging an EV at home costs about ${ev_cost(US):.0f} per 1,000 miles at the average U.S. electricity rate, versus about ${gas_cost:.0f} for a 30-mpg car with gas at ${GAS:.2f}. Calculate your own cost by state.",
f"With gas at a record ${GAS:.2f} a gallon for this time of year, the math on electric cars has never looked better. At the average U.S. electricity rate, driving 1,000 miles on home charging costs about <strong>${ev_cost(US):.0f}</strong>. The same distance in a 30-mpg car costs about <strong>${gas_cost:.0f}</strong>. But your number depends heavily on where you live, and in one state the math flips entirely.",
f"""<h2>Calculate your cost</h2>
<p>Enter your own numbers. Your electricity rate is your total bill divided by the kWh you used; if you don't know it, start with your <a href="/#rates">state average</a>.</p>
{EV_TOOL}

<h2>The formula</h2>
<p>Charging cost = miles driven × kWh per mile × your electricity rate.</p>
<p>Most EVs use between 25 and 35 kWh per 100 miles; smaller sedans sit at the low end, large SUVs and trucks at the high end. You can find your model's official figure on fueleconomy.gov. Add about 10% for energy lost while charging, so a car rated at 30 kWh per 100 miles really draws about 33 kWh from your wall.</p>
<p>A driver doing 1,000 miles a month in that car uses about <strong>{EVK:.0f} kWh</strong> a month. That's roughly a third of what a typical home uses, so expect your electric bill to rise noticeably, even as your gas spending falls to zero.</p>

<h2>EV vs gas by state</h2>
<p>Cost of 1,000 miles in an EV using 30 kWh per 100 miles, with 10% charging losses, at each area's average residential rate:</p>
{ev_table}
<p>In Texas and Florida, home charging costs about a third of gas. Even in California, one of the most expensive states for electricity, it's still cheaper than filling up at current prices. Hawaii is the exception: at over 50¢ per kWh, home charging at the standard rate costs more than gas, which is why so many Hawaii EV owners pair their cars with rooftop solar.</p>

<h2>Level 1 vs Level 2 charging</h2>
<p><strong>Level 1</strong> uses a standard 120-volt outlet and the cable that comes with most EVs. It adds only about 3–5 miles of range per hour, but costs nothing to set up. If you drive under 40 miles a day and can plug in overnight, it's often enough.</p>
<p><strong>Level 2</strong> uses a 240-volt circuit, like a dryer outlet, and adds roughly 20–30 miles of range per hour. The charger and installation usually run from several hundred dollars to over $2,000, depending on how far your panel is from the garage and whether it needs an upgrade. The electricity costs the same per kWh either way; Level 2 just charges faster.</p>

<h2>How to cut your charging cost</h2>
<h3>Charge at night on the right plan</h3>
<p>Many utilities offer time-of-use or EV rates with much cheaper overnight prices. In Texas, "free nights" plans can make overnight charging almost free, but check the daytime rate: it's usually higher to compensate. Our guide to <a href="/blog/fixed-vs-variable-electricity-rates-texas/">plan types in Texas</a> explains the trade-offs.</p>
<h3>Watch the bill credit thresholds</h3>
<p>Adding an EV can push a Texas home above 1,000 or 2,000 kWh, which changes which plan is cheapest. Plans that look expensive at 1,000 kWh are sometimes the best deal at 1,800 kWh. <a href="/blog/how-to-read-electricity-facts-label-efl/">Reading the EFL</a> shows how to compare at your new usage.</p>
<h3>Skip DC fast charging when you can</h3>
<p>Public fast chargers are convenient on road trips, but often charge 40–60¢ per kWh or more, two to three times the average home rate. Charging at home most of the time is where the savings come from.</p>

<h2>The bottom line</h2>
<p>For most Americans, charging at home costs well under half of what the same miles cost in gasoline, and with gas above $4 the savings for a typical driver can top $1,000 a year. The cheaper your electricity, the bigger the gap, so once you have an EV, it's worth <a href="/#compare">checking whether your electricity rate is competitive</a>.</p>""",
[("How much does it cost to charge an EV at home per month?",f"For 1,000 miles a month, about ${ev_cost(US):.0f} at the average U.S. rate of 18.3¢ per kWh, using an EV that needs 30 kWh per 100 miles plus charging losses."),
 ("Is it cheaper to charge an EV than to buy gas?",f"In almost every state, yes. At ${GAS:.2f} a gallon, gas for a 30-mpg car costs about {gas_cost/MI*100:.0f}¢ a mile versus about {ev_cost(US)/MI*100:.0f}¢ for an EV at the average electricity rate. Hawaii is the main exception."),
 ("How many kWh does an EV use per month?",f"About {EVK:.0f} kWh for 1,000 miles in a typical EV, including charging losses."),
 ("Is Level 2 charging more expensive than Level 1?","No. The price per kWh is the same; Level 2 just charges faster. The extra cost is the one-time charger and installation.")],
("Check your electricity rate","See if your rate is competitive before your bill goes up.","/#compare"),date="2026-09-29")
ARTICLES[-1]['script']=EV_JS
ARTICLES[-1]['sources']=["AAA, national average gas prices, September 2026 (gasprices.aaa.com)","U.S. Energy Information Administration, average residential electricity prices by state, 2026 (eia.gov)","U.S. Department of Energy and EPA, vehicle efficiency ratings (fueleconomy.gov)"]

# ---------------------------------------------------------------- Texas average bill
on=TDU['oncor']; cnp=TDU['cnp']; tn=TDU['tnmp']
TXKWH=round(173/TXR*100)
def txbill(k,t,energy=9.5): return energy/100*k+dl(t,k)
sizes=[("Apartment, 800 sq ft",650),("Small house, 1,500 sq ft",1000),("Average home",TXKWH),("Larger home, 2,500 sq ft",1600),("Large home + pool or EV",2200)]
size_rows="".join(f'<tr><td>{n}</td><td class="num">{k:,}</td><td class="num">${k*TXR/100:.0f}</td></tr>' for n,k in sizes)
tdu_rows="".join(f'<tr><td>{t["name"]}</td><td class="num">${dl(t,1000):.2f}</td><td class="num">${txbill(1000,t):.2f}</td></tr>' for t in sorted(TDU.values(),key=lambda x:dl(x,1000)))
art("average-electric-bill-texas",
"Average Electric Bill in Texas (2026): What's Normal for Your Home?",
"Average electric bill in Texas: what's normal?",
f"The average Texas electric bill is about $173 a month in 2026, for roughly {TXKWH:,} kWh at 15.9¢ per kWh. See what's normal by home size, season and utility, and how to tell if you're overpaying.",
f"The average Texas home pays about <strong>$173 a month</strong> for electricity, using roughly <strong>{TXKWH:,} kWh</strong> at an average of <strong>15.9¢ per kWh</strong>. That's one of the higher monthly bills in the country, not because Texas power is expensive, but because Texans use a lot of it.",
f"""<h2>Why Texas bills are high even though rates are low</h2>
<p>Texas's average rate of 15.9¢ per kWh is below the national average of 18.3¢. But the average Texas home uses far more electricity than a home in, say, California or New England. Long, hot summers keep air conditioners running for months, and most Texas homes heat with electricity rather than gas. Size matters too: newer suburban homes are often large, with more space to cool.</p>
<p>So when you compare your bill with friends in other states, compare the <em>rate</em>, not the total. See how Texas ranks in our <a href="/electricity-rates/texas/">Texas rate overview</a>.</p>

<h2>What's normal for your home size</h2>
<p>Typical monthly usage and the bill at the Texas average rate. Your own numbers will vary with insulation, AC age, number of people and how warm you keep the house.</p>
<div class="scroll"><table><thead><tr><th>Home</th><th class="num">kWh / month</th><th class="num">Bill at 15.9¢</th></tr></thead><tbody>{size_rows}</tbody></table></div>
<p class="hint">Annual averages. Summer months typically run well above these, spring and fall well below.</p>

<h2>How bills change through the year</h2>
<p>A Texas electric bill follows the thermometer. Usage usually peaks from <strong>July through September</strong>, when many homes use one and a half to two times what they use in April or October. Winter brings a smaller second peak, and a sharp one during hard freezes in homes with electric heat pumps and heat strips.</p>
<p>That swing is why you should never judge a plan by one month. Look at your 12-month usage history, which most providers show on the bill or in your online account, and compare plans at your summer peak as well as your average. Our <a href="/blog/how-to-read-electricity-facts-label-efl/">EFL guide</a> shows why this matters so much with bill-credit plans.</p>
<p>If summer bills hurt, ask your provider about <strong>average billing</strong> (sometimes called budget billing). It spreads your yearly cost into more even monthly payments. You don't pay less overall, but you avoid the August shock.</p>

<h2>Your utility changes the bill too</h2>
<p>Every bill in competitive Texas includes delivery charges from the local utility, and they're not the same everywhere. Here's the delivery charge at 1,000 kWh and the total bill for the same simple plan, 9.5¢ energy and no base fee, in each area:</p>
<div class="scroll"><table><thead><tr><th>Utility</th><th class="num">Delivery</th><th class="num">Total bill</th></tr></thead><tbody>{tdu_rows}</tbody></table></div>
<p>Same plan, same usage, a difference of about <strong>${txbill(1000,tn)-txbill(1000,cnp):.0f} a month</strong> just because of where you live. Find yours on your <a href="/electricity-rates/texas/#texas-cities">city page</a> or in the <a href="/texas/tdu-delivery-charges/">full delivery charge table</a>.</p>

<h2>Are you paying too much?</h2>
<p>Divide your total bill by the kWh used. If the result is well above <strong>15.9¢</strong>, something is probably off. The most common reason in Texas is an expired contract: when a fixed-rate plan ends, most providers move you to a pricier month-to-month rate. See <a href="/blog/best-time-to-switch-electricity-providers-texas/">when to switch</a> to fix it, or <a href="/#compare">run your bill through our analyzer</a>.</p>
<p>If your rate looks fine but your bill is high, the problem is usage. <a href="/blog/why-is-my-electric-bill-so-high/">Our guide to high bills</a> walks through the 12 most common causes, and our <a href="/blog/how-to-lower-electric-bill-summer/">summer savings guide</a> covers the fixes that matter most in Texas.</p>""",
[("What is the average electric bill in Texas?",f"About $173 a month in 2026, for roughly {TXKWH:,} kWh at an average of 15.9¢ per kWh."),
 ("Why is my electric bill so high in Texas?","Usually because of air conditioning in summer, electric heating in winter or an expired contract that rolled you onto a higher variable rate."),
 ("Is $200 a month high for electricity in Texas?","Not necessarily. For a larger home in summer it's normal. Divide the bill by your kWh: if your rate is well above 15.9¢, you're likely overpaying."),
 ("What is a good electricity rate in Texas?","Anything below the state average of about 15.9¢ per kWh all-in, measured at your real usage.")],
("Check your Texas bill","Compare your rate with the Texas average in seconds.","/#compare"),date="2026-09-29")
ARTICLES[-1]['sources']=["U.S. Energy Information Administration, average residential electricity prices and bills by state, 2026 (eia.gov)","Public Utility Commission of Texas, TDU residential delivery charges (puc.texas.gov)"]

# ---------------------------------------------------------------- No deposit
art("texas-electricity-no-deposit",
"Texas Electricity With No Deposit: 4 Legal Ways to Skip It (2026)",
"Texas electricity with no deposit: 4 legal ways to skip it",
"Texas electricity deposits often run $100 to $400. Here are the four legal ways to avoid one: good credit, a state waiver, a letter of credit or a prepaid plan, and what each really costs.",
"Setting up electricity in Texas can come with a surprise: a deposit of a few hundred dollars before your lights come on. You often don't have to pay it. State rules give you several ways around it, and some of them cost nothing at all.",
"""<h2>Why providers ask for a deposit</h2>
<p>Electricity is billed after you use it, so a new provider is effectively lending you a month of power. If your credit history is thin or low, most providers will ask for a security deposit to cover that risk. The Public Utility Commission of Texas (PUCT) sets the rules on how much they can charge and who they must exempt.</p>
<p>The deposit can't exceed one-fifth of your estimated annual bill or the sum of the next two estimated monthly bills, whichever is greater. In practice, that usually means a few hundred dollars. Deposits earn interest, and providers refund them, typically after 12 months of on-time payments or when you close the account.</p>

<h2>Way 1: qualify on your credit or payment history</h2>
<p>Providers run a credit check when you sign up, normally a soft check that doesn't affect your score. You can also establish satisfactory credit by showing that during the past two years you were a customer of any Texas provider or utility, you're not behind on that account, and you weren't late more than once in your last 12 months of service.</p>
<p><strong>Tip:</strong> ask your previous provider for a <strong>letter of credit</strong> (a payment history letter) before you move. It's free, and it can replace a credit score entirely.</p>

<h2>Way 2: a state deposit waiver</h2>
<p>PUCT rules require providers to waive the deposit for two groups:</p>
<ul>
<li><strong>Customers 65 or older</strong> who aren't currently behind on any electric account.</li>
<li><strong>Victims of family violence</strong>, certified by a family violence center, medical staff, law enforcement, a prosecutor's office or other listed agencies, using the Texas Council on Family Violence certification letter.</li>
</ul>
<p>These waivers don't depend on your credit score. Mention them when you sign up; the provider must accept valid documentation.</p>

<h2>Way 3: a letter of guarantee</h2>
<p>Some providers accept a written guarantee from another customer with good credit who agrees to pay if you don't. It's less common, and the guarantor takes on real risk, so treat it as a fallback.</p>

<h2>Way 4: a prepaid plan</h2>
<p>Prepaid, or "pay as you go," plans don't require a deposit or credit check. You load money onto the account and your usage draws it down, with daily balance alerts by text or email. With a smart meter, service can often start the same day.</p>
<p>The trade-off is price. Prepaid plans often cost more per kWh than the best postpaid plans, and if your balance runs out, your power can be disconnected quickly. They suit people who want control over spending or who can't qualify any other way, but compare the rate carefully.</p>

<h2>Which option is best?</h2>
<div class="scroll"><table><thead><tr><th>Option</th><th>Cost</th><th>Best for</th></tr></thead><tbody>
<tr><td>Credit or payment history</td><td>Free</td><td>Anyone with a record of on-time bills</td></tr>
<tr><td>65+ or family violence waiver</td><td>Free</td><td>Those who qualify</td></tr>
<tr><td>Letter of guarantee</td><td>Free, but risky for the guarantor</td><td>When a trusted person can vouch for you</td></tr>
<tr><td>Prepaid plan</td><td>Often a higher rate</td><td>No credit, or a preference for pay-as-you-go</td></tr>
<tr><td>Pay the deposit</td><td>Refundable, with interest</td><td>When the cheapest plan requires it</td></tr>
</tbody></table></div>

<h2>Don't let "no deposit" cost you more</h2>
<p>A refundable deposit isn't lost money. Over a year, a cheaper postpaid plan with a deposit can easily beat a more expensive no-deposit plan. Compare the <strong>average price at your usage</strong> on each plan's <a href="/blog/how-to-read-electricity-facts-label-efl/">Electricity Facts Label</a>, and use the calculator on your <a href="/electricity-rates/texas/#texas-cities">city page</a> to see the monthly difference.</p>

<h2>Starting service at a new home</h2>
<p>Have three things ready: your new address, your move-in date and the address's <a href="/esi-id-lookup/">ESI ID</a> (any provider can find it for you). Sign up a week or two before you move so service starts on time, and ask about the waivers above before you agree to pay anything.</p>""",
[("How much is an electricity deposit in Texas?","Usually a few hundred dollars. By PUCT rule it can't exceed one-fifth of your estimated annual bill or two estimated monthly bills, whichever is greater."),
 ("Do seniors have to pay an electricity deposit in Texas?","No. Customers 65 or older who aren't behind on any electric account qualify for a deposit waiver under PUCT rules."),
 ("Do I get my electricity deposit back?","Yes, with interest. It's usually refunded after 12 consecutive on-time payments or applied to your final bill when you close the account."),
 ("Are no-deposit electricity plans more expensive?","Often, especially prepaid plans. Compare the price at your usage: a cheaper plan with a refundable deposit can cost less over a year.")],
("Find your ESI ID","Have it ready when you sign up for service.","/esi-id-lookup/"),date="2026-09-29")
ARTICLES[-1]['sources']=["Public Utility Commission of Texas, Substantive Rule §25.478, Credit Requirements and Deposits (puc.texas.gov)","Public Utility Commission of Texas, Substantive Rule §25.498, Prepaid Service (puc.texas.gov)"]

# ---------------------------------------------------------------- Summer
art("how-to-lower-electric-bill-summer",
"How to Lower Your Electric Bill in Summer: 15 Tips That Work",
"How to lower your electric bill in summer: 15 tips that actually work",
"Air conditioning can double your summer electric bill. These 15 practical tips, from thermostat settings to plan choice, cut cooling costs without making your home uncomfortable.",
"Air conditioning is the single biggest reason summer bills climb, and in hot states it can double what you pay in spring. The good news: most of the savings come from a handful of changes that cost little or nothing.",
"""<h2>The thermostat: your biggest lever</h2>
<h3>1. Set it to 78°F when you're home</h3>
<p>The U.S. Department of Energy suggests 78°F as a comfortable, efficient summer setting. Every degree lower makes your AC work noticeably harder, so small changes add up over a full season.</p>
<h3>2. Turn it up when you're away</h3>
<p>Raising the setting by 7–10°F for eight hours a day, while you're at work, for example, can save up to 10% a year on heating and cooling, according to the DOE. Don't turn the AC off completely in extreme heat: the house absorbs heat and takes far longer to cool back down.</p>
<h3>3. Use a smart or programmable thermostat</h3>
<p>It makes tips 1 and 2 automatic. Many utilities and providers offer rebates or free devices, especially in exchange for joining a demand response program.</p>
<h3>4. Run ceiling fans, but only in occupied rooms</h3>
<p>A fan's breeze lets you raise the thermostat about 4°F with no loss of comfort. Fans cool people, not rooms, so switch them off when you leave. In summer, set them to spin counterclockwise.</p>

<h2>Help your AC work less</h2>
<h3>5. Change the air filter</h3>
<p>A clogged filter makes the system strain and run longer. Check it monthly during summer and replace it at least every one to three months.</p>
<h3>6. Clear the outdoor unit</h3>
<p>Keep at least two feet around the condenser free of plants and debris, and gently hose off the fins. A blocked unit can't shed heat efficiently.</p>
<h3>7. Get a tune-up before the heat</h3>
<p>A technician can check refrigerant, clean the coils and spot a failing part before it fails on the hottest day of the year.</p>
<h3>8. Block the sun</h3>
<p>Sunlight through windows is a major source of heat. Close blinds and curtains on south- and west-facing windows during the afternoon. Reflective films or exterior shades help even more.</p>
<h3>9. Seal the leaks</h3>
<p>Weatherstripping doors and caulking gaps around windows keeps cool air in. Leaky ductwork in a hot attic can also waste a large share of the air your AC produces; sealing ducts is often one of the best-value upgrades.</p>

<h2>Cut the heat you create</h2>
<h3>10. Cook outside or with small appliances</h3>
<p>An oven heats your kitchen for hours. Grill, use the microwave or an air fryer, or cook in the cooler morning.</p>
<h3>11. Run heavy appliances at night</h3>
<p>Dishwashers and dryers add heat and humidity. Running them in the evening keeps the house cooler during peak hours and helps if you're on a time-of-use plan.</p>
<h3>12. Switch remaining bulbs to LEDs</h3>
<p>Old incandescent bulbs turn most of their energy into heat. LEDs use a fraction of the power and run cool.</p>

<h2>Fix the price, not just the usage</h2>
<h3>13. Check your rate before summer starts</h3>
<p>A cheaper rate multiplies every other saving. If you're in a deregulated state and your contract has ended, you may be on an expensive variable rate right when usage peaks. See <a href="/blog/best-time-to-switch-electricity-providers-texas/">the best time to switch</a>.</p>
<h3>14. Compare plans at summer usage</h3>
<p>In Texas, a plan that's cheap at 1,000 kWh can look very different at 2,000 kWh. Use your August bill, not your April one, when you compare. Our <a href="/blog/how-to-read-electricity-facts-label-efl/">EFL guide</a> shows how.</p>
<h3>15. Smooth out the payments</h3>
<p>If the problem is budgeting rather than cost, ask about average (budget) billing. You'll pay a similar amount every month instead of facing a huge August bill.</p>

<h2>Where to start</h2>
<p>If you do only three things, make them these: set the thermostat to 78°F and raise it when you're out, change the AC filter, and make sure you're not paying an expired-contract rate. Then check whether your bill is actually normal for your home with our <a href="/blog/average-electric-bill-texas/">Texas bill guide</a> or the <a href="/#compare">bill analyzer</a>.</p>""",
[("What temperature should I set my thermostat in summer?","The U.S. Department of Energy suggests 78°F when you're home, and higher when you're away."),
 ("Is it cheaper to leave the AC on all day?","Usually it's cheaper to raise the setting by 7–10°F while you're out rather than turn it off completely, especially in extreme heat."),
 ("Do ceiling fans lower the electric bill?","Yes, if you raise the thermostat. A fan lets you set it about 4°F higher with the same comfort. Turn fans off in empty rooms."),
 ("Why is my electric bill higher in summer?","Air conditioning. In hot states it can double usage compared with spring, and some variable rates also rise in summer.")],
("Check your summer bill","See if your rate is costing you more than it should.","/#compare"),date="2026-09-29")
ARTICLES[-1]['sources']=["U.S. Department of Energy, Energy Saver: thermostats, fans and cooling (energy.gov)","U.S. Energy Information Administration, residential energy consumption (eia.gov)"]

# ---------------------------------------------------------------- Community solar
art("community-solar-how-it-works",
"Community Solar: How It Works, What You Save and Who Can Join (2026)",
"Community solar: how it works and who can join",
"Community solar lets renters and homeowners save 5–15% on electricity with no panels on the roof. Here's how subscriptions and bill credits work, which states have programs and what to check before signing.",
"Community solar is the easiest way to get the savings of solar without putting a single panel on your roof. It works for renters, condo owners and homes with shade, and in states with active programs, most subscribers save 5–15% on their electricity supply costs.",
"""<h2>How community solar works</h2>
<p>A developer builds a solar farm somewhere in your utility's territory. Instead of powering one building, the farm sends its electricity into the grid, and local households subscribe to a share of its output.</p>
<p>Each month, your utility calculates how much electricity your share produced and puts a <strong>credit</strong> on your electric bill. You then pay the solar company for those credits, at a discount. The difference is your saving.</p>
<p>Nothing changes at your home. You keep the same utility, the same meter and the same power lines. You don't own any equipment, and there's nothing to install or maintain.</p>

<h2>What you actually save</h2>
<p>Most programs are designed so you pay about <strong>5–15% less</strong> for the credited electricity than its value on your bill. On a typical bill that's often $5 to $20 a month. It's not dramatic, but it's steady, and it requires no upfront cost.</p>
<p>Low- and moderate-income households often qualify for bigger discounts. Several states run programs, such as Illinois Solar for All, that offer free or heavily discounted subscriptions to eligible customers.</p>

<h2>Where it's available</h2>
<p>About two dozen states plus Washington, D.C., have laws that enable community solar. The largest programs are in <strong>New York, Minnesota, Massachusetts, Illinois, New Jersey, Maryland and Colorado</strong>. Other active states include Maine, New Mexico, Virginia, Delaware, Connecticut, Rhode Island, Oregon and California, though program sizes and enrollment windows vary.</p>
<p><strong>Texas</strong> has no statewide community solar program, and in the competitive market you can't subscribe through your utility. Some city utilities and co-ops, such as Austin Energy, run their own local programs. Many Texas retail providers also sell renewable plans, which are a different product: see our <a href="/blog/fixed-vs-variable-electricity-rates-texas/">Texas plan types guide</a>.</p>
<p>Your state's page in our <a href="/#rates">rate table</a> mentions community solar if your state has a program.</p>

<h2>Community solar vs rooftop solar</h2>
<div class="scroll"><table><thead><tr><th></th><th>Community solar</th><th>Rooftop solar</th></tr></thead><tbody>
<tr><td>Upfront cost</td><td>None</td><td>High, unless leased or financed</td></tr>
<tr><td>Typical savings</td><td>5–15% on credited power</td><td>Much larger over the system's life</td></tr>
<tr><td>Roof needed</td><td>No</td><td>Yes, with good sun</td></tr>
<tr><td>Works for renters</td><td>Yes</td><td>Rarely</td></tr>
<tr><td>If you move</td><td>Transfer or cancel</td><td>Sell with the house</td></tr>
</tbody></table></div>

<h2>What to check before you sign</h2>
<ul>
<li><strong>Contract length:</strong> some run 20 years, others are month to month. Shorter or cancelable is better for most people.</li>
<li><strong>Cancellation fee:</strong> look for no fee, or a small one, especially if you might move.</li>
<li><strong>Guaranteed discount:</strong> a fixed percentage off the credit value is simpler than a fixed price per kWh that could end up above your utility rate.</li>
<li><strong>Price escalator:</strong> some contracts raise the price every year. Know by how much.</li>
<li><strong>What happens if you move:</strong> can you take the subscription to a new address in the same utility area?</li>
<li><strong>Credit timing:</strong> credits can lag a month or two behind the bill they apply to, so your first bills may look uneven.</li>
</ul>

<h2>Is it worth it?</h2>
<p>If your state has a program and you can find a subscription with no cancellation fee and a guaranteed discount, community solar is close to free money: a modest, reliable saving with almost no downside. It won't transform a high bill on its own, so pair it with the basics: <a href="/blog/what-is-a-good-price-per-kwh/">know whether your rate is fair</a> and <a href="/blog/why-is-my-electric-bill-so-high/">tackle what's driving your usage</a>.</p>""",
[("How does community solar save money?","You subscribe to part of a local solar farm, receive bill credits for its output and pay the solar company less than the credits are worth, usually 5–15% less."),
 ("Can renters join community solar?","Yes. Nothing is installed at your home, so renters and condo owners can subscribe."),
 ("Is community solar available in Texas?","There's no statewide program, but some city utilities and co-ops, such as Austin Energy, run local programs."),
 ("Can I cancel a community solar subscription?","It depends on the contract. Many allow cancellation with notice and no fee, but some charge fees or run for many years. Check before signing.")],
("Compare your state's rates","See how your state compares and what options you have.","/#rates"),date="2026-09-29")
ARTICLES[-1]['sources']=["Solar Energy Industries Association (SEIA), community solar and state policy resources (seia.org)","U.S. Department of Energy, community solar basics (energy.gov)","Illinois Power Agency, Illinois Solar for All (illinoissfa.com)"]

# sources for first batch
SRC1={"why-is-my-electric-bill-so-high":["U.S. Energy Information Administration, residential electricity prices and consumption (eia.gov)","U.S. Department of Energy, Energy Saver (energy.gov)"],
 "fixed-vs-variable-electricity-rates-texas":["Public Utility Commission of Texas, customer protection rules and plan types (puc.texas.gov)","Public Utility Commission of Texas, TDU delivery charges (puc.texas.gov)"],
 "how-to-read-electricity-facts-label-efl":["Public Utility Commission of Texas, Electricity Facts Label requirements (puc.texas.gov)","Public Utility Commission of Texas, TDU delivery charges (puc.texas.gov)"],
 "best-time-to-switch-electricity-providers-texas":["Public Utility Commission of Texas, customer protection rules (puc.texas.gov)"],
 "what-is-a-good-price-per-kwh":["U.S. Energy Information Administration, average residential electricity prices by state, 2026 (eia.gov)"]}
for a in ARTICLES:
    a.setdefault('sources',SRC1.get(a['slug'],[])); a.setdefault('script','')
