#!/usr/bin/env python3
"""
Comprehensive GK/GS categorization taxonomy for SSC CGL questions.
Maps each question to: Subject > Sub-topic > (optional) Sub-sub-topic.

Based on standard SSC CGL General Awareness syllabus.
"""

# ============== HISTORY ==============
HISTORY_SUBTOPICS = {
    "Prehistoric Period & Indus Valley Civilization": [
        "indus valley", "harappa", "mohenjo", "dholavira", "lothal", "kalibangan",
        "rchaeology", "prehistoric", "paleolithic", "neolithic", "chalcolithic",
        "bronze age", "stone age", "rock painting", "burial"
    ],
    "Vedic Age & Aryan Society": [
        "vedic", "arya", "aryans", "rigveda", "samaveda", "yajurveda", "atharvaveda",
        "upanishad", "brahmana", "aryan", "sapta sindhu", "sabha", "samiti",
        "vidatha", "kulapa", "grihapati"
    ],
    "Mahajanapadas, Buddhism & Jainism": [
        "mahajanapada", "buddha", "buddhism", "buddhist", "mahavira", "jainism", "jain",
        "sangha", "vihara", "stupa", "chaitya", "theravada", "mahayana", "vajrayana",
        "hinayana", "bodhisattva", "nirvana", "dharma", "ahimsa", "aprigraha",
        "satkaryavada", "syadvada", "anekantavada", "tirthankara", "magadha",
        "vajji", "malla", "sakyas", "licchavi", "ajatashatru", "bimbisara"
    ],
    "Mauryan Empire": [
        "maurya", "chandragupta maurya", "bindusara", "ashoka", "asoka", "kalinga",
        "megasthenes", "indica", "arthashastra", "chanakya", "kautilya",
        "dhamma", "edict", "pillar edict", "rock edict", "sanchi", "lumbini"
    ],
    "Post-Mauryan Period": [
        "shunga", "sunga", "kushana", "kushan", "kanishka", "saka", "indo-greek",
        "satavahana", "shatavahana", "menander", "dimitrios", "rudradaman",
        "junagarh", "nahapana"
    ],
    "Gupta & Post-Gupta Period": [
        "gupta", "chandragupta", "samudragupta", "kumargupta", "skandagupta",
        "harsha", "harshavardhana", "vardhana", "fa-hien", "hiuen tsang",
        "nalanda", "vallabhi", "prabhakaravardhana", "pushyabhuti",
        "kumarila", "bana", "bhanabhatta", "harshacharita", "kadambari"
    ],
    "Southern & Deccan Dynasties": [
        "pallava", "chola", "pandya", "chalukya", "rashtrakuta", "kakatiya",
        "hoysala", "yadava", "satavahana", "ikshvaku", "vellala", "vellala",
        "rajaraja chola", "rajendra chola", "mahendravarman", "narasimhavarman",
        "pulakeshin", "dantidurga", "kailasa", "ellora", "mahabalipuram",
        "kanchi", "kanchipuram"
    ],
    "Early Medieval India & Rajput Period": [
        "rajput", "pratihara", "paramara", "chauhan", "chahamana", "solanki",
        "rathore", "tomar", "kachwaha", "prithviraj", "prithvi raj",
        "muhammad ghori", "ghori", "second battle of tarain", "first battle of tarain",
        "jayachandra", "jaichand",
        "chittorgarh", "fort", "water bodies",
        "mesolithic", "microlith", "hunting"
    ],
    "Delhi Sultanate": [
        "delhi sultanate", "mamluk", "slave dynasty", "qutb-ud-din", "qutubuddin",
        "iltutmish", "razia", "razia sultana", "balban", "khilji", "jalaluddin",
        "alauddin khilji", "tughlaq", "ghiyasuddin", "muhammad bin tughlaq",
        "firuz shah", "firoz shah", "sayyid", "lodhi", "lodi", "ibrahim lodi",
        "qutb minar", "alai darwaza"
    ],
    "Vijayanagara & Bahmani Empires": [
        "vijayanagara", "vijayanagar", "sangama", "krishnadevaraya", "krishna deva raya",
        "bahmani", "bahmani kingdom", "ahmad shah wali", "firuz shah bahmani",
        "hampi", "virupaksha"
    ],
    "Mughal Empire": [
        "mughal", "babur", "humayun", "akbar", "jahangir", "shah jahan", "shahjahan",
        "aurangzeb", "babur", "panipat", "first battle of panipat",
        "todar mal", "mansabdari", "zabt", "din-i-ilahi", "sulh-i-kul",
        "ibrahim lodi", "rana pratap", "pratap", "todarmal", "tuzuk",
        "akbarnama", "badshahnama", "jabkha", "fatehpur sikri",
        "taj mahal", "red fort", "jama masjid", "buland darwaza"
    ],
    "Maratha, Sikh & Other Regional Powers": [
        "maratha", "marathas", "shivaji", "peshwa", "bajirao", "madhavrao",
        "sikh", "guru nanak", "guru gobind singh", "khalsa", "ranjit singh",
        "ahom", "ahom kingdom", "mewar", "marwar"
    ],
    "Bhakti & Sufi Movements": [
        "bhakti", "sufi", "sufism", "kabir", "raidas", "rahi", "mira", "meerabai",
        "tulsidas", "surdas", "chaitanya", "sankaradeva", "namdev", "jnaneshwar",
        "ramananda", "ramanuja", "nimbarka", "madhva", "vallabhacharya",
        "chishti", "suhrawardi", "qadiri", "naqshbandi", "muinuddin", "nisaruddin",
        "farid", "dargah", "khanqah", "silsila"
    ],
    "Advent of Europeans & Establishment of British Rule": [
        "portuguese", "dutch", "english east india", "british east india",
        "french", "carnatic war", "battle of plassey", "battle of buxar",
        "robert clive", "dupleix", "bombay", "madras", "calcutta",
        "factory", "farman", "dastak", "diwani", "treaty of allahabad",
        "ulglan", "tribal leader", "birsa munda", "santhal rebellion",
        "tribal rebellion", "kol rebellion", "munda"
    ],
    "British Acts, Policies & Land Revenue Systems": [
        "regulating act", "pitt's india act", "charter act", "government of india act",
        "permanent settlement", "zamindari", "ryotwari", "mahalwari",
        "doctrine of lapse", "subsidiary alliance", "ryotwari system",
        "cornwallis", "hastings", "wellesley", "bentinck", "dalhousie",
        "wood's dispatch", "wood dispatch", "macaulay", "minute on education",
        "1854 education", "modern education", "educational document",
        "wood's despatch"
    ],
    "Governor-Generals & Viceroys": [
        "governor general", "viceroy", "lord curzon", "lord dalhousie",
        "lord william bentinck", "lord hastings", "lord wellesley",
        "lord cornwallis", "warren hastings", "robert clive",
        "lord mountbatten", "lord linlithgow", "lord reading",
        "lord chelmsford", "lord minto", "lord ripon", "lord lytton",
        "lord hardinge", "lord auckland", "lord amherst", "lord william",
        "lord northbrook", "lawrence", "lord mayo", "lord north"
    ],
    "Revolt of 1857": [
        "revolt of 1857", "sepoy mutiny", "first war of independence",
        "mangal pandey", "bahadur shah zafar", "rzezee", "tatya tope",
        "nana sahib", "rani lakshmibai", "lakshmi bai", "begum hazrat",
        "kanpur", "meerut", "delhi", "lucknow"
    ],
    "Socio-Religious Reform Movements": [
        "brahmo samaj", "ram mohan roy", "ary samaj", "arya samaj", "dayanand",
        "dayananda", "ramakrishna", "vivekananda", "prarthana samaj",
        "atmaram pandurang", "ramanuja", "theosophical", "annie besant",
        "aligarh movement", "sir syed", "sir sayyid", "ahmed khan",
        "widow remarriage", "sati", "sati abolition", "ishwar chandra vidyasagar",
        "jotiba", "jyotiba phule", "narayana guru", "iede"
    ],
    "Indian National Congress & Early Nationalist Phase": [
        "indian national congress", "inc", "congress", "womesh chunder",
        "a o hume", "allen octavian hume", "dadabhai naoroji",
        "poonch", "pune congress", "surat split", "lucknow pact",
        "moderate", "extremist", "lal-bal-pal", "tilak", "lala lajpat rai",
        "bipin chandra pal", "gokhale", "meerut congress"
    ],
    "Revolutionary Movements": [
        "revolutionary", "bhagat singh", "azad", "chandrashekhar azad",
        "sukhdev", "rajguru", "surya sen", "master da",
        "hsra", "hindustan socialist", "kakori", "lahore conspiracy",
        "sandhya", "anushilan", "jugantar", "ghadar", "ghadr"
    ],
    "Gandhian Era & Mass Movements": [
        "gandhi", "gandhian", "mahatma", "non cooperation", "civil disobedience",
        "salt march", "dandi march", "quit india", "august kranti",
        "khilafat", "champaran", "kheda", "ahmedabad mill",
        "rowlatt", "jallianwala bagh", "swaraj", "harijan",
        "wardha", "sevagram", "sabarmati"
    ],
    "Independence, Partition & Post-Independence India": [
        "independence", "partition", "mountbatten plan", "june 3 plan",
        "radcliffe", "india independence act", "integration of states",
        "sardar patel", "states reorganization", "constitution", "republic",
        "first amendment", "nehru", "five year plan", "planning commission"
    ],
    "Indian Art, Architecture & Sculpture": [
        "stupa", "pillars", "rock cut", "cave", "caves", "chaitya", "vihara",
        "temple architecture", "nagara", "dravida", "vesara",
        "sikhara", "mandapa", "garbhagriha", "vimana", "koil",
        "gopuram", "pradakshina", "sculpture", "gandhara", "mathura",
        "amaravati", "ajanta", "ellora", "elephanta", "bagh",
        "mural", "fresco", "painting", "pahari", "rajput", "mughal painting",
        "monolithic", "rock-cut"
    ],
    "Indian Dance, Music & Performing Arts": [
        "dance", "bharatanatyam", "kathak", "kathakali", "manipuri", "odissi",
        "mohiniyattam", "sattriya", "kuchipudi", "folk dance", "bhangra",
        "garba", "ghoomar", "lavani", "bihu", "karma", "chhau",
        "music", "hindustani", "carnatic", "raga", "tala", "tabla",
        "sitar", "veena", "sarod", "flute", "shehnai",
        "gharana", "dhrupad", "khyal", "thumri", "bhajan", "qawwali",
        "laghu", "drutam", "jaati", "tishra", "chaturashra", "khanda",
        "mishra", "sankirna", "bandish", "kriti", "gamaka"
    ],
    "World History & Miscellaneous": [
        "world history", "french revolution", "american revolution",
        "industrial revolution", "russian revolution", "world war",
        "world war i", "world war ii", "cold war", "united nations",
        "league of nations", "nato", "warsaw pact", "berlin wall",
        "imperialism", "colonialism", "renaissance", "reformation"
    ]
}

