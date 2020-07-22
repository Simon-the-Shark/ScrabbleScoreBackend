import os.path
import sqlite3

from flask import Flask, jsonify, make_response, send_from_directory

app = Flask(__name__)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/api/v0/sjp/<string:word>", methods=['GET'])
def word_view(word):
    conn = sqlite3.connect(os.path.join("dbs", "sjp-20200717.db"))
    cursor = conn.cursor()
    result = cursor.execute("SELECT COUNT(*) FROM words WHERE word = '{}' LIMIT 1".format(word)).fetchall()
    approved = result[0][0] > 0
    cursor.close()
    conn.close()
    return jsonify({"approved": approved})


@app.route('/download/sjp-20200717.zip', methods=['GET'])
def download():
    return send_from_directory(directory=os.path.join(app.root_path, "dbs"), filename="sjp-20200717.zip")
