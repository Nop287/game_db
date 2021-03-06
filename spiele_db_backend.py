# We use flask as our backend for implementing a REST service
# Thanks to Patrick Smyth for provding an extensive tutorial on Flask.
# https://programminghistorian.org/en/lessons/creating-apis-with-python-and-flask
import flask
from flask import request, jsonify
from flask_cors import CORS
# We use a TinyDB as a database for our games
from tinydb import TinyDB, Query

# We create a flask app
app = flask.Flask(__name__)
# This will prevent errors beacaus of CORS but is probably making this unsecure
CORS(app)
# We use debug mode for now
app.config["DEBUG"] = True

# We open our TinyDB. Note that the file ist not yet in the github repository.
# There is a Jupyter notebook which builds the database.
game_db = TinyDB('spiele_tinydb.json')

# Create some test data for our catalog in the form of a list of dictionaries.
games = game_db.all()[0:4]


# This is just a static response if no existing API is given
@app.route('/', methods=['GET'])
def home():
    return '''<h1>My Game DB</h1>
<p>A prototype API for querying my collection of computer games.</p>'''

# We us this for testing for now to get a end to end prototype


@app.route('/api/v1/resources/games/all', methods=['GET'])
def api_all():
    return jsonify(games)

# This can be used to retrieve one game.
# For now we use the web-scraper-order as an ID. This has to be fixed, not all games have one.


@app.route('/api/v1/resources/games', methods=['GET'])
def api_id():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = int(request.args['id'])
    else:
        return "Error: No id field provided. Please specify an id."

    # Create an empty list for our results
    results = []

    # Loop through the data and match results that fit the requested ID.
    # IDs are unique, but other fields might return many results
    for game in games:
        if int(game['web-scraper-order']) == id:
            results.append(game)

    # Use the jsonify function from Flask to convert our list of
    # Python dictionaries to the JSON format.
    return jsonify(results)

# This was is the first version of the search function.


def search_by_rating(min_rating=0, max_rating=100):
    my_query = Query()
    def test_func(s): return True if(isinstance(
        s, float) and s >= min_rating and s <= max_rating) else False
    return game_db.search(my_query.game_rating.test(test_func))

# As I added parameters to search by in the frontend I extended the search function.


def search_api(min_rating=0, max_rating=100, min_rating_count=0, max_playing_time=1000):
    my_query = Query()

    def test_rating(s): return True if(isinstance(
        s, float) and s >= min_rating and s <= max_rating) else False
    def test_time(s): return True if(isinstance(
        s, float) and s <= max_playing_time) else False
    return game_db.search((my_query.game_rating.test(test_rating)) & (my_query.game_rating_count >= min_rating_count) &
                          (my_query.hltb_main.test(test_time)))


# This will be an endpoint for querying by rating
@app.route('/api/v1/resources/games/by_rating', methods=['GET'])
def api_rating():
    min_rating = 0
    max_rating = 100
    min_rating_count = 0
    max_playing_time = 1000
    if 'min' in request.args:
        min_rating = int(request.args['min'])
    if 'max' in request.args:
        max_rating = int(request.args['max'])
    if 'mincount' in request.args:
        min_rating_count = int(request.args['mincount'])
    if 'maxtime' in request.args:
        max_playing_time = int(request.args['maxtime'])
        return jsonify(search_api(min_rating, max_rating, min_rating_count, max_playing_time))


app.run()
