import requests


class Chatbot:
    def __init__(self) -> None:
        self.url = "http://localhost:5005/webhooks/rest/webhook"
        self.headers = {"Content-type": "application/json", "Accept": "text/plain"}

    def talk(self, message: str) -> str:
        return self._build_request(message=message)

    def _build_request(self, message: str) -> str:
        response = requests.post(
            url=self.url, headers=self.headers, json=self._build_payload(message)
        )
        response = response.json()

        return response[0]["text"]

    def _build_payload(self, message: str) -> dict:
        return {
            "sender": "Rasa",
            "message": message,
        }


if __name__ == "__main__":
    bot = Chatbot()
    text = input(">")
    while True and text != "/stop":
        print(bot.talk(text))
        text = input(">")
