# Blog articles for kWhCompare
from tx import TDU
def dl(t,k): return t['fixed']+t['kwh']/100*k
on=TDU['oncor']; cnp=TDU['cnp']
# Worked examples (Oncor)
def plan(k,energy,base=0,credit=0,cmin=0,t=on):
    c=credit if (credit and k>=cmin) else 0
    tot=energy/100*k+base+dl(t,k)-c
    return tot, tot/k*100
A500,A500r=plan(500,9.5); A1k,A1kr=plan(1000,9.5); A2k,A2kr=plan(2000,9.5)
C999,C999r=plan(999,12,credit=100,cmin=1000); C1k,C1kr=plan(1000,12,credit=100,cmin=1000); C1500,C1500r=plan(1500,12,credit=100,cmin=1000)
C500,C500r=plan(500,12,credit=100,cmin=1000); C2k,C2kr=plan(2000,12,credit=100,cmin=1000)
F1k,F1kr=plan(1000,10.5)

ARTICLES=[]
def art(slug,title,h1,desc,lede,body,faq,related_tool,date="2026-09-26"):
    ARTICLES.append(dict(slug=slug,title=title,h1=h1,desc=desc,lede=lede,body=body,faq=faq,tool=related_tool,date=date))

# ---------------------------------------------------------------- 1
art("why-is-my-electric-bill-so-high",
"Why Is My Electric Bill So High? 12 Common Causes (2026)",
"Why is my electric bill so high? 12 common causes",
"A high electric bill usually comes down to heating and cooling, rate changes or a few hidden energy hogs. Here are 12 common causes and how to fix each one.",
"A sudden jump in your electric bill almost always has an explanation. Start by checking whether you used more kWh or paid more per kWh, then work through the causes below.",
f"""<h2>First: did you use more, or pay more?</h2>
<p>Every electric bill is two numbers multiplied together: how many kilowatt-hours (kWh) you used and what you paid for each one. Before hunting for causes, find both on your bill and compare them with the same month last year. Most bills show a 12- or 13-month usage chart.</p>
<p>If your <strong>kWh went up</strong>, the cause is in your home: weather, appliances or habits. If your <strong>kWh stayed flat but the bill rose</strong>, your rate changed. Divide the total by the kWh to get your all-in rate, then <a href="/#compare">compare it with your state's average</a>.</p>

<h2>Causes that raise your usage</h2>
<h3>1. Extreme weather</h3>
<p>Heating and cooling are about half of a typical home's energy use. A heat wave or cold snap can easily push a bill 30–50% higher than the month before, even if nothing else changed. Weather is the most common cause and the one people check last.</p>
<h3>2. Electric heating, especially heat strips</h3>
<p>Heat pumps are efficient, but when it gets very cold many switch to backup electric resistance "heat strips," which use two to three times as much electricity. If your winter bill spiked during a freeze, this is likely why. Space heaters work the same way: a single 1,500-watt heater running eight hours a day uses about 360 kWh a month.</p>
<h3>3. An aging or struggling air conditioner</h3>
<p>Dirty filters, low refrigerant and blocked outdoor coils make an AC run longer for the same comfort. Replace filters every one to three months and get a tune-up before summer. A system over 15 years old may be using far more than a modern one.</p>
<h3>4. Water heating</h3>
<p>An electric water heater is often the second-biggest load in a home. Lowering the thermostat to 120°F, fixing dripping hot-water taps and washing clothes in cold water all help.</p>
<h3>5. More people at home</h3>
<p>Working from home, a new baby, house guests or kids home for the summer all mean more lighting, cooking, laundry, devices and climate control during the day.</p>
<h3>6. New appliances or equipment</h3>
<p>An EV charger, hot tub, pool pump, second fridge in the garage or crypto-mining rig can each add hundreds of kWh a month. An EV driven 1,000 miles a month typically adds about 250–350 kWh.</p>
<h3>7. Phantom loads</h3>
<p>Devices on standby, like game consoles, set-top boxes and chargers, draw power around the clock. Individually small, together they can add 5–10% to a bill. Smart power strips shut them off.</p>
<h3>8. A longer billing period</h3>
<p>Billing cycles vary from about 27 to 35 days. A 34-day bill after a 28-day one will look 20% higher with exactly the same daily usage. Check the service dates.</p>

<h2>Causes that raise your price</h2>
<h3>9. Your contract ended</h3>
<p>In deregulated states such as Texas, Pennsylvania and Ohio, fixed-rate contracts expire. When they do, most providers roll you onto a month-to-month variable rate that is often much higher. If your rate jumped with no change in usage, check your contract end date. See <a href="/blog/best-time-to-switch-electricity-providers-texas/">the best time to switch</a>.</p>
<h3>10. A variable-rate plan</h3>
<p>Variable rates can change every month, usually upward in summer and during wholesale price spikes. <a href="/blog/fixed-vs-variable-electricity-rates-texas/">Fixed vs variable rates</a> explains when each makes sense.</p>
<h3>11. Utility rate increases</h3>
<p>Delivery charges, fuel adjustments and taxes change too. The average U.S. residential rate rose about 5% over the past year, and some states rose far more. In Texas, delivery charges are updated every March and September; see <a href="/texas/tdu-delivery-charges/">current TDU charges</a>.</p>
<h3>12. Missing a bill credit threshold</h3>
<p>Some Texas plans give a bill credit only if you use at least 1,000 kWh. Use 999 kWh and you lose the whole credit, which can make a "cheap" plan one of the most expensive. <a href="/blog/how-to-read-electricity-facts-label-efl/">Reading your EFL</a> shows how to spot this.</p>

<h2>Could it be an error?</h2>
<p>Rarely, but it happens. Check that the meter number on the bill matches your meter, and whether the read says "estimated." An estimated read followed by an actual read can produce one unusually high bill. If the numbers still don't make sense, ask your utility for a meter re-read or test.</p>

<h2>How to bring the bill down</h2>
<p>Fix the biggest usage cause first, usually heating or cooling. Then look at the price: if you live in a deregulated state, a fixed-rate plan below your state average is the quickest saving. If you're regulated, ask your utility about time-of-use rates and budget billing, which spreads costs evenly across the year.</p>""",
[("Why did my electric bill double?","Usually because of extreme weather, electric backup heating, a longer billing period or a contract that expired and rolled onto a higher variable rate. Compare kWh and rate with last month to tell which."),
 ("How do I know if I'm paying too much for electricity?","Divide your total bill by the kWh used to get your all-in rate, then compare it with your state's average. More than 10% above average is worth investigating."),
 ("Can a faulty meter cause a high bill?","It's uncommon, but possible. Check for estimated reads and ask your utility for a re-read or meter test if usage doesn't match your habits.")],
("Check your bill","See how your rate compares with your state average.","/#compare"))

