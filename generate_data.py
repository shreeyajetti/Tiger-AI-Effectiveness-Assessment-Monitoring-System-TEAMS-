"""Generate all dummy CSV data for the TEAMS dashboard."""
import csv, os, random, math

random.seed(42)
os.makedirs('data', exist_ok=True)

# ── 58 Tiger Reserves: (name, state, lat, lon, core_area_km2, buffer_area_km2) ──
RESERVES = [
    ("Corbett", "Uttarakhand", 29.53, 78.78, 821, 466),
    ("Ranthambore", "Rajasthan", 26.02, 76.50, 392, 1342),
    ("Bandhavgarh", "Madhya Pradesh", 23.72, 80.96, 716, 820),
    ("Kanha", "Madhya Pradesh", 22.33, 80.62, 917, 1134),
    ("Kaziranga", "Assam", 26.58, 93.17, 430, 500),
    ("Sundarbans", "West Bengal", 21.94, 88.90, 1700, 885),
    ("Sariska", "Rajasthan", 27.31, 76.39, 881, 332),
    ("Panna", "Madhya Pradesh", 24.72, 80.03, 576, 662),
    ("Tadoba-Andhari", "Maharashtra", 20.22, 79.35, 625, 1101),
    ("Periyar", "Kerala", 9.47, 77.23, 881, 44),
    ("Nagarjunsagar-Srisailam", "Andhra Pradesh", 15.85, 78.87, 3568, 2595),
    ("Namdapha", "Arunachal Pradesh", 27.49, 96.39, 1808, 177),
    ("Dudhwa", "Uttar Pradesh", 28.60, 80.60, 884, 1535),
    ("Satpura", "Madhya Pradesh", 22.52, 77.90, 524, 794),
    ("Melghat", "Maharashtra", 21.38, 77.02, 1501, 1425),
    ("Indravati", "Chhattisgarh", 19.17, 80.97, 1258, 1540),
    ("Buxa", "West Bengal", 26.73, 89.55, 391, 367),
    ("Manas", "Assam", 26.66, 91.00, 500, 2310),
    ("Simlipal", "Odisha", 21.83, 86.33, 846, 1936),
    ("Valmiki", "Bihar", 27.33, 83.95, 899, 798),
    ("Pench-MP", "Madhya Pradesh", 21.73, 79.30, 293, 465),
    ("Sathyamangalam", "Tamil Nadu", 11.50, 77.23, 793, 614),
    ("Mudumalai", "Tamil Nadu", 11.57, 76.56, 321, 367),
    ("Anamalai", "Tamil Nadu", 10.48, 76.95, 958, 521),
    ("Kalakad-Mundanthurai", "Tamil Nadu", 8.63, 77.32, 895, 706),
    ("Bhadra", "Karnataka", 13.82, 75.63, 493, 571),
    ("Dandeli-Anshi", "Karnataka", 15.13, 74.58, 475, 382),
    ("Bandipur", "Karnataka", 11.67, 76.63, 872, 584),
    ("Nagarhole", "Karnataka", 11.93, 76.10, 644, 562),
    ("BRT Hills", "Karnataka", 11.98, 77.15, 539, 110),
    ("Achanakmar", "Chhattisgarh", 22.47, 81.73, 551, 663),
    ("Udanti-Sitanadi", "Chhattisgarh", 20.50, 81.85, 851, 990),
    ("Palamau", "Jharkhand", 23.45, 84.07, 414, 610),
    ("Dampa", "Mizoram", 23.70, 92.38, 500, 488),
    ("Pakke", "Arunachal Pradesh", 26.98, 92.98, 683, 515),
    ("Nameri", "Assam", 26.95, 92.78, 200, 144),
    ("Orang", "Assam", 26.57, 92.27, 78, 413),
    ("Kamlang", "Arunachal Pradesh", 27.62, 96.35, 783, 0),
    ("Sahyadri", "Maharashtra", 17.05, 73.70, 600, 565),
    ("Navegaon-Nagzira", "Maharashtra", 21.10, 79.95, 653, 451),
    ("Bor", "Maharashtra", 21.15, 78.65, 121, 684),
    ("Pilibhit", "Uttar Pradesh", 28.63, 80.12, 602, 191),
    ("Amrabad", "Telangana", 16.37, 79.28, 2166, 445),
    ("Kawal", "Telangana", 19.15, 79.10, 893, 123),
    ("Sanjay-Dubri", "Madhya Pradesh", 23.22, 81.72, 831, 502),
    ("Mukundra Hills", "Rajasthan", 24.63, 75.90, 417, 342),
    ("Rajaji", "Uttarakhand", 30.25, 78.10, 820, 299),
    ("Parambikulam", "Kerala", 10.43, 76.80, 391, 252),
    ("Pench-MH", "Maharashtra", 21.67, 79.45, 257, 483),
    ("Ratapani", "Madhya Pradesh", 23.17, 77.58, 824, 688),
    ("Guru Ghasidas", "Chhattisgarh", 23.65, 82.18, 1440, 478),
    ("Sunabeda", "Odisha", 19.77, 82.55, 600, 318),
    ("Tipeshwar", "Maharashtra", 19.88, 79.95, 149, 249),
    ("Trishna", "Tripura", 23.55, 91.57, 163, 331),
    ("Srivilliputhur-Megamalai", "Tamil Nadu", 9.60, 77.63, 1249, 587),
    ("Ramgarh Vishdhari", "Rajasthan", 25.28, 75.28, 252, 769),
    ("Dholpur-Karauli", "Rajasthan", 26.70, 77.05, 599, 444),
    ("Ranipur", "Uttar Pradesh", 25.05, 80.58, 230, 299),
]

