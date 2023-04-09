from datetime import datetime
import os
import pymongo


def get_db_connection() -> pymongo.MongoClient:
    connection_string = os.getenv('MONGO_CONNECTION')
    client = pymongo.MongoClient(connection_string)
    return client


def get_upcoming_matches():
    date = datetime.combine(datetime.today(), datetime.min.time())
    client = get_db_connection()
    db = client.football
    matches = db['sportinglife.matches']
    matches = matches.aggregate([
        {
            '$project': {
                'date': {
                    '$toDate': '$match_date'
                }, 
                'competition': {
                    'id': '$competition.competition_reference.id', 
                    'name': '$competition.name'
                }, 
                'teams.home': {
                    'id': '$team_score_a.team.team_reference.id', 
                    'name': '$team_score_a.team.name'
                }, 
                'teams.away': {
                    'id': '$team_score_b.team.team_reference.id', 
                    'name': '$team_score_b.team.name'
                }, 
                'scores.half_time': {
                    'home': '$half_time_score.home', 
                    'away': '$half_time_score.away'
                }, 
                'scores.full_time': {
                    'home': '$full_time_score.home', 
                    'away': '$full_time_score.away'
                }, 
                'state': '$state'
            }
        },
        {
            '$match': {'date': {'$gte': date} }
        }
    ])
    
    result = list(matches)

    return result
    