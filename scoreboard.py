import requests
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

API_URL = "https://nhl-score-api.herokuapp.com/api/scores/latest"

def fetch_scores():
    r = requests.get(API_URL)
    r.raise_for_status()
    return r.json()

def draw_scoreboard(data):
    games = data.get("games", [])
    width, height = 500, 50 + (len(games) * 40)
    img = Image.new("RGB", (width, height), color=(20, 20, 20))
    draw = ImageDraw.Draw(img)

    try:
        font = ImageFont.truetype("arial.ttf", 18)
    except:
        font = ImageFont.load_default()

    # Title
    draw.text((10, 10), f"NHL Scores – {datetime.now().strftime('%b %d')}",
              fill=(255, 255, 255), font=font)

    y = 40
    for g in games:
        home = f"{g['homeTeam']['abbrev']} {g['homeTeam']['score']}"
        away = f"{g['awayTeam']['abbrev']} {g['awayTeam']['score']}"
        status = g['status']['detailedState']
        line = f"{away} @ {home}  [{status}]"
        draw.text((10, y), line, fill=(200, 200, 200), font=font)
        y += 35

    img.save("scoreboard.png")

if __name__ == "__main__":
    scores = fetch_scores()
    draw_scoreboard(scores)
