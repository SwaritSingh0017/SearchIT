from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

load_dotenv("key.env")

app = Flask(__name__)

# Secure API keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
CUSTOM_SEARCH_ENGINE_ID = os.getenv("CUSTOM_SEARCH_ENGINE_ID")

def search_google(query):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": CUSTOM_SEARCH_ENGINE_ID,
        "q": query
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        query = request.form.get("query")
        data = search_google(query)
        if data and "items" in data:
            results = [{
                "title": item.get("title"),
                "snippet": item.get("snippet"),
                "link": item.get("link")
            } for item in data["items"][:5]]

    return render_template("index.html", results=results)

if __name__ == "__main__":
    app.run(debug=True)
