import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- CONFIG ---------------- #

st.set_page_config(
    page_title="IPL Analytics Dashboard",
    page_icon="🏏",
    layout="wide"
)

# ---------------- LOAD DATA ---------------- #

@st.cache_data
def load_data():
    matches = pd.read_csv("data/matches.csv")
    deliveries = pd.read_csv("data/deliveries.csv")
    return matches, deliveries

matches, deliveries = load_data()

# ---------------- SIDEBAR ---------------- #

st.sidebar.title("🏏 IPL Analytics")

page = st.sidebar.selectbox(
    "Select Page",
    [
        "Home",
        "Team Analysis",
        "Player Analysis",
        "Player Search",
        "Venue Analysis",
        "Head to Head",
        "Orange Cap",
        "Purple Cap",
        "Toss Analysis"
    ]
)

# ---------------- SEASON FILTER ---------------- #

season_list = ["All Seasons"] + sorted(matches["season"].astype(str).unique().tolist())

selected_season = st.sidebar.selectbox(
    "Select Season",
    season_list
)

if selected_season != "All Seasons":
    matches_filtered = matches[
        matches["season"].astype(str) == selected_season
    ]
else:
    matches_filtered = matches.copy()

# ======================================================
# HOME
# ======================================================

if page == "Home":

    st.title("🏏 IPL Analytics Dashboard")

    total_matches = len(matches_filtered)

    total_teams = len(
        pd.unique(
            pd.concat(
                [matches["team1"], matches["team2"]]
            )
        )
    )

    total_seasons = matches["season"].nunique()

    col1, col2, col3 = st.columns(3)

    col1.metric("Matches", total_matches)
    col2.metric("Teams", total_teams)
    col3.metric("Seasons", total_seasons)

    st.divider()

    team_wins = matches_filtered["winner"].value_counts()

    fig = px.bar(
        x=team_wins.index,
        y=team_wins.values,
        labels={"x": "Team", "y": "Wins"},
        title="IPL Team Wins"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# TEAM ANALYSIS
# ======================================================

elif page == "Team Analysis":

    st.title("🏆 Team Analysis")

    teams = sorted(matches["team1"].dropna().unique())

    selected_team = st.selectbox(
        "Select Team",
        teams
    )

    team_matches = matches[
        (matches["team1"] == selected_team)
        |
        (matches["team2"] == selected_team)
    ]

    team_wins = matches[
        matches["winner"] == selected_team
    ]

    matches_played = len(team_matches)
    wins = len(team_wins)

    win_percentage = (
        wins / matches_played * 100
        if matches_played > 0
        else 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Matches Played", matches_played)
    c2.metric("Matches Won", wins)
    c3.metric("Win %", f"{win_percentage:.2f}")

    results = team_matches["winner"].value_counts().head(10)

    fig = px.bar(
        x=results.index,
        y=results.values,
        title=f"{selected_team} Results"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# PLAYER ANALYSIS
# ======================================================

elif page == "Player Analysis":

    st.title("👑 Player Analysis")

    top_batsmen = (
        deliveries.groupby("batter")["batsman_runs"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig = px.bar(
        x=top_batsmen.index,
        y=top_batsmen.values,
        title="Top 10 Run Scorers"
    )

    st.plotly_chart(fig, use_container_width=True)

    wickets = deliveries[
        deliveries["is_wicket"] == 1
    ]

    top_bowlers = (
        wickets.groupby("bowler")
        .size()
        .sort_values(ascending=False)
        .head(10)
    )

    fig2 = px.bar(
        x=top_bowlers.index,
        y=top_bowlers.values,
        title="Top 10 Wicket Takers"
    )

    st.plotly_chart(fig2, use_container_width=True)

# ======================================================
# PLAYER SEARCH
# ======================================================

elif page == "Player Search":

    st.title("🔍 Player Search")

    players = sorted(
        deliveries["batter"]
        .dropna()
        .unique()
    )

    player = st.selectbox(
        "Select Player",
        players
    )

    player_data = deliveries[
        deliveries["batter"] == player
    ]

    runs = player_data["batsman_runs"].sum()

    matches_played = player_data[
        "match_id"
    ].nunique()

    balls = len(player_data)

    strike_rate = (
        (runs / balls) * 100
        if balls > 0
        else 0
    )

    c1, c2, c3 = st.columns(3)

    c1.metric("Runs", runs)
    c2.metric("Matches", matches_played)
    c3.metric("Strike Rate", f"{strike_rate:.2f}")

# ======================================================
# VENUE ANALYSIS
# ======================================================

elif page == "Venue Analysis":

    st.title("🏟 Venue Analysis")

    venue_data = (
        matches["venue"]
        .value_counts()
        .head(15)
    )

    fig = px.bar(
        x=venue_data.index,
        y=venue_data.values,
        title="Top Venues by Matches Hosted"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# HEAD TO HEAD
# ======================================================

elif page == "Head to Head":

    st.title("🤝 Head to Head")

    teams = sorted(matches["team1"].dropna().unique())

    team1 = st.selectbox(
        "Team 1",
        teams
    )

    team2 = st.selectbox(
        "Team 2",
        teams,
        index=1
    )

    h2h = matches[
        (
            (matches["team1"] == team1)
            &
            (matches["team2"] == team2)
        )
        |
        (
            (matches["team1"] == team2)
            &
            (matches["team2"] == team1)
        )
    ]

    st.metric(
        "Matches Played",
        len(h2h)
    )

    winner_count = (
        h2h["winner"]
        .value_counts()
    )

    fig = px.bar(
        x=winner_count.index,
        y=winner_count.values,
        title=f"{team1} vs {team2}"
    )

    st.plotly_chart(fig, use_container_width=True)

# ======================================================
# ORANGE CAP
# ======================================================

elif page == "Orange Cap":

    st.title("🟠 Orange Cap")

    orange = (
        deliveries.groupby("batter")
        ["batsman_runs"]
        .sum()
        .reset_index()
        .sort_values(
            "batsman_runs",
            ascending=False
        )
        .head(20)
    )

    st.dataframe(
        orange,
        use_container_width=True
    )

    st.download_button(
        "Download CSV",
        orange.to_csv(index=False),
        "orange_cap.csv"
    )

# ======================================================
# PURPLE CAP
# ======================================================

elif page == "Purple Cap":

    st.title("🟣 Purple Cap")

    wickets = deliveries[
        deliveries["is_wicket"] == 1
    ]

    purple = (
        wickets.groupby("bowler")
        .size()
        .reset_index(name="wickets")
        .sort_values(
            "wickets",
            ascending=False
        )
        .head(20)
    )

    st.dataframe(
        purple,
        use_container_width=True
    )

    st.download_button(
        "Download CSV",
        purple.to_csv(index=False),
        "purple_cap.csv"
    )

# ======================================================
# TOSS ANALYSIS
# ======================================================

elif page == "Toss Analysis":

    st.title("🪙 Toss Impact Analysis")

    toss_win_match = matches[
        matches["toss_winner"]
        ==
        matches["winner"]
    ]

    percentage = (
        len(toss_win_match)
        /
        len(matches)
    ) * 100

    st.metric(
        "Toss Winner Also Won Match %",
        f"{percentage:.2f}%"
    )

    toss_results = pd.DataFrame({
        "Outcome": [
            "Won Match",
            "Lost Match"
        ],
        "Count": [
            len(toss_win_match),
            len(matches) - len(toss_win_match)
        ]
    })

    fig = px.pie(
        toss_results,
        names="Outcome",
        values="Count",
        title="Toss Impact"
    )

    st.plotly_chart(fig, use_container_width=True)