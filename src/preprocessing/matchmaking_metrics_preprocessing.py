import pandas as pd

#check matchmaking quality over players active at the time and over party sizes
#check matchmaking time

#check matchmaking time and abortions, before and after duelyard integration and auto queue was introduced

#check user behavior, pressing requeue after how much time on avg etc.

#check how badly abortions affect queue time

def get_matchmaking_convergence(engine): #matchmaking quality on a per player basis after matches played
    df = pd.read_sql_query("SELECT match_id, user_id, team_score_ratio FROM PlayerMatchHistoryCleaned", engine)
    # Ensure team_score_ratio is numeric
    df['team_score_ratio'] = df['team_score_ratio'].astype(float)
    # Sort by user and matchID
    df = df.sort_values(by=['user_id', 'match_id'])
    # Compute each player's match number (1-based)
    df['match_number'] = df.groupby('user_id').cumcount() + 1
    # Aggregate team_score_ratio by match_number across all players
    matchmaking_convergence = df.groupby('match_number')['team_score_ratio'].mean().reset_index()
    return matchmaking_convergence