# ============== GEOGRAPHY ==============
GEOGRAPHY_SUBTOPICS = {
    "Physical Geography (Geomorphology)": [
        "earth", "interior of earth", "crust", "mantle", "core",
        "plate tectonics", "continental drift", "plate boundary",
        "earthquake", "seismic wave", "richter scale", "seismograph",
        "volcano", "volcanic", "magma", "lava", "tsunami",
        "rock", "igneous", "sedimentary", "metamorphic",
        "weathering", "erosion", "mass wasting",
        "landform", "mountain", "fold mountain", "block mountain",
        "plateau", "plain", "valley", "canyon", "gorge"
    ],
    "Indian Geography (Physiography)": [
        "himalaya", "himadri", "himachal", "shivalik", "trans himalaya",
        "karakoram", "zaskar", "ladakh", "kailash",
        "northern plain", "indogangetic", "gangetic plain",
        "peninsular india", "deccan plateau", "malwa plateau",
        "chotanagpur", "meghalaya plateau", "aravalli", "vindhya",
        "satpura", "western ghats", "eastern ghats",
        "thar desert", "kutch", "ran of kutch",
        "coastal plain", "konkan", "kanara", "coromandel",
        "islands", "andaman", "nicobar", "lakshadweep"
    ],
    "Indian Rivers & Drainage System": [
        "river", "ganga", "yamuna", "ganges", "brahmaputra",
        "indus", "sutlej", "beas", "ravi", "chenab", "jhelum",
        "godavari", "krishna", "kaveri", "cauvery", "narmada",
        "tapi", "tapti", "mahanadi", "damodar", "son",
        "tributary", "confluence", "delta", "estuary", "brahmaputra",
        "ghaghara", "gandak", "kosi", "chambal", "betwa"
    ],
    "Climate, Monsoon & Weather": [
        "climate", "monsoon", "southwest monsoon", "northeast monsoon",
        "rainfall", "precipitation", "cyclone", "hurricane", "typhoon",
        "el nino", "la nina", "jet stream", "itcz",
        "weather", "humidity", "temperature", "isotherm",
        "tropical", "subtropical", "temperate", "tundra", "equatorial"
    ],
    "Indian Soils & Natural Vegetation": [
        "soil", "alluvial", "black soil", "regur", "red soil",
        "laterite", "lateritic", "arid soil", "forest soil",
        "saline", "alkaline", "peat", "marshy",
        "forest", "tropical evergreen", "tropical deciduous",
        "thorn forest", "mangrove", "montane", "alpine",
        "wildlife", "national park", "wildlife sanctuary", "biosphere reserve",
        "tiger reserve", "project tiger", "project elephant"
    ],
    "Indian Agriculture & Crops": [
        "agriculture", "kharif", "rabi", "zaid",
        "rice", "wheat", "millets", "jowar", "bajra", "ragi",
        "pulses", "gram", "tur", "arhar",
        "sugarcane", "cotton", "jute", "tea", "coffee", "rubber",
        "spices", "cardamom", "pepper", "turmeric",
        "horticulture", "green revolution", "white revolution",
        "irrigation", "canal", "tubewell", "drip irrigation"
    ],
    "Indian Minerals, Energy & Industries": [
        "mineral", "iron ore", "manganese", "bauxite", "mica",
        "copper", "gold", "silver", "zinc", "lead",
        "coal", "petroleum", "natural gas", "uranium", "thorium",
        "thermal power", "hydroelectric", "nuclear power", "solar",
        "wind energy", "tidal energy", "geothermal",
        "industry", "iron and steel", "cotton textile", "jute textile",
        "sugar industry", "cement", "fertilizer", "aluminium",
        "light industry", "heavy industry", "manufacturing"
    ],
    "Indian Transport & Communication": [
        "transport", "railway", "rail", "road", "highway",
        "golden quadrilateral", "national highway",
        "water transport", "inland waterway", "port", "major port",
        "air transport", "airport", "air india",
        "communication", "post", "telegraph", "telephone",
        "internet", "fm radio", "doordarshan", "air radio"
    ],
    "World Geography (Continents, Countries, Capitals)": [
        "continent", "asia", "africa", "europe", "north america",
        "south america", "australia", "antarctica",
        "country", "capital", "currency", "language",
        "tokyo", "beijing", "washington", "london", "paris", "rome",
        "berlin", "moscow", "ottawa", "canberra", "brasilia",
        "sea", "ocean", "pacific", "atlantic", "indian ocean",
        "arctic", "southern ocean", "mediterranean", "caribbean",
        "strait", "isthmus", "cape", "gulf", "bay"
    ],
    "Map Work & Geographical Features": [
        "latitude", "longitude", "tropic of cancer", "tropic of capricorn",
        "equator", "prime meridian", "international date line",
        "standard time", "ist", "gmt", "utc",
        "map", "scale", "contour", "projection"
    ],
    "Environmental Geography & Ecology": [
        "ecosystem", "ecology", "biosphere", "biome",
        "food chain", "food web", "trophic level",
        "biodiversity", "conservation", "pollution",
        "air pollution", "water pollution", "noise pollution",
        "global warming", "climate change", "greenhouse effect",
        "ozone layer", "acid rain", "deforestation",
        "afforestation", "desertification", "sustainable development"
    ]
}

