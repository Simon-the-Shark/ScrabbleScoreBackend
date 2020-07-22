import sqlite3

from flask import Flask, jsonify, make_response

app = Flask(__name__)
app.config["DEBUG"] = True


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.route("/api/v0/sjp/<string:word>", methods=['GET'])
def word_view(word):
    conn = sqlite3.connect("sjp-20200717.db")
    cursor = conn.cursor()
    result = cursor.execute("SELECT COUNT(*) FROM words WHERE word = '{}' LIMIT 1".format(word)).fetchall()
    approved = result[0][0] > 0
    cursor.close()
    conn.close()
    return jsonify({"approved": approved})
