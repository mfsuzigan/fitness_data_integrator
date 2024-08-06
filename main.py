import json
import os
from flask import Flask, request, jsonify, render_template
from service import save_to_spreadsheet, save_to_requests_log

app = Flask(__name__)
config_type = os.getenv('FLASK_ENV', 'production')

if config_type.lower() == 'test':
    app.config.from_object('config_test.TestConfig')
    app.logger.warning("⚠️  Running TEST environment️")

else:
    app.config.from_object('config.Config')

if __name__ == "__main__":
    app.run(debug=True, port=8888, host="0.0.0.0")


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route('/measurement', methods=['POST'])
def save_measurement():
    input_data = request.get_json()
    app.logger.info(input_data)
    save_to_requests_log(json.dumps(input_data))
    save_to_spreadsheet(input_data, app.config['SPREADSHEET_ID'])

    return jsonify({'message': 'Measurements received successfully'})