# ============== POLITY ==============
POLITY_SUBTOPICS = {
    "Making of the Indian Constitution": [
        "constitution", "constituent assembly", "drafting committee",
        "b r ambedkar", "ambedkar", "objective resolution",
        "constitutional development", "regulating act", "pitt's india",
        "charter act", "government of india act 1935", "cabinet mission",
        "mountbatten plan", "indian independence act 1947"
    ],
    "Salient Features of the Constitution": [
        "preamble", "sovereign", "socialist", "secular", "democratic",
        "republic", "justice", "liberty", "equality", "fraternity",
        "parliamentary system", "federal system", "unitary",
        "single citizenship", "independent judiciary",
        "judicial review", "fundamental rights", "directive principles",
        "fundamental duties", "basic structure"
    ],
    "Fundamental Rights": [
        "fundamental rights", "article 12", "article 13",
        "right to equality", "article 14", "article 15", "article 16",
        "article 17", "untouchability", "article 18", "titles",
        "right to freedom", "article 19", "freedom of speech",
        "article 20", "article 21", "right to life", "article 22",
        "preventive detention", "right against exploitation",
        "article 23", "traffic in human beings", "begar",
        "article 24", "child labour",
        "right to freedom of religion", "article 25", "article 26",
        "article 27", "article 28",
        "cultural and educational rights", "article 29", "article 30",
        "right to constitutional remedies", "article 32",
        "writ", "habeas corpus", "mandamus", "certiorari", "quo warranto",
        "prohibition"
    ],
    "Directive Principles of State Policy (DPSP)": [
        "directive principles", "dpsp", "article 36", "article 37",
        "article 38", "article 39", "article 40", "village panchayat",
        "article 41", "article 42", "maternity", "article 43",
        "living wage", "article 44", "uniform civil code",
        "article 45", "free education", "article 46",
        "article 47", "prohibition", "article 48",
        "article 48a", "environment", "article 49",
        "gandhian", "socialist", "liberal intellectual"
    ],
    "Fundamental Duties": [
        "fundamental duties", "article 51a", "42nd amendment",
        "sardar swaran singh", "verma committee"
    ],
    "Union & State Executive (President, PM, Governor)": [
        "president", "election of president", "electoral college",
        "impeachment", "ordinance", "article 123",
        "vice president", "prime minister", "council of ministers",
        "cabinet", "attorney general", "article 76",
        "governor", "article 153", "chief minister",
        "advocate general"
    ],
    "Parliament & State Legislature": [
        "parliament", "lok sabha", "rajya sabha", "speaker",
        "joint sitting", "article 108", "bill", "ordinary bill",
        "money bill", "article 110", "financial bill",
        "legislative assembly", "legislative council",
        "session", "question hour", "zero hour",
        "parliamentary committee", "public accounts committee"
    ],
    "Judiciary (Supreme Court & High Courts)": [
        "supreme court", "chief justice", "high court",
        "subordinate court", "jurisdiction", "original",
        "appellate", "advisory", "writ jurisdiction",
        "judicial activism", "public interest litigation", "pil",
        "judicial review"
    ],
    "Constitutional, Statutory & Non-Statutory Bodies": [
        "election commission", "chief election commissioner",
        "finance commission", "article 280",
        "union public service commission", "upsc", "spSC",
        "state public service commission",
        "comptroller and auditor general", "cag", "article 148",
        "attorney general", "solicitor general",
        "niti aayog", "planning commission",
        "national human rights commission", "nhrc",
        "central information commission", "cic"
    ],
    "Federalism & Centre-State Relations": [
        "federalism", "centre state relations", "legislative",
        "administrative", "financial",
        "interstate council", "article 263", "zonal council",
        "schedule 7", "union list", "state list", "concurrent list",
        "residuary power"
    ],
    "Local Government & Panchayati Raj": [
        "panchayati raj", "gram panchayat", "gram sabha",
        "panchayat samiti", "zila parishad",
        "73rd amendment", "74th amendment",
        "municipality", "municipal corporation", "municipal council",
        "nagar panchayat", "ward committee"
    ],
    "Constitutional Amendments": [
        "amendment", "1st amendment", "42nd amendment", "44th amendment",
        "61st amendment", "73rd amendment", "74th amendment",
        "86th amendment", "101st amendment", "gst",
        "article 368", "simple majority", "special majority"
    ],
    "Indian Political System & Parties": [
        "political party", "national party", "state party",
        "election commission", "election symbol",
        "bjp", "congress", "left front", " BSP", "sp", "tdp",
        "election", "first past the post", "proportional representation",
        "adult franchise", "universal adult suffrage"
    ],
    "Welfare Schemes & Government Policies": [
        "mnrega", "nrega", "pm jan dhan", "jan dhan yojana",
        "ayushman bharat", "pmjay", "swachh bharat",
        "make in india", "skill india", "digital india",
        "stand up india", "startup india",
        "pm-kisan", "kisan samman", "pmay", "housing for all",
        "khelo india", "one nation one ration card",
        "pm kisan maandhan", "pm-kmy", "pmmy",
        "national education policy", "nep 2020",
        "bharatiya nagarik suraksha samhita", "bnss",
        "bharatiya nyaya samhita", "bns",
        "bharatiya sakshya adhiniyam", "bsa",
        "new criminal laws", "criminal procedure",
        "_ipc", "crpc", "evidence act",
        "national population policy", "npp 2000",
        " pm ", "scheme", "yojana", "mission",
        "stand up india", "mudra", "stand up",
        "atal pension", "national pension",
        "PMJAY", " ayushman "
    ]
}