# ---------------------------------------------------------------- 2
art("fixed-vs-variable-electricity-rates-texas",
"Fixed vs Variable Electricity Rates in Texas: Which Is Better?",
"Fixed vs variable electricity rates in Texas",
"Fixed-rate plans lock your price; variable plans can change every month. Here's how each works in Texas, when a variable rate makes sense and what to watch for.",
"For most Texas households a fixed-rate plan is the safer choice. Variable rates can be useful for short stays or bridging between contracts, but they come with price risk you don't control.",
f"""<h2>How a fixed-rate plan works</h2>
<p>A fixed-rate plan locks the energy charge for the length of the contract, usually 6, 12, 24 or 36 months. Your bill still moves with how much you use, and pass-through charges such as <a href="/texas/tdu-delivery-charges/">TDU delivery fees</a> can change when regulators update them, but the provider can't raise its own price.</p>
<p><strong>Pros:</strong> predictable costs, protection from summer and winter price spikes, easy comparison between plans.<br>
<strong>Cons:</strong> an early termination fee (often $150 or $10–20 per remaining month) if you leave early, and no benefit if market prices fall.</p>

<h2>How a variable-rate plan works</h2>
<p>A variable-rate plan has no fixed term. The provider can change the price from one billing cycle to the next, usually based on wholesale costs and its own pricing decisions. In Texas, these are typically month-to-month plans with no cancellation fee.</p>
<p><strong>Pros:</strong> no contract and no termination fee, so you can leave any time.<br>
<strong>Cons:</strong> prices can rise sharply in heat waves and freezes, and many "default" variable rates are well above the best fixed offers.</p>
<p>After Winter Storm Uri in February 2021, when some customers on wholesale-indexed plans received bills in the thousands, Texas banned wholesale-indexed plans for residential customers. Today's variable plans can still rise, but you won't be exposed to raw real-time wholesale prices.</p>

<h2>Side by side</h2>
<div class="scroll"><table><thead><tr><th></th><th>Fixed rate</th><th>Variable rate</th></tr></thead><tbody>
<tr><td>Price changes</td><td>Locked for the contract</td><td>Can change monthly</td></tr>
<tr><td>Contract</td><td>6–36 months</td><td>Month to month</td></tr>
<tr><td>Cancellation fee</td><td>Usually yes</td><td>Usually no</td></tr>
<tr><td>Summer and freeze risk</td><td>Protected</td><td>Exposed</td></tr>
<tr><td>Best for</td><td>Homeowners, long-term renters</td><td>Short stays, bridging gaps</td></tr>
</tbody></table></div>

<h2>What about indexed and time-of-use plans?</h2>
<p><strong>Indexed plans</strong> tie your rate to a published benchmark, often natural gas prices, so they move more predictably than a pure variable rate but can still rise. <strong>Time-of-use plans</strong>, including "free nights" and "free weekends," charge different prices at different times. They're usually fixed during the term, but the daytime rate is higher to pay for the free hours, so they only save money if you really shift a large share of your usage.</p>

<h2>When a variable rate makes sense</h2>
<p>Choose a variable plan if you're moving within a few months, waiting for a better fixed offer, or bridging the gap after a contract ends. Set a reminder to switch to a fixed plan as soon as you can, and check the price every month.</p>

<h2>How to compare fixed plans properly</h2>
<p>The advertised price is the average at 1,000 kWh and already includes TDU delivery. At different usage the real price can be very different, especially with bill credits or base fees. Take the energy charge and fees from the plan's <a href="/blog/how-to-read-electricity-facts-label-efl/">Electricity Facts Label</a> and run them through the calculator on your <a href="/electricity-rates/texas/#texas-cities">city page</a>.</p>
<p>For example, in Oncor territory a simple fixed plan at 10.5¢ energy with no fees costs about <strong>${F1k:.2f} at 1,000 kWh ({F1kr:.1f}¢ all-in)</strong>. That's a useful benchmark: most plans advertised well below it rely on a bill credit you may not always earn.</p>""",
[("Is a fixed or variable electricity rate better in Texas?","For most households a fixed rate is better because it protects you from summer and winter price spikes. Variable rates suit short stays or bridging between contracts."),
 ("Can a fixed-rate plan price change?","The provider's energy charge is locked, but pass-through charges such as TDU delivery fees and taxes can change when regulators update them."),
 ("What happens when my fixed-rate contract ends?","Most providers move you to a month-to-month variable rate, which is often higher. You can switch without a cancellation fee within 14 days of your contract's end.")],
("Calculate a plan's true cost","Enter any plan's energy charge and fees for your city.","/electricity-rates/texas/#texas-cities"))

