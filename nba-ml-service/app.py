import os
import streamlit as st
import requests
import plotly.graph_objects as go
from roster_service import RosterService
from cba_rules import check_salary_legality

API_BASE_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

# 1. Page Configuration
st.set_page_config(
    page_title="NBA Trade Machine & Evaluator",
    page_icon="🏀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Team Branding Palette & Official NBA IDs
NBA_TEAM_DATA = {
    "ATL": {"primary": "#E03A3E", "secondary": "#C1D32F", "name": "Atlanta Hawks", "id": 1610612737},
    "BOS": {"primary": "#007A33", "secondary": "#BA9653", "name": "Boston Celtics", "id": 1610612738},
    "BKN": {"primary": "#000000", "secondary": "#FFFFFF", "name": "Brooklyn Nets", "id": 1610612751},
    "CHA": {"primary": "#1D1160", "secondary": "#00788C", "name": "Charlotte Hornets", "id": 1610612766},
    "CHI": {"primary": "#CE1141", "secondary": "#000000", "name": "Chicago Bulls", "id": 1610612741},
    "CLE": {"primary": "#860038", "secondary": "#041E42", "name": "Cleveland Cavaliers", "id": 1610612739},
    "DAL": {"primary": "#00538C", "secondary": "#002B5E", "name": "Dallas Mavericks", "id": 1610612742},
    "DEN": {"primary": "#0E2240", "secondary": "#FEC524", "name": "Denver Nuggets", "id": 1610612743},
    "DET": {"primary": "#C8102E", "secondary": "#1D42BA", "name": "Detroit Pistons", "id": 1610612765},
    "GSW": {"primary": "#1D428A", "secondary": "#FFC72C", "name": "Golden State Warriors", "id": 1610612744},
    "HOU": {"primary": "#CE1141", "secondary": "#000000", "name": "Houston Rockets", "id": 1610612745},
    "IND": {"primary": "#002D62", "secondary": "#FDBB30", "name": "Indiana Pacers", "id": 1610612754},
    "LAC": {"primary": "#C8102E", "secondary": "#1D428A", "name": "LA Clippers", "id": 1610612746},
    "LAL": {"primary": "#552583", "secondary": "#FDB927", "name": "Los Angeles Lakers", "id": 1610612747},
    "MEM": {"primary": "#5D76A9", "secondary": "#12173F", "name": "Memphis Grizzlies", "id": 1610612763},
    "MIA": {"primary": "#98002E", "secondary": "#F9A01B", "name": "Miami Heat", "id": 1610612748},
    "MIL": {"primary": "#00471B", "secondary": "#EEE1C6", "name": "Milwaukee Bucks", "id": 1610612749},
    "MIN": {"primary": "#0C2340", "secondary": "#236192", "name": "Minnesota Timberwolves", "id": 1610612750},
    "NOP": {"primary": "#0C2340", "secondary": "#C8102E", "name": "New Orleans Pelicans", "id": 1610612740},
    "NYK": {"primary": "#006BB6", "secondary": "#F58426", "name": "New York Knicks", "id": 1610612752},
    "OKC": {"primary": "#007AC1", "secondary": "#EF3B24", "name": "Oklahoma City Thunder", "id": 1610612760},
    "ORL": {"primary": "#0077C0", "secondary": "#C4CED4", "name": "Orlando Magic", "id": 1610612753},
    "PHI": {"primary": "#006BB6", "secondary": "#ED174C", "name": "Philadelphia 76ers", "id": 1610612755},
    "PHX": {"primary": "#1D1160", "secondary": "#E56020", "name": "Phoenix Suns", "id": 1610612756},
    "POR": {"primary": "#E03A3E", "secondary": "#000000", "name": "Portland Trail Blazers", "id": 1610612757},
    "SAC": {"primary": "#5A2D81", "secondary": "#63727A", "name": "Sacramento Kings", "id": 1610612758},
    "SAS": {"primary": "#C4CED4", "secondary": "#000000", "name": "San Antonio Spurs", "id": 1610612759},
    "TOR": {"primary": "#CE1141", "secondary": "#000000", "name": "Toronto Raptors", "id": 1610612761},
    "UTA": {"primary": "#002B5C", "secondary": "#F9A01B", "name": "Utah Jazz", "id": 1610612762},
    "WAS": {"primary": "#002B5C", "secondary": "#E31837", "name": "Washington Wizards", "id": 1610612764},
}

# 3. Custom CSS
st.markdown("""
<style>
    .trade-card {
        background-color: #1a1c24;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 12px;
        border: 1px solid #2e3440;
    }
    .player-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
    }
    .badge-container {
        display: flex;
        flex-wrap: wrap;
        gap: 6px;
        margin-top: 4px;
    }
    .stat-badge {
        background-color: #2b303c;
        color: #e5e9f0;
        font-size: 0.82rem;
        font-weight: 600;
        padding: 3px 8px;
        border-radius: 6px;
        border: 1px solid #3b4252;
    }
    .team-header-box {
        padding: 12px 18px;
        border-radius: 10px;
        margin-bottom: 15px;
        color: #ffffff;
        font-weight: 700;
        font-size: 1.25rem;
        display: flex;
        align-items: center;
        gap: 12px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
    }
    .verdict-banner {
        border-radius: 10px;
        padding: 18px;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 20px;
    }
</style>
""", unsafe_allow_html=True)

# 4. Service Initialization
@st.cache_resource
def load_roster_service():
    return RosterService()

try:
    roster = load_roster_service()
    teams = roster.get_teams()
except Exception as e:
    st.error(f"Failed to load roster dataset: {e}")
    st.stop()

def get_logo_url(team_abbr: str) -> str:
    info = NBA_TEAM_DATA.get(team_abbr)
    return f"https://cdn.nba.com/logos/nba/{info['id']}/global/L/logo.svg" if info else ""

def render_player_card(player_data):
    name = player_data["name"]
    pts = player_data["PTS"]
    reb = player_data["REB"]
    ast = player_data["AST"]
    mins = player_data["MIN"]
    age = player_data["AGE"]
    
    return f"""
    <div class="trade-card">
        <div class="player-title">👤 {name}</div>
        <div class="badge-container">
            <span class="stat-badge">Age: {int(age)}</span>
            <span class="stat-badge">{pts:.1f} PPG</span>
            <span class="stat-badge">{reb:.1f} RPG</span>
            <span class="stat-badge">{ast:.1f} APG</span>
            <span class="stat-badge">{mins:.1f} MPG</span>
        </div>
    </div>
    """

def create_radar_chart(team_a_name, team_a_stats, team_b_name, team_b_stats):
    categories = ['PTS', 'REB', 'AST', 'STL', 'BLK']
    
    vals_a = [sum(p[cat] for p in team_a_stats) / len(team_a_stats) for cat in categories]
    vals_b = [sum(p[cat] for p in team_b_stats) / len(team_b_stats) for cat in categories]
    
    vals_a.append(vals_a[0])
    vals_b.append(vals_b[0])
    radar_categories = categories + [categories[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=vals_a, theta=radar_categories, fill='toself', name=f"{team_a_name} Outgoing",
        line=dict(color='#007AC1')
    ))
    fig.add_trace(go.Scatterpolar(
        r=vals_b, theta=radar_categories, fill='toself', name=f"{team_b_name} Outgoing",
        line=dict(color='#EF3B24')
    ))

    max_val = max(max(vals_a), max(vals_b), 1.0)
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True, range=[0, max_val * 1.25])),
        showlegend=True,
        template="plotly_dark",
        margin=dict(l=40, r=40, t=30, b=30),
        height=360
    )
    return fig