# ============== ECONOMICS ==============
ECONOMICS_SUBTOPICS = {
    "Basics of Indian Economy": [
        "economy", "mixed economy", "planning", "five year plan",
        "five-year plan", "planning commission", "niti aayog", "gdp", "gnp", "ndp",
        "per capita income", "national income",
        "primary sector", "secondary sector", "tertiary sector",
        "liberalization", "1991 reforms", "lpg", "privatization",
        "globalization", "mnc", "multinational",
        "mahalanobis", "model", "heavy industries",
        "minimum needs programme",
        "disinvestment", "privatization", "psu",
        "navratna", "navratnas", "maharatna", "miniratna",
        "public sector", "private sector"
    ],
    "Banking & Monetary System": [
        "rbi", "reserve bank of india", "monetary policy",
        "repo rate", "reverse repo", "bank rate", "msf",
        "cash reserve ratio", "crr", "statutory liquidity ratio", "slr",
        "open market operation", "quantitative easing",
        "commercial bank", "public sector bank", "private sector bank",
        "sbi", "hdfc", "icici", "pnb",
        "payment bank", "small finance bank",
        "nabard", "sidbi", "exim bank", "rbi governor"
    ],
    "Public Finance & Budget": [
        "budget", "union budget", "railway budget",
        "finance minister", "fiscal deficit", "revenue deficit",
        "primary deficit", "frbm act",
        "direct tax", "income tax", "corporate tax",
        "indirect tax", "gst", "customs duty", "excise",
        "tax revenue", "non tax revenue", "capital receipt",
        "plan expenditure", "non plan expenditure"
    ],
    "Inflation & Price Index": [
        "inflation", "cpi", "wpi", "consumer price index",
        "wholesale price index", "deflation", "stagflation",
        "core inflation", "purchasing power", "real vs nominal",
        "phillips curve"
    ],
    "Money & Capital Market": [
        "money market", "treasury bill", "commercial paper",
        "certificate of deposit", "call money",
        "capital market", "share", "stock exchange",
        "bombay stock exchange", "bse", "national stock exchange", "nse",
        "sensex", "nifty", "sebi", "mutual fund",
        "fdi", "fii", "fpi", "ipo"
    ],
    "International Trade & Organizations": [
        "world trade organization", "wto", "imf", "world bank",
        "world bank group", "international monetary fund",
        "asian development bank", "adb", "nDB", "brics bank",
        "opec", "oecd", "g20", "g7", "g8", "saarc",
        "import", "export", "balance of trade", "balance of payment",
        "foreign exchange", "forex", "currency", "devaluation",
        "convertibility"
    ],
    "Agriculture, Industry & Service Sectors": [
        "agriculture economics", "green revolution", "white revolution",
        "blue revolution", "yellow revolution",
        "msp", "minimum support price", "procurement",
        "industrial policy", "msme", "small scale industry",
        "industrial revolution", "make in india"
    ],
    "Population, Poverty & Unemployment": [
        "population", "demographic", "census",
        "poverty line", "below poverty line", "bpl",
        "poverty ratio", "unemployment", "types of unemployment",
        "labour force", "workforce participation",
        "human development index", "hdi", "inequality", "gini coefficient"
    ]
}

