from flask import Flask, request, jsonify, render_template

from service import save_data

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/measurement', methods=['POST'])
def save_measurement():
    raw_data = request.get_json()
    app.logger.info(raw_data)
    save_data(raw_data)

    return jsonify({'message': 'Measurements received successfully'})


if __name__ == "__main__":
    app.run(debug=True, port=8888, host="0.0.0.0")
