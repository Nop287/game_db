# Building a Computer Game Database

The idea is to build a computer game data base. This starts with getting data from the internet based on the name and platform of a game.
Then we need a backend serving the data over a REST API. Finally we will have a frontend running in a browser.

This is currently a work in progress. The following files are relevant:
- build_game_db.ipynb: A Jupyter notebook augmenting the data from the internet and exporting it to files.
- TinyCB.ipynb: Create a TinyDB document database out of the data frame. The notebook also contains examples for searching.
- spiele_db_backend.py: The Flask backend offering the REST API to the web client.
- buefy_component.htlm: The frontend in the web browser to opened in a browser. It was implemented using vue.js coupled with buefy.
