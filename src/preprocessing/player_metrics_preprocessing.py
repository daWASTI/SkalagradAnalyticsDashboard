import pandas as pd
import numpy as np

def fetch_player_match_data(engine):
    df = pd.read_sql_query("SELECT * FROM PlayerMatchHistoryCleaned", engine)
    return df

def fetch_kill_data(engine):
    df = pd.read_sql_query("SELECT * FROM Kills", engine)
    return df

def get_mmr_stat_correlation(player_match_data: pd.DataFrame, mmr_bin_size = 20, team_score_ratio_cutoff = 0.8):
    #only use columns needed
    cols_needed = ["score", "kills", "significant_assists", "assists", "teamkills", 
                   "rounds_played", "team_score_ratio", "mmr_before"]
    filtered = player_match_data[cols_needed]
    #filter for "good matches"
    filtered["team_score_ratio_group"] = np.where(
        filtered["team_score_ratio"] < team_score_ratio_cutoff,
        f"< {team_score_ratio_cutoff}",
        f">= {team_score_ratio_cutoff}"
    )
    #divide stats by amount of rounds
    cols_to_divide = filtered.columns.difference(["mmr_before", "team_score_ratio", "rounds_played", "team_score_ratio_group"])
    for col in cols_to_divide:
        filtered.loc[:, col] = filtered[col] / filtered["rounds_played"]
    #create mmr bins
    filtered.loc[:, "mmr_bin"] = (filtered["mmr_before"] // mmr_bin_size * mmr_bin_size).astype(int)
    #aggregate
    player_stats = (
        filtered.groupby(["mmr_bin", "team_score_ratio_group"], as_index=False)
        .agg({**{col: "mean" for col in cols_to_divide}, **{"mmr_before": "count"}})
        .rename(columns={"mmr_before": "match_count"})
    )
    return player_stats

def get_mmr_weapon_correlation(kill_data: pd.DataFrame):
    cols_needed = ["killed_rating", "victim_rating", "is_teamkill", "weapon", "damage_type"]
    return {}

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