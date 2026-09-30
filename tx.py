# Texas data shared by generator
TDU = {
 "cnp":   dict(name="CenterPoint Energy", short="CenterPoint", fixed=4.99, kwh=4.972, prefix=["1008901"], digits=22, phone="1-800-332-7143", area="the Houston metro area"),
 "oncor": dict(name="Oncor Electric Delivery", short="Oncor", fixed=4.23, kwh=6.013, prefix=["1044372","1017699"], digits=17, phone="1-888-313-4747", area="Dallas–Fort Worth, North, Central and parts of West and East Texas"),
 "aepc":  dict(name="AEP Texas Central", short="AEP Texas Central", fixed=3.24, kwh=5.690, prefix=["1003278"], digits=17, phone="1-877-373-4858", area="South Texas, including Corpus Christi, Laredo and the Rio Grande Valley"),
 "aepn":  dict(name="AEP Texas North", short="AEP Texas North", fixed=3.24, kwh=5.531, prefix=["1020404"], digits=17, phone="1-877-373-4858", area="West Texas, including Abilene and San Angelo"),
 "tnmp":  dict(name="Texas-New Mexico Power", short="TNMP", fixed=7.85, kwh=6.467, prefix=["1040051"], digits=17, phone="1-888-866-7456", area="scattered areas including Galveston, Texas City and parts of North and West Texas"),
}
CLIMATE = {
 "gulf":  ("Gulf Coast", "Hot, humid summers keep air conditioning running from May to October, so summer bills are often double spring bills. Hurricane season also makes a plan with good outage communication worth considering."),
 "north": ("North Texas", "Summer heat drives the biggest bills, but winter cold snaps can spike usage too, especially in homes with electric heat. A fixed-rate plan protects you from both seasonal peaks."),
 "central": ("Central Texas", "Long, hot summers mean most of the year's usage lands between June and September. Look at a plan's price at 2,000 kWh, not just 1,000 kWh, if your summer bills run high."),
 "west":  ("West Texas", "Dry heat and big day-night temperature swings mean steady cooling in summer and some heating in winter. Usage is lower than on the humid Gulf Coast, so check a plan's price at 500 and 1,000 kWh."),
 "south": ("South Texas", "The cooling season is the longest in the state, often from March through November. High year-round usage makes the per-kWh energy rate matter far more than any bill credit."),
}
# city, tdu, climate, note
CITIES = [
 ("Houston","cnp","gulf"),("Pasadena","cnp","gulf"),("Pearland","cnp","gulf"),("Sugar Land","cnp","gulf"),("Baytown","cnp","gulf"),
 ("Katy","cnp","gulf"),("The Woodlands","cnp","gulf"),("Missouri City","cnp","gulf"),
 ("Dallas","oncor","north"),("Fort Worth","oncor","north"),("Arlington","oncor","north"),("Plano","oncor","north"),("Irving","oncor","north"),
 ("Grand Prairie","oncor","north"),("McKinney","oncor","north"),("Mesquite","oncor","north"),("Carrollton","oncor","north"),("Richardson","oncor","north"),
 ("Tyler","oncor","north"),("Wichita Falls","oncor","north"),("Waco","oncor","central"),("Killeen","oncor","central"),("Temple","oncor","central"),
 ("Round Rock","oncor","central"),("Midland","oncor","west"),("Odessa","oncor","west"),
 ("Corpus Christi","aepc","south"),("Laredo","aepc","south"),("McAllen","aepc","south"),("Harlingen","aepc","south"),("Victoria","aepc","south"),
 ("Edinburg","aepc","south"),("Mission","aepc","south"),
 ("Abilene","aepn","west"),("San Angelo","aepn","west"),
 ("Galveston","tnmp","gulf"),("Texas City","tnmp","gulf"),
]
