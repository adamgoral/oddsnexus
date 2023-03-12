from oddsnexus.repositories.sports import get_upcoming_matches

from flask import Blueprint, jsonify


matches_blueprint = Blueprint('matches', __name__, url_prefix='/matches')

@matches_blueprint.route('/')
def get_matches_list():
    result = get_upcoming_matches()
    for item in result:
        item['date'] = item['date'].strftime('%Y-%m-%d %H:%M:%S')
    return jsonify(result)
