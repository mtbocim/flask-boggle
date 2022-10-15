import json
from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with self.client as client:
            response = client.get('/')
            html = response.get_data(as_text=True)
            # test that you're getting a template
            self.assertIn(
                '<!--homepage rendered (comment used for testing)-->',
                html
            )

    def test_api_new_game(self):
        """Test starting a new game."""

        with self.client as client:
            resp = client.post('/api/new-game')
            # html = resp.get_data(as_text=True)
            data = resp.get_json()

            # breakpoint()
            self.assertEqual(len(resp.json['board'][4]), 5)
            self.assertIsNotNone(resp.json['gameId'])
            self.assertIn(resp.json['gameId'], games)

    def test_api_score_word(self):
        """Test word evaluation response"""

        with self.client as client:
            resp = client.post('/api/new-game')
            game_id = resp.json['gameId']
            games[game_id].board = [
                ['C', 'A', 'T', 'A', 'T'],
                ['C', 'A', 'T', 'A', 'T'],
                ['C', 'A', 'T', 'A', 'T'],
                ['C', 'A', 'T', 'A', 'T'],
                ['C', 'A', 'T', 'A', 'T']
            ]

            # breakpoint()
            resp = client.post(
                '/api/score-word',
                json={
                    "game_id": game_id,
                    "word": "CAT"}
            )
            # breakpoint()
            json_response = resp.get_json()
            self.assertEqual({"result": "ok"}, json_response)

            resp = client.post('/api/score-word',
                               json={
                                   "game_id": game_id,
                                   "word": "FISH"}
                               )
            # breakpoint()
            json_response = resp.get_json()
            self.assertEqual({"result": "not-on-board"}, json_response)

            resp = client.post('/api/score-word',
                               json={
                                   "game_id": game_id,
                                   "word": "COASDNA"}
                               )
            # breakpoint()
            json_response = resp.get_json()
            self.assertEqual({"result": "not-word"}, json_response)
