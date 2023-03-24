import json

import requests


class Session:
    def __init__(self, title: str) -> None:
        self.title = title

    def get_questions(self) -> list:
        request = requests.get("https://rita-server.herokuapp.com/questions")

        try:
            questions = json.loads(request.text)
        except json.JSONDecodeError:
            print("[WARN] (Questions) JSON Decode Error (Ignoring)")

        return questions

    def get_understanding(self) -> int:
        request = requests.get("https://rita-server.herokuapp.com/understandings")

        try:
            understanding = json.loads(request.text)
        except json.JSONDecodeError:
            print("[WARN] (Understanding) JSON Decode Error (Ignoring)")

        return understanding["understanding"]