# ---------------------------------------------------------------- 3
art("how-to-read-electricity-facts-label-efl",
"How to Read an Electricity Facts Label (EFL) in Texas",
"How to read an Electricity Facts Label (EFL)",
"Every Texas electricity plan has an Electricity Facts Label. Learn what each section means, how bill credits and base fees change the real price, and how to compare plans correctly.",
"The Electricity Facts Label, or EFL, is a standard one- to two-page document every Texas retail provider must publish for each plan. It's the only fair way to compare plans, if you know where to look.",
f"""<h2>Where to find the EFL</h2>
<p>Every plan listing links to its EFL, usually near the price, alongside two other documents: the Terms of Service (TOS) and Your Rights as a Customer (YRAC). Download the EFL before you sign up. Providers must show it, and the terms in it are what you'll be billed.</p>

<h2>The average price table</h2>
<p>At the top you'll see the average price per kWh at three usage levels: 500, 1,000 and 2,000 kWh. These averages include the provider's energy charge, any base fee, credits and your utility's delivery charges. The 1,000 kWh number is the one used in advertising.</p>
<p>The key rule: <strong>use the column closest to your real usage</strong>. Look at your last 12 bills. If your summer months hit 2,000 kWh and your spring months are near 700 kWh, the 1,000 kWh price alone tells you little.</p>

<h2>The pricing details</h2>
<p>Below the table, the EFL breaks down how the average is built. Common items:</p>
<ul>
<li><strong>Energy charge:</strong> the provider's price per kWh, for example 9.5¢.</li>
<li><strong>Base charge:</strong> a fixed monthly fee, from $0 to about $10.</li>
<li><strong>TDU delivery charges:</strong> your utility's fixed monthly charge plus a per-kWh rate, passed through at cost. <a href="/texas/tdu-delivery-charges/">See current TDU charges</a>.</li>
<li><strong>Bill credits:</strong> money off if your usage falls in a range, for example "$100 credit when usage is 1,000 kWh or more."</li>
<li><strong>Minimum usage fee:</strong> a charge if you use less than a set amount.</li>
</ul>

<h2>Example 1: a simple plan</h2>
<p>An Oncor-area plan with a 9.5¢ energy charge, no base fee and no credits works out to:</p>
<div class="scroll"><table><thead><tr><th>Usage</th><th class="num">Monthly bill</th><th class="num">Average price</th></tr></thead><tbody>
<tr><td>500 kWh</td><td class="num">${A500:.2f}</td><td class="num">{A500r:.1f}¢</td></tr>
<tr><td>1,000 kWh</td><td class="num">${A1k:.2f}</td><td class="num">{A1kr:.1f}¢</td></tr>
<tr><td>2,000 kWh</td><td class="num">${A2k:.2f}</td><td class="num">{A2kr:.1f}¢</td></tr>
</tbody></table></div>
<p>The price barely moves with usage, which is what you want: no surprises.</p>

<h2>Example 2: a bill credit plan</h2>
<p>Now a plan with a higher 12¢ energy charge and a $100 credit at 1,000 kWh or more, same utility:</p>
<div class="scroll"><table><thead><tr><th>Usage</th><th class="num">Monthly bill</th><th class="num">Average price</th></tr></thead><tbody>
<tr><td>500 kWh</td><td class="num">${C500:.2f}</td><td class="num">{C500r:.1f}¢</td></tr>
<tr><td>999 kWh</td><td class="num">${C999:.2f}</td><td class="num">{C999r:.1f}¢</td></tr>
<tr><td>1,000 kWh</td><td class="num">${C1k:.2f}</td><td class="num">{C1kr:.1f}¢</td></tr>
<tr><td>1,500 kWh</td><td class="num">${C1500:.2f}</td><td class="num">{C1500r:.1f}¢</td></tr>
<tr><td>2,000 kWh</td><td class="num">${C2k:.2f}</td><td class="num">{C2kr:.1f}¢</td></tr>
</tbody></table></div>
<p>At exactly 1,000 kWh it's advertised at {C1kr:.1f}¢, the cheapest price you'll find. But use one kWh less and the bill jumps by <strong>${C999-C1k:.2f}</strong>. In a mild month, you'd pay far more than on the simple plan. These plans only pay off if your usage stays reliably above the threshold every month.</p>

<h2>Contract terms to check</h2>
<ul>
<li><strong>Type of product:</strong> fixed, variable or indexed. See <a href="/blog/fixed-vs-variable-electricity-rates-texas/">fixed vs variable rates</a>.</li>
<li><strong>Contract term:</strong> the length in months.</li>
<li><strong>Early termination fee:</strong> what you pay to leave early. You can't be charged it if you switch within 14 days of the contract's end or if you move.</li>
<li><strong>Renewable content:</strong> the share of renewable energy, compared with the Texas average.</li>
</ul>

<h2>Quick checklist</h2>
<p>Before signing: find your usage from your last 12 bills; compare the EFL price at that usage, not just 1,000 kWh; check for bill credits and minimum usage fees; note the contract length and cancellation fee; and save a copy of the EFL. You have three federal business days after signing to cancel without penalty.</p>""",
[("What does EFL stand for?","Electricity Facts Label, the standard document every Texas retail electricity plan must publish showing its prices, fees and contract terms."),
 ("Does the EFL price include delivery charges?","Yes. The average prices at 500, 1,000 and 2,000 kWh include the provider's charges and your utility's TDU delivery charges."),
 ("Why is the 1,000 kWh price so low on some plans?","Usually because of a bill credit that applies only at 1,000 kWh or more. At lower usage the same plan can cost much more.")],
("Test a plan from its EFL","Enter the energy charge, base fee and credit to see the real price at your usage.","/electricity-rates/texas/#texas-cities"))

