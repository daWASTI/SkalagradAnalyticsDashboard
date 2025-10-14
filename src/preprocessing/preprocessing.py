import src.preprocessing.overview_preprocessing as overview_preprocessing
import src.preprocessing.player_metrics_preprocessing as player_metrics_preprocessing
import src.preprocessing.matchmaking_metrics_preprocessing as matchmaking_metrics_preprocessing
import src.preprocessing.rating_metrics_preprocessing as rating_metrics_preprocessing
import logging
from functools import lru_cache

def get_overview_data(engine):
    try:
        return {
            "daily_matches": overview_preprocessing.get_daily_matches(engine),
            "user_count": overview_preprocessing.get_user_count(engine)
        }
    except Exception as e:
        logging.error(f"Failed to load overview data: {e}")
        return {}
    
def get_rating_metrics_data(engine):
    try:
        return {
            "rating_convergence": rating_metrics_preprocessing.get_rating_convergence(engine)
        }
    except Exception as e:
        logging.error(f"Failed to load rating metrics data: {e}")
        return {}
    
def get_matchmaking_metrics_data(engine):
    try:
        return {
            "matchmaking_convergence": matchmaking_metrics_preprocessing.get_matchmaking_convergence(engine)
        }
    except Exception as e:
        logging.error(f"Failed to load matchmaking metrics data: {e}")
        return {}


def get_player_metrics_data(engine):
    try:
        player_match_data = player_metrics_preprocessing.fetch_player_match_data(engine) #so this huge query doesn't get executed multiple times, will change this for other tabs aswell
        return {
            "player_stats": player_metrics_preprocessing.get_mmr_stat_correlation(player_match_data),
            "player_stats_2": player_metrics_preprocessing.get_mmr_stat_correlation_2(player_match_data)
        }
    except Exception as e:
        logging.error(f"Failed to load player metrics data: {e}")
        return {}
    
@lru_cache(maxsize=1) #note to self: don't use this for the live tab/dashboard later
def get_processed_data(engine):
    try:
        dashboard_data = {
            "overview_data": get_overview_data(engine),
            "rating_metrics_data": get_rating_metrics_data(engine),
            "matchmaking_metrics_data": get_matchmaking_metrics_data(engine),
            "player_metrics_data": get_player_metrics_data(engine)
        }
        for key in ["overview_data", "rating_metrics_data", "matchmaking_metrics_data", "player_metrics_data"]:
            if not dashboard_data.get(key):
                logging.warning(f"{key.replace('_', ' ').title()} is empty.")
        return dashboard_data
    except Exception as e:
        logging.error(f"Failed to load dashboard data: {e}")
        return {}
    
def refresh_processed_data():
    get_processed_data.cache_clear()
    logging.info("Cache cleared — reloading all data.")
    return get_processed_data()