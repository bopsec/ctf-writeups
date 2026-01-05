from flask import Flask, render_template, send_from_directory
import base64

app = Flask(__name__)

images = [
    "Radiant Circuit Fox",
    "Steel Grid Hound",
    "Neon Cyber Cat",
    "Holo Matrix Owl",
    "Quantum Signal Rabbit"
]

@app.route("/")
def index():
    return render_template("index.html", images=images)

@app.route("/img/<token>")
def image(token):
    if "DeW" in token:
        img = "Forbidden"
    else:
        token += "=" * (-len(token) % 4)
        img = base64.b64decode(token).decode()

    try:
        return send_from_directory("images", f"{img.lower().replace(' ', '-')}.png")
    except FileNotFoundError:
        return "Image not found", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)