# ---------------------------------------------------------------- 4
art("best-time-to-switch-electricity-providers-texas",
"Best Time to Switch Electricity Providers in Texas (2026 Guide)",
"The best time to switch electricity providers in Texas",
"When to shop for a new Texas electricity plan: the cheapest months to sign, how to avoid cancellation fees, and how to time your switch around your contract end date.",
"The best time to switch is usually in the 14 days before your contract ends, ideally during spring or fall when offers tend to be lowest. Here's how to time it.",
f"""<h2>Rule 1: switch before your contract ends</h2>
<p>Texas rules let you change provider without an early termination fee if you switch within 14 days before your fixed-rate contract expires. Your provider must also send an expiration notice in advance, typically 30 to 60 days before the end date.</p>
<p>If you do nothing, most providers move you to a month-to-month variable rate, which is often well above the best offers. That's one of the most common reasons behind <a href="/blog/why-is-my-electric-bill-so-high/">a sudden jump in your bill</a>.</p>
<p>Find your end date on your latest bill, in your online account or on your contract documents, then set a reminder about three weeks before.</p>

<h2>Rule 2: shop in spring or fall if you can</h2>
<p>Retail offers follow wholesale expectations. Prices tend to be lower in the mild "shoulder" months, roughly March to May and October to November, and higher heading into summer, when demand peaks. Signing a 12-month contract in spring locks in a lower price that then carries you through the next summer.</p>
<p>If your contract happens to end in July, consider a shorter bridge plan or a term that ends in the spring, so that future renewals line up with cheaper months.</p>

<h2>Rule 3: pick the contract length on purpose</h2>
<p>12-month plans usually offer the best price. Longer terms (24–36 months) protect you from future increases, which is worth considering after a year of rising prices; shorter terms give flexibility. Whatever you choose, aim for an end date in spring or fall.</p>

<h2>Switching when you move</h2>
<p>Moving is a natural time to switch. Texas rules generally let you end a contract without a termination fee when you move, as long as you give notice and proof of your new address. At your new home, sign up a week or two before your move-in date so service starts on time. You'll need the new address's <a href="/esi-id-lookup/">ESI ID</a>, which any provider can find from the address.</p>

<h2>How the switch works</h2>
<p>Switching doesn't interrupt your power. Your utility keeps delivering electricity; only the company that bills you changes. The new provider handles the switch, and it typically takes effect on your next meter read, often within a few days with a smart meter. You have three federal business days after signing to cancel if you change your mind.</p>

<h2>Step by step</h2>
<ol>
<li>Find your contract end date and your usage over the last 12 months.</li>
<li>About three weeks before the end, compare plans at your real usage, not just 1,000 kWh. <a href="/blog/how-to-read-electricity-facts-label-efl/">Read the EFL</a> for each.</li>
<li>Run the numbers in the calculator on your <a href="/electricity-rates/texas/#texas-cities">city page</a>.</li>
<li>Sign up within the 14-day window so you pay no cancellation fee.</li>
<li>Save the EFL and note the new end date.</li>
</ol>""",
[("When is the cheapest time to sign an electricity contract in Texas?","Usually spring (March–May) or fall (October–November), when demand and retail offers are typically lower than in summer."),
 ("Can I switch electricity providers without paying a cancellation fee?","Yes, if you switch within 14 days before your contract ends, or when you move and provide proof of your new address."),
 ("Will my power go out when I switch providers?","No. Your utility keeps delivering power over the same lines; only the company that bills you changes.")],
("Find your utility","Decode your ESI ID to see which utility serves your home.","/esi-id-lookup/"))