# 5. Header
st.title("🏀 NBA Trade Machine & Player Impact Evaluator")
st.markdown("Deterministic CBA salary matching combined with regularized machine learning impact forecasting.")

# 6. Team Columns
col_a, col_b = st.columns(2)

with col_a:
    default_a_idx = teams.index("DAL") if "DAL" in teams else 0
    team_a = st.selectbox("Select Team A", teams, index=default_a_idx, key="team_a_select")
    team_a_info = NBA_TEAM_DATA.get(team_a, {"primary": "#1D428A", "secondary": "#002B5E", "name": team_a})
    
    st.markdown(
        f"""
        <div class="team-header-box" style="background: linear-gradient(135deg, {team_a_info['primary']}, {team_a_info['secondary']});">
            <img src="{get_logo_url(team_a)}" width="45" height="45" style="vertical-align:middle;"/>
            <span>{team_a_info['name']} ({team_a})</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    team_a_players = roster.get_players_by_team(team_a)
    selected_a = st.multiselect(
        f"Select outgoing players from {team_a}:",
        [p["name"] for p in team_a_players],
        key="trade_a_players"
    )
    
    if selected_a:
        st.write("##### Assets on the Block:")
        for name in selected_a:
            p_payload = roster.get_player_payload(name)
            if p_payload:
                st.markdown(render_player_card(p_payload), unsafe_allow_html=True)

with col_b:
    default_b_idx = teams.index("LAL") if "LAL" in teams else (1 if len(teams) > 1 else 0)
    team_b = st.selectbox("Select Team B", teams, index=default_b_idx, key="team_b_select")
    team_b_info = NBA_TEAM_DATA.get(team_b, {"primary": "#552583", "secondary": "#FDB927", "name": team_b})
    
    st.markdown(
        f"""
        <div class="team-header-box" style="background: linear-gradient(135deg, {team_b_info['primary']}, {team_b_info['secondary']});">
            <img src="{get_logo_url(team_b)}" width="45" height="45" style="vertical-align:middle;"/>
            <span>{team_b_info['name']} ({team_b})</span>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    team_b_players = roster.get_players_by_team(team_b)
    selected_b = st.multiselect(
        f"Select outgoing players from {team_b}:",
        [p["name"] for p in team_b_players],
        key="trade_b_players"
    )
    
    if selected_b:
        st.write("##### Assets on the Block:")
        for name in selected_b:
            p_payload = roster.get_player_payload(name)
            if p_payload:
                st.markdown(render_player_card(p_payload), unsafe_allow_html=True)

# 7. Financial & CBA Settings
with st.expander("💼 Salary Matching & Apron Settings", expanded=False):
    s_col1, s_col2 = st.columns(2)
    with s_col1:
        team_a_status = st.selectbox(f"{team_a} Tax Apron Tier", ["NON_TAXPAYER", "FIRST_APRON", "SECOND_APRON"], key="tax_a")
        team_a_salary = st.number_input(f"{team_a} Outgoing Payroll ($M)", min_value=0.0, value=25.0, step=1.0)
    with s_col2:
        team_b_status = st.selectbox(f"{team_b} Tax Apron Tier", ["NON_TAXPAYER", "FIRST_APRON", "SECOND_APRON"], key="tax_b")
        team_b_salary = st.number_input(f"{team_b} Outgoing Payroll ($M)", min_value=0.0, value=25.0, step=1.0)

st.write("")

# 8. Evaluation Trigger
if st.button("⚡ Evaluate Trade Package", type="primary", use_container_width=True):
    if not selected_a or not selected_b:
        st.warning("Please choose at least one player from each team to construct a trade.")
    elif team_a == team_b:
        st.error("Teams must be different to complete a trade.")
    else:
        # Check CBA matching rules
        cba_check_a = check_salary_legality(team_a_salary, team_b_salary, team_a_status)
        cba_check_b = check_salary_legality(team_b_salary, team_a_salary, team_b_status)
        cba_legal = cba_check_a["is_legal"] and cba_check_b["is_legal"]

        # Build payload with non-optional AGE
        team_a_payload = [roster.get_player_payload(name) for name in selected_a]
        team_b_payload = [roster.get_player_payload(name) for name in selected_b]

        api_url = f"{API_BASE_URL}/api/ml/evaluate-trade"
        request_body = {
            "team_a_giving": team_a_payload,
            "team_b_giving": team_b_payload
        }

        try:
            with st.spinner("Executing model inference and evaluating trade equity..."):
                response = requests.post(api_url, json=request_body, timeout=60)

            if response.status_code == 200:
                data = response.json()
                verdict = data["verdict"]
                score = data["fairness_score"]

                # Verdict Banner Styling
                if verdict == "FAIR":
                    banner_bg = "rgba(46, 204, 113, 0.15)"
                    banner_border = "#2ecc71"
                    status_text = "🟢 FAIR TRADE"
                elif verdict == "SLIGHTLY_UNEVEN":
                    banner_bg = "rgba(241, 196, 15, 0.15)"
                    banner_border = "#f1c40f"
                    status_text = "🟡 SLIGHTLY UNEVEN"
                else:
                    banner_bg = "rgba(231, 76, 60, 0.15)"
                    banner_border = "#e74c3c"
                    status_text = "🔴 UNFAIR / LOPSIDED"

                st.markdown(
                    f"""
                    <div class="verdict-banner" style="background-color: {banner_bg}; border: 2px solid {banner_border};">
                        <h2 style="margin: 0; color: #ffffff;">{status_text}</h2>
                        <h4 style="margin: 5px 0 0 0; color: #d8dee9;">Trade Equity Score: {score:.1f}%</h4>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                # Context Imbalance Warnings
                avg_age_a = sum(p["AGE"] for p in team_a_payload) / len(team_a_payload)
                avg_age_b = sum(p["AGE"] for p in team_b_payload) / len(team_b_payload)
                
                if avg_age_a - avg_age_b >= 6.0:
                    st.info(f"⚠️ **Age Imbalance:** {team_b} is trading away significantly younger talent (avg {avg_age_b:.1f}) for veteran production (avg {avg_age_a:.1f}).")
                elif avg_age_b - avg_age_a >= 6.0:
                    st.info(f"⚠️ **Age Imbalance:** {team_a} is trading away significantly younger talent (avg {avg_age_a:.1f}) for veteran production (avg {avg_age_b:.1f}).")

                # Metrics Row
                m1, m2, m3, m4 = st.columns(4)
                m1.metric(f"{team_a} Total Impact Out", f"{data['team_a_total_impact']:.1f}")
                m2.metric(f"{team_b} Total Impact Out", f"{data['team_b_total_impact']:.1f}")
                m3.metric("Impact Differential", f"{data['impact_differential']:.1f}")
                m4.metric("CBA Status", "PASS" if cba_legal else "FAIL", delta=None if cba_legal else "-Violation")

                # Detailed Tabs
                tab1, tab2 = st.tabs(["📊 Impact & Head-to-Head Stats", "💼 CBA Salary Breakdown"])
                
                with tab1:
                    st.write("##### Package Comparison Radar")
                    st.plotly_chart(
                        create_radar_chart(team_a, team_a_payload, team_b, team_b_payload),
                        use_container_width=True
                    )
                    
                    r1, r2 = st.columns(2)
                    with r1:
                        st.write(f"**{team_a} Outgoing Breakdown:**")
                        st.dataframe(data["team_a_breakdown"], hide_index=True, use_container_width=True)
                    with r2:
                        st.write(f"**{team_b} Outgoing Breakdown:**")
                        st.dataframe(data["team_b_breakdown"], hide_index=True, use_container_width=True)

                with tab2:
                    if cba_legal:
                        st.success("✅ Both teams satisfy salary matching thresholds under their respective tax aprons.")
                    else:
                        st.error("❌ Trade fails NBA CBA financial requirements.")
                    
                    st.write(f"• **{team_a} ({team_a_status}):** {cba_check_a['rule_note']}")
                    st.write(f"• **{team_b} ({team_b_status}):** {cba_check_b['rule_note']}")

            else:
                st.error(f"FastAPI Service Error ({response.status_code}): {response.text}")

        except requests.exceptions.ConnectionError:
            st.error("Could not reach the API service. Locally, make sure `python3 -m uvicorn main:app --reload` is running on port 8000. When deployed, check that API_URL is set correctly.")
        except requests.exceptions.Timeout:
            st.error("The API service timed out. If it was idle, it may still be waking up, so try again in a minute.")
        except Exception as err:
            st.error(f"Evaluation failed: {err}")