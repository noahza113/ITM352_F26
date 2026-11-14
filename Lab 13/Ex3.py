from html import escape

import requests
from flask import Flask

app = Flask(__name__)

MEME_API_URL = "https://meme-api.com/gimme/wholesomememes"


@app.route("/")
def index():
    response = requests.request("GET", MEME_API_URL)
    response.raise_for_status()
    meme = response.json()

    image_url = escape(meme["url"], quote=True)
    subreddit = escape(meme["subreddit"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <title>Memes'R'Us</title>
    <meta charset="UTF-8" name="viewport" content="width=device-width, initial-scale=0.8">
    <meta http-equiv="refresh" content="10; url=http://127.0.0.1:5000">
</head>
<body>
    <h1>Memes'R'Us</h1>
    <img src="{image_url}" alt="Meme">
    <p>Source: r/{subreddit}</p>
</body>
</html>"""


if __name__ == "__main__":
    app.run(debug=True)