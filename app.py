from ast import If
from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"
debug = DebugToolbarExtension(app)

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game
    #print("generated ID = >>>>>>>>>>>>>>>>>>", game_id)
    return jsonify({"gameId": game_id, "board": game.board})


@app.post("/api/score-word")
def score_submitted_word():
    """
        Recieve JSON object containing keys of 'word' and 'game_id'

        Evaluate if the word is a valid word in dictionary, not a duplicate,
        and finally able to be found in the current board layout.
        
        Return result of evaluation:

        if not a word: {result: "not-word"}
        if not on board: {result: "not-on-board"}
        if a valid word: {result: "ok"}
    """

    word_submission_data = request.get_json()
    word = word_submission_data["word"]
    game_id = word_submission_data["game_id"]
    #print("object passed for word submission>>>>>>>>>>>>>>>>>>>>",word_submission_data)
    
    #dictionary check
    if games[game_id].is_word_in_word_list(word) != True:
        return jsonify({"result": "not-word"})
    
    #current board check
    if games[game_id].check_word_on_board(word) != True:
        return jsonify({"result": "not-on-board"})
    #valid word
    #if games[game_id].is_word_not_a_dup(word) != True:
    #    return

    return jsonify({"result": "ok"})
