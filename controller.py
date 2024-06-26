import json

from flask import Flask, request, jsonify, render_template

from service import save_to_spreadsheet, save_to_file

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/measurement', methods=['POST'])
def save_measurement():
    input_data = request.get_json()
    app.logger.info(input_data)
    save_to_file(json.dumps(input_data))
    save_to_spreadsheet(input_data)

    return jsonify({'message': 'Measurements received successfully'})


if __name__ == "__main__":
    app.run(debug=True, port=8888, host="0.0.0.0")
