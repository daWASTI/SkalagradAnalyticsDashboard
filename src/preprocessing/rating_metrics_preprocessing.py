import pandas as pd

def get_rating_population(): #current, max

    return

def get_rating_error_interval_population():

    return

def get_rating_case_study():  #rating history of a few selected players

    return

def get_rating_convergence(engine):
    df = pd.read_sql_query("SELECT matchID, userID, dMMR FROM PlayerMatchHistory", engine)
    df["dMMR"] = abs(df["dMMR"])
    df.rename(columns={"dMMR":"rating_change"}, inplace=True)
    df.sort_values(by=["userID", "matchID"])
    df["match_number"] = df.groupby("userID").cumcount() + 1
    rating_convergence = df.groupby("match_number")["rating_change"].mean().reset_index()
    return rating_convergence

def get_rating_performance_correlation(): #just compare rating order vs performance order (score)

    return

def get_rating_resilience(): #need better function name, intended to show how well the rating performs, despite inevitably "bad" matchmaking at lower player counts

    return