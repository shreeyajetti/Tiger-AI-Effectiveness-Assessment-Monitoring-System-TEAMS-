import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import sys, os

# Add imports for UI consistency
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from utils.map_utils import (GLOBAL_CSS, stat_card, stat_card_mini, section_header,
                              page_header, apply_dark_layout, divider,
                              ACCENT, ACCENT_LIGHT, ALERT, PRIMARY, SUCCESS, INFO, MUTED_TEXT, TEXT_COLOR)

st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

st.markdown(page_header(
    "Growth & Projections",
    "Analyze tiger population densities, future projections, and state performance.",
    "🐯"
), unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        density_df = pd.read_csv(r"C:\UNI\TEAMS\original data\Growth\tiger_density_matrix_separate_final.csv")
        proj_df = pd.read_csv(r"C:\UNI\TEAMS\original data\Growth\tiger_population_matrix_2030_projection.csv")
        thresholds_df = pd.read_excel(r"C:\UNI\TEAMS\original data\Growth\state_density_thresholds.xlsx")
        return density_df, proj_df, thresholds_df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

density_df, proj_df, thresholds_df = load_data()

if not density_df.empty and not proj_df.empty:
    # --- Methodology Section ---
    st.markdown(section_header("Methodology", "How Density and Projections Were Calculated"), unsafe_allow_html=True)
    
    badge = (f'min-width:28px;height:28px;background:{ACCENT}20;border:1px solid {ACCENT}50;'
             f'border-radius:50%;display:flex;align-items:center;justify-content:center;'
             f'color:{ACCENT};font-weight:700;font-size:0.8rem;flex-shrink:0;margin-top:2px;')
    method_html = (
        f'<div style="background:linear-gradient(135deg,rgba(27,67,50,0.7),rgba(10,31,21,0.85));'
        f'border:1px solid {ACCENT}30;border-left:4px solid {ACCENT};border-radius:12px;'
        f'padding:24px 28px;margin:12px 0 8px 0;">'
        f'<p style="color:{MUTED_TEXT};font-size:0.78rem;letter-spacing:0.12em;text-transform:uppercase;margin:0 0 18px 0;">'
        f'📐 Three-Step Process &nbsp;·&nbsp; 2006 – 2030</p>'
        f'<div style="display:flex;flex-direction:column;gap:16px;">'

        # Step 1
        f'<div style="display:flex;align-items:flex-start;gap:14px;">'
        f'<div style="{badge}">1</div>'
        f'<div><p style="margin:0;color:{TEXT_COLOR};font-weight:600;font-size:0.9rem;">National Interpolation</p>'
        f'<p style="margin:4px 0 0 0;color:{MUTED_TEXT};font-size:0.83rem;line-height:1.55;">'
        f'Census anchor points (2006–2022) were smoothed using <strong style="color:{ACCENT};">PCHIP</strong>, '
        f'producing a monotone curve that passes exactly through every known census value.</p></div></div>'

        # Step 2
        f'<div style="display:flex;align-items:flex-start;gap:14px;">'
        f'<div style="{badge}">2</div>'
        f'<div><p style="margin:0;color:{TEXT_COLOR};font-weight:600;font-size:0.9rem;">State Disaggregation</p>'
        f'<p style="margin:4px 0 0 0;color:{MUTED_TEXT};font-size:0.83rem;line-height:1.55;">'
        f'National density <code style="background:rgba(245,158,11,0.12);padding:1px 5px;border-radius:3px;'
        f'font-size:0.8rem;color:{ACCENT_LIGHT};">estimated_count = national_density × state_reserve_area</code> '
        f'A residual error at each census year <code style="background:rgba(245,158,11,0.12);padding:1px 5px;border-radius:3px;'
        f'font-size:0.8rem;color:{ACCENT_LIGHT};">error = actual - estimated</code> '
        f'was <strong style="color:{ACCENT};">PCHIP-interpolated</strong> per state across census years and added back. '
        f'A scaling constraint ensures all states sum to the national total each year.</p></div></div>'

        # Step 3
        f'<div style="display:flex;align-items:flex-start;gap:14px;">'
        f'<div style="{badge}">3</div>'
        f'<div><p style="margin:0;color:{TEXT_COLOR};font-weight:600;font-size:0.9rem;">Post-2022 Projections</p>'
        f'<p style="margin:4px 0 0 0;color:{MUTED_TEXT};font-size:0.83rem;line-height:1.55;">'
        f'Growth is capped at <strong style="color:{SUCCESS};">8% per state per year</strong>. '
        f'National mortality is disaggregated proportionally as a biological dampener, '
        f'keeping projections ecologically bounded.</p></div></div>'

        f'</div></div>'
    )
    st.markdown(method_html, unsafe_allow_html=True)
    st.markdown(divider(), unsafe_allow_html=True)



    # --- State Performance Analysis ---
    st.markdown(section_header("State Performance Analysis (Density)", "Evaluate State Carrying Capacity and Growth Potential"), unsafe_allow_html=True)
    
    states = sorted([c for c in density_df.columns if c.lower() != 'year'])
    selected_state = st.selectbox("Select a State to View Performance", states)
    
    if selected_state:
        latest_year = density_df['year'].max()
        latest_density = density_df[density_df['year'] == latest_year][selected_state].values[0]
        score = int(round(latest_density * 100))
        
        # Get threshold info
        state_info = thresholds_df[thresholds_df['State'] == selected_state]
        category = "Unknown"
        basis = "No data"
        if not state_info.empty:
            category = state_info['Category'].values[0]
            basis = state_info['Reserves Considered / Basis'].values[0]
            
        # Determine actionable insights
        if score < 5:
            perf_text = "Underperforming"
            color = ALERT # Red
            actionable = "Critical: Needs urgent prey base augmentation, habitat restoration, and anti-poaching measures."
        elif score < 10:
            perf_text = "Moderate"
            color = "#FFA07A"
            actionable = "Needs Improvement: Focus on corridor connectivity and reducing human-wildlife conflict."
        elif score < 15:
            perf_text = "Good"
            color = INFO # Blue/Light Green
            actionable = "Stable: Maintain current protection levels and monitor carrying capacity limits."
        else:
            perf_text = "Excellent (Healthy)"
            color = SUCCESS # Green
            actionable = "Optimal: Healthy carrying capacity reached. Potential source population for relocation."

        st.markdown(f"### Performance for {selected_state} in {latest_year}")
        
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(stat_card_mini("Raw Density", f"{latest_density:.4f}", PRIMARY), unsafe_allow_html=True)
        with c2:
            st.markdown(stat_card_mini("Density Score", f"{score} / 100 sqkm", ACCENT), unsafe_allow_html=True)
        with c3:
            st.markdown(stat_card_mini("Forest Category", str(category), INFO), unsafe_allow_html=True)
        with c4:
            st.markdown(stat_card_mini("Status", perf_text, color), unsafe_allow_html=True)
            
        st.markdown(f"""
        <div style="background-color: rgba(255,255,255,0.05); padding: 15px; border-left: 4px solid {color}; border-radius: 4px; margin-top: 10px;">
            <p style="margin:0; color:{TEXT_COLOR};"><strong>Reserves Considered / Basis:</strong> {basis}</p>
            <p style="margin:5px 0 0 0; color:{MUTED_TEXT};"><strong>Recommendation:</strong> {actionable}</p>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown(divider(), unsafe_allow_html=True)

    # --- Compare states charts ---
    st.markdown(section_header("Comparative Trajectories", "Compare Density and Population Trends Across States"), unsafe_allow_html=True)
    
    comp_states = st.multiselect("Select States to Compare (Max 4)", states, default=[selected_state] if selected_state else states[:2], max_selections=4)
    
    if comp_states:
        tab1, tab2 = st.tabs(["Density Trends (Historical)", "Population Projections (up to 2030)"])
        
        with tab1:
            fig_density = go.Figure()
            for s in comp_states:
                fig_density.add_trace(go.Scatter(
                    x=density_df['year'], y=density_df[s],
                    mode='lines+markers', name=s,
                    line=dict(width=3)
                ))
            apply_dark_layout(fig_density, title="Historical Density Comparison", xaxis_title="Year", yaxis_title="Tiger Density")
            st.plotly_chart(fig_density, use_container_width=True)
            
        with tab2:
            fig_proj = go.Figure()
            historical_year = 2022
            for s in comp_states:
                # Historical part
                hist_mask = proj_df['year'] <= historical_year
                fig_proj.add_trace(go.Scatter(
                    x=proj_df[hist_mask]['year'], y=proj_df[hist_mask][s],
                    mode='lines+markers', name=f"{s} (Hist)",
                    line=dict(width=3), legendgroup=s
                ))
                # Projected part
                proj_mask = proj_df['year'] >= historical_year
                fig_proj.add_trace(go.Scatter(
                    x=proj_df[proj_mask]['year'], y=proj_df[proj_mask][s],
                    mode='lines+markers', name=f"{s} (Proj)",
                    line=dict(width=3, dash='dash'), legendgroup=s, showlegend=False
                ))
                
            fig_proj.add_vrect(x0=historical_year, x1=proj_df['year'].max(),
                fillcolor=ACCENT, opacity=0.05, line_width=0, annotation_text="Projected (2024-2030)", annotation_position="top left")

            apply_dark_layout(fig_proj, title="Population Trajectories & Projections", xaxis_title="Year", yaxis_title="Estimated Tiger Count")
            st.plotly_chart(fig_proj, use_container_width=True)

    st.markdown(divider(), unsafe_allow_html=True)

    # --- Who is Ahead ---
    st.markdown(section_header("State Rankings & Future Outlook", "Which States Are Leading The Pack"), unsafe_allow_html=True)
    
    # Calculate top states by 2030 projection
    proj_2030 = proj_df[proj_df['year'] == 2030].drop(columns=['year']).iloc[0]
    top_3_proj = proj_2030.sort_values(ascending=False).head(3)
    
    # Calculate top states by latest density
    dens_latest = density_df[density_df['year'] == density_df['year'].max()].drop(columns=['year']).iloc[0]
    top_3_dens = dens_latest.sort_values(ascending=False).head(3)
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"### 🏆 Top Projected Populations (2030)")
        for rank, (state, pop) in enumerate(top_3_proj.items(), 1):
            st.markdown(stat_card(f"#{rank} {state}", f"{int(pop):,} Tigers", "Projected for 2030", ACCENT), unsafe_allow_html=True)
            
    with c2:
        st.markdown(f"### 🎯 Highest Densities (Latest)")
        for rank, (state, dens) in enumerate(top_3_dens.items(), 1):
            score = int(round(dens * 100))
            st.markdown(stat_card(f"#{rank} {state}", f"Score: {score}", f"Raw Density: {dens:.4f}", SUCCESS), unsafe_allow_html=True)

else:
    st.warning("No data available to display.")