# ---------------------------------------------------------------- 5
art("what-is-a-good-price-per-kwh",
"What Is a Good Price per kWh in 2026? (By State)",
"What is a good price per kWh in 2026?",
"The average U.S. home pays about 18.3¢ per kWh in 2026, but a good price depends on your state. Here's how to judge your rate and what counts as a good deal.",
"A good electricity price is one below your state's average, not the national one. The U.S. average is about 18.3¢ per kWh in 2026, but state averages range from about 13¢ to over 50¢.",
"""<h2>The national picture</h2>
<p>The average U.S. residential rate is about <strong>18.3¢ per kWh</strong> as of mid-2026, roughly 5% higher than a year earlier. That figure includes everything: generation, delivery, fees and taxes, averaged across all homes. It's a useful headline, but a poor benchmark on its own, because what you pay depends heavily on where you live.</p>

<h2>Cheapest and most expensive states</h2>
{STATE_TABLES}
<p>See every state in the <a href="/#rates">full rate table</a>.</p>

<h2>How to calculate your real price</h2>
<p>Divide the total amount on your bill by the kWh you used. $182 for 1,000 kWh is 18.2¢. This "all-in" price is the only fair comparison, because it includes delivery charges, fees and taxes that advertised rates often leave out. Our <a href="/#compare">bill analyzer</a> does this for you and compares it with your state.</p>

<h2>What counts as a good price?</h2>
<ul>
<li><strong>Below your state average:</strong> good.</li>
<li><strong>10% or more below:</strong> very good; typical of a competitive fixed plan in a deregulated state.</li>
<li><strong>More than 10% above:</strong> worth investigating. In a deregulated state, it often means you're on a default or expired variable rate.</li>
</ul>

<h2>Why one number isn't enough</h2>
<p>Your real price per kWh changes with usage. Fixed monthly charges are spread over fewer kWh in mild months, so the per-kWh price is higher when you use less. In Texas, bill credits can swing the price dramatically at certain usage levels, as shown in <a href="/blog/how-to-read-electricity-facts-label-efl/">our EFL guide</a>. Always compare at the usage you actually have.</p>

<h2>Texas: what's a good rate?</h2>
<p>The Texas average is about <strong>15.9¢ per kWh</strong>, below the national figure. Delivery charges alone differ by up to about $18 a month at 1,000 kWh depending on your utility, so a good price in Houston (CenterPoint) and in Galveston (TNMP) aren't the same. See the <a href="/texas/tdu-delivery-charges/">delivery charges by utility</a> and use your <a href="/electricity-rates/texas/#texas-cities">city page</a> to judge a plan.</p>

<h2>If your price is too high</h2>
<p>In a deregulated state, compare fixed-rate plans; that's the fastest way to lower your price. In a regulated state, ask your utility about time-of-use rates, look into community solar where available, and reduce usage. And if your bill rose without your rate changing, see <a href="/blog/why-is-my-electric-bill-so-high/">why your electric bill is so high</a>.</p>""",
[("What is a good price per kWh in 2026?","Anything below your state's average all-in rate. Nationally the average is about 18.3¢, but state averages range from about 13¢ in Nevada to over 50¢ in Hawaii."),
 ("Is 15 cents per kWh a good rate?","In most states, yes. It's below the national average of about 18.3¢, but it's roughly average in states like Texas, Florida and Arizona."),
 ("How do I calculate my price per kWh?","Divide your total bill by the kWh used in that billing period. The result is your all-in rate.")],
("Compare your rate","Enter your bill to see how you compare with your state.","/#compare"))
