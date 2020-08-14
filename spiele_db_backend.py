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
 
app.run()