# ============== GENERAL SCIENCE ==============
SCIENCE_SUBTOPICS = {
    "Physics - Mechanics & Motion": [
        "force", "motion", "velocity", "acceleration", "speed",
        "newton", "first law", "second law", "third law",
        "momentum", "inertia", "friction", "gravity", "gravitation",
        "free fall", "projectile", "circular motion", "centripetal",
        "work", "energy", "kinetic energy", "potential energy",
        "power", "conservation of energy", "conservation of momentum"
    ],
    "Physics - Light, Sound & Waves": [
        "light", "reflection", "refraction", "lens", "mirror",
        "prism", "spectrum", "rainbow", "total internal reflection",
        "sound", "wave", "longitudinal wave", "transverse wave",
        "frequency", "wavelength", "amplitude", "pitch",
        "ultrasonic", "infrasound", "sonar", "echo", "reverberation",
        "doppler effect", "resonance"
    ],
    "Physics - Heat, Electricity & Magnetism": [
        "heat", "temperature", "conduction", "convection", "radiation",
        "thermal expansion", "specific heat", "latent heat",
        "calorimetry", "thermodynamics",
        "electricity", "current", "voltage", "resistance",
        "ohm's law", "series", "parallel", "circuit",
        "ampere", "volt", "watt", "kilowatt",
        "magnetism", "magnetic field", "electromagnet",
        "electromagnetic induction", "transformer", "motor", "generator"
    ],
    "Physics - Modern Physics & Nuclear": [
        "atom", "nucleus", "proton", "neutron", "electron",
        "atomic number", "mass number", "isotope", "isobar",
        "radioactivity", "alpha", "beta", "gamma",
        "nuclear fission", "nuclear fusion",
        "x-ray", "cathode ray", "photoelectric", "einstein",
        "quantum", "planck", "dual nature", "uncertainty"
    ],
    "Chemistry - Matter & Atomic Structure": [
        "matter", "atom", "molecule", "element", "compound", "mixture",
        "atomic structure", "atomic number", "mass number",
        "bohr model", "quantum number", "electron configuration",
        "periodic table", "periodic classification", "mendeleev",
        "modern periodic law", "groups", "periods"
    ],
    "Chemistry - Chemical Bonding & Reactions": [
        "chemical bond", "ionic bond", "covalent bond", "metallic bond",
        "hydrogen bond", "vsepr", "lewis structure",
        "chemical reaction", "combination", "decomposition",
        "displacement", "double displacement",
        "oxidation", "reduction", "redox", "oxidizing agent",
        "catalyst", "exothermic", "endothermic",
        "acids", "bases", "salts", "ph", "indicators",
        "neutralization"
    ],
    "Chemistry - Industrial & Organic Chemistry": [
        "coal", "petroleum", "natural gas", "fractional distillation",
        "carbon", "hydrocarbon", "alkane", "alkene", "alkyne",
        "alcohol", "phenol", "ether", "aldehyde", "ketone",
        "carboxylic acid", "ester", "polymer", "polymerization",
        "plastic", "synthetic fibre", "rayon", "nylon", "polyester",
        "fertilizer", "urea", "cement", "glass", "steel"
    ],
    "Biology - Cell & Genetics": [
        "cell", "cell theory", "prokaryotic", "eukaryotic",
        "cell organelle", "nucleus", "mitochondria", "ribosome",
        "endoplasmic reticulum", "golgi apparatus", "lysosome",
        "chloroplast", "vacuole", "cell membrane", "cell wall",
        "cell division", "mitosis", "meiosis",
        "genetics", "heredity", "gene", "dna", "rna",
        "chromosome", "allele", "dominant", "recessive",
        "mendel", "mutation"
    ],
    "Biology - Plant Physiology": [
        "plant", "photosynthesis", "respiration", "transpiration",
        "translocation", "ascent of sap",
        "root", "stem", "leaf", "flower", "fruit", "seed",
        "tissue", "xylem", "phloem", "parenchyma", "collenchyma",
        "sclerenchyma", "meristem",
        "plant hormone", "auxin", "gibberellin", "cytokinin",
        "ethylene", "abscisic acid"
    ],
    "Biology - Human Physiology": [
        "human body", "digestive system", "digestion",
        "respiratory system", "respiration", "lung", "breathing",
        "circulatory system", "heart", "blood", "blood vessel",
        "artery", "vein", "capillary",
        "excretory system", "kidney", "urine", "nephron",
        "nervous system", "brain", "spinal cord", "neuron",
        "endocrine system", "hormone", "pituitary", "thyroid",
        "adrenal", "pancreas", "insulin",
        "reproductive system", "reproduction",
        "skeletal system", "bone", "muscle",
        "sense organ", "eye", "ear", "nose", "tongue", "skin"
    ],
    "Biology - Health, Disease & Nutrition": [
        "disease", "bacteria", "virus", "fungus", "protozoa",
        "vaccination", "vaccine", "immunity", "antibiotic",
        "infection", "communicable", "non communicable",
        "polio", "smallpox", "tuberculosis", "tb", "cancer", "aids", "hiv",
        "diabetes", "malaria", "dengue", "cholera",
        "nutrition", "carbohydrate", "protein", "fat", "vitamin",
        "mineral", "balanced diet", "malnutrition",
        "deficiency disease", "scurvy", "rickets", "goitre", "anaemia"
    ],
    "Biology - Ecology & Environment": [
        "ecosystem", "ecology", "food chain", "food web",
        "producer", "consumer", "decomposer",
        "trophic level", "energy flow", "biogeochemical cycle",
        "carbon cycle", "nitrogen cycle", "water cycle",
        "biodiversity", "conservation", "endangered species",
        "national park", "wildlife sanctuary"
    ]
}

