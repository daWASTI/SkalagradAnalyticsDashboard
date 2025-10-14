import pandas as pd

def fetch_player_match_data(engine):
    df = pd.read_sql_query("SELECT * FROM PlayerMatchHistoryCleaned", engine)
    return df

def get_mmr_stat_correlation(player_match_data: pd.DataFrame):
    #only use columns needed
    cols_needed = ["score", "kills", "significant_assists", "assists", "teamkills", 
                   "rounds_played", "team_score_ratio", "mmr_before"]
    filtered = player_match_data[cols_needed]
    #filter for "good matches"
    filtered = filtered[filtered["team_score_ratio"] < 0.85]
    #divide stats by amount of rounds
    cols_to_divide = filtered.columns.difference(["mmr_before", "team_score_ratio", "rounds_played"])
    for col in cols_to_divide:
        filtered[col] = filtered[col] / filtered["rounds_played"]
    #create mmr bins
    filtered["mmr_bin"] = (filtered["mmr_before"] // 20 * 20).astype(int)
    #aggregate
    player_stats = (
        filtered.groupby("mmr_bin", as_index=False)
        .agg({**{col: "mean" for col in cols_to_divide}, **{"mmr_before": "count"}})
        .rename(columns={"mmr_before": "match_count"})
    )
    return player_stats

def get_mmr_stat_correlation_2(player_match_data: pd.DataFrame):
    #only use columns needed
    cols_needed = ["score", "kills", "significant_assists", "assists", "teamkills", 
                   "rounds_played", "team_score_ratio", "mmr_before"]
    filtered = player_match_data[cols_needed]
    #filter for "good matches"
    filtered = filtered[filtered["team_score_ratio"] >= 0.85]
    #divide stats by amount of rounds
    cols_to_divide = filtered.columns.difference(["mmr_before", "team_score_ratio", "rounds_played"])
    for col in cols_to_divide:
        filtered[col] = filtered[col] / filtered["rounds_played"]
    #create mmr bins
    filtered["mmr_bin"] = (filtered["mmr_before"] // 20 * 20).astype(int)
    #aggregate
    player_stats = (
        filtered.groupby("mmr_bin", as_index=False)
        .agg({**{col: "mean" for col in cols_to_divide}, **{"mmr_before": "count"}})
        .rename(columns={"mmr_before": "match_count"})
    )
    return player_stats

def get_first_kill_rate(): #store rating at the time of each kill event, then aggregate over last X matches

    return

def get_first_kill_time():

    return

def get_first_death_rate():

    return

def get_first_death_time(): #round time vs mmr, color map

    return

def get_weapon_popularity(): #check all kill events, store players rating at the time for a weapon choice vs rating plot

    return

def get_duel_outcomes(): #duel outcomes by rating difference, rating level aswell (?)

    return