# ── Base tiger populations (2006) and growth multipliers ──
# Higher base = bigger reserve; growth varies to create interesting stories
BASE_POP_2006 = {
    "Corbett": 164, "Ranthambore": 41, "Bandhavgarh": 59, "Kanha": 80,
    "Kaziranga": 86, "Sundarbans": 68, "Sariska": 0, "Panna": 0,
    "Tadoba-Andhari": 43, "Periyar": 24, "Nagarjunsagar-Srisailam": 26,
    "Namdapha": 11, "Dudhwa": 58, "Satpura": 26, "Melghat": 30,
    "Indravati": 6, "Buxa": 5, "Manas": 10, "Simlipal": 18,
    "Valmiki": 12, "Pench-MP": 39, "Sathyamangalam": 25,
    "Mudumalai": 50, "Anamalai": 14, "Kalakad-Mundanthurai": 10,
    "Bhadra": 22, "Dandeli-Anshi": 8, "Bandipur": 90, "Nagarhole": 85,
    "BRT Hills": 15, "Achanakmar": 16, "Udanti-Sitanadi": 4,
    "Palamau": 7, "Dampa": 3, "Pakke": 6, "Nameri": 5, "Orang": 14,
    "Kamlang": 4, "Sahyadri": 5, "Navegaon-Nagzira": 8, "Bor": 6,
    "Pilibhit": 18, "Amrabad": 20, "Kawal": 12, "Sanjay-Dubri": 15,
    "Mukundra Hills": 0, "Rajaji": 24, "Parambikulam": 18,
    "Pench-MH": 25, "Ratapani": 11, "Guru Ghasidas": 6,
    "Sunabeda": 5, "Tipeshwar": 3, "Trishna": 2,
    "Srivilliputhur-Megamalai": 8, "Ramgarh Vishdhari": 0,
    "Dholpur-Karauli": 0, "Ranipur": 0,
}

# Growth factors per period (multiplied to base)
GROWTH_PROFILES = {
    "strong":   [1.0, 1.30, 1.70, 2.10, 2.60],
    "moderate": [1.0, 1.15, 1.35, 1.60, 1.85],
    "weak":     [1.0, 1.05, 1.10, 1.08, 1.12],
    "recovery": [1.0, 2.00, 4.00, 6.00, 8.00],  # Sariska/Panna style
    "decline":  [1.0, 0.90, 0.80, 0.70, 0.65],
    "new":      [0.0, 0.0, 0.0, 1.0, 1.5],       # Newly created reserves
}

RESERVE_GROWTH = {
    "Corbett": "strong", "Ranthambore": "strong", "Bandhavgarh": "moderate",
    "Kanha": "moderate", "Kaziranga": "moderate", "Sundarbans": "moderate",
    "Sariska": "recovery", "Panna": "recovery", "Tadoba-Andhari": "strong",
    "Periyar": "moderate", "Nagarjunsagar-Srisailam": "weak",
    "Namdapha": "decline", "Dudhwa": "moderate", "Satpura": "strong",
    "Melghat": "weak", "Indravati": "decline", "Buxa": "decline",
    "Manas": "strong", "Simlipal": "weak", "Valmiki": "moderate",
    "Pench-MP": "strong", "Sathyamangalam": "strong", "Mudumalai": "moderate",
    "Anamalai": "moderate", "Kalakad-Mundanthurai": "moderate",
    "Bhadra": "moderate", "Dandeli-Anshi": "moderate",
    "Bandipur": "strong", "Nagarhole": "strong", "BRT Hills": "weak",
    "Achanakmar": "weak", "Udanti-Sitanadi": "decline",
    "Palamau": "decline", "Dampa": "decline", "Pakke": "weak",
    "Nameri": "weak", "Orang": "moderate", "Kamlang": "decline",
    "Sahyadri": "weak", "Navegaon-Nagzira": "moderate", "Bor": "moderate",
    "Pilibhit": "strong", "Amrabad": "moderate", "Kawal": "weak",
    "Sanjay-Dubri": "moderate", "Mukundra Hills": "recovery",
    "Rajaji": "moderate", "Parambikulam": "moderate",
    "Pench-MH": "moderate", "Ratapani": "weak",
    "Guru Ghasidas": "weak", "Sunabeda": "weak",
    "Tipeshwar": "moderate", "Trishna": "decline",
    "Srivilliputhur-Megamalai": "moderate",
    "Ramgarh Vishdhari": "new", "Dholpur-Karauli": "new", "Ranipur": "new",
}

