"""
Data loading utilities for the TEAMS dashboard.
All data is sourced from CSV files in the data/ folder.
Uses a 3-tier architecture: National → State → Landscape → Reserve
"""
import pandas as pd
import streamlit as st
import os

# Normalize __file__ robustly using abspath over the entire joined path.
# This prevents issues where dirname() doesn't resolve `..` segments from st.navigation imports.
_THIS_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.abspath(os.path.join(_THIS_DIR, "..", "data"))


# ── National tiger population historical data (1973-2022) ──
# Source: NTCA All India Tiger Estimation reports
NATIONAL_TREND = {
    1973: 1827, 1979: 3015, 1984: 4005, 1989: 4334,
    1993: 3750, 1997: 3508, 2002: 3642,
    2006: 1411, 2010: 1706, 2014: 2226, 2018: 2967, 2022: 3682
}

# ── Tiger Reserve reference data (NTCA, 58 reserves) ──
# Geo/area metadata used for mapping; populations are from state-level imputed data
RESERVE_REF = [
    ("Corbett",                    "Uttarakhand",       29.53, 78.78,  821,  466),
    ("Ranthambore",                "Rajasthan",         26.02, 76.50,  392, 1342),
    ("Bandhavgarh",                "Madhya Pradesh",    23.72, 80.96,  716,  820),
    ("Kanha",                      "Madhya Pradesh",    22.33, 80.62,  917, 1134),
    ("Kaziranga",                  "Assam",             26.58, 93.17,  430,  500),
    ("Sundarbans",                 "West Bengal",       21.94, 88.90, 1700,  885),
    ("Sariska",                    "Rajasthan",         27.31, 76.39,  881,  332),
    ("Panna",                      "Madhya Pradesh",    24.72, 80.03,  576,  662),
    ("Tadoba-Andhari",             "Maharashtra",       20.22, 79.35,  625, 1101),
    ("Periyar",                    "Kerala",             9.47, 77.23,  881,   44),
    ("Nagarjunsagar-Srisailam",    "Andhra Pradesh",    15.85, 78.87, 3568, 2595),
    ("Namdapha",                   "Arunachal Pradesh", 27.49, 96.39, 1808,  177),
    ("Dudhwa",                     "Uttar Pradesh",     28.60, 80.60,  884, 1535),
    ("Satpura",                    "Madhya Pradesh",    22.52, 77.90,  524,  794),
    ("Melghat",                    "Maharashtra",       21.38, 77.02, 1501, 1425),
    ("Indravati",                  "Chhattisgarh",      19.17, 80.97, 1258, 1540),
    ("Buxa",                       "West Bengal",       26.73, 89.55,  391,  367),
    ("Manas",                      "Assam",             26.66, 91.00,  500, 2310),
    ("Simlipal",                   "Odisha",            21.83, 86.33,  846, 1936),
    ("Valmiki",                    "Bihar",             27.33, 83.95,  899,  798),
    ("Pench-MP",                   "Madhya Pradesh",    21.73, 79.30,  293,  465),
    ("Sathyamangalam",             "Tamil Nadu",        11.50, 77.23,  793,  614),
    ("Mudumalai",                  "Tamil Nadu",        11.57, 76.56,  321,  367),
    ("Anamalai",                   "Tamil Nadu",        10.48, 76.95,  958,  521),
    ("Kalakad-Mundanthurai",       "Tamil Nadu",         8.63, 77.32,  895,  706),
    ("Bhadra",                     "Karnataka",         13.82, 75.63,  493,  571),
    ("Dandeli-Anshi",              "Karnataka",         15.13, 74.58,  475,  382),
    ("Bandipur",                   "Karnataka",         11.67, 76.63,  872,  584),
    ("Nagarhole",                  "Karnataka",         11.93, 76.10,  644,  562),
    ("BRT Hills",                  "Karnataka",         11.98, 77.15,  539,  110),
    ("Achanakmar",                 "Chhattisgarh",      22.47, 81.73,  551,  663),
    ("Udanti-Sitanadi",            "Chhattisgarh",      20.50, 81.85,  851,  990),
    ("Palamau",                    "Jharkhand",         23.45, 84.07,  414,  610),
    ("Dampa",                      "Mizoram",           23.70, 92.38,  500,  488),
    ("Pakke",                      "Arunachal Pradesh", 26.98, 92.98,  683,  515),
    ("Nameri",                     "Assam",             26.95, 92.78,  200,  144),
    ("Orang",                      "Assam",             26.57, 92.27,   78,  413),
    ("Kamlang",                    "Arunachal Pradesh", 27.62, 96.35,  783,    0),
    ("Sahyadri",                   "Maharashtra",       17.05, 73.70,  600,  565),
    ("Navegaon-Nagzira",           "Maharashtra",       21.10, 79.95,  653,  451),
    ("Bor",                        "Maharashtra",       21.15, 78.65,  121,  684),
    ("Pilibhit",                   "Uttar Pradesh",     28.63, 80.12,  602,  191),
    ("Amrabad",                    "Telangana",         16.37, 79.28, 2166,  445),
    ("Kawal",                      "Telangana",         19.15, 79.10,  893,  123),
    ("Sanjay-Dubri",               "Madhya Pradesh",    23.22, 81.72,  831,  502),
    ("Mukundra Hills",             "Rajasthan",         24.63, 75.90,  417,  342),
    ("Rajaji",                     "Uttarakhand",       30.25, 78.10,  820,  299),
    ("Parambikulam",               "Kerala",            10.43, 76.80,  391,  252),
    ("Pench-MH",                   "Maharashtra",       21.67, 79.45,  257,  483),
    ("Ratapani",                   "Madhya Pradesh",    23.17, 77.58,  824,  688),
    ("Guru Ghasidas",              "Chhattisgarh",      23.65, 82.18, 1440,  478),
    ("Sunabeda",                   "Odisha",            19.77, 82.55,  600,  318),
    ("Tipeshwar",                  "Maharashtra",       19.88, 79.95,  149,  249),
    ("Trishna",                    "Tripura",           23.55, 91.57,  163,  331),
    ("Srivilliputhur-Megamalai",   "Tamil Nadu",         9.60, 77.63, 1249,  587),
    ("Ramgarh Vishdhari",          "Rajasthan",         25.28, 75.28,  252,  769),
    ("Dholpur-Karauli",            "Rajasthan",         26.70, 77.05,  599,  444),
    ("Ranipur",                    "Uttar Pradesh",     25.05, 80.58,  230,  299),
]


