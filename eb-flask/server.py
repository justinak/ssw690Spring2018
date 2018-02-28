from flask import Flask


# EB looks for an 'application' callable by default.
app = Flask(__name__)

@app.route("/videos")
def video():
    return 'Hello'


# run the app.
if __name__ == "__main__":
    app.debug = True
    app.run()