YEARS = [2006, 2010, 2014, 2018, 2022]

# ── Write reserves.csv ──
with open('data/reserves.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['reserve_name','state','latitude','longitude','core_area_km2','buffer_area_km2'])
    for r in RESERVES:
        w.writerow(r)

# ── Write census.csv ──
census_data = {}
with open('data/census.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['reserve_name','year','population'])
    for name, *_ in RESERVES:
        base = BASE_POP_2006.get(name, 10)
        profile = GROWTH_PROFILES[RESERVE_GROWTH.get(name, "moderate")]
        for i, year in enumerate(YEARS):
            pop = max(0, int(base * profile[i] + random.randint(-3, 3)))
            w.writerow([name, year, pop])
            census_data[(name, year)] = pop

# ── Write poaching.csv ──
SEVERITY_LEVELS = ["Low", "Medium", "High", "Critical"]
with open('data/poaching.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['reserve_name','year','incidents','severity'])
    for name, *_ in RESERVES:
        profile = RESERVE_GROWTH.get(name, "moderate")
        base_inc = {"strong": 2, "moderate": 4, "weak": 6, "recovery": 3,
                     "decline": 8, "new": 1}[profile]
        for year in range(2010, 2023):
            inc = max(0, base_inc + random.randint(-2, 4))
            sev = random.choices(SEVERITY_LEVELS, weights=[4,3,2,1])[0]
            if inc > 7:
                sev = random.choice(["High", "Critical"])
            w.writerow([name, year, inc, sev])

# ── Write conflict.csv ──
with open('data/conflict.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['reserve_name','year','human_deaths','cattle_kills'])
    for name, state, *_ in RESERVES:
        # Higher conflict near populated areas
        base_deaths = random.randint(0, 3)
        base_cattle = random.randint(5, 25)
        for year in range(2010, 2023):
            deaths = max(0, base_deaths + random.randint(-1, 2))
            cattle = max(0, base_cattle + random.randint(-5, 10))
            w.writerow([name, year, deaths, cattle])

# ── Write habitat.csv ──
with open('data/habitat.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['reserve_name','ndvi_2015','ndvi_2022','fragmentation_score'])
    for name, *_ in RESERVES:
        profile = RESERVE_GROWTH.get(name, "moderate")
        if profile in ("strong", "moderate"):
            ndvi_15 = round(random.uniform(0.55, 0.75), 2)
            ndvi_22 = round(ndvi_15 + random.uniform(0.01, 0.10), 2)
            frag = round(random.uniform(0.10, 0.35), 2)
        elif profile == "recovery":
            ndvi_15 = round(random.uniform(0.45, 0.60), 2)
            ndvi_22 = round(ndvi_15 + random.uniform(0.05, 0.15), 2)
            frag = round(random.uniform(0.25, 0.45), 2)
        else:
            ndvi_15 = round(random.uniform(0.50, 0.70), 2)
            ndvi_22 = round(ndvi_15 - random.uniform(0.02, 0.12), 2)
            frag = round(random.uniform(0.40, 0.70), 2)
        w.writerow([name, ndvi_15, ndvi_22, frag])

# ── Write predictions.csv ──
with open('data/predictions.csv', 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['reserve_name','predicted_population','performance_index','at_risk'])
    for name, *_ in RESERVES:
        pop_2022 = census_data.get((name, 2022), 10)
        profile = RESERVE_GROWTH.get(name, "moderate")
        if profile == "strong":
            pred = int(pop_2022 * random.uniform(1.10, 1.25))
            perf = round(random.uniform(0.75, 1.0), 2)
            risk = False
        elif profile == "moderate":
            pred = int(pop_2022 * random.uniform(1.05, 1.15))
            perf = round(random.uniform(0.55, 0.80), 2)
            risk = False
        elif profile in ("decline", "weak"):
            pred = int(pop_2022 * random.uniform(0.85, 1.02))
            perf = round(random.uniform(0.15, 0.50), 2)
            risk = True
        elif profile == "recovery":
            pred = int(pop_2022 * random.uniform(1.05, 1.20))
            perf = round(random.uniform(0.50, 0.70), 2)
            risk = False
        else:
            pred = int(pop_2022 * random.uniform(1.0, 1.30))
            perf = round(random.uniform(0.30, 0.60), 2)
            risk = random.choice([True, False])
        w.writerow([name, max(0, pred), perf, risk])

print("✅ All CSV files generated in ./data/")
