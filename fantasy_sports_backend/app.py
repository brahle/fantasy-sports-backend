from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/")
def index():
    return "Welcome to the Fantasy Premier League Backend!"


if __name__ == "__main__":
    app.run(debug=True)