# ============== STATIC GK ==============
STATIC_GK_SUBTOPICS = {
    "Books & Authors": [
        "author", "writer", "novel", "book", "autobiography",
        "written by", "penned by", "authored", "composed by",
        "geetanjali", "gitanjali", "tagore", "premchand",
        "midnight's children", "salman rushdie",
        "vine of desire", "chitra banerjee", "divakaruni",
        "the god of small things", "arundhati roy",
        "train to pakistan", "khushwant singh",
        "discovery of india", "nehru",
        "hind swaraj", "gandhi",
        "indian struggle", "subhas chandra bose",
        "raghuvamsa", "kumara", "meghaduta", "kalidasa",
        "kasturi", "katha", "kavya"
    ],
    "Awards & Honours": [
        "nobel prize", "nobel", "padma", "padma shri", "padma bhushan",
        "padma vibhushan", "bharat ratna", "gandhi peace prize",
        "sahitya akademi", "jnanpith", "booker prize", "pulitzer",
        "national film award", "oscars", "academy award",
        "arjuna award", "khel ratna", "dronacharya",
        "magsaysay", "ramon magsaysay", " Pulitzer"
    ],
    "Sports & Games": [
        "sport", "sports", "olympic", "olympics", "asian games",
        "commonwealth games", "world cup", "cricket", "football",
        "hockey", "tennis", "badminton", "chess", "wrestling",
        "boxing", "athletics", "swimming", "shooting", "archery",
        "kabaddi", "kho kho", "judo", "karate", "taekwondo", "taekwon-do",
        "gymnastics", "cycling", "weightlifting", "rowing",
        "fifa", "ioc", "bcci", "icc", "world championship",
        "cross country", "marathon", "relay race",
        "pole vault", "javelin", "long jump", "high jump",
        "basketball", "hoop", "shot put", "discus", "hammer throw",
        "vault", "sprint", "hurdles", "steeplechase",
        "santosh trophy", "football",
        "nada", "anti-doping", "wada",
        "korean terms", "match column"
    ],
    "Festivals & Fairs of India": [
        "festival", "diwali", "holi", "dussehra", "navratri",
        "durga puja", "ganesh chaturthi", "janmashtami",
        "ram navami", "shivratri", "raksha bandhan", "rakhi",
        "baisakhi", "pongal", "onam", "makar sankranti",
        "lohri", "bihu", "eid", "christmas", "easter",
        "mahavir jayanti", "budha jayanti", "guru nanak jayanti",
        "goncha", "bastar", "kumbh mela", "pushkar fair",
        "hemis festival", "baisakhi", "repellam",
        "kharchi puja", "tripura", "garia puja",
        "chapchar kut", "moatsu", "wangala",
        "bathukamma", "bonalu", "samakka saralamma",
        "sammakka", "medaram jathara",
        "nauchandi", "surajkund", "mela",
        "fair", "puja", "jatra", "utsav"
    ],
    "Indian Dance Forms": [
        "bharatanatyam", "kathak", "kathakali", "manipuri",
        "odissi", "mohiniyattam", "sattriya", "kuchipudi",
        "folk dance", "bhangra", "garba", "ghoomar", "lavani",
        "bihu dance", "karma dance", "chhau dance",
        "ghumar", "kalbelia", "bardo chham",
        "burrakatha", "tamasha", "thoda", "tippani",
        "martial art", "kalaripayattu", "silambam", "thang-ta",
        "urumi", "paika", "mallakhamb", "gatka",
        "folk theatre", "classical dance", "dance form"
    ],
    "Indian Music (Hindustani & Carnatic)": [
        "hindustani music", "carnatic music", "raga", "tala",
        "tabla", "sitar", "veena", "sarod", "sarangi", "flute",
        "shehnai", "mridangam", "ghatam", "kartal", "manjira",
        "dhrupad", "khyal", "thumri", "bhajan", "qawwali",
        "gharana", "laghu", "drutam", "jaati", "bandish",
        "kriti", "varnam", "tillana", "alapana"
    ],
    "Temple Architecture & Sculpture": [
        "temple", "nagara", "dravida", "vesara", "sikhara",
        "vimana", "mandapa", "garbhagriha", "gopuram",
        "pradakshina patha", "koil",
        "cave temple", "rock cut", "monolithic",
        "ajanta", "ellora", "elephanta",
        "kailasa", "mahabalipuram", "kanchi", "kanchipuram",
        "vijayanagara", "hampi", "virupaksha",
        "latina", "phamsana", "valabhi", "rekha", "deul",
        "pidha", "khakhara", "bhumija",
        "shikara", "amalaka", "kalasha",
        "mukha", "ardha", "maha",
        "purana qila", "old fort", "qila", "fort",
        "capuchin church", "church", "cathedral",
        "chittorgarh", "chittor", "fort",
        "double-storeyed", "gate", "pillar", "column"
    ],
    "Paintings & Art Forms": [
        "painting", "mural", "fresco", "miniature painting",
        "mughal painting", "rajput painting", "pahari painting",
        "madhubani", "mithila", "warli", "pattachitra",
        "tanjore painting", "kalamkari"
    ],
    "Important Days & Dates": [
        "important day", "world day", "international day",
        "national day", "world health day", "world environment day",
        "world earth day", "yoga day", "international yoga day",
        "world women day", "international women's day",
        "world water day", "world population day",
        "world aids day", "world tuberculosis day",
        "world blood donor day", "world habitat day",
        "world food day", "world teacher's day",
        "national science day", "national education day",
        "national youth day", "national sports day",
        "republic day", "independence day", "gandhi jayanti"
    ],
    "International Organizations & Headquarters": [
        "united nations", "un", "general assembly", "security council",
        "unesco", "who", "world health organization", "unicef",
        "world bank", "imf", "wto", "fao", "ilo", "iaea",
        "nato", "saarc", "asean", "eu", "european union",
        "g7", "g20", "opec", "oecd", "brics",
        "headquarters", "Geneva", "new york", "paris", "rome"
    ],
    "National Symbols & Insignia": [
        "national flag", "national emblem", "national anthem",
        "national song", "national animal", "national bird",
        "national flower", "national tree", "national fruit",
        "national river", "national aquatic animal",
        "national calendar", "national currency",
        "ashoka chakra", "tricolour", "tiranga"
    ],
    "Indian Railways, Metro & Transport": [
        "railway", "indian railway", "railway minister",
        "first train", "vande bharat", "bullet train",
        "metro", "delhi metro", "railway zone",
        "railway station", "longest platform",
        "national highway", "expressway"
    ],
    "Space & Defence": [
        "isro", "indian space research organisation",
        "nasa", "esa", "roscosmos", "cnsa",
        "chandrayaan", "mangalyaan", "gaganyaan", "aryabhata",
        "pslv", "gslv", "slv", "sslv",
        "defence", "indian army", "indian navy", "indian air force",
        "drdo", "agni", "prithvi", "akash", "nag", "trishul",
        "tejas", "ins vikrant", "ins vishal", "submarine",
        "nisar", "orbit", "satellite", "spacecraft",
        "geo", "gto", "leo", "meo", "polar", "sun-sync", "sun synchronous",
        "aditya-l1", "aditya l1", "l1 point", "lagrange",
        "green hydrogen", "hydrogen hub",
        " gslv ", " pslv ", " sslv ", " gslv",
        "quad", "quadrilateral", "security dialogue"
    ],
    "Science & Technology Current Developments": [
        "artificial intelligence", "ai", "machine learning",
        "blockchain", "cryptocurrency", "bitcoin", "5g", "6g",
        "quantum computing", "internet of things", "iot",
        "biotechnology", "nanotechnology", "robotics",
        "3d printing", "drone"
    ]
}

