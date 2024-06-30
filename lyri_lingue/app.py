from flask import Flask, Response, jsonify, render_template, request

from lyri_lingue.api import get_track_from_id, get_tracks_from_lyrics

app = Flask(__name__)


@app.route("/")
def home() -> str:
    """
    Render landing page.

    :return: Rendered landing page.
    """
    return render_template("index.html")


@app.route("/search", methods=["GET"])
def search() -> Response:
    """
    Search for track, as used in search bar. Used by App.js.

    :return: JSON object of track results.
    """
    query = request.args.get("query", "").lower()
    results = get_tracks_from_lyrics(query, 5)
    return jsonify(results)


@app.route("/lyrics/<int:song_id>")
def lyrics(song_id: int) -> str:
    """
    Render track lyrics page for provided track ID.

    :param song_id: The commontrack_id of track.
    :return: Rendered track lyric page.
    """
    track = get_track_from_id(song_id)
    return render_template("lyrics.html", track=track)


if __name__ == "__main__":
    app.run(debug=True)
