import pandas as pd

def get_daily_matches(engine):
    # Load data
    df = pd.read_sql_query("SELECT matchID, datetime, region FROM MatchData", engine)
    
    # Ensure datetime is a datetime object
    df["datetime"] = pd.to_datetime(df["datetime"])
    
    # Fix missing or 'n/a' regions **in place**
    df["region"] = df["region"].fillna("EU")
    df["region"] = df["region"].replace('"n/a"', "EU")
    
    # Aggregate per day **and keep region**
    daily_counts = (
        df.groupby([df["datetime"].dt.date, "region"])
          .agg(match_count=("matchID", "count"))
          .reset_index()
    )
    
    # Rename for clarity
    daily_counts.rename(columns={"datetime": "date"}, inplace=True)
    return daily_counts

def get_user_count(engine):
    df = pd.read_sql_query(
        "SELECT matchID, userID, datetime FROM PlayerMatchHistory WHERE matchID > 700", 
        engine
    )

    # Ensure datetime is datetime type
    df['datetime'] = pd.to_datetime(df['datetime'])
    df["date"] = df["datetime"].dt.date

    # Aggregate to daily level (unique players per day)
    user_count = (
        df.groupby('date')['userID']
        .apply(set)
        .reset_index(name='players')
        .sort_values('date')
    )

    players_1d, players_7d, players_30d = [], [], []
    cumulative_users = set()
    total_users = []

    for i in range(len(user_count)):
        # 1d
        window_sets = user_count['players'].iloc[max(0, i):i+1]
        players_1d.append(len(set().union(*window_sets)))

        # 7d
        window_sets = user_count['players'].iloc[max(0, i-6):i+1]
        players_7d.append(len(set().union(*window_sets)))

        # 30d
        window_sets = user_count['players'].iloc[max(0, i-29):i+1]
        players_30d.append(len(set().union(*window_sets)))

        # cumulative total users
        cumulative_users |= user_count['players'].iloc[i]
        total_users.append(len(cumulative_users))

    user_count['players_1d'] = players_1d
    user_count['players_7d'] = players_7d
    user_count['players_30d'] = players_30d
    user_count['total_users'] = total_users

    return user_count

#avg active users over local daytime (Sydney for OCE, Berlin for EU)