# ============== CURRENT AFFAIRS ==============
CURRENT_AFFAIRS_SUBTOPICS = {
    "National Affairs & Government Schemes": [
        "government scheme", "policy", "ministry", "minister",
        "parliament", "bill passed", "act passed",
        "cabinet", "prime minister", "president",
        "supreme court verdict", "high court",
        "national policy", "launch", "inauguration"
    ],
    "International Affairs & Treaties": [
        "summit", "g20", "g7", "brics", "saarc", "asean",
        "uno", "united nations", "treaty", "agreement",
        "visit", "modi", "biden", "trump", "xi jinping",
        "russia", "ukraine", "israel", "palestine",
        "war", "ceasefire",
        "quad", "quadrilateral security",
        "nato", "security council"
    ],
    "Economy & Business Current": [
        "gdp growth", "rbi policy", "repo rate", "inflation",
        "budget 2024", "budget 2025", "economic survey",
        "fortune 500", "forbes list", "richest person",
        "ipo", "merger", "acquisition", "billionaire"
    ],
    "Sports Current Affairs": [
        "olympics 2024", "paris olympics", "asian games",
        "commonwealth games", "world championship 2024", "2025",
        "won gold", "won silver", "won bronze",
        "neeraj chopra", "virat kohli", "rohit sharma",
        "world cup", "ipl", "ashes"
    ],
    "Awards & Honours Current": [
        "nobel prize 2024", "nobel prize 2025",
        "padma awards", "bharat ratna",
        "magsaysay award", "booker prize",
        "ramanujan award", "right livelihood"
    ],
    "Persons in News & Obituaries": [
        "passed away", "died", "obituary",
        "appointed", "resigned", "sworn in",
        "chief justice", "governor", "minister",
        "new ceo", "new chairman"
    ],
    "Defence & Space Current": [
        "missile test", "satellite launch", "isro mission",
        "agni missile", "tejas", " INS ",
        "exercise", "joint exercise", "military exercise",
        "yudh", "varuna", "indra", "malabar"
    ],
    "Reports, Indices & Rankings": [
        "global index", "report", "ranking",
        "world happiness index", "global peace index",
        "human development index", "hdi ranking",
        "global competitiveness", "press freedom index",
        "corruption perception index", "global hunger index",
        "oxford economics", "global cities index"
    ]
}

# Main taxonomy
TAXONOMY = {
    "History": HISTORY_SUBTOPICS,
    "Geography": GEOGRAPHY_SUBTOPICS,
    "Polity": POLITY_SUBTOPICS,
    "Economics": ECONOMICS_SUBTOPICS,
    "General Science": SCIENCE_SUBTOPICS,
    "Static GK": STATIC_GK_SUBTOPICS,
    "Current Affairs": CURRENT_AFFAIRS_SUBTOPICS,
}

if __name__ == "__main__":
    total = 0
    for subj, subs in TAXONOMY.items():
        print(f"\n{subj}:")
        for sub, kws in subs.items():
            print(f"  - {sub}: {len(kws)} keywords")
            total += len(kws)
    print(f"\nTotal sub-topics: {sum(len(s) for s in TAXONOMY.values())}")
    print(f"Total keywords: {total}")