@st.cache_data(ttl=3600)
def load_reserves():
    """Return tiger reserve reference DataFrame (geo + area metadata)."""
    df = pd.DataFrame(
        RESERVE_REF,
        columns=["reserve_name", "state", "latitude", "longitude",
                 "core_area_km2", "buffer_area_km2"]
    )
    df["total_area_km2"] = df["core_area_km2"] + df["buffer_area_km2"]
    return df


@st.cache_data(ttl=3600)
def load_census():
    """Load tiger census data from imputed master CSV (state level)."""
    path = os.path.join(DATA_DIR, "tiger_census_imputed.csv")
    df = pd.read_csv(path)
    df["year"] = df["year"].astype(int)
    df["population"] = pd.to_numeric(df["population"], errors="coerce")
    df["population_imputed"] = pd.to_numeric(df["population_imputed"], errors="coerce")
    df["population_ci_lower"] = pd.to_numeric(df["population_ci_lower"], errors="coerce")
    df["population_ci_upper"] = pd.to_numeric(df["population_ci_upper"], errors="coerce")
    return df


@st.cache_data(ttl=3600)
def load_funds():
    """Load conservation funding data from imputed master CSV (state level)."""
    path = os.path.join(DATA_DIR, "funds_imputed.csv")
    df = pd.read_csv(path)
    df["year"] = df["year"].astype(int)
    for col in ["funds_central_share", "funds_release_amount",
                "funds_state_allocation", "funds_total_including_tpf"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    # Best available funding figure: prefer total_including_tpf, fallback to central_share
    df["funds_best"] = df["funds_total_including_tpf"].fillna(df["funds_central_share"])
    return df


@st.cache_data(ttl=3600)
def load_human_deaths():
    """Load human death (conflict) data from imputed master CSV (state level)."""
    path = os.path.join(DATA_DIR, "humandeaths_imputed.csv")
    df = pd.read_csv(path)
    df["year"] = df["year"].astype(int)
    df["deaths"] = pd.to_numeric(df["deaths"], errors="coerce").fillna(0)
    df["deaths_imputed"] = pd.to_numeric(df["deaths_imputed"], errors="coerce").fillna(0)
    return df


@st.cache_data(ttl=3600)
def load_tiger_deaths():
    """Load tiger mortality data from imputed master CSV (state level)."""
    path = os.path.join(DATA_DIR, "tigerdeaths_imputed.csv")
    df = pd.read_csv(path)
    df["year"] = df["year"].astype(int)
    df["total_deaths"] = pd.to_numeric(df["total_deaths"], errors="coerce").fillna(0)
    df["deaths_poaching"] = pd.to_numeric(df["deaths_poaching"], errors="coerce").fillna(0)
    df["deaths_natural_other"] = pd.to_numeric(df["deaths_natural_other"], errors="coerce").fillna(0)
    df["total_deaths_imputed"] = pd.to_numeric(df["total_deaths_imputed"], errors="coerce").fillna(0)
    return df


def get_national_trend_df():
    """Return the national tiger population trend (1973-2022) as a DataFrame."""
    df = pd.DataFrame(list(NATIONAL_TREND.items()),
                      columns=["year", "population"])
    return df.sort_values("year").reset_index(drop=True)


def get_state_census_latest(year=2022):
    """Return per-state population for a given census year."""
    census = load_census()
    return (census[census["year"] == year]
            .groupby("state", as_index=False)["population_imputed"].sum()
            .rename(columns={"population_imputed": "population"}))


def get_reserves_with_population(year=2022):
    """
    Join reserve reference with state-level population (proportionally distributed).
    Each reserve in a state gets the state's per-km2 density × reserve core area.
    """
    reserves = load_reserves()
    state_pop = get_state_census_latest(year)

    # State total core area
    state_area = (reserves.groupby("state")["core_area_km2"]
                  .sum().reset_index()
                  .rename(columns={"core_area_km2": "state_core_km2"}))

    merged = reserves.merge(state_pop, on="state", how="left")
    merged = merged.merge(state_area, on="state", how="left")
    merged["population"] = (
        (merged["population"] / merged["state_core_km2"].replace(0, 1))
        * merged["core_area_km2"]
    ).round(0).fillna(0).astype(int)
    merged["density_per_100km2"] = (
        merged["population"] / merged["total_area_km2"].replace(0, 1) * 100
    ).round(2)
    merged["note"] = "Proportional estimate from state-level census data"
    return merged


def get_imputation_explanation(method: str, ci_lower=None, ci_upper=None, ci_method=None) -> str:
    """
    Return a human-readable explanation of the imputation method used.
    Used in 'How was this estimated?' expanders across the dashboard.
    """
    methods = {
        "none":   ("Direct Observation", "This value was directly recorded from an official NTCA/WII census report with no imputation required."),
        "linear": ("Linear Interpolation", "Missing years were filled using linear interpolation between the nearest known survey values on either side."),
        "spline": ("Spline Interpolation", "A cubic spline curve was fitted through the known data points to smoothly estimate missing values, better capturing non-linear population trends."),
        "kalman": ("Kalman Filter", "A Kalman smoother was applied — a recursive Bayesian estimation technique that models population as a latent state, accounting for process noise and measurement uncertainty. Best suited where data is sparse or inconsistent across years."),
        "constant": ("Constant Value", "No variation was detected across available data; the value was held constant where observations were missing."),
    }
    key = (method or "none").strip().lower()
    name, desc = methods.get(
        key, ("Unknown Method", "The estimation method is not documented for this entry."))

    ci_text = ""
    if ci_lower is not None and ci_upper is not None and str(ci_lower) not in ("nan", ""):
        ci_text = f" The 95% confidence interval is [{float(ci_lower):.1f}, {float(ci_upper):.1f}]"
        if ci_method == "t-distribution":
            ci_text += " (computed using a t-distribution over historical observations)."
        elif ci_method == "constant":
            ci_text += " (constant — no variance in data)."

    return f"**{name}**: {desc}{ci_text}"


# ── Convenience aggregations ──

def get_states():
    """Sorted list of all states present in the census data."""
    return sorted(load_census()["state"].unique().tolist())


def get_state_summary():
    """
    Returns a summary DataFrame with latest stats per state:
    population (2022), total tiger deaths, total human deaths, total funds.
    """
    census = load_census()
    pop = (census[census["year"] == 2022]
           .groupby("state")["population_imputed"].sum()
           .reset_index().rename(columns={"population_imputed": "pop_2022"}))

    td = load_tiger_deaths()
    td_sum = (td.groupby("state")["total_deaths_imputed"].sum()
              .reset_index().rename(columns={"total_deaths_imputed": "tiger_deaths_total"}))

    hd = load_human_deaths()
    hd_sum = (hd.groupby("state")["deaths_imputed"].sum()
              .reset_index().rename(columns={"deaths_imputed": "human_deaths_total"}))

    funds = load_funds()
    f_sum = (funds.groupby("state")["funds_best"].sum()
             .reset_index().rename(columns={"funds_best": "total_funds_lakh"}))

    summary = (pop.merge(td_sum, on="state", how="left")
                  .merge(hd_sum, on="state", how="left")
                  .merge(f_sum, on="state", how="left"))
    summary = summary.fillna(0)
    return summary
